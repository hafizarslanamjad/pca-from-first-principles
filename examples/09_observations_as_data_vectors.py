"""Construct observation vectors before arranging a dataset matrix."""

import numpy as np
from numpy.typing import NDArray

from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthDifference,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
    difference_from,
)


def main() -> None:
    """Read every row, column, and difference through the shared schema."""
    first = LengthWidthObservation(ObservationId("A"), LengthCm(10.0), WidthCm(4.0))
    second = LengthWidthObservation(ObservationId("B"), LengthCm(12.0), WidthCm(5.0))
    third = LengthWidthObservation(ObservationId("C"), LengthCm(9.0), WidthCm(3.0))
    fourth = LengthWidthObservation(ObservationId("D"), LengthCm(11.0), WidthCm(5.0))
    dataset = ComponentDataset((first, second, third, fourth))
    change: LengthWidthDifference = difference_from(first, second)
    matrix: NDArray[np.float64] = dataset.to_matrix()

    print("Schema: [length in cm, width in cm]")
    print(f"B minus A: length {change.length:g} cm; width {change.width:g} cm")
    print("Dataset matrix: rows = observations; columns = length, width")
    print(matrix)
    print(f"Shape: {matrix.shape}")
    print(f"Observation A row: {matrix[0].tolist()}")
    print(f"Length column (cm): {dataset.length_column()}")
    print(f"Width column (cm): {dataset.width_column()}")
    print(f"X[3,2] mathematically = matrix[2,1] in Python: {matrix[2, 1]:g} cm")
    print("The last value is width for observation 3.")


if __name__ == "__main__":
    main()
