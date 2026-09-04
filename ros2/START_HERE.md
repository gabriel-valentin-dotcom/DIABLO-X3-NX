# Start here — DIABLO X3-NX ROS 2

> 🚧 **REAL ROBOT / ACTIVE DEVELOPMENT**
>
> This is a public technical tour of the ROS 2 side of DIABLO X3-NX. The repository intentionally shows work while it is still being built, tested and changed on the physical robot.

## If you only have five minutes

Start with these links:

1. [`development_workspace/CURRENT_SOURCE_2026-09-04.md`](development_workspace/CURRENT_SOURCE_2026-09-04.md) — what was reviewed from the current NX `diablo_ws/src` archive and what was deliberately excluded.
2. [`development_workspace/src/diablo_camera/diablo_camera/vision_track_node.py`](development_workspace/src/diablo_camera/diablo_camera/vision_track_node.py) — current target/depth/floor processing from the real robot workspace.
3. [`development_workspace/src/diablo_camera/diablo_camera/follow_manager_node.py`](development_workspace/src/diablo_camera/diablo_camera/follow_manager_node.py) — current FOLLOW arm/start/dependency state handling.
4. [`development_workspace/src/diablo_camera/diablo_camera/auto_supervisor_node.py`](development_workspace/src/diablo_camera/diablo_camera/auto_supervisor_node.py) — current permission/safety supervision for AUTO and FOLLOW.
5. [`development_workspace/src/diablo_voice_command/diablo_voice_command/voice_command_node.py`](development_workspace/src/diablo_voice_command/diablo_voice_command/voice_command_node.py) — current INTERACT wakeword and German intent mapping.
6. [`development_workspace/src/diablo_mode_manager/diablo_mode_manager/voice_runtime_manager_node.py`](development_workspace/src/diablo_mode_manager/diablo_mode_manager/voice_runtime_manager_node.py) — current on-demand voice-runtime ownership and readiness checks.
7. [`../docs/ros2/SAFETY_AND_MOTION_FLOW.md`](../docs/ros2/SAFETY_AND_MOTION_FLOW.md) — how high-level behavior is kept behind safety and motion-request layers.

## What makes this ROS 2 project different

DIABLO X3-NX is not a simulation-only repository. It is a two-computer ROS 2 system running on a real self-balancing DIABLO robot:

- **RDK X3** stays close to the robot controller, LiDAR, touch UI and motion bridge.
- **Jetson Xavier NX** handles higher-level perception, camera, FOLLOW/AUTO logic, interaction and supervision.
- ROS 2 connects the layers while motion is intentionally separated from higher-level behavior through explicit request, permission and safety paths.

See [`../docs/ros2/X3_NX_ROLES.md`](../docs/ros2/X3_NX_ROLES.md) and [`../docs/ros2/NODES_AND_SERVICES.md`](../docs/ros2/NODES_AND_SERVICES.md).

## Public real-source snapshots

### Foundation snapshot — 2026-08-19

The first reviewed source publication preserved three real NX packages:

| Package | What to look at | Publication state |
|---|---|---|
| `diablo_safety` | RealSense safety state + system-state logic | historical source snapshot |
| `diablo_tracker` | UWB serial distance/tracker experiment | historical source snapshot |
| `diablo_nx_bringup` | NX ROS 2 bringup structure | historical source snapshot |

### Current integration selection — 2026-09-04

A newer real `diablo_ws/src` archive was reviewed and selected current source was added for:

- Camera / RealSense runtime
- perception and vision tracking
- FOLLOW manager state/dependency logic
- AUTO manager and supervisor
- LiDAR / safety bubble / motor-stall protection
- INTERACT voice-command mapping
- on-demand voice runtime management

Browse [`development_workspace/src/diablo_camera/`](development_workspace/src/diablo_camera/), [`development_workspace/src/diablo_mode_manager/`](development_workspace/src/diablo_mode_manager/) and [`development_workspace/src/diablo_voice_command/`](development_workspace/src/diablo_voice_command/).

## Important publication boundary

This is a **selected real-source publication**, not a dump of the complete live workspace. Large current files such as the full FOLLOW action implementation, central mode manager, safe voice pose and voice input remain outside this public selection. Upstream RealSense/SLLIDAR repositories, backups, generated files and private deployment details are also excluded.

See [`development_workspace/SOURCE_PUBLICATION_ROADMAP.md`](development_workspace/SOURCE_PUBLICATION_ROADMAP.md).

## Verification language

- **VERIFIED** — demonstrated on the physical robot.
- **ACTIVE DEVELOPMENT** — real implementation that is still changing.
- **EXPERIMENTAL** — exploratory subsystem or behavior.
- **PLANNED** — direction only; not presented as working.

Current component status: [`../docs/ros2/PACKAGE_STATUS.md`](../docs/ros2/PACKAGE_STATUS.md).

## Publication direction

After the 2026-09-04 integration-source selection, larger source expansion is intentionally paused while DIABLO continues toward stable real-world use. A future stable release will be prepared separately with stronger deployment, licensing and repeatable validation documentation.

The goal remains simple: **real code, real hardware, clear status, no fake completeness.**
