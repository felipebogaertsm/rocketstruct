# Bulkhead wall

Size a flat circular bulkhead (end cap) for a target margin of safety against burst, given working pressure, material, and bulkhead diameter.

The model is membrane-only: a uniformly loaded, simply supported circular plate. Real bulkheads with edge bending restraint or doming will be stronger than this estimate, so the resulting thickness is conservative.

## 1. Define the material and load case

```python
from rocketstruct.components.flat_plate import FlatPlate
from rocketstruct.materials.material import Material

al6061 = Material(
    yield_strength=276e6,
    allowable_shear_stress=207e6,
    allowable_bearing_stress=386e6,
    allowable_tensile_stress=276e6,
)

diameter = 80e-3                     # m
working_pressure = 12e6              # Pa
target_mos = 1.0
```

## 2. Solve for the minimum thickness

Membrane burst is \(p_\text{burst} = 2\sigma_y t / d\). Inverting for a target burst of \((1 + \text{MoS}) \cdot p_\text{working}\):

```python
t_min = (1 + target_mos) * working_pressure * diameter / (2 * al6061.yield_strength)
print(f"minimum thickness = {t_min * 1e3:.2f} mm")
```

## 3. Verify

```python
bulkhead = FlatPlate(diameter=diameter, thickness=t_min, material=al6061)
print(f"burst = {bulkhead.burst_pressure() / 1e6:.1f} MPa")
print(f"MoS   = {bulkhead.margin_of_safety(working_pressure):.2f}")
```
