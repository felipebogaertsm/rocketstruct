from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    """
    Material strength properties used by structural components.

    Attributes:
        yield_strength: Yield strength [Pa]. Used by pressure-vessel and
            flat-plate burst-pressure calculations.
        allowable_shear_stress: Allowable shear stress [Pa]. Used by bolt-shear
            and tear-out limit-load calculations.
        allowable_bearing_stress: Allowable bearing stress [Pa]. Used by
            bearing limit-load calculations.
        allowable_tensile_stress: Allowable tensile stress [Pa]. Used by
            net-section tension limit-load calculations.
    """

    yield_strength: float
    allowable_shear_stress: float
    allowable_bearing_stress: float
    allowable_tensile_stress: float
