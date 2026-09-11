"""Points, translated coordinate frames, and directed feature differences.

The model fixes axis order (length, mass), units (cm, g), and orientation.
Only the origin varies. No mixed-unit Euclidean metric is defined.
"""

from dataclasses import dataclass
from typing import NewType

LengthCm = NewType("LengthCm", float)
MassG = NewType("MassG", float)
LengthCoordinateCm = NewType("LengthCoordinateCm", float)
MassCoordinateG = NewType("MassCoordinateG", float)
LengthChangeCm = NewType("LengthChangeCm", float)
MassChangeG = NewType("MassChangeG", float)


@dataclass(frozen=True)
class FeaturePoint:
    """An observation point stored in the fixed physical measurement scheme."""

    length: LengthCm
    mass: MassG


@dataclass(frozen=True)
class CoordinateFrame:
    """An origin in the fixed length-cm, mass-g feature model."""

    origin_length: LengthCm
    origin_mass: MassG


@dataclass(frozen=True)
class PointCoordinates:
    """Coordinates of a point relative to an explicitly recorded frame."""

    length: LengthCoordinateCm
    mass: MassCoordinateG
    frame: CoordinateFrame


@dataclass(frozen=True)
class Displacement:
    """Directed change, expressed in cm and g along the fixed feature axes."""

    length: LengthChangeCm
    mass: MassChangeG


def coordinates_in(point: FeaturePoint, frame: CoordinateFrame) -> PointCoordinates:
    """Express a fixed point relative to the supplied origin."""
    return PointCoordinates(
        length=LengthCoordinateCm(point.length - frame.origin_length),
        mass=MassCoordinateG(point.mass - frame.origin_mass),
        frame=frame,
    )


def difference_from(
    reference: PointCoordinates, target: PointCoordinates
) -> Displacement:
    """Return target minus reference; both coordinate frames must agree."""
    if reference.frame != target.frame:
        raise ValueError("Express both points in the same frame before subtraction.")
    return Displacement(
        length=LengthChangeCm(target.length - reference.length),
        mass=MassChangeG(target.mass - reference.mass),
    )


def translated(point: FeaturePoint, change: Displacement) -> FeaturePoint:
    """Apply a displacement to obtain a point in the same feature model."""
    return FeaturePoint(
        length=LengthCm(point.length + change.length),
        mass=MassG(point.mass + change.mass),
    )
