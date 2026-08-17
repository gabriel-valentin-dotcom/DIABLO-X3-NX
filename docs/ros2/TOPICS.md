# ROS 2 Topic Map

> **Status:** WORK IN PROGRESS  
> This is an initial public map and is not exhaustive.

| Topic | Purpose |
|---|---|
| `/diablo/sensor/Body_state` | Robot body/status telemetry |
| `/diablo/sensor/Battery` | Battery telemetry |
| `/diablo/sensor/Motors` | Motor telemetry |
| `/diablo/sensor/Imu` | IMU telemetry |
| `/diablo/sensor/ImuEuler` | Euler orientation telemetry |
| `/diablo/MotionCmd` | Low-level motion command path |
| `/diablo_motion_request` | High-level motion request |
| `/scan` | LiDAR scan |
| `/diablo/safety/lidar_safe_filtered` | Authoritative filtered LiDAR safety state |
| `/diablo/auto/permission` | Autonomous permission state |
| `/diablo/auto/state` | Autonomous state |
| `/vision_track/target` | Vision target direction/depth state |

## Why publish the topic map?

The topic map gives ROS 2 developers a quick orientation without requiring publication of the entire production source tree.

Additional interfaces will be added as they are reviewed and considered useful for understanding the project.
