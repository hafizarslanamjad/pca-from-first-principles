"""Length-width observations and an observations-by-features dataset.

The fixed schema is length in cm followed by width in cm, using physical
measurement zeros. No Euclidean metric or centering operation is defined.
"""

from dataclasses import dataclass
from math import isfinite
from typing import NewType

import numpy as np
from numpy.typing import NDArray

from pca_from_first_principles.feature_space import LengthChangeCm, LengthCm

WidthCm = NewType("WidthCm", float)
WidthChangeCm = NewType("WidthChangeCm", float)
ObservationId = NewType("ObservationId", str)


@dataclass(frozen=True)
class LengthWidthObservation:
    """One component's selected measurements, not a physical component."""

    identifier: ObservationId
    length: LengthCm
    width: WidthCm

    def __post_init__(self) -> None:
        if not all(
            isfinite(value) and value > 0.0 for value in (self.length, self.width)
        ):
            raise ValueError("Component measurements must be finite and positive.")


@dataclass(frozen=True)
class LengthWidthDifference:
    """Target minus reference; negative and zero changes are meaningful."""

    length: LengthChangeCm
    width: WidthChangeCm

    def __post_init__(self) -> None:
        if not all(isfinite(value) for value in (self.length, self.width)):
            raise ValueError("Feature differences must be finite.")


def difference_from(
    reference: LengthWidthObservation, target: LengthWidthObservation
) -> LengthWidthDifference:
    """Compare matching features under the fixed centimeter schema."""
    return LengthWidthDifference(
        length=LengthChangeCm(target.length - reference.length),
        width=WidthChangeCm(target.width - reference.width),
    )


@dataclass(frozen=True)
class ComponentDataset:
    """Ordered observations sharing a fixed two-feature measurement schema."""

    observations: tuple[LengthWidthObservation, ...]

    def length_column(self) -> tuple[LengthCm, ...]:
        """Hold length identity fixed and vary the observation."""
        return tuple(observation.length for observation in self.observations)

    def width_column(self) -> tuple[WidthCm, ...]:
        """Hold width identity fixed and vary the observation."""
        return tuple(observation.width for observation in self.observations)

    def to_matrix(self) -> NDArray[np.float64]:
        """Export a fresh (n, 2) array: rows observations, columns length/width.

        Values are numerical centimeter measurements. Labels and scalar
        semantic types are not retained by the NumPy array itself.
        An empty dataset preserves its two feature columns.
        """
        values = [(item.length, item.width) for item in self.observations]
        return np.array(values, dtype=np.float64).reshape(len(self.observations), 2)
