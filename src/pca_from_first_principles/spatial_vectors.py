"""Displacements in one fixed orthonormal Cartesian frame, measured in meters.

This is a different model from the length-mass feature space. All functions
assume the same axes, orientation, origin for points, and meter convention.
Annotations express semantic roles; they do not validate units at runtime.
"""

from dataclasses import dataclass
from math import hypot
from typing import NewType

XPositionM = NewType("XPositionM", float)
YPositionM = NewType("YPositionM", float)
XChangeM = NewType("XChangeM", float)
YChangeM = NewType("YChangeM", float)
MagnitudeM = NewType("MagnitudeM", float)
ScaleFactor = NewType("ScaleFactor", float)


@dataclass(frozen=True)
class SpatialPoint:
    """Position coordinates in the fixed meter-based frame."""

    x: XPositionM
    y: YPositionM


@dataclass(frozen=True)
class SpatialVector:
    """Components of a free displacement; no starting point is stored."""

    dx: XChangeM
    dy: YChangeM


def displacement_from(reference: SpatialPoint, target: SpatialPoint) -> SpatialVector:
    """Return the directed change from reference to target."""
    return SpatialVector(
        dx=XChangeM(target.x - reference.x),
        dy=YChangeM(target.y - reference.y),
    )


def move(start: SpatialPoint, change: SpatialVector) -> SpatialPoint:
    """Apply a displacement to a specified starting point."""
    return SpatialPoint(
        x=XPositionM(start.x + change.dx),
        y=YPositionM(start.y + change.dy),
    )


def add(first: SpatialVector, second: SpatialVector) -> SpatialVector:
    """Compose two changes in the same fixed frame."""
    return SpatialVector(
        dx=XChangeM(first.dx + second.dx),
        dy=YChangeM(first.dy + second.dy),
    )


def scale(vector: SpatialVector, factor: ScaleFactor) -> SpatialVector:
    """Multiply every component by the same dimensionless factor."""
    return SpatialVector(
        dx=XChangeM(factor * vector.dx),
        dy=YChangeM(factor * vector.dy),
    )


def magnitude(vector: SpatialVector) -> MagnitudeM:
    """Return straight-line displacement size in the declared Euclidean frame."""
    return MagnitudeM(hypot(vector.dx, vector.dy))
