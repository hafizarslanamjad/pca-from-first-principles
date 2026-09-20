"""Retain a dataset-derived reference alongside signed feature deviations.

The fixed schema is length and width in centimeters. Centering keeps feature
roles and units; it changes their reference. No variance or metric is defined.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from pca_from_first_principles.dataset_dimensions import ColumnMeans, column_means
from pca_from_first_principles.feature_space import LengthChangeCm, LengthCm
from pca_from_first_principles.observation_data import (
    ComponentDataset,
    LengthWidthDifference,
    LengthWidthObservation,
    ObservationId,
    WidthChangeCm,
    WidthCm,
)


@dataclass(frozen=True)
class CenteredObservation:
    """An observation identifier and its deviation, not absolute sizes."""

    identifier: ObservationId
    deviation: LengthWidthDifference


@dataclass(frozen=True)
class CenteredDataset:
    """Output of center: a shared mean plus ordered signed deviations.

    Construct through center when mean-centered semantics are required.
    This record alone does not validate a zero-sum invariant for arbitrary
    manually supplied values. Floating-point residual sums may be nonzero.
    """

    reference: ColumnMeans
    observations: tuple[CenteredObservation, ...]

    def to_matrix(self) -> NDArray[np.float64]:
        """Export numerical deviations in cm: rows observations, columns features."""
        return np.array(
            [
                (item.deviation.length, item.deviation.width)
                for item in self.observations
            ],
            dtype=np.float64,
        ).reshape(len(self.observations), 2)


def center(dataset: ComponentDataset) -> CenteredDataset:
    """Subtract each feature mean; preserve the reference and row identity.

    Empty datasets are rejected by column_means. Existing difference records
    reject nonfinite deviations. Units remain centimeters.
    """
    reference: ColumnMeans = column_means(dataset)
    observations = tuple(
        CenteredObservation(
            identifier=item.identifier,
            deviation=LengthWidthDifference(
                length=LengthChangeCm(item.length - reference.length),
                width=WidthChangeCm(item.width - reference.width),
            ),
        )
        for item in dataset.observations
    )
    return CenteredDataset(reference=reference, observations=observations)


def reconstruct(centered: CenteredDataset) -> ComponentDataset:
    """Add the retained reference to recover measured feature records.

    This is algebraically inverse to centering, subject to float rounding.
    Existing observation validation rejects nonpositive or nonfinite sizes.
    """
    return ComponentDataset(
        tuple(
            LengthWidthObservation(
                identifier=item.identifier,
                length=LengthCm(centered.reference.length + item.deviation.length),
                width=WidthCm(centered.reference.width + item.deviation.width),
            )
            for item in centered.observations
        )
    )
