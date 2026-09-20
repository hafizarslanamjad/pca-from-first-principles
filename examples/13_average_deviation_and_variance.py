"""Reproduce the lecture's cancellation, absolute-deviation, and variance examples."""

from math import fsum

from pca_from_first_principles.variance import FeatureCoordinateCm, summarize_feature


def main() -> None:
    for label, values in (
        ("Centered A", (-2.0, 0.0, 2.0)),
        ("Centered B", (-100.0, 0.0, 100.0)),
        ("Centered C", (0.0, 0.0, 0.0)),
        ("Observed A", (8.0, 10.0, 12.0)),
        ("Observed B", (0.0, 10.0, 20.0)),
    ):
        result = summarize_feature(tuple(FeatureCoordinateCm(x) for x in values))
        print(f"{label}: {values}")
        print(f"  Mean: {result.mean:g} cm; deviations: {result.deviations}")
        print(f"  Signed mean deviation: {fsum(result.deviations) / len(values):g} cm")
        print(f"  Mean absolute deviation: {result.mean_absolute_deviation:.6g} cm")
        print(f"  Squared deviations: {result.squared_deviations} cm²")
        print(f"  Population variance: {result.population_variance:.6g} cm²")


if __name__ == "__main__":
    main()
