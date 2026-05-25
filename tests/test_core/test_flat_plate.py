import pytest

import rocketstruct.core.flat_plate as flat_plate


@pytest.mark.parametrize(
    "pressure, diameter, thickness",
    [
        (2.0e6, 0.30, 6.0e-3),
        (7.5e5, 0.20, 4.0e-3),
    ],
)
def test_flat_plate_stress_formula(pressure, diameter, thickness) -> None:
    """Direct check against sigma = P*d / (2*t)."""
    expected = pressure * diameter / (2.0 * thickness)
    result = flat_plate.get_flat_plate_stress(pressure, diameter, thickness)

    assert result == pytest.approx(expected)


def test_flat_plate_stress_linear_pressure() -> None:
    """Doubling pressure should double membrane stress."""
    p1, p2 = 0.9e6, 1.8e6
    d = 0.25
    t = 5.0e-3

    s1 = flat_plate.get_flat_plate_stress(p1, d, t)
    s2 = flat_plate.get_flat_plate_stress(p2, d, t)

    assert s2 == pytest.approx(2 * s1)


def test_flat_plate_zero_thickness_raises() -> None:
    """Zero thickness must raise ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        flat_plate.get_flat_plate_stress(1.0e6, 0.3, 0.0)
