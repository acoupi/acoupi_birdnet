import datetime

from acoupi.components import MicrophoneConfig
from acoupi.programs.templates import MessagingConfig

from acoupi_birdnet.configuration import BirdNETConfig


def test_can_instantiate_default_configurations():
    config = BirdNETConfig(
        microphone=MicrophoneConfig(
            device_name="test_device",
        ),
        messaging=MessagingConfig(),
    )

    assert config.recording.schedule_start == datetime.time(hour=4)
    assert config.recording.schedule_end == datetime.time(hour=23)

    assert config.model.detection_threshold == 0.4
