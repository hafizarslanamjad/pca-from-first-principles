"""Run the origin-shift and change-of-basis examples from Lecture 7."""

from pca_from_first_principles.reference_systems import (
    BasisCoordinates2D,
    ReferenceBasis,
    point_coordinates,
    represent,
    vector_from_coordinates,
)
from pca_from_first_principles.spatial_vectors import (
    MagnitudeM,
    SpatialPoint,
    SpatialVector,
    XChangeM,
    XPositionM,
    YChangeM,
    YPositionM,
    magnitude,
)


def describe(label: str, coordinates: BasisCoordinates2D) -> None:
    """Print coefficients with their basis and physical unit."""
    print(
        f"{label}: "
        f"({coordinates.first:g}, {coordinates.second:g}) m "
        f"in basis {coordinates.basis.value}"
    )


def main() -> None:
    """Preserve the point or vector while changing its reference."""
    old_origin = SpatialPoint(x=XPositionM(0.0), y=YPositionM(0.0))
    new_origin = SpatialPoint(x=XPositionM(2.0), y=YPositionM(0.0))
    tree = SpatialPoint(x=XPositionM(5.0), y=YPositionM(0.0))

    print("One fixed tree, two origins:")
    describe(
        "Relative to O",
        point_coordinates(tree, old_origin, ReferenceBasis.STANDARD_E),
    )
    describe(
        "Relative to O prime",
        point_coordinates(tree, new_origin, ReferenceBasis.STANDARD_E),
    )

    vector = SpatialVector(dx=XChangeM(3.0), dy=YChangeM(2.0))
    original: BasisCoordinates2D = represent(vector, ReferenceBasis.STANDARD_E)
    alternative: BasisCoordinates2D = represent(vector, ReferenceBasis.OBLIQUE_P)
    recovered: SpatialVector = vector_from_coordinates(alternative)
    vector_amount: MagnitudeM = magnitude(vector)

    print("\nOne fixed displacement, two bases:")
    describe("Original coordinates", original)
    describe("New coordinates", alternative)
    print(f"Reconstructed E components: ({recovered.dx:g}, {recovered.dy:g}) m")
    print(f"Geometric magnitude: {vector_amount:.6f} m")
    print("The negative coefficient removes one extra upward contribution.")


if __name__ == "__main__":
    main()
