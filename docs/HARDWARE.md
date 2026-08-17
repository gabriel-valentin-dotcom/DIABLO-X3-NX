# Hardware

> **Status:** ACTIVE DEVELOPMENT

## Core platform

- **Robot base:** Direct Drive Technology DIABLO two-wheel platform
- **Robot-side compute:** D-Robotics RDK X3
- **High-level compute:** NVIDIA Jetson Xavier NX 16GB
- **LiDAR:** RPLIDAR C1
- **Depth / RGB camera:** Intel RealSense D435
- **Audio:** ReSpeaker XVF3800 family
- **UWB development:** Ai-Thinker BU04
- **Touch display:** X3-side display for direct status and mode control
- **Middleware:** ROS 2

## Compute split

The RDK X3 is used for robot-near control and direct interfaces. The Jetson Xavier NX is used for higher-level behavior and perception.

## Sensors

LiDAR and depth vision are used as complementary information sources. They are not treated as interchangeable: each has a different role in perception and safety.

## Power system

The battery and power subsystem is undergoing a separate redesign. Final public specifications will be documented when the new configuration is stable and verified.

## Future documentation

Hardware photographs, physical mounting details and sensor-layout images will be added progressively when time allows.
