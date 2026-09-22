"""Accurate plots of the section 2 datasets, relative to feature means."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    destination = (
        Path(__file__).resolve().parents[1]
        / "lectures/15-relationships-between-features"
    )
    destination.mkdir(parents=True, exist_ok=True)
    plt.rcParams["svg.hashsalt"] = "lecture15"
    first = np.array([-2.0, -1.0, 1.0, 2.0])
    for sign, name in ((1.0, "positive-covariance"), (-1.0, "negative-covariance")):
        second = sign * np.array([-3.0, -2.0, 2.0, 3.0])
        fig, ax = plt.subplots(figsize=(5.5, 4.5), layout="constrained")
        points = ax.scatter(first, second, s=65, color="navy", zorder=3)
        np.testing.assert_allclose(
            np.asarray(points.get_offsets(), dtype=np.float64),
            np.column_stack((first, second)),
        )
        ax.axhline(0, color="gray", linewidth=1)
        ax.axvline(0, color="gray", linewidth=1)
        ax.set(
            xlim=(-3.5, 3.5),
            ylim=(-3.5, 3.5),
            aspect="equal",
            xlabel="Length deviation from mean (cm)",
            ylabel="Width deviation from mean (cm)",
            title=f"Section 2: covariance = {np.mean(first * second):g} cm²",
        )
        ax.grid(alpha=0.2)
        fig.savefig(destination / f"{name}.svg", metadata={"Date": None})
        fig.savefig(destination / f"{name}.png", dpi=130)
        plt.close(fig)


if __name__ == "__main__":
    main()
