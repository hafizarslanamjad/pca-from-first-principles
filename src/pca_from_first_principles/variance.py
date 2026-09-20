"""Population spread of one chosen feature axis measured in centimeters.

Feature coordinates can be signed or zero. These are not positive physical
component sizes. NewType documents roles; functions validate finite inputs
and reject unrepresentable squared contributions instead of silently losing them.
"""

from dataclasses import dataclass
from math import fsum, isfinite
from typing import NewType

FeatureCoordinateCm = NewType("FeatureCoordinateCm", float)
FeatureMeanCm = NewType("FeatureMeanCm", float)
DeviationCm = NewType("DeviationCm", float)
SquaredDeviationCm2 = NewType("SquaredDeviationCm2", float)
MeanAbsoluteDeviationCm = NewType("MeanAbsoluteDeviationCm", float)
PopulationVarianceCm2 = NewType("PopulationVarianceCm2", float)


@dataclass(frozen=True)
class FeatureSpread:
    """One-feature summary and observation-specific intermediate quantities."""

    mean: FeatureMeanCm
    deviations: tuple[DeviationCm, ...]
    squared_deviations: tuple[SquaredDeviationCm2, ...]
    mean_absolute_deviation: MeanAbsoluteDeviationCm
    population_variance: PopulationVarianceCm2


def summarize_feature(values: tuple[FeatureCoordinateCm, ...]) -> FeatureSpread:
    """Use divisor n: summarize this full collection, not estimate with n-1.

    Construct records through this function for validated results. Annotations
    and the output dataclass alone do not enforce units or numerical invariants.
    Floating-point cancellation and rounding still apply.
    """
    if not values or not all(isfinite(value) for value in values):
        raise ValueError("Provide a nonempty collection of finite coordinates.")
    count = len(values)
    mean = FeatureMeanCm(fsum(value / count for value in values))
    deviations = tuple(DeviationCm(value - mean) for value in values)
    squares = tuple(SquaredDeviationCm2(value * value) for value in deviations)
    if any(not isfinite(value) for value in deviations + squares):
        raise ValueError("Deviation or squared deviation is not representable.")
    if any(d != 0.0 and s == 0.0 for d, s in zip(deviations, squares, strict=True)):
        raise ValueError("A squared deviation underflowed to zero.")
    absolute_mean = fsum(abs(value) / count for value in deviations)
    variance = fsum(value / count for value in squares)
    if variance == 0.0 and any(value != 0.0 for value in squares):
        raise ValueError("Population variance underflowed to zero.")
    return FeatureSpread(
        mean=mean,
        deviations=deviations,
        squared_deviations=squares,
        mean_absolute_deviation=MeanAbsoluteDeviationCm(absolute_mean),
        population_variance=PopulationVarianceCm2(variance),
    )
