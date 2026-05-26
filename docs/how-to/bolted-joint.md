# Bolted joint

Check a bolted joint against all four failure modes — bolt shear, plate bearing, edge tear-out, net-section tension — and report the governing mode.

## 1. Define the material and joint geometry

```python
from rocketstruct.components.bolted_joint import BoltedJoint
from rocketstruct.materials.material import Material

al6061 = Material(
    yield_strength=276e6,
    allowable_shear_stress=207e6,
    allowable_bearing_stress=386e6,
    allowable_tensile_stress=276e6,
)

joint = BoltedJoint(
    shank_diameter=3.3e-3,           # M4 effective shaft
    hole_diameter=4.2e-3,
    thickness=3e-3,
    edge_distance=8e-3,
    pitch_distance=12e-3,
    material=al6061,
    n_bolts_in_row=4,
    n_shear_planes=1,
)
```

For a bolted row on a thin-walled cylinder, use `BoltedJoint.from_cylinder(...)`, which converts edge and pitch angles to arc-length distances on the outer surface.

## 2. Evaluate the per-bolt limit load in each mode

```python
limits = {
    "shear":       joint.max_shear_load(),
    "bearing":     joint.max_bearing_load(),
    "tear-out":    joint.max_tearout_load(),
    "net-section": joint.max_net_tension_load() / joint.n_bolts_in_row,
}
for mode, load in sorted(limits.items(), key=lambda kv: kv[1]):
    print(f"{mode:<12} {load:7.0f} N")
```

Net-section tension is a per-row limit; dividing by `n_bolts_in_row` puts all four modes on a per-bolt basis.

## 3. Check against the applied load

```python
load_per_bolt = 1200                 # N

governing = min(limits, key=limits.get)
mos = joint.margin_of_safety(load_per_bolt)

print(f"governing mode = {governing}")
print(f"MoS            = {mos:.2f}")
```
