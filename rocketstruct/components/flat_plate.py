from dataclasses import dataclass

import rocketstruct.core.flat_plate as flat_plate
from rocketstruct.materials.material import Material


@dataclass(frozen=True)
class FlatPlate:
    """
    Uniformly loaded circular flat plate.

    Wraps `rocketstruct.core.flat_plate` and exposes membrane stress and burst
    pressure for a given geometry and material.

    Attributes:
        diameter: Plate diameter [m].
        thickness: Plate thickness [m].
        material: Material strength properties.
    """

    diameter: float
    thickness: float
    material: Material

    def stress(self, pressure: float) -> float:
        """Membrane stress under uniform internal pressure [Pa]."""
        return flat_plate.get_flat_plate_stress(pressure, self.diameter, self.thickness)

    def burst_pressure(self) -> float:
        """Internal pressure at which membrane stress reaches yield [Pa]."""
        return flat_plate.get_flat_plate_burst_pressure(
            self.diameter, self.thickness, self.material.yield_strength
        )

    def margin_of_safety(self, pressure: float) -> float:
        """Margin of safety against burst at the given internal pressure."""
        return self.burst_pressure() / pressure - 1.0
