"""Run Lecture 5 examples without computing a 2D unit representative."""

from pca_from_first_principles.direction_representatives import (
    LineOrientation,
    SignedDisplacementM,
    amount_of,
    compose_displacement,
    orientation_of,
)
from pca_from_first_principles.spatial_vectors import (
    MagnitudeM,
    ScaleFactor,
    SpatialVector,
    XChangeM,
    YChangeM,
    magnitude,
    scale,
)


def main() -> None:
    """Keep directed displacements, amounts, and representatives distinct."""
    equal_size_vectors: tuple[SpatialVector, ...] = (
        SpatialVector(XChangeM(3.0), YChangeM(4.0)),
        SpatialVector(XChangeM(-3.0), YChangeM(4.0)),
        SpatialVector(XChangeM(0.0), YChangeM(5.0)),
        SpatialVector(XChangeM(-5.0), YChangeM(0.0)),
    )
    print("Different directions, equal magnitude:")
    for vector in equal_size_vectors:
        amount: MagnitudeM = magnitude(vector)
        print(f"  ({vector.dx:g}, {vector.dy:g}) m -> {amount:g} m")

    reference: SpatialVector = equal_size_vectors[0]
    factors: tuple[ScaleFactor, ...] = (
        ScaleFactor(1.0),
        ScaleFactor(2.0),
        ScaleFactor(0.1),
    )
    print("Same ray, different amounts (positive scaling):")
    for factor in factors:
        scaled: SpatialVector = scale(reference, factor)
        print(f"  ({scaled.dx:g}, {scaled.dy:g}) m -> {magnitude(scaled):g} m")

    print("Line displacement = amount x standard orientation representative:")
    displacements: tuple[SignedDisplacementM, ...] = (
        SignedDisplacementM(5.0),
        SignedDisplacementM(-5.0),
        SignedDisplacementM(37.0),
        SignedDisplacementM(0.2),
    )
    for displacement in displacements:
        orientation: LineOrientation = orientation_of(displacement)
        line_amount: MagnitudeM = amount_of(displacement)
        reconstructed: SignedDisplacementM = compose_displacement(
            line_amount, orientation
        )
        print(
            f"  {displacement:+g} m = {line_amount:g} m x "
            f"({orientation.value:+d}); {orientation.name.lower()}; "
            f"reconstructed {reconstructed:+g} m"
        )


if __name__ == "__main__":
    main()
