# External Source and Dependency Boundaries

This development snapshot intentionally does **not** copy every repository found inside the private ROS 2 workspace.

## Kept external

### DDTRobot DIABLO ROS 2 interfaces

DIABLO controller interfaces such as `motion_msgs` and `ception_msgs` originate from the upstream DDTRobot DIABLO ROS 2 project. They are treated as an external dependency rather than being republished as GVM project source.

Upstream project: `DDTRobot/diablo_ros2`

### Intel / RealSense ROS

The RealSense ROS wrapper used by the camera stack is third-party software and is not vendored into this DIABLO source snapshot.

### SLAMTEC SLLIDAR ROS 2

The RPLIDAR/SLLIDAR ROS 2 driver is third-party software and is not vendored into this DIABLO source snapshot.

## Why keep these separate?

Keeping upstream projects separate makes ownership, attribution, versioning and licensing clearer. DIABLO X3-NX documentation may reference these dependencies, but the public development snapshot focuses on project-specific code.

Third-party projects remain governed by their own licenses and upstream repositories.
