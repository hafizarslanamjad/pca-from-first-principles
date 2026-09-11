"""Show that coordinates change with the origin but a displacement does not."""

from pca_from_first_principles.feature_space import (
    CoordinateFrame,
    Displacement,
    FeaturePoint,
    LengthCm,
    MassG,
    PointCoordinates,
    coordinates_in,
    difference_from,
    translated,
)


def main() -> None:
    """Connect the rod example to explicit point and coordinate types."""
    point_a: FeaturePoint = FeaturePoint(length=LengthCm(10.0), mass=MassG(40.0))
    point_b: FeaturePoint = FeaturePoint(length=LengthCm(15.0), mass=MassG(60.0))
    frame_e: CoordinateFrame = CoordinateFrame(LengthCm(0.0), MassG(0.0))
    frame_f: CoordinateFrame = CoordinateFrame(LengthCm(5.0), MassG(20.0))
    a_in_e: PointCoordinates = coordinates_in(point_a, frame_e)
    b_in_e: PointCoordinates = coordinates_in(point_b, frame_e)
    a_in_f: PointCoordinates = coordinates_in(point_a, frame_f)
    b_in_f: PointCoordinates = coordinates_in(point_b, frame_f)
    change_e: Displacement = difference_from(a_in_e, b_in_e)
    change_f: Displacement = difference_from(a_in_f, b_in_f)
    reached: FeaturePoint = translated(point_a, change_e)

    print(f"B in E: ({b_in_e.length:g} cm, {b_in_e.mass:g} g)")
    print(f"B in F: ({b_in_f.length:g} cm, {b_in_f.mass:g} g)")
    print(f"A to B in E: ({change_e.length:g} cm, {change_e.mass:g} g)")
    print(f"A to B in F: ({change_f.length:g} cm, {change_f.mass:g} g)")
    print(f"Same displacement after shifting origin: {change_e == change_f}")
    print(f"A plus displacement reaches B: {reached == point_b}")


if __name__ == "__main__":
    main()
