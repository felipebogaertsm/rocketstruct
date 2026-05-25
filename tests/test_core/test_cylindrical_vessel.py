import numpy as np
import pytest

import rocketstruct.core.cylindrical_vessel as cylindrical_vessel


def test_unit_pressure_stresses() -> None:
    """Test the stresses for a unit pressure in a cylindrical vessel."""
    a = 1.0  # Inner radius
    b = np.sqrt(2)  # Outer radius
    p = 1.0  # Unit pressure

    hoop = cylindrical_vessel._get_cylindrical_vessel_hoop_stress(p, a, b)
    radial = cylindrical_vessel._get_cylindrical_vessel_radial_stress(p, a, b)
    longitudinal = cylindrical_vessel._get_cylindrical_vessel_logitudinal_stress(
        p, a, b
    )

    assert pytest.approx(3.0) == hoop
    assert pytest.approx(-1.0) == radial
    assert pytest.approx(2.0) == longitudinal


def test_von_mises_reference_case() -> None:
    """Test the Von Mises stress for a reference case."""
    a = 1.0
    b = np.sqrt(2.0)
    p = 1.0

    expected = np.sqrt(13.0)
    result = cylindrical_vessel.get_cylindrical_vessel_von_mises_stress(p, a, b)

    assert result == pytest.approx(expected)


def test_von_mises_scales_linearly_with_pressure() -> None:
    """Von Mises stress should scale proportionally to the applied pressure."""
    a = 0.04  # 40 mm inner radius
    b = 0.06  # 60 mm outer radius
    p1, p2 = 4.0e6, 9.0e6  # Pa

    vm1 = cylindrical_vessel.get_cylindrical_vessel_von_mises_stress(p1, a, b)
    vm2 = cylindrical_vessel.get_cylindrical_vessel_von_mises_stress(p2, a, b)

    assert vm2 == pytest.approx(vm1 * (p2 / p1))


def test_burst_pressure_reference_case() -> None:
    """Test the burst pressure for a reference case."""
    a = 1.0
    b = np.sqrt(2)
    sigma_y = 13.0

    burst = cylindrical_vessel.get_cylindrical_vessel_burst_pressure(a, b, sigma_y)
    expected = sigma_y / np.sqrt(13.0)
    assert pytest.approx(expected) == burst


def test_burst_pressure_scales_linearly_with_yield() -> None:
    """Test that burst pressure scales linearly with yield strength."""
    a = 1.0
    b = 2.0
    yield1 = 100.0
    yield2 = 200.0
    bp1 = cylindrical_vessel.get_cylindrical_vessel_burst_pressure(a, b, yield1)
    bp2 = cylindrical_vessel.get_cylindrical_vessel_burst_pressure(a, b, yield2)

    # Doubling yield strength should double burst pressure
    assert pytest.approx(2 * bp1) == bp2


def test_cylindrical_vessel_burst_pressure_zero_radius() -> None:
    """Test the burst pressure for a case with zero inner radius."""
    a = 0.0
    b = 1.0
    sigma_y = 13.0

    with pytest.raises(ZeroDivisionError):
        cylindrical_vessel.get_cylindrical_vessel_burst_pressure(a, b, sigma_y)


def test_cylindrical_vessel_burst_pressure_reference_case() -> None:
    """Test the burst pressure for a reference case."""
    a = 101.6e-3
    b = 95.25e-3
    sigma_y = 40e6

    burst = cylindrical_vessel.get_cylindrical_vessel_burst_pressure(a, b, sigma_y)
    expected = 2659383.0
    assert pytest.approx(expected) == burst
