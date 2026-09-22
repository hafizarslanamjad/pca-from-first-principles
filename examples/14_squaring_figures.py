"""Replace source sketches with numerical, equal-aspect Matplotlib plots."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    destination = (
        Path(__file__).resolve().parents[1]
        / "lectures/14-why-squaring-becomes-powerful"
    )
    destination.mkdir(parents=True, exist_ok=True)
    plt.rcParams["svg.hashsalt"] = "lecture14"
    fig, ax = plt.subplots(figsize=(5, 5), layout="constrained")
    ax.plot([0, 3, 3], [0, 0, 4], color="darkorange", linewidth=2)
    ax.annotate(
        "",
        xy=(3, 4),
        xytext=(0, 0),
        arrowprops={"arrowstyle": "->", "color": "navy", "lw": 2},
    )
    ax.text(1.5, -0.35, "3", ha="center")
    ax.text(3.2, 2, "4")
    ax.text(1.1, 2.2, "5", color="navy")
    ax.plot([2.7, 2.7, 3], [0, 0.3, 0.3], color="gray")
    ax.scatter([0, 3], [0, 4], color="navy")
    ax.set(
        xlim=(-0.6, 4),
        ylim=(-0.6, 4.6),
        xlabel="Coordinate 1 (units)",
        ylabel="Coordinate 2 (units)",
        title="Perpendicular contributions: 3² + 4² = 5²",
        aspect="equal",
    )
    ax.grid(alpha=0.2)
    fig.savefig(destination / "pythagorean.svg", metadata={"Date": None})
    fig.savefig(destination / "pythagorean.png", dpi=130)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(5, 4), layout="constrained")
    lengths = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    widths = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    points = ax.scatter(lengths, widths, color="navy")
    np.testing.assert_allclose(
        np.asarray(points.get_offsets(), dtype=np.float64),
        np.column_stack((lengths, widths)),
    )
    ax.set(
        xlim=(0, 6),
        ylim=(0, 6),
        xlabel="Length (illustrative units)",
        ylabel="Width (illustrative units)",
        title="Illustrative coordinated variation",
        aspect="equal",
    )
    ax.grid(alpha=0.2)
    fig.savefig(destination / "coordinated-variation.svg", metadata={"Date": None})
    fig.savefig(destination / "coordinated-variation.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
