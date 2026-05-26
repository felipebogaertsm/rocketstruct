# 2. Flat Plate

Membrane-only burst-pressure estimate for a circular flat closure (bulkhead, end cap) under uniform internal pressure.

## The model used

The plate is treated as a thin membrane whose peak stress under uniform pressure follows the thin-walled hoop-stress form:

\[
\sigma = \frac{p D}{2 t}
\]

The corresponding first-yield burst pressure is:

\[
p_\text{burst} = \frac{2\,\sigma_y\,t}{D}
\]

This is a deliberately conservative estimate for an end cap: it ignores plate bending stiffness and edge restraint, so any real closure with a clamped or welded perimeter carries more pressure than predicted.

## What rigorous plate theory predicts

For a uniformly loaded circular plate of radius \(a\) and thickness \(t\), small-deflection plate-bending theory gives a peak bending stress at the centre (Roark Ch. 11, Table 11.2):

\[
\sigma_\text{max} = \beta\,\frac{p\,a^2}{t^2}
\]

with \(\beta = 3(3+\nu)/8 \approx 1.24\) (simply supported) or \(\beta = 3/4\) (clamped). Plate bending scales as \((a/t)^2\), not \(D/t\), so the bending and membrane regimes are distinct.

The membrane model used here is appropriate only when bending stiffness is small (very thin, large deflection — von Kármán regime) or as a deliberately conservative quick check.

## Limits of applicability

- **Bending-dominated plates** (\(t/a\) not very small, intact edge restraint): use Roark Ch. 11 instead. The membrane formula under-predicts capacity, sometimes by an order of magnitude.
- **Edge restraint**: clamped, welded, or filleted closures all increase capacity above the membrane estimate.
- **Domed heads** (ellipsoidal, hemispherical, torispherical): use the appropriate ASME-style closed forms; do not analyse with this model.
- **Large deflection / plasticity / fatigue**: not modeled.

## References

- Roark, R.J., Young, W.C. (2002). *Roark's Formulas for Stress and Strain*, 7th ed., Ch. 11 (flat plates).
- Megyesy, E.F. (2008). *Pressure Vessel Handbook*, 14th ed. (heads and closures).
