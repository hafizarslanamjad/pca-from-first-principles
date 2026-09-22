"""A feature-by-feature table, distinct from observation-by-feature data.

The existing length-width schema is measured in cm, so entries have cm² units.
Population divisor n is used. Static types document roles, not physical units.
"""

from dataclasses import dataclass
from enum import Enum
from math import isfinite

import numpy as np
from numpy.typing import NDArray

from pca_from_first_principles.deviation_products import (
    PopulationCovarianceCm2,
    summarize_products,
)
from pca_from_first_principles.observation_data import ComponentDataset
from pca_from_first_principles.variance import PopulationVarianceCm2


class FeatureRole(Enum):
    """Both axes of the covariance table use the same ordered feature schema."""

    LENGTH = 0
    WIDTH = 1


@dataclass(frozen=True)
class CovarianceTable2D:
    """Three distinct relationships determine the symmetric two-feature table.

    Validation checks finite values and nonnegative diagonal entries. It does
    not prove that an arbitrary manually constructed table comes from a dataset.
    Use population_covariance_table to obtain a computed covariance summary.
    """

    length_variance: PopulationVarianceCm2
    width_variance: PopulationVarianceCm2
    length_width_covariance: PopulationCovarianceCm2

    def __post_init__(self) -> None:
        if not all(
            isfinite(x)
            for x in (
                self.length_variance,
                self.width_variance,
                self.length_width_covariance,
            )
        ):
            raise ValueError("Covariance entries must be finite.")
        if self.length_variance < 0 or self.width_variance < 0:
            raise ValueError("Variances must be nonnegative.")

    def entry(self, first: FeatureRole, second: FeatureRole) -> PopulationCovarianceCm2:
        """Select a relationship by feature identities, not observation indices."""
        if first is second:
            variance = (
                self.length_variance
                if first is FeatureRole.LENGTH
                else self.width_variance
            )
            return PopulationCovarianceCm2(variance)
        return self.length_width_covariance

    def to_matrix(self) -> NDArray[np.float64]:
        """Export a fresh numeric array; both axes are ordered length, width."""
        return np.array(
            [
                [self.length_variance, self.length_width_covariance],
                [self.length_width_covariance, self.width_variance],
            ],
            dtype=np.float64,
        )


def population_covariance_table(dataset: ComponentDataset) -> CovarianceTable2D:
    """Package the validated pairwise calculations developed in Lecture 14.

    This explicitly constructs the desired relationship table; the companion
    independently demonstrates its equality to centered.T @ centered / n.
    Empty input and unrepresentable contributions are rejected upstream.
    """
    summary = summarize_products(dataset)
    return CovarianceTable2D(
        summary.length_variance, summary.width_variance, summary.length_width_covariance
    )
