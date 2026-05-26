# Rocketstruct

Rocketstruct is a Python library for structural analysis of rocket-engine components. It covers thick-walled pressure vessels, circular flat plates, and bolted joints — stresses, limit loads, and burst pressures — with SI units throughout.

## Getting Started

### Installation

Install Rocketstruct using pip:

```bash
pip install rocketstruct
```

### Documentation

The full documentation is available at
[felipebogaertsm.github.io/rocketstruct](http://felipebogaertsm.github.io/rocketstruct/).

### Development Setup

If you're contributing to Rocketstruct, you'll need [uv](https://docs.astral.sh/uv/) for dependency management.

#### Installing uv

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more details, visit the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

#### Clone and Install

Clone the repository and install dependencies:

```bash
git clone https://github.com/felipebogaertsm/rocketstruct.git
cd rocketstruct
make install
```

#### Publishing a New Release

1. **Create a release** on GitHub with a tag matching `vX.Y.Z` (e.g. `v1.2.0`).
   The version is derived automatically from the git tag.

2. The publish workflow builds the package and publishes it to PyPI via trusted publishing (OIDC).
