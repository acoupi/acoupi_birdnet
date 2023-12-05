"""Test Suite for Acoupi BirdNET Model."""
import datetime
from pathlib import Path

from acoupi import data

from acoupi_birdnet.model import BirdNET

TEST_RECORDING = Path(__file__).parent / "data" / "soundscape.wav"


def test_birdnet():
    recording = data.Recording(
        path=TEST_RECORDING,
        duration=2 * 60,
        samplerate=48_000,
        datetime=datetime.datetime.now(),
        deployment=data.Deployment(
            name="test",
        ),
    )

    model = BirdNET()
    detections = model.run(recording)

    assert isinstance(detections, data.ModelOutput)
    assert detections.name_model == "BirdNET"
    assert len(detections.detections) == 25
