import numpy as np
import pytest

import rocketstruct.core.cylindrical_vessel as core
from rocketstruct.components import CylindricalVessel
from rocketstruct.materials import Material


def _material(yield_strength: float = 40e6) -> Material:
    return Material(
        yield_strength=yield_strength,
        allowable_shear_stress=0.0,
        allowable_bearing_stress=0.0,
        allowable_tensile_stress=0.0,
    )


def test_radii_and_thickness_from_diameters():
    vessel = CylindricalVessel(
        inner_diameter=0.100,
        outer_diameter=0.120,
        material=_material(),
    )
    assert vessel.inner_radius == pytest.approx(0.050)
    assert vessel.outer_radius == pytest.approx(0.060)
    assert vessel.wall_thickness == pytest.approx(0.010)


def test_stress_methods_match_core():
    inner_d = 2.0
    outer_d = 2.0 * np.sqrt(2)
    pressure = 1.0
    vessel = CylindricalVessel(
        inner_diameter=inner_d, outer_diameter=outer_d, material=_material()
    )

    a = inner_d / 2.0
    b = outer_d / 2.0

    assert vessel.hoop_stress(pressure) == pytest.approx(
        core._get_cylindrical_vessel_hoop_stress(pressure, a, b)
    )
    assert vessel.radial_stress(pressure) == pytest.approx(
        core._get_cylindrical_vessel_radial_stress(pressure, a, b)
    )
    assert vessel.longitudinal_stress(pressure) == pytest.approx(
        core._get_cylindrical_vessel_logitudinal_stress(pressure, a, b)
    )
    assert vessel.von_mises_stress(pressure) == pytest.approx(
        core.get_cylindrical_vessel_von_mises_stress(pressure, a, b)
    )


def test_burst_pressure_matches_core():
    inner_d = 95.25e-3 * 2.0
    outer_d = 101.6e-3 * 2.0
    sigma_y = 40e6
    vessel = CylindricalVessel(
        inner_diameter=inner_d,
        outer_diameter=outer_d,
        material=_material(sigma_y),
    )
    expected = core.get_cylindrical_vessel_burst_pressure(
        inner_d / 2.0, outer_d / 2.0, sigma_y
    )
    assert vessel.burst_pressure() == pytest.approx(expected)


def test_margin_of_safety_is_burst_over_applied_minus_one():
    vessel = CylindricalVessel(
        inner_diameter=0.100, outer_diameter=0.120, material=_material(270e6)
    )
    burst = vessel.burst_pressure()
    applied = burst / 3.0
    assert vessel.margin_of_safety(applied) == pytest.approx(2.0)
