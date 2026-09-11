"""Distinguish scalar measurements, ordered observations, and differences."""

from typing import NamedTuple, NewType

MassKg = NewType("MassKg", float)
LengthCm = NewType("LengthCm", float)
WidthCm = NewType("WidthCm", float)
MassDifferenceKg = NewType("MassDifferenceKg", float)
LengthDifferenceCm = NewType("LengthDifferenceCm", float)
WidthDifferenceCm = NewType("WidthDifferenceCm", float)


class MassObservation(NamedTuple):
    """One observation with one feature; distinct from a scalar mass."""

    mass: MassKg


class MassLengthObservation(NamedTuple):
    """One observation ordered as mass in kg, then length in cm."""

    mass: MassKg
    length: LengthCm


class ComponentObservation(NamedTuple):
    """One observation ordered as mass, length, and width."""

    mass: MassKg
    length: LengthCm
    width: WidthCm


class MeasurementDifference(NamedTuple):
    """Signed changes in matching properties, relative to a reference."""

    mass: MassDifferenceKg
    length: LengthDifferenceCm
    width: WidthDifferenceCm


def difference_from(
    reference: ComponentObservation, target: ComponentObservation
) -> MeasurementDifference:
    """Return target minus reference in each feature's declared unit."""
    return MeasurementDifference(
        mass=MassDifferenceKg(target.mass - reference.mass),
        length=LengthDifferenceCm(target.length - reference.length),
        width=WidthDifferenceCm(target.width - reference.width),
    )


def main() -> None:
    """Connect every numerical value to its measurement role."""
    mass: MassKg = MassKg(5.0)
    one_feature: MassObservation = MassObservation(mass=mass)
    two_features: MassLengthObservation = MassLengthObservation(
        mass=mass, length=LengthCm(20.0)
    )
    reference: ComponentObservation = ComponentObservation(
        mass=mass, length=LengthCm(20.0), width=WidthCm(8.0)
    )
    target: ComponentObservation = ComponentObservation(
        mass=MassKg(6.0), length=LengthCm(22.0), width=WidthCm(8.0)
    )
    change: MeasurementDifference = difference_from(reference, target)

    print(f"Scalar mass: {mass:g} kg")
    print(f"One-feature observation: {one_feature}")
    print(f"Two-feature observation: {two_features}")
    print(f"Three-feature observation: {reference}")
    print(f"Feature count: {len(reference)}")
    print(f"First entry by position: {reference[0]:g} kg")
    print(f"First entry by name: {reference.mass:g} kg")
    print("Target minus reference:")
    print(f"  Mass change: {change.mass:g} kg")
    print(f"  Length change: {change.length:g} cm")
    print(f"  Width change: {change.width:g} cm")
    print("No combined magnitude is defined for these mixed-unit changes.")


if __name__ == "__main__":
    main()
