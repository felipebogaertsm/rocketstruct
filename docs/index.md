# rocketstruct

Structural analysis for pressure vessels, plates, and bolted joints, aimed at sizing rocket-engine structural components.

### Scope

- **Thick-walled cylindrical pressure vessels** — Lamé stresses, Von Mises burst pressure.
- **Circular flat plates** — membrane stress and burst pressure.
- **Bolted joints** (plates and thin-walled cylinders) — shear, bearing, tear-out, and net-section stresses and limit loads.

All inputs and outputs are SI: lengths in **metres**, pressures and stresses in **pascals**.

## Installation

rocketstruct requires **Python 3.11 – 3.13**.

```bash
pip install rocketstruct
```

## Quick Start

See the [Quick Start](quickstart.md) for an end-to-end vessel-sizing walkthrough.

For task-focused recipes (sizing a vessel wall, checking a bolted joint against every failure mode, sizing a bulkhead), see the [How-to guides](how-to/cylindrical-vessel-wall.md).

For the underlying assumptions and regime of validity of each calculation, see the [Theory](theory/cylindrical_vessel.md) section.

## Development Setup

[uv](https://docs.astral.sh/uv/) is required for dependency management.

```bash
git clone https://github.com/felipebogaertsm/rocketstruct.git
cd rocketstruct
uv sync
```

## References

- Shigley, J.E., Mischke, C.R., & Budynas, R.G. (2015). *Mechanical Engineering Design* (10th ed.). McGraw-Hill.
