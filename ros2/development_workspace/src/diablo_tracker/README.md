# `diablo_tracker`

> Source snapshot: **2026-08-19**  
> Status: **EXPERIMENTAL / real development source**

This package contains an experimental UWB distance/tracker path from the real NX `diablo_ws` workspace.

## Main source

### [`diablo_tracker/tracker_node.py`](diablo_tracker/tracker_node.py)

The node is a useful example of a hardware-facing ROS 2 component that does more than simply forward serial text.

In this snapshot it:

- enables work from `/diablo/mode/track_enabled`
- opens a configurable serial device
- sends an AT-style distance request
- parses `distance:` responses
- publishes calibrated distance on `/uwb_distance`
- publishes raw responses on `/uwb_raw`
- publishes tracker health/state on `/tracker_status`
- rejects zero and out-of-range readings
- detects repeated/stale measurements
- attempts serial reconnection after errors

Default serial communication in the snapshot is configured for **115200 baud**.

## Why this code is public even though UWB is experimental

The public project deliberately distinguishes **EXPERIMENTAL** from **VERIFIED**. Publishing exploratory code makes the development process easier to understand and gives other robotics developers something concrete to inspect and discuss without pretending that the subsystem is finished.

Current project-wide status is documented in [`../../../../docs/ros2/PACKAGE_STATUS.md`](../../../../docs/ros2/PACKAGE_STATUS.md).

## Hardware context

The project has used the Ai-Thinker BU04 as the UWB development target. The tracker subsystem remains an experimental part of the wider DIABLO X3-NX architecture.
