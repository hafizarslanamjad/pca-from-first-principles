"""Construct the four relationships first, then verify the matrix expression."""

import numpy as np

from pca_from_first_principles.centering import center
from pca_from_first_principles.covariance_table import (
    FeatureRole,
    population_covariance_table,
)
from pca_from_first_principles.feature_space import LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthObservation,
    ObservationId,
    WidthCm,
)


def main() -> None:
    dataset = ComponentDataset(
        tuple(
            LengthWidthObservation(ObservationId(str(i)), LengthCm(a), WidthCm(b))
            for i, (a, b) in enumerate(
                ((10.0, 4.0), (12.0, 5.0), (9.0, 3.0), (11.0, 5.0))
            )
        )
    )
    centered = center(dataset).to_matrix()
    a, b = centered[:, 0], centered[:, 1]
    desired_products = np.array([[a @ a, a @ b], [b @ a, b @ b]])
    gram = centered.T @ centered
    table = population_covariance_table(dataset)
    np.testing.assert_allclose(desired_products, gram)
    np.testing.assert_allclose(table.to_matrix(), gram / len(dataset.observations))
    print("Centered data (observations × features):\n", centered)
    print("Pairwise sums of products:\n", desired_products)
    print("Population covariance (features × features):\n", table.to_matrix())
    print("Shapes:", centered.shape, "→", table.to_matrix().shape)
    for first in FeatureRole:
        for second in FeatureRole:
            print(
                f"Cov({first.name.lower()}, {second.name.lower()}) = {table.entry(first, second):g} cm²"
            )


if __name__ == "__main__":
    main()
