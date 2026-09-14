"""Verify composition, translation, and scaling relationships."""

import unittest

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
    magnitude,
    move,
    scale,
)


class SpatialVectorTests(unittest.TestCase):
    def test_displacement_reconstructs_target(self) -> None:
        start: SpatialPoint = SpatialPoint(XPositionM(2.0), YPositionM(1.0))
        target: SpatialPoint = SpatialPoint(XPositionM(5.0), YPositionM(3.0))
        change: SpatialVector = displacement_from(start, target)
        self.assertEqual(move(start, change), target)
        shifted_start: SpatialPoint = SpatialPoint(XPositionM(12.0), YPositionM(11.0))
        shifted_target: SpatialPoint = SpatialPoint(XPositionM(15.0), YPositionM(13.0))
        self.assertEqual(displacement_from(shifted_start, shifted_target), change)

    def test_addition_matches_sequential_movement(self) -> None:
        start: SpatialPoint = SpatialPoint(XPositionM(2.0), YPositionM(1.0))
        first: SpatialVector = SpatialVector(XChangeM(3.0), YChangeM(2.0))
        second: SpatialVector = SpatialVector(XChangeM(1.0), YChangeM(4.0))
        self.assertEqual(
            move(move(start, first), second), move(start, add(first, second))
        )

    def test_scaling_size_and_component_proportions(self) -> None:
        vector: SpatialVector = SpatialVector(XChangeM(3.0), YChangeM(2.0))
        for value in (2.0, 0.5, -1.0, -3.0, 0.0):
            with self.subTest(factor=value):
                scaled: SpatialVector = scale(vector, ScaleFactor(value))
                self.assertAlmostEqual(
                    magnitude(scaled), abs(value) * magnitude(vector)
                )
                self.assertAlmostEqual(scaled.dx * vector.dy, scaled.dy * vector.dx)
        self.assertEqual(
            scale(vector, ScaleFactor(0.0)),
            SpatialVector(XChangeM(0.0), YChangeM(0.0)),
        )

    def test_reversal_cancels_and_scaling_distributes(self) -> None:
        first: SpatialVector = SpatialVector(XChangeM(3.0), YChangeM(2.0))
        second: SpatialVector = SpatialVector(XChangeM(-1.0), YChangeM(4.0))
        self.assertEqual(
            add(first, scale(first, ScaleFactor(-1.0))),
            SpatialVector(XChangeM(0.0), YChangeM(0.0)),
        )
        factor: ScaleFactor = ScaleFactor(2.0)
        self.assertEqual(
            scale(add(first, second), factor),
            add(scale(first, factor), scale(second, factor)),
        )


if __name__ == "__main__":
    unittest.main()
