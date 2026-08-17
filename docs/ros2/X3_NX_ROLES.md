# RDK X3 and Jetson NX Roles

> **Status:** ACTIVE DEVELOPMENT

## D-Robotics RDK X3

Current robot-side responsibilities include:

- Robot controller access
- Motion bridge
- LiDAR scan/runtime
- Robot-side touch UI
- Robot-near status and selected safety functions

## NVIDIA Jetson Xavier NX

Current higher-level responsibilities include:

- Higher-level behavior
- Vision/perception
- FOLLOW decision logic
- Camera runtime management
- Autonomous supervision
- On-demand voice/interaction

## Why split the system?

The two-computer design keeps robot-near control separate from compute-heavy or higher-level tasks. This helps make subsystem ownership clearer and allows optional workloads to be started only when needed.
