# DIABLO X3-NX — Real NX Development Source

> 🚧 **WORK IN PROGRESS — ACTIVE ROBOT DEVELOPMENT**
>
> This directory contains selected **real source code from the DIABLO X3-NX ROS 2 workspace**. It intentionally preserves development history while also exposing a newer reviewed integration selection.

The code is published while the robot is still being developed and tested. Interfaces, parameters, package structure and implementation details may change.

## Public source snapshots

### Batch 1 — 2026-08-19

The first reviewed publication contains real NX packages for:

- [`diablo_safety`](src/diablo_safety/) — RealSense-based safety state and system-state logic
- [`diablo_tracker`](src/diablo_tracker/) — experimental UWB distance/tracker integration
- [`diablo_nx_bringup`](src/diablo_nx_bringup/) — NX ROS 2 bringup structure

Historical manifest: [`SNAPSHOT_MANIFEST.md`](SNAPSHOT_MANIFEST.md).

### Current integration source — 2026-09-04

A newer real NX `diablo_ws/src` archive was reviewed and a selected current source set was added for:

- [`diablo_camera`](src/diablo_camera/) — Camera, perception, FOLLOW manager, AUTO supervision and safety-related runtime components
- [`diablo_mode_manager`](src/diablo_mode_manager/) — selected current runtime ownership / INTERACT management
- [`diablo_voice_command`](src/diablo_voice_command/) — selected current INTERACT command handling

Full review record, source-archive hash, publication boundaries and sanitization notes:

**[`CURRENT_SOURCE_2026-09-04.md`](CURRENT_SOURCE_2026-09-04.md)**

## Good current files to inspect first

- [`vision_track_node.py`](src/diablo_camera/diablo_camera/vision_track_node.py)
- [`camera_manager_node.py`](src/diablo_camera/diablo_camera/camera_manager_node.py)
- [`follow_manager_node.py`](src/diablo_camera/diablo_camera/follow_manager_node.py)
- [`auto_supervisor_node.py`](src/diablo_camera/diablo_camera/auto_supervisor_node.py)
- [`lidar_safety_node.py`](src/diablo_camera/diablo_camera/lidar_safety_node.py)
- [`motor_stall_protect_node.py`](src/diablo_camera/diablo_camera/motor_stall_protect_node.py)
- [`voice_command_node.py`](src/diablo_voice_command/diablo_voice_command/voice_command_node.py)
- [`voice_runtime_manager_node.py`](src/diablo_mode_manager/diablo_mode_manager/voice_runtime_manager_node.py)

For a short project-wide tour, see [`../START_HERE.md`](../START_HERE.md).

## Important boundary

This directory is **not a complete mirror of the live workspace**. The 2026-09-04 archive also contains larger current project files that remain outside this selected publication, including the full FOLLOW action implementation, central mode manager, safe voice pose and voice input.

Upstream/vendor repositories, nested Git history, backups, generated files and private deployment details are deliberately not copied into this public tree.

The repository does not substitute simplified or synthetic implementations for files that are not published.

## Publication direction

See [`SOURCE_PUBLICATION_ROADMAP.md`](SOURCE_PUBLICATION_ROADMAP.md).

After the 2026-09-04 integration-source selection, the next **large source expansion is intentionally paused** while DIABLO continues toward stable real-world use. A future stable release can then be prepared separately with a stronger licensing, deployment and validation pass.

## What this source is not

This is **not yet a stable plug-and-play release**. Running DIABLO requires the corresponding robot-side X3 software, external ROS 2 dependencies, hardware, models, runtime services and configuration that are not all represented here.

A historical snapshot is also not silently rewritten to match a newer runtime. Historical names and interfaces can remain in old snapshot source while current architecture/status is documented separately.

## Publication review

Before publication, source is checked for:

- credentials and secrets
- private contact and network information
- machine-specific deployment identifiers
- obsolete backups and temporary diagnostic material
- third-party/vendor source that should remain upstream
- license and attribution boundaries

See [DEPENDENCIES.md](DEPENDENCIES.md), [SNAPSHOT_MANIFEST.md](SNAPSHOT_MANIFEST.md), [CURRENT_SOURCE_2026-09-04.md](CURRENT_SOURCE_2026-09-04.md) and [LICENSE_STATUS.md](LICENSE_STATUS.md).

## Status language

- **VERIFIED** — demonstrated in the real robot system
- **ACTIVE DEVELOPMENT** — real implementation that may still change
- **EXPERIMENTAL** — exploratory implementation or subsystem
- **PLANNED** — documented direction not yet presented as working

The final source of truth remains repeatable evidence from the real robot.
