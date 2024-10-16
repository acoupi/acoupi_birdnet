"""Acoupi-BirdNET Program."""

import datetime

from acoupi import components, tasks
from acoupi.components import types
from acoupi.programs.templates import DetectionProgram

from acoupi_birdnet.configuration import BirdNETConfig
from acoupi_birdnet.model import BirdNET


class BirdNETProgram(DetectionProgram[BirdNETConfig]):
    """BirdNET Program."""

    config_schema = BirdNETConfig

    def setup(self, config):
        super().setup(config)

        if config.summaries and config.summaries.interval:
            summary_task = tasks.generate_summariser_task(
                summarisers=self.get_summarisers(config),
                message_store=self.message_store,
                logger=self.logger.getChild("summary"),
            )

            self.add_task(
                function=summary_task,
                schedule=datetime.timedelta(minutes=config.summaries.interval),
            )

    def configure_model(self, config):
        return BirdNET()

    def get_summarisers(self, config: BirdNETConfig) -> list[types.Summariser]:
        if not config.summaries:
            return []

        summarisers = []
        summariser_config = config.summaries

        if summariser_config.interval:
            summarisers.append(
                components.StatisticsDetectionsSummariser(
                    store=self.store,  # type: ignore
                    interval=summariser_config.interval,
                )
            )

        if (
            summariser_config.interval
            and summariser_config.low_band_threshold
            and summariser_config.mid_band_threshold
            and summariser_config.high_band_threshold
        ):
            summarisers.append(
                components.ThresholdsDetectionsSummariser(
                    store=self.store,  # type: ignore
                    interval=summariser_config.interval,
                    low_band_threshold=summariser_config.low_band_threshold,
                    mid_band_threshold=summariser_config.mid_band_threshold,
                    high_band_threshold=summariser_config.high_band_threshold,
                )
            )

        return summarisers

    def get_message_factories(self, config) -> list[types.MessageBuilder]:
        return [
            components.DetectionThresholdMessageBuilder(
                detection_threshold=config.model.detection_threshold
            )
        ]
