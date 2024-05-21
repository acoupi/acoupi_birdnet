"""Acoupi-BirdNET program configuration."""

import datetime
from pathlib import Path
from typing import Annotated, Optional

from acoupi.components.audio_recorder import MicrophoneConfig
from acoupi.files import TEMP_PATH
from acoupi.programs import NoUserPrompt
from pydantic import BaseModel, Field


class AudioConfig(BaseModel):
    """Audio recording configuration parameters."""

    audio_duration: int = 3
    """Duration of each audio recording in seconds."""

    recording_interval: int = 5
    """Interval between each audio recording in seconds."""

    chunksize: int = 8192
    """Chunksize of audio recording."""


class RecordingSchedule(BaseModel):
    """Recording schedule config."""

    start_recording: datetime.time = datetime.time(hour=5, minute=30, second=0)

    end_recording: datetime.time = datetime.time(hour=20, minute=0, second=0)


class SaveRecordingFilter(BaseModel):
    """Recording saving options configuration."""

    starttime: datetime.time = datetime.time(hour=5, minute=30, second=0)

    endtime: datetime.time = datetime.time(hour=20, minute=30, second=0)

    before_dawndusk_duration: Optional[int] = None

    after_dawndusk_duration: Optional[int] = None

    frequency_duration: Optional[int] = None

    frequency_interval: Optional[int] = None

    saving_threshold: Optional[float] = 0.4


class AudioDirectories(BaseModel):
    """Audio Recording Directories configuration."""

    audio_dir: Path = Path.home() / "storages" / "recordings"

    audio_dir_true: Path = Path.home() / "storages" / "recordings" / "bats"

    audio_dir_false: Path = Path.home() / "storages" / "recordings" / "no_bats"


class Summariser(BaseModel):
    """Summariser configuration."""

    interval: Optional[float] = 10  # interval in minutes

    low_band_threshold: Optional[float] = None

    mid_band_threshold: Optional[float] = None

    high_band_threshold: Optional[float] = None


class MQTT_MessageConfig(BaseModel):
    """MQTT configuration to send messages."""

    host: str = "default_host"

    port: int = 1884

    client_username: str = "guest_username"

    client_password: str = "guest_password"

    topic: str = "mqtt-topic"

    clientid: str = "mqtt-clientid"


class HTTP_MessageConfig(BaseModel):
    """MQTT configuration to send messages."""

    deviceid: str = "device-id"

    baseurl: str = "base-url"

    client_password: str = "guest_password"

    client_id: str = "guest_clientid"

    api_key: str = "guest_apikey"

    content_type: str = "application-json"


class BirdNETConfigSchema(BaseModel):
    """BirdNET Configuration Schematic."""

    tmp_path: Annotated[Path, NoUserPrompt] = TEMP_PATH

    name: str = "BirdNET"

    detection_threshold: float = 0.2

    dbpath: Path = Path.home() / "storages" / "acoupi.db"

    dbpath_messages: Path = Path.home() / "storages" / "acoupi_messages.db"

    timeformat: str = "%Y%m%d_%H%M%S"

    timezone: str = "Europe/London"

    microphone_config: MicrophoneConfig

    audio_config: AudioConfig = Field(
        default_factory=AudioConfig,
    )

    recording_schedule: RecordingSchedule = Field(
        default_factory=RecordingSchedule,
    )

    recording_saving: Optional[SaveRecordingFilter] = Field(
        default_factory=SaveRecordingFilter,
    )

    audio_directories: AudioDirectories = Field(
        default_factory=AudioDirectories,
    )

    summariser_config: Optional[Summariser] = Field(
        default_factory=Summariser,
    )

    mqtt_config: Optional[MQTT_MessageConfig] = Field(
        default_factory=MQTT_MessageConfig,
    )

    http_config: Optional[HTTP_MessageConfig] = Field(
        default_factory=HTTP_MessageConfig,
    )
