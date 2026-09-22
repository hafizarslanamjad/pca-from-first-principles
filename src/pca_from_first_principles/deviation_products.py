"""Products of centimeter deviations in the declared equal-scale Euclidean model.

Reuses existing observation and deviation types. The metric is an explicit
modeling choice, not inferred from units or enforced by static annotations.
"""

from dataclasses import dataclass
from math import fsum, isfinite
from typing import NewType

from pca_from_first_principles.centering import center
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthDifference,
)
from pca_from_first_principles.variance import PopulationVarianceCm2

SquaredMagnitudeCm2 = NewType("SquaredMagnitudeCm2", float)
DeviationProductCm2 = NewType("DeviationProductCm2", float)
PopulationCovarianceCm2 = NewType("PopulationCovarianceCm2", float)


def checked_product(first: float, second: float) -> float:
    """Reject nonfinite inputs, product overflow, and complete underflow."""
    product = first * second
    if not all(isfinite(x) for x in (first, second, product)):
        raise ValueError("Inputs and product must be finite.")
    if first != 0.0 and second != 0.0 and product == 0.0:
        raise ValueError("Product underflowed to zero.")
    return product


def squared_magnitude(deviation: LengthWidthDifference) -> SquaredMagnitudeCm2:
    """Sum coordinate squares under the explicitly chosen feature metric."""
    first = checked_product(deviation.length, deviation.length)
    second = checked_product(deviation.width, deviation.width)
    result = first + second
    if not isfinite(result):
        raise ValueError("Squared magnitude is not representable.")
    return SquaredMagnitudeCm2(result)


def cross_product(deviation: LengthWidthDifference) -> DeviationProductCm2:
    """Multiply length and width deviations; not the geometric vector cross product."""
    return DeviationProductCm2(checked_product(deviation.length, deviation.width))


@dataclass(frozen=True)
class DeviationSummary:
    """Separate per-observation magnitudes from feature-level population moments.

    Construct through summarize_products for calculated results. The record
    itself does not validate mathematical or physical-unit invariants.
    """

    observation_squared_magnitudes: tuple[SquaredMagnitudeCm2, ...]
    length_variance: PopulationVarianceCm2
    width_variance: PopulationVarianceCm2
    length_width_covariance: PopulationCovarianceCm2


def summarize_products(dataset: ComponentDataset) -> DeviationSummary:
    """Center raw observations, then average products with population divisor n.

    Empty input is rejected by center. All operations use floats and are subject
    to rounding. Retaining both feature variances alone loses cross-feature signs.
    """
    centered = center(dataset)
    deviations = tuple(item.deviation for item in centered.observations)
    count = len(deviations)
    return DeviationSummary(
        observation_squared_magnitudes=tuple(squared_magnitude(d) for d in deviations),
        length_variance=PopulationVarianceCm2(
            fsum(checked_product(d.length, d.length) / count for d in deviations)
        ),
        width_variance=PopulationVarianceCm2(
            fsum(checked_product(d.width, d.width) / count for d in deviations)
        ),
        length_width_covariance=PopulationCovarianceCm2(
            fsum(cross_product(d) / count for d in deviations)
        ),
    )
