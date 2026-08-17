# ROS 2 Data Flow

> **Status:** WORK IN PROGRESS

A simplified view of the current architecture:

```text
Robot sensors
     |
     v
X3 controller / sensor nodes
     |
     | ROS 2 telemetry
     v
Jetson NX
- perception
- safety supervision
- modes
- FOLLOW / AUTO decisions
     |
     | high-level motion request
     v
X3 motion bridge
     |
     v
DIABLO robot base
```

## Design intent

Sensor data flows upward toward decision layers. Motion requests flow back toward the robot through a controlled bridge.

Safety and permission state can prevent a requested action from becoming physical movement.

The public diagram is intentionally high level. More detailed ownership and message-flow diagrams can be added later.
