"""Demonstrate measurement semantics without introducing vector geometry."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentMeasurements:
    """Selected properties; the field names explicitly record their units."""

    length_cm: float
    width_cm: float
    mass_g: float


def main() -> None:
    """Compare labels with measurements of the same components."""
    identifiers = {"A": 1, "B": 2, "C": 3}
    relabeled = {"A": 40, "B": 7, "C": 2}
    print("Identifier difference C - A:", identifiers["C"] - identifiers["A"])
    print("After relabeling C - A:", relabeled["C"] - relabeled["A"])
    print("The components did not change; identifier arithmetic changed.")

    a = ComponentMeasurements(length_cm=10, width_cm=5, mass_g=20)
    b = ComponentMeasurements(length_cm=11, width_cm=5, mass_g=21)
    print("Measurement differences B - A:")
    print(f"Length: {b.length_cm - a.length_cm:g} cm")
    print(f"Width: {b.width_cm - a.width_cm:g} cm")
    print(f"Mass: {b.mass_g - a.mass_g:g} g")


if __name__ == "__main__":
    main()
