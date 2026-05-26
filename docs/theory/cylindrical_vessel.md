# 1. Cylindrical Vessel

Closed-form stresses and first-yield burst pressure for a thick-walled cylindrical vessel with closed ends, under internal pressure only. Lamé's equations.

## Assumptions

- Axisymmetric geometry, isotropic linear-elastic material.
- Quasi-static internal pressure \(p\); external pressure \(p_o = 0\).
- Closed ends (axial-force balance applies to the end caps).
- Section far from end-cap discontinuities, weld lines, and ports.

## Lamé stresses at the inner wall

For internal pressure \(p\), inner radius \(a\), and outer radius \(b\), the principal stresses at \(r = a\) are (Shigley §3-14, Eq. 3-50):

\[
\sigma_t = p\,\frac{a^2 + b^2}{b^2 - a^2} \qquad \text{(hoop)}
\]

\[
\sigma_r = -p \qquad \text{(radial; satisfies the BC at } r=a\text{)}
\]

\[
\sigma_a = p\,\frac{a^2}{b^2 - a^2} \qquad \text{(longitudinal, from end-cap force balance)}
\]

Hoop is the maximum principal stress and is positive (tensile) for internal pressure. All three are evaluated at the inner wall, where they are most critical.

## Von Mises equivalent stress

\[
\sigma_\text{eq} = \sqrt{\tfrac{1}{2}\!\left[(\sigma_a - \sigma_r)^2 + (\sigma_r - \sigma_t)^2 + (\sigma_t - \sigma_a)^2\right]}
\]

\(\sigma_\text{eq}\) is maximum at the inner wall and decreases monotonically outward. Because Lamé is linear in \(p\), so is \(\sigma_\text{eq}\).

## Burst pressure

Defined as the internal pressure at which \(\sigma_\text{eq}(r=a) = \sigma_y\):

\[
p_\text{burst} = \frac{\sigma_y}{\sigma_\text{eq}(p=1,\,a,\,b)}
\]

This is a **first-yield** criterion at the inner wall, not a true plastic burst. Real burst is higher because the wall plastically redistributes stress before rupture (autofrettage and beyond); first-yield is the conservative, code-friendly bound.

## Limits of applicability

- **Thin-wall regime** (\(D/t \gtrsim 20\)): the membrane approximation \(\sigma_t \approx pD/(2t)\) is accurate within a few percent and Lamé is unnecessary.
- **End-cap discontinuities**: bending and shear concentrations near closures, fillets, and ports are not captured. Use Roark Ch. 13 or FE for these.
- **Buckling**: external pressure, axial compression, or bending loads can govern below the burst pressure (Roark Ch. 15).
- **Fatigue**: static analysis only. Pressure cycling life requires \(K_t\)-corrected fatigue analysis (Shigley §6).
- **Plasticity / autofrettage / strain hardening**: not modeled.

## References

- Shigley, J.E., Mischke, C.R., Budynas, R.G. (2015). *Mechanical Engineering Design*, 10th ed., §3-14.
- Roark, R.J., Young, W.C. (2002). *Roark's Formulas for Stress and Strain*, 7th ed., Ch. 13.
