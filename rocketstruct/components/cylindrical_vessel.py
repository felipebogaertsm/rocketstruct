from dataclasses import dataclass

import rocketstruct.core.cylindrical_vessel as cylindrical_vessel
from rocketstruct.materials.material import Material


@dataclass(frozen=True)
class CylindricalVessel:
    """
    Thick-walled cylindrical pressure vessel with closed ends.

    Wraps `rocketstruct.core.cylindrical_vessel` and exposes stresses and burst
    pressure for a given geometry and material.

    Attributes:
        inner_diameter: Inner diameter of the cylinder [m].
        outer_diameter: Outer diameter of the cylinder [m].
        material: Material strength properties.
    """

    inner_diameter: float
    outer_diameter: float
    material: Material

    @property
    def inner_radius(self) -> float:
        return self.inner_diameter / 2.0

    @property
    def outer_radius(self) -> float:
        return self.outer_diameter / 2.0

    @property
    def wall_thickness(self) -> float:
        return (self.outer_diameter - self.inner_diameter) / 2.0

    def hoop_stress(self, pressure: float) -> float:
        """Hoop stress at the inner wall [Pa]."""
        return cylindrical_vessel._get_cylindrical_vessel_hoop_stress(
            pressure, self.inner_radius, self.outer_radius
        )

    def radial_stress(self, pressure: float) -> float:
        """Radial stress at the inner wall [Pa]."""
        return cylindrical_vessel._get_cylindrical_vessel_radial_stress(
            pressure, self.inner_radius, self.outer_radius
        )

    def longitudinal_stress(self, pressure: float) -> float:
        """Longitudinal stress at the inner wall [Pa]."""
        return cylindrical_vessel._get_cylindrical_vessel_logitudinal_stress(
            pressure, self.inner_radius, self.outer_radius
        )

    def von_mises_stress(self, pressure: float) -> float:
        """Von Mises equivalent stress at the inner wall [Pa]."""
        return cylindrical_vessel.get_cylindrical_vessel_von_mises_stress(
            pressure, self.inner_radius, self.outer_radius
        )

    def burst_pressure(self) -> float:
        """Internal pressure at which Von Mises stress reaches yield [Pa]."""
        return cylindrical_vessel.get_cylindrical_vessel_burst_pressure(
            self.inner_radius, self.outer_radius, self.material.yield_strength
        )

    def margin_of_safety(self, pressure: float) -> float:
        """Margin of safety against burst at the given internal pressure."""
        return self.burst_pressure() / pressure - 1.0
