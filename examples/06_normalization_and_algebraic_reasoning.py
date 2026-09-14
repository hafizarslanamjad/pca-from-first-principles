"""Execute the scaling, normalization, and reconstruction examples of Lecture 6."""

from pca_from_first_principles.normalization import (
    MagnitudeDirection,
    UnitDirection2D,
    decompose,
    normalize,
    reconstruct,
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
    """Show each mathematical role using semantic names and annotations."""
    vector: SpatialVector = SpatialVector(XChangeM(3.0), YChangeM(4.0))
    old_magnitude: MagnitudeM = magnitude(vector)
    scale_factor: ScaleFactor = ScaleFactor(5.0)
    scaled_vector: SpatialVector = scale(vector, scale_factor)
    new_magnitude: MagnitudeM = magnitude(scaled_vector)
    old_magnitude_squared: float = vector.dx**2 + vector.dy**2
    expanded_new_squared: float = scaled_vector.dx**2 + scaled_vector.dy**2
    factored_new_squared: float = scale_factor**2 * old_magnitude_squared
    print("Expose the old magnitude inside the scaled expression:")
    print(f"  r^2 = {old_magnitude_squared:g} m^2")
    print(f"  R^2 = {expanded_new_squared:g} m^2 = {factored_new_squared:g} m^2")
    print(f"  R = {new_magnitude:g} m = 5 x {old_magnitude:g} m")

    pieces: MagnitudeDirection = decompose(vector)
    direction: UnitDirection2D = pieces.direction
    rebuilt: SpatialVector = reconstruct(pieces.amount, direction)
    print("Extract direction, retain amount, and reconstruct:")
    print(f"  u = ({direction.x:g}, {direction.y:g}), dimensionless")
    print(f"  retained magnitude = {pieces.amount:g} m")
    print(f"  reconstructed v = ({rebuilt.dx:g}, {rebuilt.dy:g}) m")
    print(f"  component sum = {direction.x + direction.y:g}")
    print(f"  sum of component squares = {direction.x**2 + direction.y**2:g}")

    print("Positive scales give the same representative:")
    factors: tuple[ScaleFactor, ...] = (
        ScaleFactor(0.1),
        ScaleFactor(1.0),
        ScaleFactor(2.0),
    )
    for factor in factors:
        representative: UnitDirection2D = normalize(scale(vector, factor))
        print(f"  scale {factor:g}: ({representative.x:g}, {representative.y:g})")

    other_vector: SpatialVector = SpatialVector(XChangeM(3.0), YChangeM(2.0))
    other_pieces: MagnitudeDirection = decompose(other_vector)
    print("Reconnect with Lecture 4's (3, 2) example:")
    print(f"  magnitude = {other_pieces.amount:.6f} m")
    print(
        f"  direction = ({other_pieces.direction.x:.6f}, "
        f"{other_pieces.direction.y:.6f})"
    )


if __name__ == "__main__":
    main()
