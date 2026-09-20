"""What changes and what is retained when every row uses the same new zero."""

import numpy as np

from pca_from_first_principles.centering import center, reconstruct
from pca_from_first_principles.centering_arrays import center_with_broadcasting
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)


def main() -> None:
    """Connect row broadcasting with deviations and unchanged pairwise differences."""
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
    reference, deviations = center_with_broadcasting(dataset)
    typed_centered = center(dataset)
    measured = dataset.to_matrix()
    print(f"Mean reference: ({reference.length:g}, {reference.width:g}) cm")
    print("Centered rows [length deviation, width deviation] in cm:")
    print(deviations)
    print(f"Shapes: X={measured.shape}, mean=(2,), centered={deviations.shape}")
    print(f"Original x2 - x1: {measured[1] - measured[0]}")
    print(f"Centered x2 - x1: {deviations[1] - deviations[0]}")
    print(f"Sum by feature: {deviations.sum(axis=0)}")
    print(f"Mean by feature: {deviations.mean(axis=0)}")
    print(
        f"Broadcasting agrees with typed rows: {np.allclose(deviations, typed_centered.to_matrix())}"
    )
    print(
        f"Reconstruction agrees: {np.allclose(reconstruct(typed_centered).to_matrix(), measured)}"
    )
    for values in (
        [8.0, 10.0, 12.0],
        [98.0, 100.0, 102.0],
        [998.0, 1000.0, 1002.0],
        [1008.0, 1010.0, 1012.0],
    ):
        lengths = np.array(values, dtype=np.float64)
        print(
            f"Lengths {values}, mean {lengths.mean():g}, deviations {lengths - lengths.mean()}"
        )
    for values in ([-2.0, 0.0, 2.0], [-100.0, 0.0, 100.0], [0.0, 0.0, 0.0]):
        signed_deviations = np.array(values, dtype=np.float64)
        print(f"Signed deviations {values}: average {signed_deviations.mean():g}")


if __name__ == "__main__":
    main()
