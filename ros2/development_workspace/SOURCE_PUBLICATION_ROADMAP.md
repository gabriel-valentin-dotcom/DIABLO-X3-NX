# Real source publication roadmap

> 🚧 **ACTIVE DEVELOPMENT / PUBLICATION ROADMAP**
>
> DIABLO X3-NX intentionally publishes real development snapshots while keeping a clear boundary between public source history and a future stable release.

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

## Published — current integration source

Review/publication date: **2026-09-04**

A newer NX `diablo_ws/src` archive was reviewed and a selected current integration set was added. See [`CURRENT_SOURCE_2026-09-04.md`](CURRENT_SOURCE_2026-09-04.md) for the archive hash, publication boundaries and sanitization record.

### Camera / perception

Now public:

- camera command and runtime management
- RealSense preview / CUDA-YOLO integration
- vision target and depth/floor processing
- LiDAR safety integration
- safety-bubble processing
- motor-stall protection

### FOLLOW

Now public:

- current `follow_manager_node.py`
- FOLLOW arm/start/dependency ownership and readiness logic

The much larger current `follow_action_node.py` remains outside this selected public snapshot, so the repository does **not** claim to contain the complete current FOLLOW implementation.

### AUTO

Now public:

- `auto_manager_node.py`
- `auto_supervisor_node.py`
- current AUTO/FOLLOW permission-oriented safety supervision

### Mode management

Now public:

- current `voice_runtime_manager_node.py`
- mode-manager package metadata

The large current central `mode_manager_node.py` remains outside this selected public snapshot.

### INTERACT / voice

Now public:

- current `voice_command_node.py`
- current on-demand voice runtime manager
- package metadata

The active workspace contains additional INTERACT source such as `safe_voice_pose_node.py` and `voice_input_node.py`; those larger files are not part of this selected public publication.

## Publication pause after this integration batch

This repository now exposes enough current real ROS 2 implementation to show the architecture and development direction without pretending that the entire live workspace is a stable release.

The next **large source expansion is intentionally deferred** until DIABLO reaches a later stable, real-world in-use state. At that point the project can prepare a cleaner release-oriented source set, complete licensing review and repeatable deployment/validation documentation.

Smaller documentation corrections, verified status updates and real-hardware media can still be added while development continues.

## Later — X3-side project-specific integration

Where licensing and ownership boundaries allow, a later release can cover project-specific X3-side integration such as:

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

A published snapshot remains useful even when the live robot evolves beyond it. Snapshot code is kept as technical history; current behavior and verification status are documented separately under [`../../docs/`](../../docs/).

The repository will not silently rewrite old source to make it look newer than it is.

## Long-term goal

The public source should make it possible to understand the real control direction:

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

A stable release will be identified separately when the project reaches repeatable full-system validation and real-world use.
