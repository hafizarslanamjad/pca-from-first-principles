"""Check feature identities and the independently computed matrix formula."""

import numpy as np
import pytest

from pca_from_first_principles.centering import center
from pca_from_first_principles.covariance_table import (
    FeatureRole,
    population_covariance_table,
)
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)


def dataset(rows: tuple[tuple[float, float], ...]) -> ComponentDataset:
    return ComponentDataset(
        tuple(
            LengthWidthObservation(ObservationId(str(i)), LengthCm(a), WidthCm(b))
            for i, (a, b) in enumerate(rows)
        )
    )


ROWS = ((10.0, 4.0), (12.0, 5.0), (9.0, 3.0), (11.0, 5.0))


def test_worked_table_and_feature_lookup() -> None:
    table = population_covariance_table(dataset(ROWS))
    np.testing.assert_allclose(table.to_matrix(), [[1.25, 0.875], [0.875, 0.6875]])
    assert table.entry(FeatureRole.LENGTH, FeatureRole.LENGTH) == 1.25
    assert table.entry(FeatureRole.WIDTH, FeatureRole.WIDTH) == 0.6875
    assert table.entry(FeatureRole.LENGTH, FeatureRole.WIDTH) == table.entry(
        FeatureRole.WIDTH, FeatureRole.LENGTH
    )


def test_relationship_table_matches_matrix_product_and_numpy() -> None:
    data = dataset(ROWS)
    values = center(data).to_matrix()
    actual = population_covariance_table(data).to_matrix()
    assert values.shape == (4, 2)
    assert actual.shape == (2, 2)
    np.testing.assert_allclose(actual, values.T @ values / 4)
    np.testing.assert_allclose(
        actual, np.cov(data.to_matrix(), rowvar=False, bias=True)
    )


def test_feature_swap_reorders_both_output_axes() -> None:
    original = population_covariance_table(dataset(ROWS)).to_matrix()
    swapped = population_covariance_table(
        dataset(tuple((b, a) for a, b in ROWS))
    ).to_matrix()
    np.testing.assert_allclose(swapped, original[::-1, ::-1])


@pytest.mark.parametrize(
    "rows", [ROWS[::-1], ROWS * 2, tuple((a + 100, b + 200) for a, b in ROWS)]
)
def test_discarded_row_identity_and_location(
    rows: tuple[tuple[float, float], ...],
) -> None:
    np.testing.assert_allclose(
        population_covariance_table(dataset(rows)).to_matrix(),
        population_covariance_table(dataset(ROWS)).to_matrix(),
    )


def test_export_does_not_mutate_table() -> None:
    table = population_covariance_table(dataset(ROWS))
    exported = table.to_matrix()
    exported[0, 0] = 999
    assert table.entry(FeatureRole.LENGTH, FeatureRole.LENGTH) == 1.25


def test_single_observation_has_zero_population_covariance() -> None:
    np.testing.assert_array_equal(
        population_covariance_table(dataset(((10.0, 4.0),))).to_matrix(),
        np.zeros((2, 2)),
    )


def test_empty_rejected() -> None:
    with pytest.raises(ValueError):
        population_covariance_table(dataset(()))
