# `diablo_mode_manager` — selected current development source

> 🚧 **ACTIVE DEVELOPMENT — REAL ROBOT SOURCE**

This directory represents the current Jetson Xavier NX mode-management package in the public source snapshot.

## Published now

- `voice_runtime_manager_node.py` — starts/stops the INTERACT voice stack on demand, publishes voice-enabled state, checks ROS endpoints and body-state health, and exposes an INTERACT-ready signal
- `package.xml`
- `setup.py`
- `setup.cfg`

## Important boundary

The active workspace also contains the large current `mode_manager_node.py`, which coordinates a much broader set of DIABLO operating modes and safety/ownership transitions. That large implementation is **not included in this selected public snapshot**.

This means the repository now shows a real mode-owned runtime component and the package structure, but it does not claim to expose the complete current mode manager.

## Publication note

Private machine-specific home paths and maintainer contact data were generalized for publication. Existing package license declarations were not normalized as part of this source-copy step; see [`../../LICENSE_STATUS.md`](../../LICENSE_STATUS.md).

Snapshot details: [`../../CURRENT_SOURCE_2026-09-04.md`](../../CURRENT_SOURCE_2026-09-04.md).
