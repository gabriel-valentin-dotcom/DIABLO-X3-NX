# `diablo_safety`

> Source snapshot: **2026-08-19**  
> Status: **real development source / historical snapshot**

This package is part of the first reviewed public source snapshot from the NX `diablo_ws` workspace.

## Files worth opening first

### [`diablo_safety/realsense_safety_node.py`](diablo_safety/realsense_safety_node.py)

A compact depth-safety node using the RealSense depth image.

In this snapshot it:

- subscribes to `/camera/camera/depth/image_rect_raw` by default
- reads `16UC1` depth data
- evaluates a center image region
- uses the median valid depth in that region
- publishes a textual state on `/safety_state`
- publishes a boolean stop signal on `/safety_stop`
- exposes stop/slow distances as ROS 2 parameters

The source is intentionally simple enough to inspect directly and is useful as an early example of how depth information entered DIABLO's safety work.

### [`diablo_safety/diablo_system_state_node.py`](diablo_safety/diablo_system_state_node.py)

An early system-state snapshot that checks for selected ROS 2 node and topic names and publishes `/diablo_system_status`.

Because this is a historical source snapshot, some node names and mode labels inside the file reflect an earlier stage of the project. Do not treat its embedded required-node list as the current authoritative runtime inventory.

For the current architecture/status documentation, see:

- [`../../../../docs/ros2/NODES_AND_SERVICES.md`](../../../../docs/ros2/NODES_AND_SERVICES.md)
- [`../../../../docs/ros2/PACKAGE_STATUS.md`](../../../../docs/ros2/PACKAGE_STATUS.md)
- [`../../../../docs/ros2/SAFETY_AND_MOTION_FLOW.md`](../../../../docs/ros2/SAFETY_AND_MOTION_FLOW.md)

## Why keep early source public?

DIABLO X3-NX is being documented as an evolving real robot. Early source is useful because it shows how the architecture grew rather than presenting only a cleaned-up final result.

This package should therefore be read as **real development history**, not as a promise that every topic and threshold shown here matches the newest robot configuration.
