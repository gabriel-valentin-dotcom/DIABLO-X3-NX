# Start here — DIABLO X3-NX ROS 2

> 🚧 **REAL ROBOT / ACTIVE DEVELOPMENT**
>
> This is a public technical tour of the ROS 2 side of DIABLO X3-NX. The repository intentionally shows work while it is still being built, tested and changed on the physical robot.

## If you only have five minutes

Start with these links:

1. [`development_workspace/`](development_workspace/) — reviewed source copied from the real NX `diablo_ws/src` workspace.
2. [`development_workspace/src/diablo_safety/diablo_safety/realsense_safety_node.py`](development_workspace/src/diablo_safety/diablo_safety/realsense_safety_node.py) — a compact example of RealSense depth data being turned into ROS 2 safety state.
3. [`development_workspace/src/diablo_tracker/diablo_tracker/tracker_node.py`](development_workspace/src/diablo_tracker/diablo_tracker/tracker_node.py) — experimental UWB serial integration with stale-data handling and ROS 2 status/distance output.
4. [`development_workspace/src/diablo_nx_bringup/launch/diablo_nx_base.launch.py`](development_workspace/src/diablo_nx_bringup/launch/diablo_nx_base.launch.py) — part of the NX bringup structure.
5. [`../docs/ros2/SAFETY_AND_MOTION_FLOW.md`](../docs/ros2/SAFETY_AND_MOTION_FLOW.md) — how high-level behavior is kept behind safety and motion-request layers.

## What makes this ROS 2 project different

DIABLO X3-NX is not a simulation-only repository. It is a two-computer ROS 2 system running on a real self-balancing DIABLO robot:

- **RDK X3** stays close to the robot controller, LiDAR, touch UI and motion bridge.
- **Jetson Xavier NX** handles higher-level perception, camera, FOLLOW/AUTO logic, interaction and supervision.
- ROS 2 connects the layers while motion is intentionally separated from higher-level behavior through explicit request and safety paths.

See [`../docs/ros2/X3_NX_ROLES.md`](../docs/ros2/X3_NX_ROLES.md) and [`../docs/ros2/NODES_AND_SERVICES.md`](../docs/ros2/NODES_AND_SERVICES.md).

## Source available now

The first reviewed source publication contains three real packages:

| Package | What to look at | Publication state |
|---|---|---|
| `diablo_safety` | RealSense safety state + system-state logic | published source snapshot |
| `diablo_tracker` | UWB serial distance/tracker experiment | published source snapshot |
| `diablo_nx_bringup` | NX ROS 2 bringup structure | published source snapshot |

The snapshot is dated **2026-08-19**. It is intentionally preserved as development history, so some names or interfaces inside that snapshot may differ from the newest runtime documentation.

## Important active areas not yet included as source

The live project also contains larger connected areas for camera/perception, FOLLOW, AUTO, mode management and INTERACT/voice. Their behavior is already documented in the repository, but current source files will only be added after the same publication review used for Batch 1.

See [`development_workspace/SOURCE_PUBLICATION_ROADMAP.md`](development_workspace/SOURCE_PUBLICATION_ROADMAP.md).

## Verification language

- **VERIFIED** — demonstrated on the physical robot.
- **ACTIVE DEVELOPMENT** — real implementation that is still changing.
- **EXPERIMENTAL** — exploratory subsystem or behavior.
- **PLANNED** — direction only; not presented as working.

Current component status: [`../docs/ros2/PACKAGE_STATUS.md`](../docs/ros2/PACKAGE_STATUS.md).

## Why the repository does not simply dump the entire workspace

The active workspace also contains build output, backups, machine-local deployment details and third-party/vendor packages. Public batches are reviewed so that the repository can show the real project without publishing credentials, private host information, temporary diagnostics or source that belongs upstream.

The goal is simple: **real code, real hardware, clear status, no fake completeness.**
