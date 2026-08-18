# ROS 2 Nodes and Runtime Components

> 🚧 **WORK IN PROGRESS — ACTIVE ROBOT DEVELOPMENT**
>
> This page documents important ROS 2 runtime components currently used or
> being developed for DIABLO X3-NX.
>
> It is intentionally not presented as a final API reference.

## Status terminology

**VERIFIED**  
The function has been demonstrated on the real robot.

**IN DEVELOPMENT**  
The component is active but still changing, being extended or being diagnosed.

**EXPERIMENTAL**  
The component or behavior is being evaluated and may be replaced.

**PLANNED**  
The component or feature is part of the intended direction but is not yet
presented as implemented.

---

## RDK X3 — robot-side components

### `/diablo_ctrl_node`

**Status: VERIFIED / ACTIVE DEVELOPMENT**

Main interface between ROS 2 and the DIABLO robot controller.

Responsibilities include:

- robot telemetry
- controller communication
- body-state information
- battery information
- motor telemetry
- IMU telemetry

The controller interface is currently also part of ongoing ROS 2 / DDS
delivery diagnostics.

The internal telemetry and ROS publishing paths have been observed working,
while end-to-end message delivery is still being investigated in some runtime
situations.

---

### `/diablo_motion_bridge_node`

**Status: VERIFIED**

Converts higher-level motion requests into DIABLO motion-control messages.

Typical flow:

```text
higher-level behavior
        |
        v
/diablo_motion_request
        |
        v
motion bridge
        |
        v
/diablo/MotionCmd
        |
        v
DIABLO controller
```

This separation allows higher-level behavior to request movement without
directly owning the low-level controller interface.

---

### `/sllidar_node`

**Status: VERIFIED**

Publishes RPLIDAR C1 scan data.

Primary scan topic:

`/scan`

---

### X3 LiDAR safety component

**Status: VERIFIED / ACTIVE DEVELOPMENT**

Processes LiDAR information for obstacle and safety evaluation.

Different areas around the robot are evaluated separately, including:

- front
- front-left
- front-right
- left
- right
- rear

The safety layer uses stop/release hysteresis to avoid rapid state changes.

---

### X3 touch UI

**Status: VERIFIED / ACTIVE DEVELOPMENT**

The robot-side UI provides direct status visualization and access to selected
operating modes.

Current visible mode areas include:

- TRACK
- CAM
- AUTO
- LIDAR
- INTERACT
- SHOW
- FOLLOW

The UI is intentionally evolving together with the robot.

---

# Jetson Xavier NX — higher-level components

### `/mode_manager_node`

**Status: VERIFIED / ACTIVE DEVELOPMENT**

Coordinates high-level operating modes and runtime enable states.

---

### `/camera_manager_node`

**Status: VERIFIED**

Controls the RealSense camera runtime.

The camera does not need to run permanently when its functionality is not
required.

---

### `/follow_manager_node`

**Status: VERIFIED / ACTIVE DEVELOPMENT**

Maintains FOLLOW state and permission-related information.

---

### `/follow_action_node`

**Status: VERIFIED / ACTIVE DEVELOPMENT**

Contains higher-level FOLLOW decision logic.

Inputs can include:

- target direction
- target distance/depth
- LiDAR safety
- vision safety
- FOLLOW state
- movement permission

Outputs are controlled movement requests rather than unrestricted direct motor
control.

---

### `/auto_supervisor_node`

**Status: IN DEVELOPMENT**

Supervises autonomous behavior and permission.

Important concepts include:

- AUTO state
- AUTO permission
- safety gating

AUTO is not currently presented as a finished autonomous navigation stack.

---

### `/voice_runtime_manager_node`

**Status: VERIFIED**

Starts and stops the voice interaction runtime on demand.

The full voice stack is intentionally not required to run permanently at boot.

---

### Voice interaction nodes

**Status: VERIFIED BASIC FUNCTIONS / ACTIVE DEVELOPMENT**

The current INTERACT design focuses on short and controlled actions.

Verified basic intents include:

- STOP
- STAND_UP
- SIT_DOWN

Additional short-motion commands are under active development and diagnosis.

Continuous unrestricted voice driving is not the design goal.

---

## Important note

This list is intended to help other developers understand the architecture.

It is not yet a complete list of every temporary node, diagnostic process or
development experiment used during the project.
