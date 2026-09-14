"""Execute the lecture's point, composition, and scaling examples."""

from pca_from_first_principles.spatial_vectors import (
    ScaleFactor,
    SpatialPoint,
    SpatialVector,
    XChangeM,
    XPositionM,
    YChangeM,
    YPositionM,
    add,
    displacement_from,
    move,
    scale,
)


def main() -> None:
    """Keep positions, directed changes, and scalar sizes explicit."""
    start: SpatialPoint = SpatialPoint(XPositionM(2.0), YPositionM(1.0))
    target: SpatialPoint = SpatialPoint(XPositionM(5.0), YPositionM(3.0))
    vector: SpatialVector = displacement_from(start, target)
    next_change: SpatialVector = SpatialVector(XChangeM(1.0), YChangeM(4.0))
    total: SpatialVector = add(vector, next_change)
    reached: SpatialPoint = move(start, total)
    factors: tuple[ScaleFactor, ...] = (
        ScaleFactor(2.0),
        ScaleFactor(0.5),
        ScaleFactor(-1.0),
    )

    print(f"A to B: ({vector.dx:g}, {vector.dy:g}) m")
    print(f"Combined change: ({total.dx:g}, {total.dy:g}) m")
    print(f"Final point from A: ({reached.x:g}, {reached.y:g}) m")
    for factor in factors:
        scaled: SpatialVector = scale(vector, factor)
        print(f"Scale {factor:g}: ({scaled.dx:g}, {scaled.dy:g}) m")


if __name__ == "__main__":
    main()
