"""Regenerate every coordinate plot in Lecture 12 from numerical data.

Run from the repository root. SVG assets are committed so rendering the lecture
need not regenerate figures. Optional PNG previews support visual inspection.
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from pca_from_first_principles.centering_arrays import center_with_broadcasting
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)

BLUE = "#175cd3"
ORANGE = "#b45309"
OUTPUT = Path(__file__).resolve().parents[1] / "lectures/12-centering-reference-change"


def save(fig: Figure, name: str, preview: Path | None) -> None:
    """Write deterministic SVG source and optional inspection PNG."""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT / f"{name}.svg", metadata={"Date": None})
    if preview is not None:
        preview.mkdir(parents=True, exist_ok=True)
        fig.savefig(preview / f"{name}.png", dpi=125)
    plt.close(fig)


def number_line(
    ax: Axes,
    values: list[float],
    labels: list[str],
    limits: tuple[float, float],
    ticks: list[float],
    title: str,
    xlabel: str,
) -> None:
    """Place each mark at its numerical horizontal coordinate."""
    ax.axhline(0, color="#596579", linewidth=1)
    points = ax.scatter(values, [0.0] * len(values), s=70, color=BLUE, zorder=3)
    np.testing.assert_allclose(np.asarray(points.get_offsets())[:, 0], values)
    for value, label in zip(values, labels, strict=True):
        ax.annotate(
            label, (value, 0), xytext=(0, 15), textcoords="offset points", ha="center"
        )
    ax.set(
        xlim=limits,
        ylim=(-0.7, 0.8),
        yticks=[],
        xticks=ticks,
        title=title,
        xlabel=xlabel,
    )
    for side in ("top", "left", "right"):
        ax.spines[side].set_visible(False)


def main() -> None:
    """Draw the source's 1D references, 2D points, and translated examples."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path)
    preview: Path | None = parser.parse_args().preview_dir
    plt.rcParams.update(
        {"font.size": 11, "svg.fonttype": "none", "svg.hashsalt": "lecture12"}
    )

    configurations = (
        (
            "original-lengths",
            [8.0, 10.0, 12.0],
            ["$x_1=8$", "$x_2=\\mu=10$", "$x_3=12$"],
            (-0.5, 13.0),
            [0.0, 4.0, 8.0, 10.0, 12.0],
            "Original measurement coordinates",
            "Length (cm)",
        ),
        (
            "original-ruler",
            [8.0, 10.0, 12.0],
            ["A", "B", "C"],
            (-0.5, 13.0),
            [0.0, 4.0, 8.0, 10.0, 12.0],
            "Original ruler: A to C = 4 cm",
            "Original length coordinate (cm)",
        ),
        (
            "centered-ruler",
            [-2.0, 0.0, 2.0],
            ["A", "B", "C"],
            (-3.0, 3.0),
            [-2.0, -1.0, 0.0, 1.0, 2.0],
            "Relabeled ruler: A to C = 4 cm",
            "Length relative to the mean (cm)",
        ),
        (
            "shared-centered",
            [-2.0, 0.0, 2.0],
            ["−2", "0", "+2"],
            (-3.0, 3.0),
            [-2.0, -1.0, 0.0, 1.0, 2.0],
            "Both datasets share this centered configuration",
            "Deviation from each dataset's own mean (cm)",
        ),
    )
    for name, values, labels, limits, ticks, title, xlabel in configurations:
        fig, ax = plt.subplots(figsize=(8, 2.5), layout="constrained")
        number_line(ax, values, labels, limits, ticks, title, xlabel)
        save(fig, name, preview)

    fig, axes = plt.subplots(2, 1, figsize=(8, 4.6), layout="constrained")
    for ax, start, title, label in zip(
        axes,
        [0.0, 10.0],
        [
            "Original question: from measurement zero",
            "Centered question: from the dataset mean",
        ],
        ["+8 cm", "−2 cm"],
        strict=True,
    ):
        number_line(
            ax,
            [0.0, 8.0, 10.0],
            ["O", "$x_1$", "$\\mu$"],
            (-0.5, 11.0),
            [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
            title,
            "Original coordinate axis (cm)",
        )
        ax.annotate(
            "",
            xy=(8.0, -0.28),
            xytext=(start, -0.28),
            arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 2},
        )
        ax.text((start + 8.0) / 2, -0.55, label, ha="center", color=ORANGE)
    save(fig, "reference-arrows", preview)

    dataset = ComponentDataset(
        tuple(
            LengthWidthObservation(
                ObservationId(str(i)), LengthCm(length), WidthCm(width)
            )
            for i, (length, width) in enumerate(
                ((10.0, 4.0), (12.0, 5.0), (9.0, 3.0), (11.0, 5.0)), start=1
            )
        )
    )
    reference, centered = center_with_broadcasting(dataset)
    for name, feature_values, mean, is_centered in (
        (
            "original-feature-points",
            dataset.to_matrix(),
            [reference.length, reference.width],
            False,
        ),
        ("centered-feature-points", centered, [0.0, 0.0], True),
    ):
        fig, ax = plt.subplots(figsize=(8, 4.7), layout="constrained")
        points = ax.scatter(
            feature_values[:, 0], feature_values[:, 1], s=60, color=BLUE, zorder=3
        )
        np.testing.assert_allclose(np.asarray(points.get_offsets()), feature_values)
        mean_mark = ax.scatter(
            [mean[0]], [mean[1]], marker="x", s=95, linewidths=2, color=ORANGE, zorder=4
        )
        np.testing.assert_allclose(np.asarray(mean_mark.get_offsets()), [mean])
        offsets = [(-30, -20), (8, 8), (-30, -18), (-30, 12)]
        for i, (point, offset) in enumerate(
            zip(feature_values, offsets, strict=True), start=1
        ):
            label = f"$\\tilde{{x}}_{i}$" if is_centered else f"$x_{i}$"
            ax.annotate(
                label,
                (float(point[0]), float(point[1])),
                xytext=offset,
                textcoords="offset points",
            )
        label = "$\\tilde{\\mu}=(0,0)$" if is_centered else "$\\mu=(10.5,4.25)$"
        ax.annotate(
            label,
            (mean[0], mean[1]),
            xytext=(12, -27),
            textcoords="offset points",
            color=ORANGE,
        )
        if is_centered:
            ax.set(
                xlim=(-2.1, 2.1),
                ylim=(-1.8, 1.3),
                xlabel="Centered length (cm)",
                ylabel="Centered width (cm)",
                title="Same points relative to the mean",
            )
        else:
            ax.set(
                xlim=(-0.5, 13.0),
                ylim=(-0.5, 6.5),
                xlabel="Length (cm)",
                ylabel="Width (cm)",
                title="Original feature coordinates",
            )
        ax.axhline(0, color="#8a94a3", lw=1)
        ax.axvline(0, color="#8a94a3", lw=1)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(alpha=0.18)
        save(fig, name, preview)

    fig, axes = plt.subplots(2, 1, figsize=(8, 4.5), layout="constrained")
    for ax, values, limits, title in zip(
        axes,
        [[8.0, 10.0, 12.0], [1008.0, 1010.0, 1012.0]],
        [(6.0, 14.0), (1006.0, 1014.0)],
        ["Dataset A: mean 10 cm", "Dataset B: mean 1010 cm"],
        strict=True,
    ):
        number_line(
            ax,
            values,
            [str(int(x)) for x in values],
            limits,
            values,
            title,
            "Original length coordinate (cm)",
        )
        ax.ticklabel_format(axis="x", style="plain", useOffset=False)
    fig.suptitle("Separate numerical axes; equal scale; different absolute locations")
    save(fig, "translated-datasets", preview)


if __name__ == "__main__":
    main()
