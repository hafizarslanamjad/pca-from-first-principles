"""Check feature roles, dataset layout, and meaningful numerical boundaries."""

import numpy as np
import pytest

from pca_from_first_principles.feature_space import LengthChangeCm, LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthDifference,
    LengthWidthObservation,
    ObservationId,
    WidthChangeCm,
    WidthCm,
    difference_from,
)


def observation(name: str, length: float, width: float) -> LengthWidthObservation:
    """Create a record under the fixed test measurement scheme."""
    return LengthWidthObservation(ObservationId(name), LengthCm(length), WidthCm(width))


def test_directed_difference_and_endpoint_reconstruction() -> None:
    first = observation("A", 10.0, 4.0)
    second = observation("B", 12.0, 5.0)
    change = difference_from(first, second)
    reverse = difference_from(second, first)
    assert (change.length, change.width) == (2.0, 1.0)
    assert (reverse.length, reverse.width) == (-2.0, -1.0)
    assert first.length + change.length == second.length
    assert first.width + change.width == second.width
    assert difference_from(first, first) == LengthWidthDifference(
        LengthChangeCm(0.0), WidthChangeCm(0.0)
    )


def test_dataset_rows_columns_and_index_roles() -> None:
    dataset = ComponentDataset(
        (
            observation("A", 10.0, 4.0),
            observation("B", 12.0, 5.0),
            observation("C", 9.0, 3.0),
            observation("D", 11.0, 5.0),
        )
    )
    matrix = dataset.to_matrix()
    np.testing.assert_array_equal(matrix, [[10, 4], [12, 5], [9, 3], [11, 5]])
    assert matrix.shape == (4, 2)
    assert matrix.dtype == np.dtype(np.float64)
    np.testing.assert_array_equal(matrix[:, 0], dataset.length_column())
    np.testing.assert_array_equal(matrix[:, 1], dataset.width_column())
    for row, record in zip(matrix, dataset.observations, strict=True):
        np.testing.assert_array_equal(row, [record.length, record.width])
    assert matrix[2, 1] == 3.0


def test_reordering_observations_moves_rows_not_feature_roles() -> None:
    first = observation("A", 10.0, 4.0)
    second = observation("B", 12.0, 5.0)
    forward = ComponentDataset((first, second)).to_matrix()
    reverse = ComponentDataset((second, first)).to_matrix()
    np.testing.assert_array_equal(reverse, forward[::-1])
    assert reverse.shape == (2, 2)


def test_equal_measurements_do_not_imply_same_component_identifier() -> None:
    first = observation("A", 10.0, 4.0)
    second = observation("B", 10.0, 4.0)
    matrix = ComponentDataset((first, second)).to_matrix()
    assert first.identifier != second.identifier
    np.testing.assert_array_equal(matrix[0], matrix[1])


def test_array_export_does_not_mutate_measurement_records() -> None:
    dataset = ComponentDataset((observation("A", 10.0, 4.0),))
    exported = dataset.to_matrix()
    exported[0, 0] = 999.0
    assert dataset.observations[0].length == 10.0
    assert dataset.to_matrix()[0, 0] == 10.0


def test_empty_dataset_preserves_feature_schema() -> None:
    empty = ComponentDataset(())
    assert empty.to_matrix().shape == (0, 2)
    assert empty.length_column() == ()
    assert empty.width_column() == ()


@pytest.mark.parametrize(
    "invalid", [0.0, -1.0, float("nan"), float("inf"), -float("inf")]
)
@pytest.mark.parametrize("invalid_length", [True, False])
def test_observations_reject_nonphysical_or_nonfinite_measurements(
    invalid: float, invalid_length: bool
) -> None:
    with pytest.raises(ValueError, match="finite and positive"):
        observation(
            "A", invalid if invalid_length else 10.0, 4.0 if invalid_length else invalid
        )


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -float("inf")])
@pytest.mark.parametrize("invalid_length", [True, False])
def test_differences_reject_nonfinite_values(
    invalid: float, invalid_length: bool
) -> None:
    with pytest.raises(ValueError, match="finite"):
        LengthWidthDifference(
            LengthChangeCm(invalid if invalid_length else -2.0),
            WidthChangeCm(-1.0 if invalid_length else invalid),
        )
