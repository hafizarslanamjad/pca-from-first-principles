"""Covariance as an average of observation-specific signed products.

Reuses Lecture 14 operations rather than introducing another covariance type.
The source deviations are interpreted in cm; raw observations below add a
stated 10 cm reference to each feature so existing positive-size types apply.
"""

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


def main() -> None:
    examples: tuple[tuple[str, tuple[tuple[float, float], ...]], ...] = (
        ("Section 2: A", ((-2.0, -3.0), (-1.0, -2.0), (1.0, 2.0), (2.0, 3.0))),
        ("Section 2: B", ((-2.0, 3.0), (-1.0, 2.0), (1.0, -2.0), (2.0, -3.0))),
        ("Section 11", ((-2.0, -3.0), (-1.0, -1.0), (1.0, 2.0), (2.0, 2.0))),
        ("Section 12", ((-2.0, 3.0), (-1.0, 1.0), (1.0, -2.0), (2.0, -2.0))),
    )
    for label, rows in examples:
        dataset = ComponentDataset(
            tuple(
                LengthWidthObservation(
                    ObservationId(str(i)), LengthCm(10 + a), WidthCm(10 + b)
                )
                for i, (a, b) in enumerate(rows)
            )
        )
        centered = center(dataset)
        result = summarize_products(dataset)
        print(label)
        print("  Reference:", centered.reference)
        print(
            "  Products:",
            tuple(cross_product(item.deviation) for item in centered.observations),
        )
        print("  Length variance:", result.length_variance, "cm²")
        print("  Width variance:", result.width_variance, "cm²")
        print("  Population covariance:", result.length_width_covariance, "cm²")
    print("Section 9: raw product =", 1002 * 1003)
    print(
        "Section 9: product relative to means 1000, 1000 =",
        (1002 - 1000) * (1003 - 1000),
    )


if __name__ == "__main__":
    main()
