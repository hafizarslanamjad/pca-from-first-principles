"""The same reference change applied to each observation row by broadcasting."""

import numpy as np
from numpy.typing import NDArray

from pca_from_first_principles.dataset_dimensions import ColumnMeans, column_means
from pca_from_first_principles.observation_data import ComponentDataset


def center_with_broadcasting(
    dataset: ComponentDataset,
) -> tuple[ColumnMeans, NDArray[np.float64]]:
    """Return the retained mean and an (n, 2) matrix of signed cm deviations.

    Rows follow the dataset's observation order; columns are length and width.
    The numerical array alone carries no units or observation identifiers.
    Empty datasets have no mean. The input observations are not mutated.
    """
    reference: ColumnMeans = column_means(dataset)
    mean_values: NDArray[np.float64] = np.array(
        [reference.length, reference.width], dtype=np.float64
    )
    measured_values: NDArray[np.float64] = dataset.to_matrix()
    deviations: NDArray[np.float64] = measured_values - mean_values
    return reference, deviations
