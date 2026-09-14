"""Separate orientation and amount on a fixed right-positive number line.

The enum values are dimensionless representatives, not physical distances.
No two-dimensional normalization procedure is introduced in this module.
"""

from enum import Enum
from math import isfinite
from typing import NewType

from pca_from_first_principles.spatial_vectors import MagnitudeM

SignedDisplacementM = NewType("SignedDisplacementM", float)


class LineOrientation(Enum):
    """Standard numerical representatives of the two line orientations."""

    LEFT = -1
    RIGHT = 1


def orientation_of(displacement: SignedDisplacementM) -> LineOrientation:
    """Extract orientation; zero has no unique direction."""
    if not isfinite(displacement):
        raise ValueError("Displacement must be finite.")
    if displacement == 0.0:
        raise ValueError("Zero displacement has no unique direction.")
    return LineOrientation.RIGHT if displacement > 0.0 else LineOrientation.LEFT


def amount_of(displacement: SignedDisplacementM) -> MagnitudeM:
    """Retain the nonnegative amount in meters and discard orientation."""
    if not isfinite(displacement):
        raise ValueError("Displacement must be finite.")
    return MagnitudeM(abs(displacement))


def compose_displacement(
    amount: MagnitudeM, orientation: LineOrientation
) -> SignedDisplacementM:
    """Multiply an amount in meters by a dimensionless representative."""
    if not isfinite(amount) or amount < 0.0:
        raise ValueError("Amount must be finite and nonnegative.")
    return SignedDisplacementM(amount * orientation.value)
