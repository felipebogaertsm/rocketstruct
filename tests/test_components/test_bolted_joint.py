import numpy as np
import pytest

import rocketstruct.core.bolted_joint as core
from rocketstruct.components import BoltedJoint
from rocketstruct.materials import Material


def _material(
    shear: float = 160e6,
    bearing: float = 540e6,
    tensile: float = 270e6,
) -> Material:
    return Material(
        yield_strength=0.0,
        allowable_shear_stress=shear,
        allowable_bearing_stress=bearing,
        allowable_tensile_stress=tensile,
    )


def _plate_joint(**overrides) -> BoltedJoint:
    defaults = dict(
        shank_diameter=5.2e-3,
        hole_diameter=6.0e-3,
        thickness=0.010,
        edge_distance=0.012,
        pitch_distance=0.025,
        material=_material(),
        n_bolts_in_row=2,
        n_shear_planes=1,
    )
    defaults.update(overrides)
    return BoltedJoint(**defaults)


def test_stress_methods_match_core():
    joint = _plate_joint()
    load = 12_000.0
    row_load = 22_000.0

    assert joint.shear_stress(load) == pytest.approx(
        core.get_shear_stress_per_bolt(load, joint.shank_diameter, n_shear_planes=1)
    )
    assert joint.bearing_stress(load) == pytest.approx(
        core.get_bearing_stress(load, joint.thickness, joint.hole_diameter)
    )
    assert joint.tearout_shear_stress(load) == pytest.approx(
        core.get_tearout_shear_stress_plate(load, joint.edge_distance, joint.thickness)
    )
    assert joint.net_section_tension_stress(row_load) == pytest.approx(
        core.get_net_section_tension_stress_plate(
            row_load,
            joint.pitch_distance,
            joint.thickness,
            joint.hole_diameter,
            n_bolts_in_row=joint.n_bolts_in_row,
        )
    )


def test_max_loads_match_core():
    joint = _plate_joint()
    m = joint.material

    assert joint.max_shear_load() == pytest.approx(
        core.get_max_shear_load(
            joint.shank_diameter,
            m.allowable_shear_stress,
            n_shear_planes=joint.n_shear_planes,
        )
    )
    assert joint.max_bearing_load() == pytest.approx(
        core.get_max_bearing_load(
            joint.thickness, joint.hole_diameter, m.allowable_bearing_stress
        )
    )
    assert joint.max_tearout_load() == pytest.approx(
        core.get_max_tearout_load_plate(
            joint.edge_distance, joint.thickness, m.allowable_shear_stress
        )
    )
    assert joint.max_net_tension_load() == pytest.approx(
        core.get_max_net_tension_load_plate(
            joint.pitch_distance,
            joint.thickness,
            joint.hole_diameter,
            m.allowable_tensile_stress,
            n_bolts_in_row=joint.n_bolts_in_row,
        )
    )


def test_limiting_load_is_minimum_per_bolt():
    joint = _plate_joint()
    expected = min(
        joint.max_shear_load(),
        joint.max_bearing_load(),
        joint.max_tearout_load(),
        joint.max_net_tension_load() / joint.n_bolts_in_row,
    )
    assert joint.limiting_load_per_bolt() == pytest.approx(expected)


def test_margin_of_safety_is_limiting_over_applied_minus_one():
    joint = _plate_joint()
    limiting = joint.limiting_load_per_bolt()
    applied = limiting / 2.0
    assert joint.margin_of_safety(applied) == pytest.approx(1.0)


def test_from_cylinder_converts_angles_to_arc_lengths():
    outer_diameter = 0.080
    edge_angle = 15.0
    pitch_angle = 30.0

    joint = BoltedJoint.from_cylinder(
        shank_diameter=5.2e-3,
        hole_diameter=6.0e-3,
        wall_thickness=0.003,
        outer_diameter=outer_diameter,
        edge_angle=edge_angle,
        pitch_angle=pitch_angle,
        material=_material(),
        n_bolts_in_row=2,
    )

    outer_radius = outer_diameter / 2.0
    assert joint.edge_distance == pytest.approx(np.deg2rad(edge_angle) * outer_radius)
    assert joint.pitch_distance == pytest.approx(np.deg2rad(pitch_angle) * outer_radius)
    assert joint.thickness == pytest.approx(0.003)


def test_from_cylinder_max_loads_match_core_cylinder_helpers():
    args = dict(
        shank_diameter=5.2e-3,
        hole_diameter=6.0e-3,
        wall_thickness=0.003,
        outer_diameter=0.080,
        edge_angle=15.0,
        pitch_angle=30.0,
        n_bolts_in_row=2,
    )
    material = _material()
    joint = BoltedJoint.from_cylinder(material=material, **args)

    assert joint.max_tearout_load() == pytest.approx(
        core.get_max_tearout_load_cylinder(
            args["edge_angle"],
            args["wall_thickness"],
            args["outer_diameter"],
            material.allowable_shear_stress,
        )
    )
    assert joint.max_net_tension_load() == pytest.approx(
        core.get_max_net_tension_load_cylinder(
            args["pitch_angle"],
            args["wall_thickness"],
            args["hole_diameter"],
            material.allowable_tensile_stress,
            args["outer_diameter"],
            n_bolts_in_row=args["n_bolts_in_row"],
        )
    )
