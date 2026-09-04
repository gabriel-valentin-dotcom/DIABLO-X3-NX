# `diablo_camera` — selected current development source

> 🚧 **ACTIVE DEVELOPMENT — REAL ROBOT SOURCE**

This directory contains a reviewed selection from the current Jetson Xavier NX `diablo_ws/src/diablo_camera` package.

## Published current nodes

- `camera_cmd_node.py` — camera command/service bridge
- `camera_manager_node.py` — on-demand RealSense runtime management and watchdog
- `realsense_preview_node.py` — RealSense preview / CUDA-YOLO object integration
- `vision_track_node.py` — target direction, depth and floor/depth safety processing
- `follow_manager_node.py` — FOLLOW arm/start/dependency state management
- `auto_manager_node.py` — AUTO helper state commands
- `auto_supervisor_node.py` — permission/safety supervision for AUTO and FOLLOW
- `lidar_safety_node.py` — LiDAR sector safety processing
- `safety_bubble_node.py` — local safety-bubble state
- `motor_stall_protect_node.py` — motor-stall protection using motion, LiDAR and motor telemetry

Package metadata and the development launch file are also included.

## Important boundary

The active package contains additional current and historical files. In particular, the large current `follow_action_node.py` is not included in this selected public snapshot. The public source therefore shows the FOLLOW state/dependency layer but **not the entire current FOLLOW decision implementation**.

The copied `setup.py` is preserved as development metadata and may reference entry points whose source is outside this selected publication. This is expected in an active-workspace snapshot and should not be interpreted as a polished release package.

## Safety / licensing

Private machine-specific home paths and maintainer contact data were generalized for publication. License metadata remains development-stage; see [`../../LICENSE_STATUS.md`](../../LICENSE_STATUS.md).

Snapshot details: [`../../CURRENT_SOURCE_2026-09-04.md`](../../CURRENT_SOURCE_2026-09-04.md).
