# Cylindrical vessel wall

Size a thick-walled cylindrical vessel for a target margin of safety against burst, given working pressure, material, and inner diameter.

## 1. Define the material and load case

```python
import numpy as np

from rocketstruct.components.cylindrical_vessel import CylindricalVessel
from rocketstruct.materials.material import Material

al6061 = Material(
    yield_strength=276e6,            # Pa
    allowable_shear_stress=207e6,
    allowable_bearing_stress=386e6,
    allowable_tensile_stress=276e6,
)

inner_diameter = 80e-3               # m
working_pressure = 12e6              # Pa
target_mos = 1.0                     # 2× burst margin
```

## 2. Evaluate a candidate wall

```python
vessel = CylindricalVessel(
    inner_diameter=inner_diameter,
    outer_diameter=90e-3,
    material=al6061,
)

print(f"burst = {vessel.burst_pressure() / 1e6:.1f} MPa")
print(f"MoS   = {vessel.margin_of_safety(working_pressure):.2f}")
```

## 3. Solve for the minimum wall thickness

Burst pressure is monotonically increasing in outer diameter. Sweep and pick the smallest value whose MoS clears the target.

```python
outer_diameters = np.linspace(inner_diameter + 1e-3, inner_diameter + 30e-3, 200)
mos = np.array([
    CylindricalVessel(inner_diameter, od, al6061).margin_of_safety(working_pressure)
    for od in outer_diameters
])

d_outer_min = outer_diameters[mos >= target_mos][0]
t_min = (d_outer_min - inner_diameter) / 2.0
print(f"minimum wall thickness = {t_min * 1e3:.2f} mm")
```

For a real build, round up to the next available stock wall thickness and re-evaluate the MoS.
