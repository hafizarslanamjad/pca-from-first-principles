"""Reproduce the supplied mean, centered values, balance, and reconstruction."""

from pca_from_first_principles.centering import CenteredDataset, center, reconstruct
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)


def main() -> None:
    """Read deviations relative to the mean rather than measurement zero."""
    dataset = ComponentDataset(
        (
            LengthWidthObservation(ObservationId("1"), LengthCm(10), WidthCm(4)),
            LengthWidthObservation(ObservationId("2"), LengthCm(12), WidthCm(5)),
            LengthWidthObservation(ObservationId("3"), LengthCm(9), WidthCm(3)),
            LengthWidthObservation(ObservationId("4"), LengthCm(11), WidthCm(5)),
        )
    )
    centered: CenteredDataset = center(dataset)
    print("Original rows [length, width] in cm:")
    print(dataset.to_matrix())
    print(
        f"Dataset reference: ({centered.reference.length:g}, {centered.reference.width:g}) cm"
    )
    print("Signed deviations from that reference in cm:")
    print(centered.to_matrix())
    print(f"Sum of deviations by feature: {centered.to_matrix().sum(axis=0)}")
    print("Reconstructed measured rows in cm:")
    print(reconstruct(centered).to_matrix())
    print("Observation 2 remains 12 cm long; +1.5 cm is its deviation from the mean.")


if __name__ == "__main__":
    main()
