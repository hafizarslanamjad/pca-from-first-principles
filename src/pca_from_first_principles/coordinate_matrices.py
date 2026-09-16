"""Matrix-vector products with explicit input and output coordinate bases.

Entries are dimensionless. Coordinate coefficients carry meters.
The two supplied maps implement the exact basis change from Lectures 7-8.
No general matrix-inverse algorithm is provided.
"""

from dataclasses import dataclass
from math import isfinite

from pca_from_first_principles.reference_systems import (
    BasisCoordinates2D,
    ReferenceBasis,
    SignedBasisAmountM,
)
from pca_from_first_principles.spatial_vectors import ScaleFactor


@dataclass(frozen=True)
class CoordinateMap2D:
    """A dimensionless 2-by-2 linear map between coordinate descriptions.

    Basis labels specify how to interpret inputs and outputs.
    They do not imply that an arbitrary instance is invertible.
    """

    input_basis: ReferenceBasis
    output_basis: ReferenceBasis
    row1_col1: ScaleFactor
    row1_col2: ScaleFactor
    row2_col1: ScaleFactor
    row2_col2: ScaleFactor

    def __post_init__(self) -> None:
        if not (
            isinstance(self.input_basis, ReferenceBasis)
            and isinstance(self.output_basis, ReferenceBasis)
        ):
            raise ValueError("Input and output bases must be declared bases.")

        entries = (
            self.row1_col1,
            self.row1_col2,
            self.row2_col1,
            self.row2_col2,
        )
        if not all(isfinite(entry) for entry in entries):
            raise ValueError("Matrix entries must be finite.")

    def apply(self, coordinates: BasisCoordinates2D) -> BasisCoordinates2D:
        """Scale and sum contributions to each output coordinate.

        A nonfinite output is rejected by BasisCoordinates2D.
        Ordinary floating-point arithmetic may still round finite results.
        """
        if coordinates.basis is not self.input_basis:
            raise ValueError("Input coordinates use the wrong basis.")

        first = SignedBasisAmountM(
            self.row1_col1 * coordinates.first + self.row1_col2 * coordinates.second
        )
        second = SignedBasisAmountM(
            self.row2_col1 * coordinates.first + self.row2_col2 * coordinates.second
        )
        return BasisCoordinates2D(
            first=first,
            second=second,
            basis=self.output_basis,
        )


P_TO_E = CoordinateMap2D(
    input_basis=ReferenceBasis.OBLIQUE_P,
    output_basis=ReferenceBasis.STANDARD_E,
    row1_col1=ScaleFactor(1.0),
    row1_col2=ScaleFactor(0.0),
    row2_col1=ScaleFactor(1.0),
    row2_col2=ScaleFactor(1.0),
)

E_TO_P = CoordinateMap2D(
    input_basis=ReferenceBasis.STANDARD_E,
    output_basis=ReferenceBasis.OBLIQUE_P,
    row1_col1=ScaleFactor(1.0),
    row1_col2=ScaleFactor(0.0),
    row2_col1=ScaleFactor(-1.0),
    row2_col2=ScaleFactor(1.0),
)
