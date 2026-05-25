import pytest

from rocketstruct.materials import Material


def test_material_holds_all_fields():
    m = Material(
        yield_strength=270e6,
        allowable_shear_stress=160e6,
        allowable_bearing_stress=540e6,
        allowable_tensile_stress=270e6,
    )
    assert m.yield_strength == pytest.approx(270e6)
    assert m.allowable_shear_stress == pytest.approx(160e6)
    assert m.allowable_bearing_stress == pytest.approx(540e6)
    assert m.allowable_tensile_stress == pytest.approx(270e6)


def test_material_is_frozen():
    m = Material(
        yield_strength=270e6,
        allowable_shear_stress=160e6,
        allowable_bearing_stress=540e6,
        allowable_tensile_stress=270e6,
    )
    with pytest.raises(Exception):
        m.yield_strength = 1.0  # type: ignore[misc]
