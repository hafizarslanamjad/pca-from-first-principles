"""Test normalization's geometric contract and floating-point boundaries."""

import unittest
from math import hypot, isclose

from pca_from_first_principles.normalization import (
    DirectionX,
    DirectionY,
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


class NormalizationTests(unittest.TestCase):
    def test_three_four_unit_representative(self) -> None:
        direction = normalize(SpatialVector(XChangeM(3.0), YChangeM(4.0)))
        self.assertAlmostEqual(direction.x, 0.6)
        self.assertAlmostEqual(direction.y, 0.8)
        self.assertAlmostEqual(hypot(direction.x, direction.y), 1.0)
        self.assertNotAlmostEqual(direction.x + direction.y, 1.0)

    def test_reconstruction_across_quadrants_and_axes(self) -> None:
        cases = ((3.0, 4.0), (3.0, 2.0), (-3.0, 4.0), (0.0, -5.0), (-5.0, 0.0))
        for x, y in cases:
            with self.subTest(x=x, y=y):
                vector = SpatialVector(XChangeM(x), YChangeM(y))
                pieces = decompose(vector)
                rebuilt = reconstruct(pieces.amount, pieces.direction)
                self.assertAlmostEqual(rebuilt.dx, x)
                self.assertAlmostEqual(rebuilt.dy, y)

    def test_positive_scaling_preserves_representative(self) -> None:
        vector = SpatialVector(XChangeM(3.0), YChangeM(-4.0))
        original = normalize(vector)
        for factor in (0.01, 0.5, 2.0, 100.0):
            direction = normalize(scale(vector, ScaleFactor(factor)))
            self.assertAlmostEqual(direction.x, original.x)
            self.assertAlmostEqual(direction.y, original.y)

    def test_negative_scaling_reverses_representative(self) -> None:
        vector = SpatialVector(XChangeM(3.0), YChangeM(4.0))
        original = normalize(vector)
        reversed_direction = normalize(scale(vector, ScaleFactor(-5.0)))
        self.assertAlmostEqual(reversed_direction.x, -original.x)
        self.assertAlmostEqual(reversed_direction.y, -original.y)

    def test_magnitude_scaling_uses_absolute_factor(self) -> None:
        vector = SpatialVector(XChangeM(-3.0), YChangeM(2.0))
        for factor in (-5.0, -0.5, 0.0, 0.2, 5.0):
            self.assertAlmostEqual(
                magnitude(scale(vector, ScaleFactor(factor))),
                abs(factor) * magnitude(vector),
            )

    def test_zero_has_no_normalization_or_decomposition(self) -> None:
        zero = SpatialVector(XChangeM(0.0), YChangeM(0.0))
        with self.assertRaises(ValueError):
            normalize(zero)
        with self.assertRaises(ValueError):
            decompose(zero)
        direction = UnitDirection2D(DirectionX(1.0), DirectionY(0.0))
        self.assertEqual(reconstruct(MagnitudeM(0.0), direction), zero)

    def test_invalid_unit_representatives_are_rejected(self) -> None:
        for x, y in ((0.0, 0.0), (3.0, 4.0), (float("nan"), 0.0)):
            with self.assertRaises(ValueError):
                UnitDirection2D(DirectionX(x), DirectionY(y))

    def test_nonfinite_vectors_and_invalid_amounts_are_rejected(self) -> None:
        direction = UnitDirection2D(DirectionX(1.0), DirectionY(0.0))
        for invalid in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                normalize(SpatialVector(XChangeM(invalid), YChangeM(1.0)))
            with self.assertRaises(ValueError):
                reconstruct(MagnitudeM(invalid), direction)
        with self.assertRaises(ValueError):
            reconstruct(MagnitudeM(-1.0), direction)

    def test_normalization_handles_extreme_finite_components(self) -> None:
        for component in (1e-320, 1e308):
            with self.subTest(component=component):
                direction = normalize(
                    SpatialVector(XChangeM(component), YChangeM(-component))
                )
                self.assertTrue(isclose(hypot(direction.x, direction.y), 1.0))
                self.assertAlmostEqual(direction.x, -direction.y)
                self.assertGreater(direction.x, 0.0)

    def test_unrepresentable_magnitude_cannot_be_decomposed(self) -> None:
        vector = SpatialVector(XChangeM(1.7e308), YChangeM(1.7e308))
        direction = normalize(vector)
        self.assertTrue(isclose(hypot(direction.x, direction.y), 1.0))
        with self.assertRaises(ValueError):
            decompose(vector)


if __name__ == "__main__":
    unittest.main()
