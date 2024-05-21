"""Acoupi-BirdNET Program."""

import datetime
from typing import List, Optional

import pytz
from acoupi import components, data, tasks
from acoupi.components import types
from acoupi.programs.base import AcoupiProgram
from acoupi.programs.workers import AcoupiWorker, WorkerConfig

from acoupi_birdnet.configuration import BirdNETConfigSchema
from acoupi_birdnet.model import BirdNET


class BirdNETProgram(AcoupiProgram):
    """BirdNET Program."""

    config: BirdNETConfigSchema

    worker_config: Optional[WorkerConfig] = WorkerConfig(
        workers=[
            AcoupiWorker(
                name="recording",
                queues=["recording"],
                concurrency=1,
            ),
            AcoupiWorker(
                name="default",
                queues=["celery"],
            ),
        ],
    )

    def setup(self, config: BirdNETConfigSchema):
        self.validate_dirs(config)

        microphone = config.microphone_config
        self.recorder = components.PyAudioRecorder(
            duration=config.audio_config.audio_duration,
            chunksize=config.audio_config.chunksize,
            samplerate=microphone.samplerate,
            audio_channels=microphone.audio_channels,
            device_name=microphone.device_name,
            audio_dir=config.tmp_path,
        )

        self.model = BirdNET()
        self.file_manager = components.SaveRecordingManager(
            dirpath=config.audio_directories.audio_dir,
            dirpath_true=config.audio_directories.audio_dir_true,
            dirpath_false=config.audio_directories.audio_dir_false,
            timeformat=config.timeformat,
            threshold=config.detection_threshold,
        )
        self.store = components.SqliteStore(config.dbpath)
        self.message_store = components.SqliteMessageStore(
            config.dbpath_messages
        )

        self.add_task(
            function=tasks.generate_recording_task(
                recorder=self.recorder,
                store=self.store,
                logger=self.logger.getChild("recording"),
                recording_conditions=self.create_recording_conditions(config),
            ),
            schedule=datetime.timedelta(
                seconds=config.audio_config.recording_interval
            ),
            callbacks=[
                tasks.generate_detection_task(
                    store=self.store,
                    model=self.model,
                    message_store=self.message_store,
                    logger=self.logger.getChild("detection"),
                    output_cleaners=self.create_detection_cleaners(config),
                    message_factories=[
                        components.FullModelOutputMessageBuilder()
                    ],
                ),
            ],
            queue="recording",
        )

        self.add_task(
            function=tasks.generate_file_management_task(
                store=self.store,
                logger=self.logger.getChild("file_management"),
                file_manager=self.file_manager,
                file_filters=self.create_file_filters(config),
                temp_path=config.tmp_path,
            ),
            schedule=datetime.timedelta(seconds=30),
        )

        if (
            config.summariser_config is not None
            and config.summariser_config.interval is not None
        ):
            self.add_task(
                function=tasks.generate_summariser_task(
                    summarisers=self.create_summariser(config),
                    message_store=self.message_store,
                    logger=self.logger.getChild("summary"),
                ),
                schedule=datetime.timedelta(
                    minutes=config.summariser_config.interval
                ),
            )

        # Step 4 - Send Data Task
        self.add_task(
            function=tasks.generate_send_data_task(
                message_store=self.message_store,
                messengers=self.create_messenger(config),
                logger=self.logger.getChild("messaging"),
            ),
            schedule=datetime.timedelta(seconds=10),
        )

    def check(self, config: BirdNETConfigSchema):
        self.recorder.check()

        messengers = self.create_messenger(config)
        for messenger in messengers:
            if hasattr(messenger, "check"):
                messenger.check()  # type: ignore

    def validate_dirs(self, config: BirdNETConfigSchema):
        """Validate Stores Directories."""
        for path in [
            config.audio_directories.audio_dir,
            config.audio_directories.audio_dir_true,
            config.audio_directories.audio_dir_false,
            config.dbpath.parent,
            config.dbpath_messages.parent,
        ]:
            if not path.exists():
                path.mkdir(parents=True)

    def create_recording_conditions(
        self, config: BirdNETConfigSchema
    ) -> List[types.RecordingCondition]:
        """Create Recording Conditions."""
        timezone = pytz.timezone(config.timezone)
        return [
            components.IsInIntervals(
                intervals=[
                    data.TimeInterval(
                        start=config.recording_schedule.start_recording,
                        end=config.recording_schedule.end_recording,
                    ),
                ],
                timezone=timezone,
            )
        ]

    def create_detection_cleaners(
        self, config: BirdNETConfigSchema
    ) -> List[types.ModelOutputCleaner]:
        """Create Detection Cleaners."""
        return [
            components.ThresholdDetectionFilter(
                threshold=config.detection_threshold,
            ),
        ]

    def create_file_filters(
        self, config: BirdNETConfigSchema
    ) -> List[types.RecordingSavingFilter]:
        """Create File Filters."""
        if not config.recording_saving:
            # No saving filters defined
            return []

        saving_filters = []
        timezone = pytz.timezone(config.timezone)
        recording_saving = config.recording_saving

        # Main saving_file filter
        # Will only save recordings if the recording time is in the
        # interval defined by the start and end time.
        if (
            recording_saving.starttime is not None
            and recording_saving.endtime is not None
        ):
            saving_filters.append(
                components.SaveIfInInterval(
                    interval=data.TimeInterval(
                        start=recording_saving.starttime,
                        end=recording_saving.endtime,
                    ),
                    timezone=timezone,
                )
            )

        # Additional saving_file filters
        if (
            recording_saving.frequency_duration is not None
            and recording_saving.frequency_interval is not None
        ):
            # This filter will only save recordings at a frequency defined
            # by the duration (length of time in which files are saved) and
            # interval (period of time between each duration in which files are not saved).
            saving_filters.append(
                components.FrequencySchedule(
                    duration=recording_saving.frequency_duration,
                    frequency=recording_saving.frequency_interval,
                )
            )

        if recording_saving.before_dawndusk_duration is not None:
            # This filter will only save recordings if the recording time is
            # within the duration (lenght of time in minutes) before dawn and dusk.
            saving_filters.append(
                components.Before_DawnDuskTimeInterval(
                    duration=recording_saving.before_dawndusk_duration,
                    timezone=timezone,
                )
            )

        if recording_saving.after_dawndusk_duration is not None:
            # This filter will only save recordings if the recording time is
            # within the duration (lenght of time in minutes) after dawn and dusk.
            saving_filters.append(
                components.After_DawnDuskTimeInterval(
                    duration=recording_saving.after_dawndusk_duration,
                    timezone=timezone,
                )
            )

        if recording_saving.saving_threshold is not None:
            # This filter will only save recordings if the recording files
            # have a positive detection above the threshold.
            saving_filters.append(
                components.ThresholdRecordingFilter(
                    threshold=recording_saving.saving_threshold,
                )
            )

        return saving_filters

    def create_summariser(
        self,
        config: BirdNETConfigSchema,
    ) -> List[types.Summariser]:
        """Create summarisers."""
        if not config.summariser_config:
            raise UserWarning(
                "Cannot create summariser - no summariser config defined."
            )

        summariser_config = config.summariser_config

        summarisers = []
        if summariser_config.interval is not None:
            summarisers.append(
                components.StatisticsDetectionsSummariser(
                    store=self.store,
                    interval=summariser_config.interval,
                )
            )

        if (
            summariser_config.interval is not None
            and summariser_config.low_band_threshold is not None
            and summariser_config.mid_band_threshold is not None
            and summariser_config.high_band_threshold is not None
        ):
            summarisers.append(
                components.ThresholdsDetectionsSummariser(
                    store=self.store,
                    interval=summariser_config.interval,
                    low_band_threshold=summariser_config.low_band_threshold,
                    mid_band_threshold=summariser_config.mid_band_threshold,
                    high_band_threshold=summariser_config.high_band_threshold,
                )
            )

        return summarisers

    def create_messenger(
        self,
        config: BirdNETConfigSchema,
    ) -> List[types.Messenger]:
        """Create Messengers - Send Detection Results."""
        # Main Messenger will send messages to remote server.
        if not config.mqtt_config and not config.http_config:
            raise UserWarning(
                "No messengers defined - no messages will be sent."
            )

        messengers = []

        """MQTT Messenger - Will send messages to a MQTT broker."""
        if (
            config.mqtt_config is not None
            and config.mqtt_config.client_password != "guest_password"
        ):
            messengers.append(
                components.MQTTMessenger(
                    host=config.mqtt_config.host,
                    port=config.mqtt_config.port,
                    password=config.mqtt_config.client_password,
                    username=config.mqtt_config.client_username,
                    topic=config.mqtt_config.topic,
                    clientid=config.mqtt_config.clientid,
                )
            )

        if (
            config.http_config is not None
            and config.http_config.client_password != "guest_password"
        ):
            messengers.append(
                components.HTTPMessenger(
                    base_url=config.http_config.baseurl,
                    base_params={
                        "client-id": config.http_config.client_id,
                        "password": config.http_config.client_password,
                    },
                    headers={
                        "Accept": config.http_config.content_type,
                        "Authorization": config.http_config.api_key,
                    },
                )
            )

        return messengers
