"""
Flat plate stress and burst pressure calculations.

Simple closed-form membrane stress for uniformly loaded circular flat plates.

References:
    Shigley, J.E., Mischke, C.R., & Budynas, R.G. (2015). Mechanical
    Engineering Design (10th ed.). McGraw-Hill.
"""


def get_flat_plate_stress(pressure: float, diameter: float, thickness: float) -> float:
    """
    Return the membrane (tensile) stress in a uniformly loaded flat plate.

    Applies to a simply supported circular plate loaded by uniform internal pressure.
    Conservative for real end caps, which often include edge bending restraint or
    doming.

    Args:
        pressure: Internal pressure [Pa].
        diameter: Plate diameter [m].
        thickness: Plate thickness [m].

    Returns:
        Membrane stress [Pa].
    """
    return pressure * diameter / (2.0 * thickness)


def get_flat_plate_burst_pressure(
    diameter: float,
    thickness: float,
    material_yield_strength: float,
) -> float:
    """
    Return the burst pressure for a flat plate.

    Defined as the internal pressure at which the membrane stress reaches the
    material's yield strength.

    Args:
        diameter: Plate diameter [m].
        thickness: Plate thickness [m].
        material_yield_strength: Material yield strength [Pa].

    Returns:
        Burst pressure [Pa].
    """
    return 2 * material_yield_strength * thickness / diameter
