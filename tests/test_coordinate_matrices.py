"""Relationships and numerical boundaries for Lecture 8."""

import sys

import pytest

from pca_from_first_principles.coordinate_matrices import (
    E_TO_P,
    P_TO_E,
    CoordinateMap2D,
)
from pca_from_first_principles.reference_systems import (
    BasisCoordinates2D,
    ReferenceBasis,
    SignedBasisAmountM,
    represent,
    vector_from_coordinates,
)
from pca_from_first_principles.spatial_vectors import (
    ScaleFactor,
    SpatialVector,
    XChangeM,
    YChangeM,
)


def test_worked_example_reconstructs_and_extracts() -> None:
    coefficients = BasisCoordinates2D(
        first=SignedBasisAmountM(3.0),
        second=SignedBasisAmountM(-1.0),
        basis=ReferenceBasis.OBLIQUE_P,
    )

    result = P_TO_E.apply(coefficients)

    assert (result.first, result.second) == (3.0, 2.0)
    assert result.basis is ReferenceBasis.STANDARD_E
    assert E_TO_P.apply(result) == coefficients


def test_row_arithmetic_matches_weighted_columns() -> None:
    matrix = CoordinateMap2D(
        input_basis=ReferenceBasis.OBLIQUE_P,
        output_basis=ReferenceBasis.STANDARD_E,
        row1_col1=ScaleFactor(2.0),
        row1_col2=ScaleFactor(-3.0),
        row2_col1=ScaleFactor(5.0),
        row2_col2=ScaleFactor(4.0),
    )
    coordinates = BasisCoordinates2D(
        first=SignedBasisAmountM(3.0),
        second=SignedBasisAmountM(-2.0),
        basis=ReferenceBasis.OBLIQUE_P,
    )

    # 3 * (2, 5) + (-2) * (-3, 4) = (6, 15) + (6, -8).
    result = matrix.apply(coordinates)

    assert (result.first, result.second) == (12.0, 7.0)


@pytest.mark.parametrize(
    ("first", "second"),
    [(3.0, -1.0), (0.0, 0.0), (-4.0, 7.0), (0.5, -0.25)],
)
@pytest.mark.parametrize("basis", list(ReferenceBasis))
def test_supplied_maps_reverse_each_other(
    first: float, second: float, basis: ReferenceBasis
) -> None:
    original = BasisCoordinates2D(
        first=SignedBasisAmountM(first),
        second=SignedBasisAmountM(second),
        basis=basis,
    )

    if basis is ReferenceBasis.OBLIQUE_P:
        recovered = E_TO_P.apply(P_TO_E.apply(original))
    else:
        recovered = P_TO_E.apply(E_TO_P.apply(original))

    assert recovered.basis is original.basis
    assert recovered.first == pytest.approx(first)
    assert recovered.second == pytest.approx(second)


@pytest.mark.parametrize(
    ("dx", "dy"),
    [(3.0, 2.0), (-2.0, 5.0), (0.0, 0.0), (0.25, -0.5)],
)
def test_matrices_agree_with_lecture_seven(dx: float, dy: float) -> None:
    vector = SpatialVector(dx=XChangeM(dx), dy=YChangeM(dy))
    in_e = represent(vector, ReferenceBasis.STANDARD_E)
    in_p = represent(vector, ReferenceBasis.OBLIQUE_P)

    extracted = E_TO_P.apply(in_e)
    reconstructed = P_TO_E.apply(in_p)
    recovered_vector = vector_from_coordinates(reconstructed)

    assert extracted == in_p
    assert reconstructed == in_e
    assert recovered_vector.dx == pytest.approx(vector.dx)
    assert recovered_vector.dy == pytest.approx(vector.dy)


def test_transpose_of_oblique_matrix_does_not_extract_coordinates() -> None:
    in_e = BasisCoordinates2D(
        first=SignedBasisAmountM(3.0),
        second=SignedBasisAmountM(2.0),
        basis=ReferenceBasis.STANDARD_E,
    )
    transpose_candidate = CoordinateMap2D(
        input_basis=ReferenceBasis.STANDARD_E,
        output_basis=ReferenceBasis.OBLIQUE_P,
        row1_col1=ScaleFactor(1.0),
        row1_col2=ScaleFactor(1.0),
        row2_col1=ScaleFactor(0.0),
        row2_col2=ScaleFactor(1.0),
    )

    wrong = transpose_candidate.apply(in_e)
    correct = E_TO_P.apply(in_e)

    assert (wrong.first, wrong.second) == (5.0, 2.0)
    assert (correct.first, correct.second) == (3.0, -1.0)


def test_map_rejects_coordinates_in_wrong_basis() -> None:
    in_e = BasisCoordinates2D(
        first=SignedBasisAmountM(3.0),
        second=SignedBasisAmountM(2.0),
        basis=ReferenceBasis.STANDARD_E,
    )

    with pytest.raises(ValueError, match="wrong basis"):
        P_TO_E.apply(in_e)


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize("entry_index", [0, 1, 2, 3])
def test_matrix_rejects_nonfinite_entries(invalid: float, entry_index: int) -> None:
    entries = [1.0, 0.0, 1.0, 1.0]
    entries[entry_index] = invalid

    with pytest.raises(ValueError, match="finite"):
        CoordinateMap2D(
            input_basis=ReferenceBasis.OBLIQUE_P,
            output_basis=ReferenceBasis.STANDARD_E,
            row1_col1=ScaleFactor(entries[0]),
            row1_col2=ScaleFactor(entries[1]),
            row2_col1=ScaleFactor(entries[2]),
            row2_col2=ScaleFactor(entries[3]),
        )


def test_nonfinite_output_is_rejected() -> None:
    largest = sys.float_info.max
    coordinates = BasisCoordinates2D(
        first=SignedBasisAmountM(largest),
        second=SignedBasisAmountM(largest),
        basis=ReferenceBasis.OBLIQUE_P,
    )

    with pytest.raises(ValueError, match="finite"):
        P_TO_E.apply(coordinates)
