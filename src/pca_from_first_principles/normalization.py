"""Unit representatives in the fixed Euclidean spatial frame of Lecture 4."""

from dataclasses import dataclass
from math import hypot, isclose, isfinite
from typing import NewType

from pca_from_first_principles.spatial_vectors import (
    MagnitudeM,
    SpatialVector,
    XChangeM,
    YChangeM,
    magnitude,
)

DirectionX = NewType("DirectionX", float)
DirectionY = NewType("DirectionY", float)


@dataclass(frozen=True)
class UnitDirection2D:
    """Dimensionless components of a unit representative in the fixed basis."""

    x: DirectionX
    y: DirectionY

    def __post_init__(self) -> None:
        if not (isfinite(self.x) and isfinite(self.y)):
            raise ValueError("Direction components must be finite.")
        if not isclose(hypot(self.x, self.y), 1.0, rel_tol=1e-12, abs_tol=0.0):
            raise ValueError("Direction representative must have unit magnitude.")


@dataclass(frozen=True)
class MagnitudeDirection:
    """Amount in meters and direction sufficient to reconstruct a nonzero vector."""

    amount: MagnitudeM
    direction: UnitDirection2D

    def __post_init__(self) -> None:
        if not isfinite(self.amount) or self.amount <= 0.0:
            raise ValueError("Decomposed magnitude must be finite and positive.")


def normalize(vector: SpatialVector) -> UnitDirection2D:
    """Preserve the ray and return a dimensionless unit representative.

    Preliminary scaling by the largest absolute component avoids overflow
    and underflow in the norm calculation. Direct component division avoids
    forming a reciprocal that might overflow for a very small vector.
    """
    if not (isfinite(vector.dx) and isfinite(vector.dy)):
        raise ValueError("Displacement components must be finite.")
    component_scale: float = max(abs(vector.dx), abs(vector.dy))
    if component_scale == 0.0:
        raise ValueError("Zero displacement has no unique direction.")
    scaled_x: float = vector.dx / component_scale
    scaled_y: float = vector.dy / component_scale
    scaled_magnitude: float = hypot(scaled_x, scaled_y)
    return UnitDirection2D(
        x=DirectionX(scaled_x / scaled_magnitude),
        y=DirectionY(scaled_y / scaled_magnitude),
    )


def decompose(vector: SpatialVector) -> MagnitudeDirection:
    """Retain both magnitude and unit direction for a nonzero displacement.

    Raise ValueError if the physical magnitude is not a finite float.
    Normalization alone can still be possible for such a vector.
    """
    direction: UnitDirection2D = normalize(vector)
    amount: MagnitudeM = magnitude(vector)
    return MagnitudeDirection(amount=amount, direction=direction)


def reconstruct(amount: MagnitudeM, direction: UnitDirection2D) -> SpatialVector:
    """Combine a nonnegative meter amount with a dimensionless representative.

    Zero amount constructs the zero vector; it does not give zero a unique
    recoverable direction. A negative magnitude is not a signed scale factor.
    """
    if not isfinite(amount) or amount < 0.0:
        raise ValueError("Reconstruction amount must be finite and nonnegative.")
    return SpatialVector(
        dx=XChangeM(amount * direction.x),
        dy=YChangeM(amount * direction.y),
    )
