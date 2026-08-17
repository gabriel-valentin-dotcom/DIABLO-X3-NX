# System Architecture

> **Status:** ACTIVE DEVELOPMENT

DIABLO X3-NX uses a two-computer architecture that separates robot-near functions from compute-heavy and higher-level behavior.

```text
Sensors / DIABLO robot base
          |
          v
D-Robotics RDK X3
- robot-side controller access
- motion bridge
- LiDAR runtime
- X3 touch UI
- robot-near status and selected safety functions
          |
          | ROS 2
          v
NVIDIA Jetson Xavier NX
- perception
- FOLLOW decision logic
- safety supervision
- camera runtime
- autonomous behavior
- voice / interaction
          |
          v
high-level decisions and motion requests
```

## RDK X3

The X3 stays close to the physical robot layer. It provides controller access, sensor/runtime integration and direct touch control.

## Jetson Xavier NX

The NX handles higher-level logic and workloads that benefit from more compute, including perception, FOLLOW behavior and interaction.

## ROS 2

ROS 2 is the communication and coordination layer between the two computers and the project subsystems.

The architecture is intentionally modular: a mode can be enabled or disabled without turning the entire robot software into one monolithic process.

## Development rule

Architecture shown here describes the **current direction**, not an immutable final design. Meaningful changes should be reflected in the documentation and changelog.
