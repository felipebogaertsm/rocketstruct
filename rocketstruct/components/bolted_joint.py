from dataclasses import dataclass

import numpy as np

import rocketstruct.core.bolted_joint as bolted_joint
from rocketstruct.materials.material import Material


@dataclass(frozen=True)
class BoltedJoint:
    """
    Bolted joint on a flat plate or thin-walled cylinder.

    Wraps `rocketstruct.core.bolted_joint` and exposes per-bolt stresses and
    limit loads across all four failure modes (bolt shear, plate bearing,
    edge tear-out, net-section tension).

    For cylinder geometries, construct via `BoltedJoint.from_cylinder(...)`,
    which converts edge and pitch angles to arc-length distances.

    Attributes:
        shank_diameter: Effective diameter of the bolt shank [m].
        hole_diameter: Diameter of the bolt hole [m].
        thickness: Thickness of the plate or cylinder wall [m].
        edge_distance: Distance from bolt centre to free edge [m].
        pitch_distance: Distance between adjacent bolt centres [m].
        material: Material strength properties.
        n_bolts_in_row: Number of bolts sharing the net-section row. Defaults
            to 1.
        n_shear_planes: 1 for single shear, 2 for double shear. Defaults to 1.
    """

    shank_diameter: float
    hole_diameter: float
    thickness: float
    edge_distance: float
    pitch_distance: float
    material: Material
    n_bolts_in_row: int = 1
    n_shear_planes: int = 1

    @classmethod
    def from_cylinder(
        cls,
        shank_diameter: float,
        hole_diameter: float,
        wall_thickness: float,
        outer_diameter: float,
        edge_angle: float,
        pitch_angle: float,
        material: Material,
        n_bolts_in_row: int = 1,
        n_shear_planes: int = 1,
    ) -> "BoltedJoint":
        """
        Build a BoltedJoint on a thin-walled cylinder.

        Converts central edge and pitch angles to arc-length distances on the
        outer surface.

        Args:
            shank_diameter: Effective diameter of the bolt shank [m].
            hole_diameter: Diameter of the bolt hole [m].
            wall_thickness: Thickness of the cylinder wall [m].
            outer_diameter: Outer diameter of the cylinder [m].
            edge_angle: Central angle from bolt centre to free edge [deg].
            pitch_angle: Central angle between adjacent bolt centres [deg].
            material: Material strength properties.
            n_bolts_in_row: Number of bolts sharing the net-section row.
            n_shear_planes: 1 for single shear, 2 for double shear.

        Returns:
            BoltedJoint with linear edge and pitch distances computed from the
            given angles.
        """
        outer_radius = outer_diameter / 2.0
        edge_distance = np.deg2rad(edge_angle) * outer_radius
        pitch_distance = np.deg2rad(pitch_angle) * outer_radius
        return cls(
            shank_diameter=shank_diameter,
            hole_diameter=hole_diameter,
            thickness=wall_thickness,
            edge_distance=edge_distance,
            pitch_distance=pitch_distance,
            material=material,
            n_bolts_in_row=n_bolts_in_row,
            n_shear_planes=n_shear_planes,
        )

    def shear_stress(self, load_per_bolt: float) -> float:
        """Transverse shear stress on a bolt [Pa]."""
        return bolted_joint.get_shear_stress_per_bolt(
            load_per_bolt, self.shank_diameter, n_shear_planes=self.n_shear_planes
        )

    def bearing_stress(self, load_per_bolt: float) -> float:
        """Bearing stress between bolt shank and plate [Pa]."""
        return bolted_joint.get_bearing_stress(
            load_per_bolt, self.thickness, self.hole_diameter
        )

    def tearout_shear_stress(self, load_per_bolt: float) -> float:
        """Average shear stress along the tear-out plane to a free edge [Pa]."""
        return bolted_joint.get_tearout_shear_stress_plate(
            load_per_bolt, self.edge_distance, self.thickness
        )

    def net_section_tension_stress(self, load_across_row: float) -> float:
        """Tensile stress across the reduced net section of a bolt row [Pa]."""
        return bolted_joint.get_net_section_tension_stress_plate(
            load_across_row,
            self.pitch_distance,
            self.thickness,
            self.hole_diameter,
            n_bolts_in_row=self.n_bolts_in_row,
        )

    def max_shear_load(self) -> float:
        """Per-bolt limit load before shear failure [N]."""
        return bolted_joint.get_max_shear_load(
            self.shank_diameter,
            self.material.allowable_shear_stress,
            n_shear_planes=self.n_shear_planes,
        )

    def max_bearing_load(self) -> float:
        """Per-bolt limit load before bearing failure [N]."""
        return bolted_joint.get_max_bearing_load(
            self.thickness,
            self.hole_diameter,
            self.material.allowable_bearing_stress,
        )

    def max_tearout_load(self) -> float:
        """Per-bolt limit load before tear-out failure [N]."""
        return bolted_joint.get_max_tearout_load_plate(
            self.edge_distance,
            self.thickness,
            self.material.allowable_shear_stress,
        )

    def max_net_tension_load(self) -> float:
        """Limit axial load across the bolt row before net-section failure [N]."""
        return bolted_joint.get_max_net_tension_load_plate(
            self.pitch_distance,
            self.thickness,
            self.hole_diameter,
            self.material.allowable_tensile_stress,
            n_bolts_in_row=self.n_bolts_in_row,
        )

    def limiting_load_per_bolt(self) -> float:
        """
        Lowest per-bolt load across all four failure modes [N].

        Net-section tension is converted from its per-row limit by dividing by
        `n_bolts_in_row`, so all four values are on a per-bolt basis.
        """
        return min(
            self.max_shear_load(),
            self.max_bearing_load(),
            self.max_tearout_load(),
            self.max_net_tension_load() / self.n_bolts_in_row,
        )

    def margin_of_safety(self, load_per_bolt: float) -> float:
        """Margin of safety against the limiting failure mode."""
        return self.limiting_load_per_bolt() / load_per_bolt - 1.0
