"""Test geometry, aggregation axes, and coordinated signs separately."""

import pytest

from pca_from_first_principles.deviation_products import (
    cross_product,
    squared_magnitude,
    summarize_products,
)
from pca_from_first_principles.feature_space import LengthChangeCm, LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthDifference,
    LengthWidthObservation,
    ObservationId,
    WidthChangeCm,
    WidthCm,
)


def deviation(a: float, b: float) -> LengthWidthDifference:
    return LengthWidthDifference(LengthChangeCm(a), WidthChangeCm(b))


def dataset(rows: tuple[tuple[float, float], ...]) -> ComponentDataset:
    return ComponentDataset(
        tuple(
            LengthWidthObservation(ObservationId(str(i)), LengthCm(a), WidthCm(b))
            for i, (a, b) in enumerate(rows)
        )
    )


def test_magnitude_and_scaling() -> None:
    assert squared_magnitude(deviation(3, 4)) == 25.0
    assert squared_magnitude(deviation(1.5, 0.75)) == 2.8125
    for scale in (-2, 0, 2):
        assert squared_magnitude(deviation(scale * 3, scale * 4)) == float(
            scale**2 * 25
        )


@pytest.mark.parametrize(
    "a,b,expected",
    [(2.0, 3.0, 6.0), (-2.0, -3.0, 6.0), (2.0, -3.0, -6.0), (0.0, 3.0, 0.0)],
)
def test_signs(a: float, b: float, expected: float) -> None:
    assert cross_product(deviation(a, b)) == expected


def test_aggregation_axes() -> None:
    result = summarize_products(
        dataset(((10.0, 4.0), (12.0, 5.0), (9.0, 3.0), (11.0, 5.0)))
    )
    assert result.observation_squared_magnitudes == pytest.approx(
        (0.3125, 2.8125, 3.8125, 0.8125)
    )
    assert result.length_variance == 1.25
    assert result.width_variance == 0.6875
    assert result.length_width_covariance == 0.875
    assert (
        sum(result.observation_squared_magnitudes) / 4
        == result.length_variance + result.width_variance
    )


def test_same_variances_opposite_covariance() -> None:
    positive = summarize_products(dataset(((1.0, 1.0), (2.0, 2.0), (3.0, 3.0))))
    negative = summarize_products(dataset(((1.0, 3.0), (2.0, 2.0), (3.0, 1.0))))
    assert positive.length_variance == negative.length_variance
    assert positive.width_variance == negative.width_variance
    assert positive.length_width_covariance == -negative.length_width_covariance


def test_translation_and_row_order() -> None:
    original = summarize_products(dataset(((1.0, 2.0), (3.0, 5.0), (2.0, 4.0))))
    shifted = summarize_products(dataset(((12.0, 24.0), (13.0, 25.0), (11.0, 22.0))))
    assert shifted.length_variance == pytest.approx(original.length_variance)
    assert shifted.width_variance == pytest.approx(original.width_variance)
    assert shifted.length_width_covariance == pytest.approx(
        original.length_width_covariance
    )


def test_empty_rejected() -> None:
    with pytest.raises(ValueError):
        summarize_products(dataset(()))


@pytest.mark.parametrize("size", [1e200, 1e-200])
def test_unrepresentable_square_rejected(size: float) -> None:
    with pytest.raises(ValueError):
        squared_magnitude(deviation(size, 0))
