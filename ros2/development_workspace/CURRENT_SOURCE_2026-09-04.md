# Current ROS 2 integration source — 2026-09-04

> 🚧 **REAL ROBOT / ACTIVE DEVELOPMENT**
>
> This page records the second public source review from the current DIABLO X3-NX `diablo_ws/src` workspace. It is intentionally a **selected development snapshot**, not a claim that the entire live workspace is public or release-ready.

## Source archive reviewed

- Archive supplied from the Jetson Xavier NX workspace: `DIABLO_diablo_ws_src_CURRENT.tar.gz`
- Review/publication date: **2026-09-04**
- SHA-256: `37f725965ad49d6efc750ebb68c177588d3b66679a538805e99a633ebfc5c196`
- Archive size: about **79 MB**
- Source root: `diablo_ws/src`

The archive contains both project-specific packages and upstream/vendor repositories. Upstream RealSense and SLLIDAR repositories, nested Git history, backups, generated Python cache files and historical variants are not republished here.

## Newly published current source

### Camera / perception

Public current files under [`src/diablo_camera/`](src/diablo_camera/):

- `camera_cmd_node.py`
- `camera_manager_node.py`
- `realsense_preview_node.py`
- `vision_track_node.py`
- `lidar_safety_node.py`
- `safety_bubble_node.py`
- `motor_stall_protect_node.py`
- `camera_system.launch.py`
- package metadata

These files show on-demand RealSense management, CUDA/YOLO preview integration, target/depth processing, floor/depth safety, LiDAR sector handling, a safety bubble and motor-stall protection.

### FOLLOW

Published current source includes:

- `diablo_camera/follow_manager_node.py`

This exposes the current FOLLOW arm/start/dependency state handling, CAM/TRACK ownership, target readiness checks and explicit `HOLD_NO_MOVE` states.

The current live workspace also contains a much larger `follow_action_node.py`. That file is **not included in this selected public snapshot**, so this repository must not be read as containing the complete current FOLLOW implementation.

### AUTO

Published current source includes:

- `diablo_camera/auto_manager_node.py`
- `diablo_camera/auto_supervisor_node.py`

The supervisor shows the permission-oriented AUTO/FOLLOW safety layer and explicitly does not directly own low-level motor control.

### Mode / runtime ownership

Public current files under [`src/diablo_mode_manager/`](src/diablo_mode_manager/):

- `voice_runtime_manager_node.py`
- package metadata

This shows the on-demand INTERACT runtime, readiness checks and runtime ownership around the voice stack.

The large current `mode_manager_node.py` remains outside this selected public snapshot. Therefore this publication does not claim to expose the complete mode-management implementation.

### INTERACT / voice command path

Public current files under [`src/diablo_voice_command/`](src/diablo_voice_command/):

- `voice_command_node.py`
- package metadata

This exposes wakeword handling, current German command mapping, duplicate suppression and the controlled publication of voice intents.

The active workspace also contains `safe_voice_pose_node.py` and `voice_input_node.py`; those larger files are not included in this selected publication. The public code therefore shows important parts of INTERACT without pretending that the entire audio-to-motion path has been released.

## Publication-safety edits

Only publication-safety edits were made to copied source:

- the private NX home-directory username was generalized from `/home/<private-user>/...` to `/home/diablo/...`
- personal maintainer email data was replaced with a non-routable project placeholder where package metadata was published
- no passwords, tokens or private network/SSH values were found in the selected files

These edits are not presented as runtime changes to the robot.

## Deliberately excluded

The current archive also contains material that is intentionally not copied into the public repository:

- `realsense-ros/` upstream source
- `sllidar_ros2/` upstream source
- nested `.git/` history from third-party repositories
- `__pycache__` and `.pyc` files
- numerous timestamped `BACKUP_*` and historical development variants
- temporary or broken source variants
- project-specific files outside the selected Camera/FOLLOW/Mode/AUTO/INTERACT publication scope

## Status

This source is useful for understanding the real architecture and development direction, but it is **not a stable plug-and-play release**. The physical robot remains the final source of truth for behavior and verification.

After this integration-source publication, larger source expansion can wait until DIABLO reaches a later stable in-use state and a formal release is prepared.
