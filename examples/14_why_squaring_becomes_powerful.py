"""Follow the lecture from squared magnitude to row/column aggregation."""

import numpy as np

from pca_from_first_principles.centering import center
from pca_from_first_principles.deviation_products import (
    cross_product,
    squared_magnitude,
    summarize_products,
)
from pca_from_first_principles.feature_space import LengthChangeCm, LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthDifference,
    LengthWidthObservation,
    ObservationId,
    WidthChangeCm,
    WidthCm,
)


def main() -> None:
    for length, width in ((3.0, 4.0), (6.0, 8.0), (1.5, 0.75)):
        deviation = LengthWidthDifference(LengthChangeCm(length), WidthChangeCm(width))
        print(
            f"({length}, {width}): squared magnitude = {squared_magnitude(deviation)} cm²"
        )
    for length, width in ((2.0, 3.0), (-2.0, -3.0), (2.0, -3.0)):
        deviation = LengthWidthDifference(LengthChangeCm(length), WidthChangeCm(width))
        print(f"Deviation product ({length}, {width}) = {cross_product(deviation)} cm²")
    dataset = ComponentDataset(
        tuple(
            LengthWidthObservation(
                ObservationId(str(i)), LengthCm(length), WidthCm(width)
            )
            for i, (length, width) in enumerate(
                ((10.0, 4.0), (12.0, 5.0), (9.0, 3.0), (11.0, 5.0))
            )
        )
    )
    matrix = center(dataset).to_matrix()
    result = summarize_products(dataset)
    np.testing.assert_allclose(
        result.observation_squared_magnitudes, (matrix * matrix).sum(axis=1)
    )
    np.testing.assert_allclose(
        (result.length_variance, result.width_variance), (matrix * matrix).mean(axis=0)
    )
    print("Centered matrix:\n", matrix)
    print("Per-observation squared magnitudes:", result.observation_squared_magnitudes)
    print("Length variance:", result.length_variance, "cm²")
    print("Width variance:", result.width_variance, "cm²")
    print("Mean length-width deviation product:", result.length_width_covariance, "cm²")


if __name__ == "__main__":
    main()
