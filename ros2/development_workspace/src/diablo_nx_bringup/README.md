# `diablo_nx_bringup`

> Source snapshot: **2026-08-19**  
> Status: **real development source / historical bringup snapshot**

This package preserves part of the Jetson Xavier NX ROS 2 bringup structure from the real DIABLO development workspace.

## Launch file

### [`launch/diablo_nx_base.launch.py`](launch/diablo_nx_base.launch.py)

The published launch snapshot starts four nodes from the camera and voice-command packages:

- `camera_cmd_node`
- `command_router_node`
- `safety_gate_node`
- `beep_feedback_node`

This is useful as development history, but it is **not** the current complete NX runtime definition. DIABLO X3-NX has evolved toward a more distributed service/runtime structure since this snapshot was captured.

For the current public architecture description, see:

- [`../../../../docs/ros2/NODES_AND_SERVICES.md`](../../../../docs/ros2/NODES_AND_SERVICES.md)
- [`../../../../docs/ros2/WORKSPACE_STRUCTURE.md`](../../../../docs/ros2/WORKSPACE_STRUCTURE.md)
- [`../../../../docs/ros2/X3_NX_ROLES.md`](../../../../docs/ros2/X3_NX_ROLES.md)

## Why publish an older bringup snapshot?

The project is intended to preserve technical evolution, not only a final cleaned-up state. This launch file shows an earlier organization of the NX runtime and helps explain how the current architecture emerged.
