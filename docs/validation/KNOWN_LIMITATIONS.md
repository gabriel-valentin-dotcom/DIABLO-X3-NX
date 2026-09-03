# Known Limitations

> 🚧 **ACTIVE DEVELOPMENT**

This page lists important known limitations that should remain visible while DIABLO X3-NX is being developed.

## Current limitations

- The complete ROS 2 development workspace has not yet been published.
- AUTO is not presented as a finished autonomous navigation system.
- UWB integration remains experimental.
- Battery V2 is still a hardware-development project and has not yet completed real-robot validation.
- Long-duration and repeated full-system validation is not yet complete.
- DDS/telemetry delivery now has a working real-hardware baseline, but longer-term robustness is still being monitored.
- The LiDAR manager's `LIDAR_READY` heartbeat can require targeted runtime recovery even while `/scan` and the safety state remain active; this behavior is still being hardened.
- Custom Moonwalker V1 is implemented but has **not yet completed a successful physical choreography run**. The latest live attempt stopped before custom motion execution because controller confirmation timed out.
- SHOW functions remain under active validation and should not be interpreted as finished release features.
- Public documentation may lag behind private development between updates.

## Interpretation

A documented limitation does not necessarily mean the corresponding subsystem is unusable. It means the project does not yet claim stable release-level behavior for that area.

This list will be updated as limitations are resolved, replaced or newly discovered.
