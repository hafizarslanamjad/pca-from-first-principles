"""Coordinates in the two reference bases developed in Lecture 7.

SpatialVector retains the project's fixed orthonormal, meter-based frame.
BasisCoordinates2D describes that displacement using either E or the
specific oblique basis P, where p1 = e1 + e2 and p2 = e2.

The reference vectors are dimensionless. Their coefficients carry meters.
Annotations describe semantic roles; runtime checks do not validate units.
"""

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import NewType

from pca_from_first_principles.spatial_vectors import (
    SpatialPoint,
    SpatialVector,
    XChangeM,
    YChangeM,
    displacement_from,
)

SignedBasisAmountM = NewType("SignedBasisAmountM", float)


class ReferenceBasis(Enum):
    """The two ordered bases explicitly defined in the lecture."""

    STANDARD_E = "E"
    OBLIQUE_P = "P"


@dataclass(frozen=True)
class BasisCoordinates2D:
    """Signed coefficients paired with the basis that interprets them."""

    first: SignedBasisAmountM
    second: SignedBasisAmountM
    basis: ReferenceBasis

    def __post_init__(self) -> None:
        if not isinstance(self.basis, ReferenceBasis):
            raise ValueError("Basis must be one of the declared reference bases.")
        if not (isfinite(self.first) and isfinite(self.second)):
            raise ValueError("Coordinate coefficients must be finite.")


def represent(vector: SpatialVector, basis: ReferenceBasis) -> BasisCoordinates2D:
    """Describe a fixed displacement using E or the specified oblique P.

    For P, matching coefficients in E gives:
        first = dx
        first + second = dy
    Therefore second = dy - dx.

    Reject a result outside the finite float range.
    """
    if not (isfinite(vector.dx) and isfinite(vector.dy)):
        raise ValueError("Displacement components must be finite.")

    first = SignedBasisAmountM(vector.dx)
    second: SignedBasisAmountM

    if basis is ReferenceBasis.STANDARD_E:
        second = SignedBasisAmountM(vector.dy)
    elif basis is ReferenceBasis.OBLIQUE_P:
        second = SignedBasisAmountM(vector.dy - vector.dx)
    else:
        raise ValueError("Basis must be one of the declared reference bases.")

    return BasisCoordinates2D(first=first, second=second, basis=basis)


def vector_from_coordinates(
    coordinates: BasisCoordinates2D,
) -> SpatialVector:
    """Reconstruct a displacement in the project's fixed spatial frame.

    In P, first*p1 + second*p2 equals
    first*e1 + (first + second)*e2.
    """
    x_component: float = coordinates.first
    y_component: float

    if coordinates.basis is ReferenceBasis.STANDARD_E:
        y_component = coordinates.second
    elif coordinates.basis is ReferenceBasis.OBLIQUE_P:
        y_component = coordinates.first + coordinates.second
    else:
        raise ValueError("Basis must be one of the declared reference bases.")

    if not (isfinite(x_component) and isfinite(y_component)):
        raise ValueError("Reconstructed components must be finite.")

    return SpatialVector(
        dx=XChangeM(x_component),
        dy=YChangeM(y_component),
    )


def point_coordinates(
    point: SpatialPoint,
    origin: SpatialPoint,
    basis: ReferenceBasis,
) -> BasisCoordinates2D:
    """Represent the displacement from a chosen origin to a point.

    Both SpatialPoint inputs use the existing fixed global spatial frame.
    The result describes the point relative to the supplied local origin
    and one of the two supported bases.
    """
    return represent(displacement_from(origin, point), basis)
