"""Acoupi-BirdNET program configuration."""

from typing import Optional

from acoupi.programs.templates import DetectionProgramConfiguration
from pydantic import BaseModel, Field


class SummaryConfig(BaseModel):
    """Summariser configuration."""

    interval: Optional[float] = 10  # interval in minutes

    low_band_threshold: Optional[float] = None

    mid_band_threshold: Optional[float] = None

    high_band_threshold: Optional[float] = None


class ModelConfig(BaseModel):
    detection_threshold: float = 0.2


class BirdNETConfig(DetectionProgramConfiguration):
    """BirdNET Configuration Schema."""

    summaries: Optional[SummaryConfig] = Field(
        default_factory=SummaryConfig,
    )

    model: ModelConfig = Field(
        default_factory=ModelConfig,
    )
