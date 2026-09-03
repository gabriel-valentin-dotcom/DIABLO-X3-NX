# ROS 2 Overview

> 🚧 **WORK IN PROGRESS — ACTIVE ROBOT DEVELOPMENT**

This section documents selected ROS 2 interfaces and architecture used by DIABLO X3-NX.

Reviewed source from the real NX `diablo_ws/src` workspace is now published progressively under [`../../ros2/development_workspace/`](../../ros2/development_workspace/). New visitors can use [`../../ros2/START_HERE.md`](../../ros2/START_HERE.md) for a short source-oriented technical tour.

## Main ROS 2 areas

- Robot control and telemetry
- Sensor data
- Safety state
- Camera and perception
- FOLLOW and autonomous behavior
- Mode management
- On-demand interaction
- X3 ↔ Jetson NX communication

## Public source status

The first reviewed source batch contains real NX packages for bringup, safety and experimental UWB/tracker integration.

Larger connected areas such as camera/perception/FOLLOW, mode management/AUTO and INTERACT/voice are documented here but are not all present yet as public source. They are tracked in the [`source publication roadmap`](../../ros2/development_workspace/SOURCE_PUBLICATION_ROADMAP.md).

## Important note

This documentation is not yet intended as a complete plug-and-play software distribution. Topics, parameters and implementation details may change while the robot is developed.

## Related pages

- [ROS 2 source — start here](../../ros2/START_HERE.md)
- [Nodes and runtime components](NODES_AND_SERVICES.md)
- [Component status](PACKAGE_STATUS.md)
- [Safety and motion flow](SAFETY_AND_MOTION_FLOW.md)
- [Topic map](TOPICS.md)
- [X3 / NX role split](X3_NX_ROLES.md)
- [Data flow](DATA_FLOW.md)
