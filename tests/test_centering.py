"""Test the mean reference, signed deviations, and recoverable information."""

import numpy as np
import pytest

from pca_from_first_principles.centering import center, reconstruct
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)


def dataset_from(rows: tuple[tuple[float, float], ...]) -> ComponentDataset:
    """Build a positive, fixed-schema test dataset with row identifiers."""
    return ComponentDataset(
        tuple(
            LengthWidthObservation(
                ObservationId(str(index)), LengthCm(length), WidthCm(width)
            )
            for index, (length, width) in enumerate(rows)
        )
    )


def test_supplied_example_reference_deviations_and_balance() -> None:
    original = dataset_from(((10, 4), (12, 5), (9, 3), (11, 5)))
    centered = center(original)
    assert centered.reference.length == pytest.approx(10.5)
    assert centered.reference.width == pytest.approx(4.25)
    np.testing.assert_allclose(
        centered.to_matrix(), [[-0.5, -0.25], [1.5, 0.75], [-1.5, -1.25], [0.5, 0.75]]
    )
    np.testing.assert_allclose(centered.to_matrix().sum(axis=0), [0, 0], atol=1e-12)
    assert original.observations[1].length == 12.0
    assert centered.observations[1].deviation.length == 1.5


@pytest.mark.parametrize(
    "rows",
    [((10.0, 4.0),), ((10.0, 4.0), (10.0, 4.0)), ((0.2, 1.7), (9.4, 5.3), (3.1, 2.2))],
)
def test_retained_reference_reconstructs_values_and_identifiers(
    rows: tuple[tuple[float, float], ...],
) -> None:
    original = dataset_from(rows)
    recovered = reconstruct(center(original))
    np.testing.assert_allclose(
        recovered.to_matrix(), original.to_matrix(), rtol=1e-12, atol=1e-12
    )
    assert [item.identifier for item in recovered.observations] == [
        item.identifier for item in original.observations
    ]


def test_identical_observations_have_zero_deviations() -> None:
    centered = center(dataset_from(((10, 4), (10, 4), (10, 4))))
    np.testing.assert_array_equal(centered.to_matrix(), np.zeros((3, 2)))


def test_translated_lengths_retain_the_source_deviations() -> None:
    first = center(dataset_from(((10, 4), (12, 5), (9, 3), (11, 5))))
    shifted = center(dataset_from(((1000, 4), (1002, 5), (999, 3), (1001, 5))))
    assert shifted.reference.length == pytest.approx(1000.5)
    np.testing.assert_allclose(first.to_matrix(), shifted.to_matrix(), atol=1e-12)


def test_empty_dataset_cannot_define_a_mean_reference() -> None:
    with pytest.raises(ValueError, match="empty"):
        center(ComponentDataset(()))


def test_matrix_export_does_not_change_retained_deviations() -> None:
    centered = center(dataset_from(((10, 4), (12, 5))))
    matrix = centered.to_matrix()
    matrix[0, 0] = 999
    assert centered.observations[0].deviation.length == -1.0
    assert centered.to_matrix()[0, 0] == -1
