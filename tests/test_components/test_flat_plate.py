import pytest

import rocketstruct.core.flat_plate as core
from rocketstruct.components import FlatPlate
from rocketstruct.materials import Material


def _material(yield_strength: float = 270e6) -> Material:
    return Material(
        yield_strength=yield_strength,
        allowable_shear_stress=0.0,
        allowable_bearing_stress=0.0,
        allowable_tensile_stress=0.0,
    )


def test_stress_matches_core():
    plate = FlatPlate(diameter=0.30, thickness=6.0e-3, material=_material())
    pressure = 2.0e6
    assert plate.stress(pressure) == pytest.approx(
        core.get_flat_plate_stress(pressure, 0.30, 6.0e-3)
    )


def test_burst_pressure_matches_core():
    plate = FlatPlate(diameter=0.30, thickness=6.0e-3, material=_material(270e6))
    assert plate.burst_pressure() == pytest.approx(
        core.get_flat_plate_burst_pressure(0.30, 6.0e-3, 270e6)
    )


def test_margin_of_safety_is_burst_over_applied_minus_one():
    plate = FlatPlate(diameter=0.30, thickness=6.0e-3, material=_material(270e6))
    burst = plate.burst_pressure()
    applied = burst / 4.0
    assert plate.margin_of_safety(applied) == pytest.approx(3.0)


def test_zero_thickness_raises():
    plate = FlatPlate(diameter=0.30, thickness=0.0, material=_material())
    with pytest.raises(ZeroDivisionError):
        plate.stress(1.0e6)
