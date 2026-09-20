"""Plot the same-mean examples on identical coordinate scales."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from pca_from_first_principles.variance import FeatureCoordinateCm, summarize_feature


def main() -> None:
    plt.rcParams["svg.hashsalt"] = "lecture13"
    figure, axes = plt.subplots(2, 1, figsize=(9, 4.5), layout="constrained")
    for axis, label, values in zip(
        axes, ("A", "B"), ((8.0, 10.0, 12.0), (0.0, 10.0, 20.0)), strict=True
    ):
        summary = summarize_feature(tuple(FeatureCoordinateCm(x) for x in values))
        points = axis.scatter(values, [0.0] * 3, s=70, zorder=3)
        np.testing.assert_allclose(points.get_offsets()[:, 0], values)
        axis.axhline(0, color="gray", linewidth=1)
        axis.axvline(
            summary.mean, color="darkorange", linestyle="--", label="Mean = 10 cm"
        )
        axis.set(
            xlim=(-2, 22), ylim=(-0.5, 0.5), yticks=[], xlabel="Feature coordinate (cm)"
        )
        axis.set_title(
            f"Dataset {label}: population variance = {summary.population_variance:.4g} cm²"
        )
        axis.set_xticks(range(0, 21, 2))
        axis.legend(loc="upper right")
    destination = (
        Path(__file__).resolve().parents[1]
        / "lectures/13-average-deviation-and-variance"
    )
    destination.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        destination / "same-mean-different-spread.svg", metadata={"Date": None}
    )
    figure.savefig(destination / "same-mean-different-spread.png", dpi=150)
    plt.close(figure)


if __name__ == "__main__":
    main()
