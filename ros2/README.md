# DIABLO X3-NX — ROS 2 Source Area

> 🚧 **WORK IN PROGRESS — ACTIVE ROBOT DEVELOPMENT**
>
> This area contains reviewed source snapshots from the real DIABLO X3-NX ROS 2 development workspace.
>
> The codebase is still evolving. Files published here may change as the robot is tested, diagnosed and extended.

## New here?

**Start with [`START_HERE.md`](START_HERE.md).** It gives a short technical tour and links directly to the most interesting source files already public.

## Real development source

The first larger real NX source publication is available at:

**[`development_workspace/`](development_workspace/)**

Snapshot date: **2026-08-19**

Batch 1 publishes complete reviewed packages for NX bringup, safety and UWB/tracker integration. Larger active packages for camera/perception, FOLLOW/AUTO, mode management and INTERACT/voice are planned as subsequent reviewed source batches.

The source comes from the real `diablo_ws/src` workspace. It is not reconstructed example code. Limited publication-safety edits are documented in the snapshot manifest.

### Direct source entry points

- [`diablo_safety`](development_workspace/src/diablo_safety/) — RealSense safety and an early system-state node
- [`diablo_tracker`](development_workspace/src/diablo_tracker/) — experimental UWB serial tracker/distance integration
- [`diablo_nx_bringup`](development_workspace/src/diablo_nx_bringup/) — historical NX bringup structure
- [`SOURCE_PUBLICATION_ROADMAP.md`](development_workspace/SOURCE_PUBLICATION_ROADMAP.md) — what is intended to be reviewed for the next real source batches

## Related ROS 2 documentation

- [`../docs/ros2/NODES_AND_SERVICES.md`](../docs/ros2/NODES_AND_SERVICES.md)
- [`../docs/ros2/SAFETY_AND_MOTION_FLOW.md`](../docs/ros2/SAFETY_AND_MOTION_FLOW.md)
- [`../docs/ros2/TOPICS.md`](../docs/ros2/TOPICS.md)
- [`../docs/ros2/PACKAGE_STATUS.md`](../docs/ros2/PACKAGE_STATUS.md)
- [`../docs/ros2/WORKSPACE_STRUCTURE.md`](../docs/ros2/WORKSPACE_STRUCTURE.md)

## Examples

The earlier [`examples/armed_state/`](examples/armed_state/) area remains as an explanatory WIP area. Real source publication is now centered on the development workspace rather than synthetic standalone examples.

## Publication model

DIABLO X3-NX is a real multi-computer ROS 2 system. Development snapshots are published to show:

- real package structure
- real nodes and interfaces
- interaction between X3 and Jetson NX
- safety and permission logic
- mode implementation direction
- current technical development state

They should **not** be interpreted as finished plug-and-play releases.

Public source review excludes or separately handles build output, local backups, credentials/private data, temporary diagnostic captures, machine-specific secrets and third-party/vendor code that should remain upstream.

## Stable release later

A future stable release will be explicitly tagged and documented separately from ongoing development. Until then, `main` is a living development history.

The project-wide open-source license is still being prepared and will be finalized before the first formal stable open-source release.
