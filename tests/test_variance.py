"""Relationships that distinguish location, direction, and collection spread."""

import math

import pytest

from pca_from_first_principles.variance import FeatureCoordinateCm, summarize_feature


def coordinates(*values: float) -> tuple[FeatureCoordinateCm, ...]:
    return tuple(FeatureCoordinateCm(x) for x in values)


def test_worked_example() -> None:
    result = summarize_feature(coordinates(8, 10, 12))
    assert result.mean == 10.0
    assert result.deviations == (-2.0, 0.0, 2.0)
    assert result.squared_deviations == (4.0, 0.0, 4.0)
    assert result.mean_absolute_deviation == pytest.approx(4 / 3)
    assert result.population_variance == pytest.approx(8 / 3)


def test_signed_cancellation_does_not_measure_spread() -> None:
    results = [summarize_feature(coordinates(-a, 0, a)) for a in (0, 2, 100)]
    assert all(math.fsum(r.deviations) == 0 for r in results)
    assert results[0].population_variance < results[1].population_variance
    assert results[1].population_variance < results[2].population_variance


@pytest.mark.parametrize("factor", [-3.0, 0.0, 2.0])
def test_scaling_and_translation(factor: float) -> None:
    original = summarize_feature(coordinates(8, 10, 12))
    changed = summarize_feature(coordinates(*(100 + factor * x for x in (8, 10, 12))))
    assert changed.population_variance == pytest.approx(
        factor**2 * original.population_variance
    )
    assert changed.mean_absolute_deviation == pytest.approx(
        abs(factor) * original.mean_absolute_deviation
    )


@pytest.mark.parametrize("values", [(7.0,), (7.0, 7.0, 7.0)])
def test_constant_collection(values: tuple[float, ...]) -> None:
    assert summarize_feature(coordinates(*values)).population_variance == 0.0


@pytest.mark.parametrize(
    "values",
    [(), (math.nan,), (math.inf,), (-math.inf,), (-1e200, 1e200), (-1e-200, 1e-200)],
)
def test_invalid_or_unrepresentable_inputs(values: tuple[float, ...]) -> None:
    with pytest.raises(ValueError):
        summarize_feature(coordinates(*values))


def test_order_and_duplication_preserve_population_summary() -> None:
    values = coordinates(8, 10, 12)
    reference = summarize_feature(values)
    for reordered in (values[::-1], values * 2):
        result = summarize_feature(reordered)
        assert result.mean == reference.mean
        assert result.population_variance == reference.population_variance
