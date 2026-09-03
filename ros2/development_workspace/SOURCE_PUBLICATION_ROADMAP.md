# Real source publication roadmap

> 🚧 **ACTIVE DEVELOPMENT / PUBLICATION ROADMAP**
>
> This page describes which parts of the real DIABLO X3-NX `diablo_ws` are already represented in the public source snapshot and which connected areas are intended for later reviewed source batches.

## Published — Batch 1

Snapshot date: **2026-08-19**

Already public under [`src/`](src/):

- `diablo_safety`
  - `realsense_safety_node.py`
  - `diablo_system_state_node.py`
  - package metadata
- `diablo_tracker`
  - `tracker_node.py`
  - package metadata
- `diablo_nx_bringup`
  - NX bringup package
  - launch structure

These files come from the real NX development workspace. They are not reconstructed examples.

## High-priority next source areas

The following areas are especially important because they show how the robot moves from perception and user intent toward controlled physical behavior.

### Batch 2 — Camera / perception / FOLLOW

Planned publication focus:

- current camera-management source
- RealSense preview/perception nodes used by the project
- FOLLOW manager logic
- FOLLOW action/decision logic
- package metadata and relevant configuration

Why this matters: FOLLOW is one of the strongest examples of the project combining target information, depth, LiDAR/safety state, permission and controlled motion requests. Physical forward/left/right FOLLOW behavior has been demonstrated on the real robot, while tuning and integration continue.

### Batch 3 — Mode management / AUTO

Planned publication focus:

- mode-manager source
- AUTO supervisor source
- enable/permission state handling
- configuration needed to understand how operating modes are coordinated

Why this matters: DIABLO X3-NX is not a collection of unrelated ROS nodes. Mode ownership and permission are used to prevent multiple higher-level behaviors from independently treating motion as unrestricted.

### Batch 4 — INTERACT / voice runtime

Planned publication focus:

- on-demand voice runtime management
- voice input / command mapping source where publication review allows it
- safe short-action path
- package metadata and runtime configuration

Why this matters: INTERACT demonstrates a resource-aware voice design where the full audio stack is not required to run continuously at boot. Basic `STOP`, `STAND_UP` and `SIT_DOWN` behavior has been verified on the real robot.

### Later — X3-side project-specific integration

Where licensing and ownership boundaries allow, later public material can cover project-specific X3-side integration such as:

- high-level motion-request bridge integration
- robot-side launch/runtime structure
- project-specific LiDAR safety integration
- touch-UI integration points

Third-party/vendor SDK source is not automatically republished and should remain with its upstream owner unless redistribution is clearly permitted.

## Publication rules

Every source batch is reviewed before it reaches the public repository. The review excludes or sanitizes:

- credentials, tokens and secrets
- private contact information
- private network/SSH details
- machine-specific deployment identifiers that do not belong in public source
- backups, temporary diagnostics and generated build output
- vendor or third-party source that should remain upstream

## Historical snapshots versus current runtime

A published snapshot is valuable even when the live robot has already evolved beyond it. Snapshot code is kept as technical history; current behavior and verification status are documented separately under [`../../docs/`](../../docs/).

The repository will not silently rewrite old source to make it look newer than it is.

## Goal

The long-term goal is to make enough of the real project public that another robotics developer can understand:

```text
sensor / user intent
        |
        v
perception + mode state
        |
        v
permission + safety gates
        |
        v
high-level motion request
        |
        v
X3 motion bridge
        |
        v
DIABLO controller / physical robot
```

A stable release will be identified separately when the project reaches repeatable full-system validation.
