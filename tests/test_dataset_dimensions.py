"""Verify semantic counts, aggregation axes, and feature extension."""

import sys

import numpy as np
import pytest

from pca_from_first_principles.dataset_dimensions import (
    LengthWidthThicknessObservation,
    ThicknessCm,
    column_means,
    shape_of,
    thickness_matrix,
)
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)


def record(length: float = 10.0, width: float = 4.0) -> LengthWidthObservation:
    """A typed observation under the shared centimeter schema."""
    return LengthWidthObservation(
        ObservationId("test"), LengthCm(length), WidthCm(width)
    )


@pytest.mark.parametrize("count", [0, 1, 2, 4, 1000])
def test_more_rows_do_not_add_features(count: int) -> None:
    shape = shape_of(ComponentDataset((record(),) * count).to_matrix())
    assert shape.observations == count
    assert shape.features == 2


def test_source_means_preserve_feature_identity() -> None:
    data = ComponentDataset((record(10, 4), record(12, 5), record(9, 3), record(11, 5)))
    means = column_means(data)
    assert means.length == pytest.approx(10.5)
    assert means.width == pytest.approx(4.25)
    np.testing.assert_allclose(
        [means.length, means.width], data.to_matrix().mean(axis=0)
    )
    assert data.to_matrix().mean(axis=1)[0] == 7.0
    repeated = column_means(ComponentDataset(data.observations * 2))
    assert repeated == means


def test_empty_dataset_has_shape_but_no_mean() -> None:
    with pytest.raises(ValueError, match="empty"):
        column_means(ComponentDataset(()))


def test_mean_of_large_values_does_not_overflow_raw_sum() -> None:
    value = sys.float_info.max
    means = column_means(ComponentDataset((record(value, value),) * 4))
    assert means.length == value
    assert means.width == value


def test_mean_of_smallest_positive_values_is_retained() -> None:
    value = float.fromhex("0x0.0000000000001p-1022")
    means = column_means(ComponentDataset((record(value, value),) * 4))
    assert means.length == value
    assert means.width == value


def test_dependent_thickness_still_adds_a_feature_slot() -> None:
    records = tuple(
        LengthWidthThicknessObservation(
            ObservationId(str(index)),
            LengthCm(length),
            WidthCm(width),
            ThicknessCm(0.1 * length),
        )
        for index, (length, width) in enumerate(((10.0, 4.0), (12.0, 5.0)))
    )
    matrix = thickness_matrix(records)
    assert shape_of(matrix).observations == 2
    assert shape_of(matrix).features == 3
    np.testing.assert_allclose(matrix[:, 2], 0.1 * matrix[:, 0])
    np.testing.assert_array_equal(matrix[:, :2], [[10, 4], [12, 5]])
    assert thickness_matrix(()).shape == (0, 3)


@pytest.mark.parametrize("value", [0.0, -1.0, float("nan"), float("inf")])
def test_thickness_validation(value: float) -> None:
    with pytest.raises(ValueError, match="Thickness"):
        LengthWidthThicknessObservation(
            ObservationId("A"), LengthCm(10), WidthCm(4), ThicknessCm(value)
        )


def test_extended_record_keeps_existing_length_validation() -> None:
    with pytest.raises(ValueError, match="measurements"):
        LengthWidthThicknessObservation(
            ObservationId("A"), LengthCm(-10), WidthCm(4), ThicknessCm(1)
        )


@pytest.mark.parametrize("shape", [(2,), (1, 2, 3)])
def test_shape_requires_two_array_axes(shape: tuple[int, ...]) -> None:
    with pytest.raises(ValueError, match="matrix"):
        shape_of(np.zeros(shape, dtype=np.float64))
