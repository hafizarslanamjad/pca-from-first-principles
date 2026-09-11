"""Check affine relationships and frame compatibility on exact examples."""

import unittest

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


class FeatureSpaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.a: FeaturePoint = FeaturePoint(LengthCm(10.0), MassG(40.0))
        self.b: FeaturePoint = FeaturePoint(LengthCm(15.0), MassG(60.0))
        self.e: CoordinateFrame = CoordinateFrame(LengthCm(0.0), MassG(0.0))
        self.f: CoordinateFrame = CoordinateFrame(LengthCm(5.0), MassG(20.0))

    def test_origin_shift_changes_coordinates_not_difference(self) -> None:
        a_e: PointCoordinates = coordinates_in(self.a, self.e)
        b_e: PointCoordinates = coordinates_in(self.b, self.e)
        a_f: PointCoordinates = coordinates_in(self.a, self.f)
        b_f: PointCoordinates = coordinates_in(self.b, self.f)
        self.assertEqual((b_e.length, b_e.mass), (15.0, 60.0))
        self.assertEqual((b_f.length, b_f.mass), (10.0, 40.0))
        self.assertEqual(difference_from(a_e, b_e), difference_from(a_f, b_f))

    def test_displacement_reconstructs_target_and_reverses(self) -> None:
        a: PointCoordinates = coordinates_in(self.a, self.e)
        b: PointCoordinates = coordinates_in(self.b, self.e)
        forward: Displacement = difference_from(a, b)
        backward: Displacement = difference_from(b, a)
        self.assertEqual(translated(self.a, forward), self.b)
        self.assertEqual(translated(self.b, backward), self.a)
        self.assertEqual(forward.length, -backward.length)
        self.assertEqual(forward.mass, -backward.mass)
        zero: Displacement = difference_from(a, a)
        self.assertEqual(translated(self.a, zero), self.a)

    def test_mixed_origins_are_rejected(self) -> None:
        a: PointCoordinates = coordinates_in(self.a, self.e)
        b: PointCoordinates = coordinates_in(self.b, self.f)
        with self.assertRaisesRegex(ValueError, "same frame"):
            difference_from(a, b)


if __name__ == "__main__":
    unittest.main()
