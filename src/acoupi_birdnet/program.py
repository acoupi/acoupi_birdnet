"""BirdNET Program."""
import datetime
import pytz

from acoupi import components, data, tasks
from acoupi.programs.base import AcoupiProgram
from celery.schedules import crontab

from acoupi_birdnet.configuration import BirdNET_ConfigSchema
from acoupi_birdnet.model import BirdNET


class BirdNET_Program(AcoupiProgram):
    """BirdNET Program."""

    config: BirdNET_ConfigSchema

    def setup(self, config: BirdNET_ConfigSchema):
        """Setup.

        1. Create Audio Recording Task
        2. Create Detection Task
        3. Create Saving Recording Filter and Management Task
        4. Create Message Task

        """
        timezone = pytz.timezone(config.timezone)

        # dbpath = components.SqliteStore(config.dbpath)
        # dbpath_message = components.SqliteMessageStore(db_path=config.dbpath)

        # Step 1 - Audio Recordings Task
        recording_task = tasks.generate_recording_task(
            recorder=components.PyAudioRecorder(
                duration=config.audio_config.audio_duration,
                samplerate=config.audio_config.samplerate,
                audio_channels=config.audio_config.audio_channels,
                chunksize=config.audio_config.chunksize,
                device_index=config.audio_config.device_index,
            ),
            store=components.SqliteStore(config.dbpath),
            # logger
            recording_conditions=[
                components.IsInIntervals(
                    intervals=[
                        data.TimeInterval(
                            start=config.recording_schedule.start_recording,
                            end=datetime.datetime.strptime(
                                "23:59:59", "%H:%M:%S"
                            ).time(),
                        ),
                        data.TimeInterval(
                            start=datetime.datetime.strptime(
                                "00:00:00", "%H:%M:%S"
                            ).time(),
                            end=config.recording_schedule.end_recording,
                        ),
                    ],
                    timezone=timezone,
                )
            ],
        )

        # Step 2 - Model Detections Task
        detection_task = tasks.generate_detection_task(
            store=components.SqliteStore(config.dbpath),
            model=BirdNET(),
            message_store=components.SqliteStore(config.dbpath_message),
            # logger
            output_cleaners=[
                components.ThresholdDetectionFilter(threshold=config.threshold)
            ],
            message_factories=[components.FullModelOutputMessageBuilder()],
        )

        # Step 3 - Files Management Task
        def create_file_filters():
            recording_saving = config.recording_saving

            if recording_saving is None:
                return []

            saving_filters = []

            if (
                recording_saving.starttime is not None
                and recording_saving.endtime is not None
            ):
                saving_filters.append(
                    components.SaveIfInInterval(
                        interval=data.TimeInterval(
                            start=config.recording_saving.starttime,
                            end=config.recording_saving.endtime,
                        ),
                        timezone=timezone,
                    )
                )
            elif (
                recording_saving.frequency_duration is not None
                and recording_saving.frequency_interval is not None
            ):
                saving_filters.append(
                    components.FrequencySchedule(
                        duration=recording_saving.frequency_duration,
                        frequency=recording_saving.frequency_interval,
                    )
                )
            elif recording_saving.before_dawndusk_duration is not None:
                saving_filters.append(
                    components.Before_DawnDuskTimeInterval(
                        duration=recording_saving.before_dawndusk_duration,
                        timezone=timezone,
                    )
                )
            elif recording_saving.after_dawndusk_duration is not None:
                saving_filters.append(
                    components.After_DawnDuskTimeInterval(
                        duration=recording_saving.after_dawndusk_duration,
                        timezone=timezone,
                    )
                )
            elif recording_saving.threshold is not None:
                saving_filters.append(
                    components.ThresholdRecordingFilter(
                        threshold=recording_saving.threshold,
                    )
                )
            else:
                raise UserWarning("No saving filters defined - no files will be saved.")

            return saving_filters

        file_management_task = (
            tasks.generate_file_management_task(
                store=components.SqliteStore(config.dbpath),
                file_manager=components.SaveRecordingManager(
                    dirpath_true=config.audio_directories.audio_dir_true,
                    dirpath_false=config.audio_directories.audio_dir_false,
                    timeformat=config.timeformat,
                    threshold=config.threshold,
                ),
                file_filters=create_file_filters(),
            ),
        )

        # Step 4 - Send Data Task
        def create_messenger():
            if config.http_message_config is not None:
                return components.HTTPMessenger(
                    base_url=config.http_message_config.baseurl,
                    base_params={
                        "client-id": config.http_message_config.client_id,
                        "password": config.http_message_config.client_password,
                    },
                    headers={
                        "Accept": config.http_message_config.content_type,
                        "Authorization": config.http_message_config.api_key,
                    },
                )
            if config.mqtt_message_config is not None:
                return components.MQTTMessenger(
                    host=config.mqtt_message_config.host,
                    port=config.mqtt_message_config.port,
                    password=config.mqtt_message_config.client_password,
                    username=config.mqtt_message_config.client_username,
                    topic=config.mqtt_message_config.topic,
                    clientid=config.mqtt_message_config.clientid,
                )
            else:
                raise UserWarning(
                    "No Messenger defined - no data will be communicated."
                )

        send_data_task = tasks.generate_send_data_task(
            message_store=components.SqliteStore(config.dbpath_message),
            messengers=create_messenger(),
        )

        self.add_task(
            function=recording_task,
            callbacks=[detection_task],
            schedule=datetime.timedelta(seconds=10),
        )

        self.add_task(
            function=file_management_task,
            schedule=datetime.timedelta(minutes=10),
        )

        self.add_task(
            function=send_data_task,
            schedule=crontab(minute="*/1"),
        )
