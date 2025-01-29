"""Acoupi-compatible Model that runs BirdNET."""

from acoupi import data
from acoupi.components import types
from audioclass.models import birdnet


class BirdNET(types.Model):
    """BirdNET Model to analyse the audio recording.

    This model uses the audioclass library to import the BirdNET model and
    identify and classify birds vocalisation in audio recordings.

    Attributes
    ----------
    name : str
        The name of the model, by default "BirdNET".
    """

    name = "BirdNET"

    def __init__(self, min_conf: float = 0.25, common_name: bool = False):
        """Initialize the model."""
        self.min_conf = min_conf
        self.common_name = common_name
        self._model = None

    @property
    def model(self) -> birdnet.BirdNET:
        """Get the BirdNET model."""
        if self._model is None:
            self._model = birdnet.BirdNET.load(
                confidence_threshold=self.min_conf,
                common_name=self.common_name,
            )
        return self._model

    def run(self, recording: data.Recording) -> data.ModelOutput:
        """Run the model on the recording.

        Parameters
        ----------
        recording : data.Recording
            The audio recording to process.

        Returns
        -------
        data.ModelOutput
            The model output containing the detections.
        """
        if not recording.path:
            return data.ModelOutput(
                name_model="BirdNET",
                recording=recording,
            )

        predictions = self.model.process_file(recording.path)
        high_freq = recording.samplerate / 2

        return data.ModelOutput(
            name_model="BirdNET",
            recording=recording,
            detections=[
                data.Detection(
                    detection_score=predicted_tag.score,
                    location=data.BoundingBox.from_coordinates(
                        prediction.clip.start_time,
                        0,
                        prediction.clip.end_time,
                        high_freq,
                    ),
                    tags=[
                        data.PredictedTag(
                            tag=data.Tag(
                                key=predicted_tag.tag.term.label,
                                value=predicted_tag.tag.value,
                            ),
                            confidence_score=predicted_tag.score,
                        )
                    ],
                )
                for prediction in predictions
                for predicted_tag in prediction.tags
            ],
        )
