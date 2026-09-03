# DIABLO X3-NX — Public Changelog

This changelog records meaningful **public project changes**, not every private diagnostic action.

## 2026-09-03

- Published the current **DIABLO X3-NX — INTERACT Voice Command Test | Real Robot** video and linked it from the repository documentation.
- Updated the public current-status, INTERACT, SHOW and known-limitations pages to reflect the latest real-hardware development state.
- Established a working controller telemetry/DDS baseline from X3 UART/OSDK through ROS 2 and cross-host `Body_state` delivery; the current X3 runtime uses an explicit Fast DDS UDPv4 transport profile.
- Corrected controller-authority first-command handling so the first valid command after authority reacquisition is preserved instead of being discarded.
- Removed a recurring generic idle HOLD repetition while retaining explicit STOP, LiDAR, bubble, stall and custom safety-abort behavior.
- Added an INTERACT-off voice-pose gate so stale/late voice pose and short-motion requests cannot continue after INTERACT is disabled, while STOP remains available.
- Added internal start/runtime safety gates to Custom Moonwalker V1 for fresh body state, standing mode, controller authority and zero error/warning state.
- Verified recovery of the LiDAR manager `LIDAR_READY` heartbeat with a targeted manager-service restart while `/scan` and LiDAR safety remained active.
- Performed the first live Custom Moonwalker trigger attempt. The request reached the NX mode-manager and motion-request path, but the X3 custom controller was not confirmed active before timeout; the choreography therefore remains **not yet physically validated**.

## 2026-08-19

- Published **NX Development Source Snapshot — Batch 1** from the real `diablo_ws/src` workspace.
- Recorded the reviewed source archive SHA-256 in the public snapshot manifest.
- Added complete reviewed ROS 2 packages for `diablo_safety`, `diablo_tracker` and `diablo_nx_bringup`.
- Added snapshot documentation covering publication boundaries, external dependencies and current license status.
- Applied limited publication-safety sanitization to private contact and machine-specific identifiers; no synthetic replacement implementation was introduced.
- Kept upstream DDTRobot interfaces, RealSense ROS and SLLIDAR ROS 2 outside the project-source snapshot.
- Kept backup/history variants, temporary diagnostics and older prototype material out of the current source batch.
- Updated the main README and ROS 2 source index to link directly to the real development source.
- Added a professional ROS 2 source-publication area under `ros2/`.
- Added a repository `.gitignore` for ROS 2 build output, local backups, runtime captures and common secret-file patterns.
- Added `CONTRIBUTING.md` with current contribution and status-language guidance.
- Added a validation section with a real-world test plan, known limitations and future release-readiness criteria.
- Kept the repository explicitly marked as active development rather than a stable plug-and-play release.

## 2026-08-17

- Added the first structured public documentation set.
- Added project overview, architecture, hardware and safety pages.
- Added dedicated pages for FOLLOW, TRACK, CAM, AUTO, LIDAR, INTERACT and SHOW.
- Added ROS 2 overview, topic map, X3/NX role split and data-flow documentation.
- Added current-status, design-decisions and Human-AI workflow pages.
- Added public roadmap and changelog.

## 2026-08-16

- Public repository opened as an **Early Public Preview / Work in Progress**.
- Initial public project preview added.
- First current X3 touch UI presentation image added under `media/images/ui/`.

Future documentation, architecture updates, media and reviewed development source snapshots will be recorded here as they are published.
