"""BirdNET Program."""
import datetime
from pathlib import Path

from celery.schedules import crontab
from pydantic import BaseModel, Field

from acoupi import components, data, tasks
from acoupi_birdnet.model import BirdNET
from acoupi.programs.base import AcoupiProgram
from acoupi.system.constants import ACOUPI_HOME

"""Default paramaters for Batdetect2 Program"""


class AudioConfig(BaseModel):
    """Audio and microphone configuration parameters."""

    audio_duration: int = 3

    samplerate: int = 48000

    audio_channels: int = 1

    chunksize: int = 4096

    device_index: int = 0

    recording_interval: int = 0


class RecordingSchedule(BaseModel):
    """Recording schedule config."""

    start_recording: datetime.time = datetime.time(hour=4, minute=0, second=0)

    end_recording: datetime.time = datetime.time(hour=20, minute=0, second=0)


# class RecordingSaving(BaseModel):
class SaveRecordingFilter(BaseModel):
    """Recording saving options configuration."""

    starttime: datetime.time = datetime.time(hour=5, minute=30, second=0)

    endtime: datetime.time = datetime.time(hour=7, minute=30, second=0)

    before_dawndusk_duration: int = 20

    after_dawndusk_duration: int = 20

    frequency_duration: int = 5

    frequency_interval: int = 30

    threshold: float = 0.8


class AudioDirectories(BaseModel):
    """Audio Recording Directories configuration."""

    audio_dir_true: Path = Path.home() / "storages" / "birds" / "recordings"

    audio_dir_false: Path = Path.home() / "storages" / "no_birds" / "recordings"


class MQTT_MessageConfig(BaseModel):
    """MQTT configuration to send messages."""

    host: str = "localhost"

    port: int = 1884

    client_password: str = "guest"

    client_username: str = "guest"

    topic: str = "mqtt-topic"

    clientid: str = "mqtt-clientid"


class HTTP_MessageConfig(BaseModel):
    """MQTT configuration to send messages."""

    deviceid: str = "device-id"

    baseurl: str = "base-url"

    client_password: str = "guest"

    client_id: str = "guest"

    api_key: str = "guest"

    content_type: str = "application-json"


class BirdNet_ConfigSchema(BaseModel):
    """BatDetect2 Configuration Schematic."""

    name: str = "birdnet"

    threshold: float = 0.25

    dbpath: Path = ACOUPI_HOME / "storages" / "acoupi.db"

    timeformat: str = "%Y%m%d_%H%M%S"

    timezone: str = "Europe/London"

    audio_config: AudioConfig = Field(default_factory=AudioConfig)

    recording_schedule: RecordingSchedule = Field(default_factory=RecordingSchedule)

    recording_saving: SaveRecordingFilter = Field(default_factory=SaveRecordingFilter)

    audio_directories: AudioDirectories = Field(default_factory=AudioDirectories)

    mqtt_message_config: MQTT_MessageConfig = Field(default_factory=MQTT_MessageConfig)
    http_message_config: HTTP_MessageConfig = Field(default_factory=HTTP_MessageConfig)


class BirdNET_Program(AcoupiProgram):
    """BatDetect2 Program."""

    config: BirdNet_ConfigSchema

    def setup(self, config: BirdNet_ConfigSchema):
        """Setup.

        1. Create Audio Recording Task
        2. Create Detection Task
        3. Create Saving Recording Filter and Management Task
        4. Create Message Task

        """
        dbpath = components.SqliteStore(config.dbpath)
        dbpath_message = components.SqliteMessageStore(db_path=config.dbpath)

        # Step 1 - Audio Recordings Task
        recording_task = tasks.generate_recording_task(
            recorder=components.PyAudioRecorder(
                duration=config.audio_config.audio_duration,
                samplerate=config.audio_config.samplerate,
                audio_channels=config.audio_config.audio_channels,
                chunksize=config.audio_config.chunksize,
                device_index=config.audio_config.device_index,
            ),
            store=dbpath,
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
                    timezone=config.timezone,
                )
            ],
        )

        # Step 2 - Model Detections Task
        detection_task = tasks.generate_detection_task(
            store=dbpath,
            model=BirdNET(),
            message_store=dbpath_message,
            # logger
            output_cleaners=[
                components.ThresholdDetectionFilter(threshold=config.threshold)
            ],
            message_factories=[components.FullModelOutputMessageBuilder()],
        )

        # Step 3 - Files Management Task
        def create_file_filters():
            saving_filters = []

            if components.SaveIfInInterval is not None:
                saving_filters.add(
                    components.SaveIfInInterval(
                        interval=data.TimeInterval(
                            start=config.recording_saving.starttime,
                            end=config.recording_saving.endtime,
                        ),
                        timezone=config.timezone,
                    )
                )
            elif components.FrequencySchedule is not None:
                saving_filters.add(
                    components.FrequencySchedule(
                        duration=config.recording_saving.frequency_duration,
                        frequency=config.recording_saving.frequency_interval,
                    )
                )
            elif components.Before_DawnDuskTimeInterval is not None:
                saving_filters.add(
                    components.Before_DawnDuskTimeInterval(
                        duration=config.recording_saving.before_dawndusk_duration,
                        timezone=config.timezone,
                    )
                )
            elif components.After_DawnDuskTimeInterval is not None:
                saving_filters.add(
                    components.After_DawnDuskTimeInterval(
                        duration=config.recording_saving.after_dawndusk_duration,
                        timezone=config.timezone,
                    )
                )
            elif components.ThresholdRecordingFilter is not None:
                saving_filters.add(
                    components.ThresholdRecordingFilter(
                        threshold=config.recording_saving.threshold,
                    )
                )
            else:
                raise UserWarning("No saving filters defined - no files will be saved.")

            return saving_filters

        file_management_task = (
            tasks.generate_file_management_task(
                store=dbpath,
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
            data_messengers = []

            if components.HTTPMessenger is not None:
                data_messengers.add(
                    components.HTTPMessenger(
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
                )
            elif components.MQTTMessenger is not None:
                data_messengers.add(
                    components.MQTTMessenger(
                        host=config.mqtt_message_config.host,
                        port=config.mqtt_message_config.port,
                        password=config.mqtt_message_config.client_password,
                        username=config.mqtt_message_config.client_username,
                        topic=config.mqtt_message_config.topic,
                        clientid=config.mqtt_message_config.clientid,
                    )
                )
            else:
                raise UserWarning(
                    "No Messenger defined - no data will be communicated."
                )

            return data_messengers

        send_data_task = tasks.generate_send_data_task(
            message_store=dbpath_message,
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
