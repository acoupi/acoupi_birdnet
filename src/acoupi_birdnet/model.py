"""Acoupi-compatible Model that runs BirdNET."""


from acoupi import data
from acoupi.components import types
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer


class BirdNET(types.Model):
    """Model that runs BirdNET."""

    def __init__(self, min_conf: float = 0.25):
        """Initialize the model."""
        self.analyzer = Analyzer()
        self.min_conf = min_conf

    def run(self, recording: data.Recording) -> data.ModelOutput:
        """Process the recording with BirdNET."""
        if not recording.path:
            return data.ModelOutput(
                name_model="BirdNET",
                recording=recording,
            )

        deployment = recording.deployment

        birdnet_recording = Recording(
            self.analyzer,
            path=recording.path,
            lat=deployment.latitude,
            lon=deployment.longitude,
            date=recording.datetime.date(),
            min_conf=self.min_conf,
        )
        birdnet_recording.analyze()

        high_freq = recording.samplerate / 2

        return data.ModelOutput(
            name_model="BirdNET",
            recording=recording,
            detections=[
                data.Detection(
                    probability=detection["confidence"],
                    location=data.BoundingBox.from_coordinates(
                        detection["start_time"],
                        0,
                        detection["end_time"],
                        high_freq,
                    ),
                    tags=[
                        data.PredictedTag(
                            tag=data.Tag(
                                key="species",
                                value=detection["scientific_name"],
                            ),
                            probability=detection["confidence"],
                        ),
                        data.PredictedTag(
                            tag=data.Tag(
                                key="common name",
                                value=detection["common_name"],
                            ),
                            probability=detection["confidence"],
                        ),
                    ],
                )
                for detection in birdnet_recording.detections
            ],
        )
