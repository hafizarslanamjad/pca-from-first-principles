"""Lecture 15: joint signs, marginal information, and zero covariance."""

import pytest

from pca_from_first_principles.centering import center
from pca_from_first_principles.deviation_products import (
    cross_product,
    summarize_products,
)
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)


def dataset(
    rows: tuple[tuple[float, float], ...], baseline: float = 10.0
) -> ComponentDataset:
    return ComponentDataset(
        tuple(
            LengthWidthObservation(
                ObservationId(str(i)), LengthCm(baseline + a), WidthCm(baseline + b)
            )
            for i, (a, b) in enumerate(rows)
        )
    )


@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_worked_products_and_population_average(sign: float) -> None:
    data = dataset(
        ((-2.0, -3.0 * sign), (-1.0, -sign), (1.0, 2.0 * sign), (2.0, 2.0 * sign))
    )
    products = tuple(
        cross_product(item.deviation) for item in center(data).observations
    )
    assert products == pytest.approx(
        tuple(sign * value for value in (6.0, 1.0, 2.0, 4.0))
    )
    assert summarize_products(data).length_width_covariance == sign * 3.25


def test_identical_marginal_variances_hide_opposite_relationships() -> None:
    rows = ((-2.0, -3.0), (-1.0, -2.0), (1.0, 2.0), (2.0, 3.0))
    a = summarize_products(dataset(rows))
    b = summarize_products(dataset(tuple((x, -y) for x, y in rows)))
    assert a.length_variance == b.length_variance == 2.5
    assert a.width_variance == b.width_variance == 6.5
    assert a.length_width_covariance == 4.0
    assert b.length_width_covariance == -4.0


def test_independent_reference_shifts_leave_covariance_unchanged() -> None:
    rows = ((-2.0, -3.0), (-1.0, -1.0), (1.0, 2.0), (2.0, 2.0))
    original = summarize_products(dataset(rows))
    shifted = summarize_products(dataset(tuple((x + 1000, y + 2000) for x, y in rows)))
    assert shifted.length_width_covariance == original.length_width_covariance


def test_zero_covariance_can_hide_a_deterministic_curve() -> None:
    rows = tuple((x, x * x) for x in (-2.0, -1.0, 0.0, 1.0, 2.0))
    result = summarize_products(dataset(rows))
    assert result.length_width_covariance == 0.0
    assert result.length_variance > 0.0
    assert result.width_variance > 0.0


def test_self_covariance_and_exchange_symmetry() -> None:
    rows = ((-2.0, -3.0), (-1.0, -1.0), (1.0, 2.0), (2.0, 2.0))
    original = summarize_products(dataset(rows))
    exchanged = summarize_products(dataset(tuple((y, x) for x, y in rows)))
    self_pair = summarize_products(dataset(tuple((x, x) for x, _ in rows)))
    assert exchanged.length_width_covariance == original.length_width_covariance
    assert float(self_pair.length_width_covariance) == float(original.length_variance)
