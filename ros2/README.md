# DIABLO X3-NX — ROS 2 Source Area

> 🚧 **WORK IN PROGRESS — ACTIVE ROBOT DEVELOPMENT**
>
> This area contains reviewed source snapshots from the real DIABLO X3-NX ROS 2 development workspace.
>
> The codebase is still evolving. Files published here may change as the robot is tested, diagnosed and extended.

## New here?

**Start with [`START_HERE.md`](START_HERE.md).** It gives a short technical tour and links directly to useful real source.

## Real development source

Browse:

**[`development_workspace/`](development_workspace/)**

Two reviewed source stages are represented publicly:

- **2026-08-19 — Batch 1:** NX bringup, safety and UWB/tracker packages
- **2026-09-04 — current integration selection:** Camera/perception, FOLLOW manager, AUTO supervision, LiDAR/safety, INTERACT command and on-demand voice-runtime components

The source comes from the real `diablo_ws/src` workspace. It is not reconstructed example code. Publication-safety edits and exact source boundaries are documented alongside each snapshot.

### Direct current-source entry points

- [`CURRENT_SOURCE_2026-09-04.md`](development_workspace/CURRENT_SOURCE_2026-09-04.md) — current archive review record and publication boundary
- [`diablo_camera`](development_workspace/src/diablo_camera/) — selected current camera, perception, FOLLOW/AUTO and safety-related source
- [`diablo_mode_manager`](development_workspace/src/diablo_mode_manager/) — selected current runtime ownership / INTERACT management source
- [`diablo_voice_command`](development_workspace/src/diablo_voice_command/) — selected current INTERACT command source
- [`diablo_safety`](development_workspace/src/diablo_safety/) — earlier RealSense safety/system-state snapshot
- [`diablo_tracker`](development_workspace/src/diablo_tracker/) — earlier experimental UWB serial tracker snapshot
- [`diablo_nx_bringup`](development_workspace/src/diablo_nx_bringup/) — earlier NX bringup snapshot
- [`SOURCE_PUBLICATION_ROADMAP.md`](development_workspace/SOURCE_PUBLICATION_ROADMAP.md) — publication status and later release direction

## Important boundary

The public tree is a selected real-source publication, **not a complete mirror of the live workspace**. Large current implementations that are outside the selection are documented as such rather than being replaced with simplified or synthetic code.

Upstream/vendor repositories, backups, generated files, nested Git history and private deployment details are excluded from the public source review.

## Related ROS 2 documentation

- [`../docs/ros2/NODES_AND_SERVICES.md`](../docs/ros2/NODES_AND_SERVICES.md)
- [`../docs/ros2/SAFETY_AND_MOTION_FLOW.md`](../docs/ros2/SAFETY_AND_MOTION_FLOW.md)
- [`../docs/ros2/TOPICS.md`](../docs/ros2/TOPICS.md)
- [`../docs/ros2/PACKAGE_STATUS.md`](../docs/ros2/PACKAGE_STATUS.md)
- [`../docs/ros2/WORKSPACE_STRUCTURE.md`](../docs/ros2/WORKSPACE_STRUCTURE.md)

## Examples

The earlier [`examples/armed_state/`](examples/armed_state/) area remains as an explanatory WIP area. Real source publication is centered on the development workspace rather than synthetic standalone examples.

## Publication model

DIABLO X3-NX is a real multi-computer ROS 2 system. Development snapshots are published to show:

- real package structure
- real nodes and interfaces
- interaction between X3 and Jetson NX
- safety and permission logic
- mode implementation direction
- current technical development state

They should **not** be interpreted as finished plug-and-play releases.

## Stable release later

After the 2026-09-04 integration selection, larger source expansion is intentionally paused while DIABLO continues toward stable real-world use.

A future stable release will be explicitly tagged and documented separately from ongoing development. Until then, `main` remains a living development history.

The project-wide open-source license is still being prepared and will be finalized before the first formal stable open-source release.
