"""Connect scaled columns, row arithmetic, and coordinate extraction."""

from pca_from_first_principles.coordinate_matrices import E_TO_P, P_TO_E
from pca_from_first_principles.reference_systems import (
    BasisCoordinates2D,
    ReferenceBasis,
    SignedBasisAmountM,
)


def describe(label: str, coordinates: BasisCoordinates2D) -> None:
    """Print a coordinate description with its interpretation."""
    print(
        f"{label}: "
        f"({coordinates.first:g}, {coordinates.second:g}) m "
        f"in basis {coordinates.basis.value}"
    )


def main() -> None:
    """Evaluate the lecture's reconstruction in both arithmetic views."""
    coefficients = BasisCoordinates2D(
        first=SignedBasisAmountM(3.0),
        second=SignedBasisAmountM(-1.0),
        basis=ReferenceBasis.OBLIQUE_P,
    )

    first_contribution = BasisCoordinates2D(
        first=SignedBasisAmountM(P_TO_E.row1_col1 * coefficients.first),
        second=SignedBasisAmountM(P_TO_E.row2_col1 * coefficients.first),
        basis=ReferenceBasis.STANDARD_E,
    )
    second_contribution = BasisCoordinates2D(
        first=SignedBasisAmountM(P_TO_E.row1_col2 * coefficients.second),
        second=SignedBasisAmountM(P_TO_E.row2_col2 * coefficients.second),
        basis=ReferenceBasis.STANDARD_E,
    )
    column_sum = BasisCoordinates2D(
        first=SignedBasisAmountM(first_contribution.first + second_contribution.first),
        second=SignedBasisAmountM(
            first_contribution.second + second_contribution.second
        ),
        basis=ReferenceBasis.STANDARD_E,
    )

    matrix_result: BasisCoordinates2D = P_TO_E.apply(coefficients)
    recovered: BasisCoordinates2D = E_TO_P.apply(matrix_result)

    describe("Input coefficients", coefficients)
    describe("First scaled column", first_contribution)
    describe("Second scaled column", second_contribution)
    describe("Sum of scaled columns", column_sum)
    describe("Row-by-column result", matrix_result)
    describe("Recovered coefficients", recovered)
    print("The two arithmetic views reconstruct the same E-coordinate column.")


if __name__ == "__main__":
    main()
