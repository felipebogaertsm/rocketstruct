# 4. Margin of Safety

rocketstruct uses the aerospace convention (Bruhn §A1.1; MIL-HDBK-5J / MMPDS):

\[
\text{MoS} = \frac{P_\text{limit}}{P_\text{applied}} - 1
\]

\(\text{MoS} \geq 0\) means the structure is OK against the chosen failure criterion at the applied load. \(\text{MoS} = 0\) means zero margin; \(\text{MoS} = 1.0\) means a factor of two over the limit load.

## No implicit factor of safety

The component-level MoS does **not** include a design factor of safety. Two consistent ways to apply one:

- **Bake the FoS into the allowables.** Reduce `Material.allowable_*` (or `yield_strength`) by the FoS before constructing the component. `margin_of_safety` then reports the margin against the de-rated allowables.
- **Bake the FoS into the target MoS.** Require \(\text{MoS} \geq (\text{FoS} - 1)\) at the applied load.

Apply one convention consistently across a project — mixing them double-counts the safety factor.

## Limit vs. ultimate

`CylindricalVessel.margin_of_safety` and `FlatPlate.margin_of_safety` compare burst pressure (first yield at the critical point) to the applied pressure. This is a **yield** margin, not an **ultimate** margin: real burst is higher than first-yield burst due to plastic redistribution.

`BoltedJoint.margin_of_safety` compares applied load to the per-bolt limit load computed from `Material.allowable_*`. The interpretation (yield, ultimate, or design allowable) follows the source of the allowables — `Material` does not enforce a convention. MIL-HDBK-5J / MMPDS values are the typical source for aerospace work.

## References

- Bruhn, E.F. (1973). *Analysis and Design of Flight Vehicle Structures*, §A1.1.
- MIL-HDBK-5J / MMPDS-XX. (Design allowables and margin conventions.)
