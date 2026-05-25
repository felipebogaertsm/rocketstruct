# rocketstruct

Structural analysis for rocket engines.

## Scope

- **`rocketstruct.core`** — pure closed-form stress and load functions.
  - `cylindrical_vessel` — thick-walled cylinder under internal pressure (Lamé equations, Von Mises burst).
  - `flat_plate` — membrane stress and burst pressure for circular flat plates.
  - `bolted_joint` — shear, bearing, tear-out, and net-section stresses and limit loads for bolted plates and thin-walled cylinders.

## Install

```bash
pip install rocketstruct
```

## References

- Shigley, J.E., Mischke, C.R., & Budynas, R.G. (2015). _Mechanical Engineering Design_ (10th ed.). McGraw-Hill.