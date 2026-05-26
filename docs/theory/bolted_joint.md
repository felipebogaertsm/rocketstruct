# 3. Bolted Joint

Closed-form stresses and per-bolt limit loads for a bolted joint in a thin-walled plate or cylinder. Four independent failure modes are evaluated; the joint capacity is the minimum across all four.

## The four failure modes

Per Shigley §8-9 to §8-11 and Bruhn Ch. D1:

**1. Bolt shear** (single or double plane), \(n_p\) shear planes:

\[
\tau = \frac{P}{n_p\,A_s}, \qquad A_s = \frac{\pi d_s^2}{4}
\]

**2. Plate bearing** (compression of plate material at the hole):

\[
\sigma_b = \frac{P}{t\,d_h}
\]

**3. Plate tear-out** (block shear toward a free edge):

\[
\tau = \frac{P}{2\,e\,t}
\]

**4. Plate net-section tension** (tensile rupture across the bolt row):

\[
\sigma = \frac{P}{(s - d_h)\,t}
\]

where \(d_s\) is the bolt shank effective diameter, \(d_h\) the hole diameter, \(t\) the plate (or wall) thickness, \(e\) the edge distance (centre to free edge), and \(s\) the pitch (centre-to-centre between adjacent bolts in a row).

## Limit load and governing mode

Each mode has a corresponding limit load obtained by setting the stress equal to the material allowable for that mode (shear, bearing, or tensile). The per-bolt joint capacity is the minimum:

\[
P_\text{lim} = \min\{P_\text{shear},\,P_\text{bearing},\,P_\text{tear-out},\,P_\text{net-section}\}
\]

Net-section tension is a per-row limit; it is normalised to per-bolt by dividing by `n_bolts_in_row` before taking the minimum.

## Cylinder geometry

For a bolt row on a thin-walled cylinder, edge and pitch are specified as central angles and converted to arc length on the outer surface:

\[
e = \tfrac{1}{2} D_o\,\theta_e, \qquad s = \tfrac{1}{2} D_o\,\theta_s
\]

The four failure formulas above then apply unchanged. This is a thin-wall assumption: the plate model ignores cylinder curvature in the bolt vicinity.

## Limits of applicability

- **Preload and friction grip**: not modeled. Slip-critical bolted joints carry load through clamp-induced friction rather than shank shear; use preload-based formulas instead (Shigley §8-7).
- **Bolt-group eccentricity**: a load whose line of action does not pass through the bolt-group centroid produces unequal per-bolt loads. Resolve to per-bolt loads externally.
- **Bolt tension and joint separation**: not modeled. These formulas address transverse shear and net-section tension only.
- **Fatigue**: static analysis only. Fastener fatigue requires preload, \(K_t\), and mean/alternating decomposition (Shigley §8-11).
- **Bolt bending and hole-edge plasticity**: not modeled.

## References

- Shigley, J.E., Mischke, C.R., Budynas, R.G. (2015). *Mechanical Engineering Design*, 10th ed., §8-9 to §8-11.
- Bruhn, E.F. (1973). *Analysis and Design of Flight Vehicle Structures*, Ch. D1 (mechanical connections).
- MIL-HDBK-5J / MMPDS (current ed.). (Design allowables for fasteners and plate bearing.)
