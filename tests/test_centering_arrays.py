"""Verify common-reference broadcasting and the relationships it preserves."""

import numpy as np
import pytest

from pca_from_first_principles.centering import center
from pca_from_first_principles.centering_arrays import center_with_broadcasting
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)


def example_dataset(length_shift: float = 0.0) -> ComponentDataset:
    """The four source observations, optionally translated in length."""
    return ComponentDataset(
        tuple(
            LengthWidthObservation(
                ObservationId(str(i)), LengthCm(length + length_shift), WidthCm(width)
            )
            for i, (length, width) in enumerate(
                ((10.0, 4.0), (12.0, 5.0), (9.0, 3.0), (11.0, 5.0))
            )
        )
    )


def test_broadcasting_matches_typed_centering_and_source_values() -> None:
    dataset = example_dataset()
    reference, deviations = center_with_broadcasting(dataset)
    assert (reference.length, reference.width) == (10.5, 4.25)
    assert deviations.shape == (4, 2)
    np.testing.assert_allclose(
        deviations, [[-0.5, -0.25], [1.5, 0.75], [-1.5, -1.25], [0.5, 0.75]]
    )
    np.testing.assert_allclose(deviations, center(dataset).to_matrix())
    np.testing.assert_allclose(deviations.mean(axis=0), [0, 0], atol=1e-12)


def test_every_pairwise_displacement_is_preserved() -> None:
    dataset = example_dataset()
    original = dataset.to_matrix()
    _, deviations = center_with_broadcasting(dataset)
    for first in range(len(original)):
        for second in range(len(original)):
            np.testing.assert_allclose(
                deviations[second] - deviations[first],
                original[second] - original[first],
                atol=1e-12,
            )


def test_retained_mean_reconstructs_without_mutating_input() -> None:
    dataset = example_dataset()
    before = dataset.to_matrix()
    reference, deviations = center_with_broadcasting(dataset)
    np.testing.assert_allclose(deviations + [reference.length, reference.width], before)
    deviations[0, 0] = 999
    np.testing.assert_array_equal(dataset.to_matrix(), before)


@pytest.mark.parametrize("shift", [90.0, 990.0, 1000.0])
def test_centered_configuration_alone_does_not_identify_location(shift: float) -> None:
    first_reference, first = center_with_broadcasting(example_dataset())
    other_reference, other = center_with_broadcasting(example_dataset(shift))
    np.testing.assert_allclose(first, other, atol=1e-12)
    assert other_reference.length - first_reference.length == pytest.approx(shift)


def test_empty_dataset_has_no_mean() -> None:
    with pytest.raises(ValueError, match="empty"):
        center_with_broadcasting(ComponentDataset(()))


@pytest.mark.parametrize(
    "deviations", [[-2.0, 0.0, 2.0], [-100.0, 0.0, 100.0], [0.0, 0.0, 0.0]]
)
def test_signed_average_cannot_distinguish_supplied_spreads(
    deviations: list[float],
) -> None:
    assert np.array(deviations, dtype=np.float64).mean() == 0.0
