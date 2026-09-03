# DIABLO X3-NX — Real NX Development Source Snapshot

> 🚧 **WORK IN PROGRESS — ACTIVE ROBOT DEVELOPMENT**
>
> This directory contains selected **real source code from the active DIABLO X3-NX ROS 2 workspace**.
>
> The code is published while the robot is still being developed and tested. Interfaces, parameters, package structure and implementation details may change.

## Snapshot

- Source system: NVIDIA Jetson Xavier NX development workspace
- Internal workspace: `diablo_ws/src`
- Snapshot date: **2026-08-19**
- Publication stage: **Batch 1 — foundation / safety / tracking**
- Runtime status: **ACTIVE DEVELOPMENT**

This is not reconstructed example code. It comes from the real development workspace used for DIABLO X3-NX. Only publication-safety edits were applied where necessary, such as replacing private maintainer contact data and machine-specific deployment identifiers.

## Published in Batch 1

The first source batch contains complete reviewed ROS 2 packages for:

- [`diablo_safety`](src/diablo_safety/) — RealSense-based safety state and system-state logic
- [`diablo_tracker`](src/diablo_tracker/) — experimental UWB distance/tracker integration
- [`diablo_nx_bringup`](src/diablo_nx_bringup/) — NX ROS 2 bringup structure

Each package now has a short public navigation README to explain what is worth opening first and where the historical snapshot differs from current runtime documentation.

## Good files to inspect first

- [`realsense_safety_node.py`](src/diablo_safety/diablo_safety/realsense_safety_node.py)
- [`diablo_system_state_node.py`](src/diablo_safety/diablo_safety/diablo_system_state_node.py)
- [`tracker_node.py`](src/diablo_tracker/diablo_tracker/tracker_node.py)
- [`diablo_nx_base.launch.py`](src/diablo_nx_bringup/launch/diablo_nx_base.launch.py)

For a short project-wide tour, see [`../START_HERE.md`](../START_HERE.md).

## Next real source batches

See [`SOURCE_PUBLICATION_ROADMAP.md`](SOURCE_PUBLICATION_ROADMAP.md).

The highest-priority future source areas are camera/perception/FOLLOW, mode management/AUTO and INTERACT/voice. They will only be published from real reviewed workspace files; the repository will not substitute synthetic implementations just to make the tree look complete.

## Why batches?

DIABLO X3-NX is a connected multi-package system. The goal is to publish the real codebase progressively while keeping each public change reviewable and understandable.

## What this snapshot is not

This is **not yet a stable plug-and-play release**. Running DIABLO requires the corresponding robot-side X3 software, external ROS 2 dependencies, hardware, models, runtime services and configuration that are not all part of this first batch.

A snapshot is also not silently rewritten to match a newer runtime. Historical names and interfaces can remain in snapshot source while current architecture/status is documented separately.

## Publication review

Before publication, the source snapshot is checked for:

- credentials and secrets
- private contact and network information
- machine-specific deployment identifiers
- obsolete backups and temporary diagnostic material
- third-party/vendor source that should remain upstream
- license and attribution boundaries

See [DEPENDENCIES.md](DEPENDENCIES.md), [SNAPSHOT_MANIFEST.md](SNAPSHOT_MANIFEST.md) and [LICENSE_STATUS.md](LICENSE_STATUS.md).

## Status language

- **VERIFIED** — demonstrated in the real robot system
- **ACTIVE DEVELOPMENT** — real implementation that may still change
- **EXPERIMENTAL** — exploratory implementation or subsystem
- **PLANNED** — documented direction not yet presented as working

The final source of truth remains repeatable evidence from the real robot.
