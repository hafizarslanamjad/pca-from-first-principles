"""Mathematical relationships and numerical limits for Lecture 7."""

import sys

import pytest

from pca_from_first_principles.reference_systems import (
    BasisCoordinates2D,
    ReferenceBasis,
    SignedBasisAmountM,
    point_coordinates,
    represent,
    vector_from_coordinates,
)
from pca_from_first_principles.spatial_vectors import (
    SpatialPoint,
    SpatialVector,
    XChangeM,
    XPositionM,
    YChangeM,
    YPositionM,
    displacement_from,
    magnitude,
)


def test_worked_example_has_negative_second_coefficient() -> None:
    vector = SpatialVector(dx=XChangeM(3.0), dy=YChangeM(2.0))

    coordinates = represent(vector, ReferenceBasis.OBLIQUE_P)

    assert coordinates.first == 3.0
    assert coordinates.second == -1.0
    assert coordinates.basis is ReferenceBasis.OBLIQUE_P
    assert vector_from_coordinates(coordinates) == vector


@pytest.mark.parametrize(
    ("dx", "dy"),
    [(3.0, 2.0), (-4.0, 7.0), (0.0, 0.0), (0.5, -0.25)],
)
@pytest.mark.parametrize("basis", list(ReferenceBasis))
def test_coordinates_reconstruct_displacement(
    dx: float, dy: float, basis: ReferenceBasis
) -> None:
    vector = SpatialVector(dx=XChangeM(dx), dy=YChangeM(dy))

    recovered = vector_from_coordinates(represent(vector, basis))

    assert recovered.dx == pytest.approx(dx)
    assert recovered.dy == pytest.approx(dy)


def test_oblique_reference_vectors_have_expected_coordinates() -> None:
    diagonal_reference = SpatialVector(dx=XChangeM(1.0), dy=YChangeM(1.0))
    vertical_reference = SpatialVector(dx=XChangeM(0.0), dy=YChangeM(1.0))

    diagonal = represent(diagonal_reference, ReferenceBasis.OBLIQUE_P)
    vertical = represent(vertical_reference, ReferenceBasis.OBLIQUE_P)

    assert (diagonal.first, diagonal.second) == (1.0, 0.0)
    assert (vertical.first, vertical.second) == (0.0, 1.0)


def test_origin_shift_changes_tree_coordinate() -> None:
    tree = SpatialPoint(x=XPositionM(5.0), y=YPositionM(0.0))
    old_origin = SpatialPoint(x=XPositionM(0.0), y=YPositionM(0.0))
    new_origin = SpatialPoint(x=XPositionM(2.0), y=YPositionM(0.0))

    old = point_coordinates(tree, old_origin, ReferenceBasis.STANDARD_E)
    new = point_coordinates(tree, new_origin, ReferenceBasis.STANDARD_E)

    assert old.first == 5.0
    assert new.first == 3.0
    assert tree.x == 5.0


@pytest.mark.parametrize("basis", list(ReferenceBasis))
def test_point_coordinate_difference_is_independent_of_origin(
    basis: ReferenceBasis,
) -> None:
    start = SpatialPoint(x=XPositionM(1.0), y=YPositionM(-2.0))
    end = SpatialPoint(x=XPositionM(5.0), y=YPositionM(3.0))
    origins = (
        SpatialPoint(x=XPositionM(0.0), y=YPositionM(0.0)),
        SpatialPoint(x=XPositionM(2.0), y=YPositionM(4.0)),
    )
    expected = represent(displacement_from(start, end), basis)

    for origin in origins:
        start_coordinates = point_coordinates(start, origin, basis)
        end_coordinates = point_coordinates(end, origin, basis)

        assert end_coordinates.first - start_coordinates.first == pytest.approx(
            expected.first
        )
        assert end_coordinates.second - start_coordinates.second == pytest.approx(
            expected.second
        )


def test_oblique_coefficient_squares_are_not_squared_magnitude() -> None:
    vector = SpatialVector(dx=XChangeM(3.0), dy=YChangeM(2.0))
    coordinates = represent(vector, ReferenceBasis.OBLIQUE_P)

    geometric_squared = magnitude(vector) ** 2
    naive_squared = coordinates.first**2 + coordinates.second**2
    corrected_squared = (
        coordinates.first**2 + (coordinates.first + coordinates.second) ** 2
    )

    assert geometric_squared == pytest.approx(13.0)
    assert naive_squared == 10.0
    assert corrected_squared == pytest.approx(geometric_squared)


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize("invalid_first", [True, False])
def test_representation_rejects_nonfinite_components(
    invalid: float, invalid_first: bool
) -> None:
    vector = SpatialVector(
        dx=XChangeM(invalid if invalid_first else 1.0),
        dy=YChangeM(1.0 if invalid_first else invalid),
    )

    with pytest.raises(ValueError, match="finite"):
        represent(vector, ReferenceBasis.OBLIQUE_P)


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize("invalid_first", [True, False])
def test_coordinate_object_rejects_nonfinite_coefficients(
    invalid: float, invalid_first: bool
) -> None:
    with pytest.raises(ValueError, match="finite"):
        BasisCoordinates2D(
            first=SignedBasisAmountM(invalid if invalid_first else 1.0),
            second=SignedBasisAmountM(1.0 if invalid_first else invalid),
            basis=ReferenceBasis.STANDARD_E,
        )


def test_representation_rejects_unrepresentable_coefficient() -> None:
    largest = sys.float_info.max
    vector = SpatialVector(dx=XChangeM(-largest), dy=YChangeM(largest))

    with pytest.raises(ValueError, match="finite"):
        represent(vector, ReferenceBasis.OBLIQUE_P)


def test_reconstruction_rejects_unrepresentable_component() -> None:
    largest = sys.float_info.max
    coordinates = BasisCoordinates2D(
        first=SignedBasisAmountM(largest),
        second=SignedBasisAmountM(largest),
        basis=ReferenceBasis.OBLIQUE_P,
    )

    with pytest.raises(ValueError, match="finite"):
        vector_from_coordinates(coordinates)
