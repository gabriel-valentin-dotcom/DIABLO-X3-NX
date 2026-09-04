# `diablo_voice_command` — selected current INTERACT source

> 🚧 **ACTIVE DEVELOPMENT — REAL ROBOT SOURCE**

This directory contains a reviewed current source selection from the DIABLO INTERACT command package.

## Published now

- `voice_command_node.py` — current wakeword handling, German intent mapping, duplicate suppression and publication to `/voice_cmd_de`
- `package.xml`
- `setup.py`
- `setup.cfg`

The published command node shows current intent handling for STOP, stand/sit, approved short motions and selected body-pose commands.

## Important boundary

The active workspace contains additional INTERACT nodes, including the larger current `safe_voice_pose_node.py`, feedback nodes and other development components. Those are not all copied into this selected public snapshot.

The public code therefore exposes an important real part of the voice-command path without claiming that the entire audio-to-motion implementation is released.

The on-demand runtime component is published separately at [`../diablo_mode_manager/diablo_mode_manager/voice_runtime_manager_node.py`](../diablo_mode_manager/diablo_mode_manager/voice_runtime_manager_node.py).

## Publication note

Personal maintainer contact information was removed from copied package metadata. Existing development-stage license fields were not normalized; see [`../../LICENSE_STATUS.md`](../../LICENSE_STATUS.md).

Snapshot details: [`../../CURRENT_SOURCE_2026-09-04.md`](../../CURRENT_SOURCE_2026-09-04.md).
