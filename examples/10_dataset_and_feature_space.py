"""More observations change n; another feature changes d."""

from pca_from_first_principles.dataset_dimensions import (
    ColumnMeans,
    LengthWidthThicknessObservation,
    ThicknessCm,
    column_means,
    shape_of,
    thickness_matrix,
)
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)


def main() -> None:
    """Reproduce the source's counts, axis means, and dependent feature."""
    observations = (
        LengthWidthObservation(ObservationId("A"), LengthCm(10.0), WidthCm(4.0)),
        LengthWidthObservation(ObservationId("B"), LengthCm(12.0), WidthCm(5.0)),
        LengthWidthObservation(ObservationId("C"), LengthCm(9.0), WidthCm(3.0)),
        LengthWidthObservation(ObservationId("D"), LengthCm(11.0), WidthCm(5.0)),
    )
    for count in (1, 2, 4):
        dataset = ComponentDataset(observations[:count])
        shape = shape_of(dataset.to_matrix())
        print(f"n={shape.observations}, d={shape.features}: same two feature roles")

    full = ComponentDataset(observations)
    means: ColumnMeans = column_means(full)
    print(f"Column means: length={means.length:g} cm; width={means.width:g} cm")
    print(
        f"First-row arithmetic: {(observations[0].length + observations[0].width) / 2:g}"
    )
    print("That row calculation combines different features; it is not mean length.")
    extended = tuple(
        LengthWidthThicknessObservation(
            item.identifier, item.length, item.width, ThicknessCm(0.1 * item.length)
        )
        for item in observations
    )
    print(f"Added thickness: {shape_of(thickness_matrix(extended))}")
    print("Three stored features, even though thickness = 0.1 * length.")
    repeated = tuple(extended[index % len(extended)] for index in range(1000))
    print(
        f"1000 rows (repeated records for illustration): {shape_of(thickness_matrix(repeated))}"
    )


if __name__ == "__main__":
    main()
