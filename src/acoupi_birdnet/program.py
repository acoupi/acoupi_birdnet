"""BirdNET Program."""

import datetime

import pytz
from acoupi import components, data, tasks
from acoupi.components import types
from acoupi.programs.templates import DetectionProgram

from acoupi_birdnet.configuration import BirdNET_ConfigSchema
from acoupi_birdnet.model import BirdNET


class BirdNET_Program(DetectionProgram[BirdNET_ConfigSchema]):
    """BirdNET Program Configuration."""

    config_schema = BirdNET_ConfigSchema

    def setup(self, config: BirdNET_ConfigSchema):
        """Set up the BirdNET Program.

        This method initialises the birdnet program, registers the
        recording, detection, management, messaging, and summariser tasks,
        and performs any necessary setup for the program to run.
        """
        # Setup all the elements from the DetectionProgram
        self.validate_dirs(config)
        super().setup(config)

        if config.summariser_config and config.summariser_config.interval:
            summary_task = tasks.generate_summariser_task(
                summarisers=self.get_summarisers(config),
                message_store=self.message_store,
                logger=self.logger.getChild("summary"),
            )

            self.add_task(
                function=summary_task,
                schedule=datetime.timedelta(minutes=config.summariser_config.interval),
            )

    def configure_model(self, config):
        """Configure the BirdNET model.

        Returns
        -------
        BirdNET
            The BirdNET model instance.
        """
        return BirdNET()

    def get_summarisers(self, config: BirdNET_ConfigSchema) -> list[types.Summariser]:
        """Get the summarisers for the BirdNET Program.

        Parameters
        ----------
        config : BirdNET_ConfigSchema
            The configuration schema for the _acoupi_birdnet_ program defined in
            the configuration.py file and configured by a user via the CLI.

        Returns
        -------
        list[types.Summariser]
            A list of summarisers for the birdnet program. By default,
            the summariser will use the `summariser_config.interval` parameter for summarising
            the detections and calculating the minimum, maximum, and average
            confidence scores of the detections in each interval.
        """
        if not config.summariser_config:
            return []

        summarisers = []
        summariser_config = config.summariser_config

        if summariser_config.interval != 0.0:
            summarisers.append(
                components.StatisticsDetectionsSummariser(
                    store=self.store,  # type: ignore
                    interval=summariser_config.interval,
                )
            )

        if (
            summariser_config.interval != 0.0
            and summariser_config.low_band_threshold != 0.0
            and summariser_config.mid_band_threshold != 0.0
            and summariser_config.high_band_threshold != 0.0
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

    def get_file_managers(
        self, config: BirdNET_ConfigSchema
    ) -> list[types.RecordingSavingManager]:
        """Get the file managers for the BirdNET Program.

        Parameters
        ----------
        config : BirdNET_ConfigSchema
            The configuration schema for the _acoupi_birdnet_ program defined in
            the configuration.py file and configured by a user via the CLI.

        Returns
        -------
        list[types.RecordingSavingManager]
            A list of file managers for the birdnet program.
        """
        return [
            components.SaveRecordingManager(
                dirpath=config.paths.recordings,
                dirpath_true=config.paths.recordings / config.recording_saving.true_dir,
                dirpath_false=config.paths.recordings
                / config.recording_saving.false_dir,
                timeformat=config.recording_saving.timeformat,
                detection_threshold=config.model.detection_threshold,
                saving_threshold=config.recording_saving.saving_threshold,
            )
        ]

    def get_message_factories(
        self, config: BirdNET_ConfigSchema
    ) -> list[types.MessageBuilder]:
        """Get the message factories for the BirdNET Program.

        Parameters
        ----------
        config : BirdNET_ConfigSchema
            The configuration schema for the _acoupi_birdnet_ program defined in
            the configuration.py file and configured by a user via the CLI.

        Returns
        -------
        list[types.MessageBuilder]
            A list of message factories for the birdnet program. By default,
            the message factory will use the `detection_threshold` parameter for
            buildling messages.
        """
        return [
            components.DetectionThresholdMessageBuilder(
                detection_threshold=config.model.detection_threshold
            )
        ]

    def get_recording_filters(
        self, config: BirdNET_ConfigSchema
    ) -> list[types.RecordingSavingFilter]:
        """Get the recording filters for the BirdNET Program.

        Parameters
        ----------
        config : BirdNET_ConfigSchema
            The configuration schema for the _acoupi_birdnet_ program defined in
            the configuration.py file and configured by a user via the CLI.

        Returns
        -------
        list[types.RecordingSavingFilter]
            A list of recording filters for the birdnet program. If no
            saving filters are defined, the method will not save any recordings.
        """
        if not config.recording_saving:
            # No saving filters defined
            return []

        saving_filters = []
        timezone = pytz.timezone(config.timezone)
        recording_saving = config.recording_saving

        # Main filter
        # Will only save recordings if the recording time is in the
        # interval defined by the start and end time.
        if (
            recording_saving.filters is not None
            and recording_saving.filters.starttime is not None
            and recording_saving.filters.endtime is not None
        ):
            saving_filters.append(
                components.SaveIfInInterval(
                    interval=data.TimeInterval(
                        start=recording_saving.filters.starttime,
                        end=recording_saving.filters.endtime,
                    ),
                    timezone=timezone,
                )
            )

        # Additional filters
        if (
            recording_saving.filters is not None
            and recording_saving.filters.frequency_duration != 0
            and recording_saving.filters.frequency_interval != 0
        ):
            # This filter will only save recordings at a frequency defined
            # by the duration and interval.
            saving_filters.append(
                components.FrequencySchedule(
                    duration=recording_saving.filters.frequency_duration,
                    frequency=recording_saving.filters.frequency_interval,
                )
            )

        if (
            recording_saving.filters is not None
            and recording_saving.filters.before_dawndusk_duration != 0
        ):
            # This filter will only save recordings if the recording time
            # is before dawn or dusk.
            saving_filters.append(
                components.Before_DawnDuskTimeInterval(
                    duration=recording_saving.filters.before_dawndusk_duration,
                    timezone=timezone,
                )
            )

        if (
            recording_saving.filters is not None
            and recording_saving.filters.after_dawndusk_duration != 0
        ):
            # This filter will only save recordings if the recording time
            # is after dawn or dusk.
            saving_filters.append(
                components.After_DawnDuskTimeInterval(
                    duration=recording_saving.filters.after_dawndusk_duration,
                    timezone=timezone,
                )
            )

        return saving_filters
