"""Distinguish collection size, representation size, and column means."""

from dataclasses import dataclass
from math import fsum, isfinite
from typing import NewType

import numpy as np
from numpy.typing import NDArray

from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
)

ObservationCount = NewType("ObservationCount", int)
FeatureCount = NewType("FeatureCount", int)
MeanLengthCm = NewType("MeanLengthCm", float)
MeanWidthCm = NewType("MeanWidthCm", float)
ThicknessCm = NewType("ThicknessCm", float)


@dataclass(frozen=True)
class DatasetShape:
    """Counts under the observations-as-rows convention; not matrix rank."""

    observations: ObservationCount
    features: FeatureCount


def shape_of(matrix: NDArray[np.float64]) -> DatasetShape:
    """Interpret a two-axis array under the declared row/column convention.

    Shape alone cannot verify that a caller used the intended convention.
    """
    if matrix.ndim != 2:
        raise ValueError("Expected an observations-by-features matrix.")
    return DatasetShape(
        observations=ObservationCount(matrix.shape[0]),
        features=FeatureCount(matrix.shape[1]),
    )


@dataclass(frozen=True)
class ColumnMeans:
    """One mean per feature, aggregated across observations in centimeters."""

    length: MeanLengthCm
    width: MeanWidthCm

    def __post_init__(self) -> None:
        if not (isfinite(self.length) and isfinite(self.width)):
            raise ValueError("Column means must be finite.")


def column_means(dataset: ComponentDataset) -> ColumnMeans:
    """Average each feature without mixing its identity with another feature.

    The fixed observation model requires positive finite values. Scaling by
    the maximum before summing avoids overflow of the raw positive sum.
    Empty collections have no arithmetic mean here.
    """
    if not dataset.observations:
        raise ValueError("An empty dataset has no column means.")
    lengths = dataset.length_column()
    widths = dataset.width_column()
    count = len(dataset.observations)
    length_scale = max(lengths)
    width_scale = max(widths)
    return ColumnMeans(
        length=MeanLengthCm(
            length_scale * (fsum(x / length_scale for x in lengths) / count)
        ),
        width=MeanWidthCm(
            width_scale * (fsum(x / width_scale for x in widths) / count)
        ),
    )


@dataclass(frozen=True)
class LengthWidthThicknessObservation(LengthWidthObservation):
    """Extend the existing measurement record by one feature, not one row."""

    thickness: ThicknessCm

    def __post_init__(self) -> None:
        super().__post_init__()
        if not isfinite(self.thickness) or self.thickness <= 0.0:
            raise ValueError("Thickness must be finite and positive.")


def thickness_matrix(
    observations: tuple[LengthWidthThicknessObservation, ...],
) -> NDArray[np.float64]:
    """Export rows of length, width, thickness in that order, all in cm."""
    return np.array(
        [(item.length, item.width, item.thickness) for item in observations],
        dtype=np.float64,
    ).reshape(len(observations), 3)
