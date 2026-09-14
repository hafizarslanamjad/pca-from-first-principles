"""Test retention of amount and orientation, including the zero boundary."""

import unittest

from pca_from_first_principles.direction_representatives import (
    LineOrientation,
    SignedDisplacementM,
    amount_of,
    compose_displacement,
    orientation_of,
)
from pca_from_first_principles.spatial_vectors import MagnitudeM


class DirectionRepresentativeTests(unittest.TestCase):
    def test_amount_discards_orientation(self) -> None:
        self.assertEqual(
            amount_of(SignedDisplacementM(5.0)),
            amount_of(SignedDisplacementM(-5.0)),
        )
        self.assertNotEqual(
            orientation_of(SignedDisplacementM(5.0)),
            orientation_of(SignedDisplacementM(-5.0)),
        )

    def test_nonzero_displacements_reconstruct(self) -> None:
        for value in (-37.0, -5.0, -0.2, 0.01, 5.0, 37.0):
            with self.subTest(value=value):
                displacement = SignedDisplacementM(value)
                self.assertEqual(
                    compose_displacement(
                        amount_of(displacement), orientation_of(displacement)
                    ),
                    displacement,
                )

    def test_direction_ignores_positive_amount(self) -> None:
        for value in (0.01, 5.0, 37.0):
            self.assertIs(
                orientation_of(SignedDisplacementM(value)), LineOrientation.RIGHT
            )

    def test_zero_has_amount_but_no_unique_orientation(self) -> None:
        self.assertEqual(amount_of(SignedDisplacementM(0.0)), 0.0)
        with self.assertRaises(ValueError):
            orientation_of(SignedDisplacementM(0.0))
        for orientation in LineOrientation:
            self.assertEqual(compose_displacement(MagnitudeM(0.0), orientation), 0.0)

    def test_negative_amount_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            compose_displacement(MagnitudeM(-5.0), LineOrientation.RIGHT)

    def test_nonfinite_quantities_are_rejected(self) -> None:
        for value in (float("inf"), float("-inf"), float("nan")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    orientation_of(SignedDisplacementM(value))
                with self.assertRaises(ValueError):
                    amount_of(SignedDisplacementM(value))
                with self.assertRaises(ValueError):
                    compose_displacement(MagnitudeM(value), LineOrientation.RIGHT)


if __name__ == "__main__":
    unittest.main()
