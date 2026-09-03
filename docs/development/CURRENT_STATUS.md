# Current Development Status

**Last updated:** 3 September 2026

> The project changes frequently. This page describes the current public development picture, not a final release state.

## FOLLOW

**VERIFIED / ACTIVE DEVELOPMENT**

Core FOLLOW behavior has been verified on the real robot. The accepted FOLLOW baseline remains intact while other subsystems continue to evolve.

## LiDAR safety

**VERIFIED / ACTIVE DEVELOPMENT**

LiDAR safety is active and used as an authoritative motion-safety input. Fresh scans and SAFE/BLOCKED safety state are available during normal operation.

A separate LiDAR-manager `LIDAR_READY` status heartbeat is also used by selected higher-level actions. A recent runtime loss of that heartbeat was recovered by a targeted restart of the LiDAR manager while scan and safety data remained active. Recovery robustness is still being validated.

## Vision

**ACTIVE DEVELOPMENT**

Target direction and depth information are used by higher-level behavior and safety logic.

## INTERACT

**VERIFIED REAL-HARDWARE FUNCTIONS / ACTIVE DEVELOPMENT**

The on-demand voice runtime is active. The real voice-command path and basic controlled intents have been verified on the physical robot, including `STOP`, `STAND_UP` and `SIT_DOWN`.

INTERACT is designed so that voice pose/motion requests are gated by the current INTERACT state, while safety/STOP behavior remains available. Further robustness and command expansion remain active development work.

A current real-robot INTERACT test is published on YouTube:

[DIABLO X3-NX — INTERACT Voice Command Test | Real Robot](https://www.youtube.com/watch?v=1tYXHSDjvRE)

## X3 touch UI

**ACTIVE**

The current UI includes INTERACT and SHOW areas and continues to evolve. A current presentation image is available under `media/images/ui/`.

## Controller telemetry / DDS

**WORKING BASELINE / CONTINUED VALIDATION**

The X3 UART -> OSDK -> telemetry -> ROS publish path has been proven end to end on real hardware. Cross-host `Body_state` delivery was restored and stabilized using the current X3 Fast DDS UDPv4 transport profile.

Controller authority reacquisition and first-command preservation were also corrected so the first valid command after authority recovery is not discarded.

Longer-term DDS/runtime robustness continues to be monitored, but the earlier controller-publish path itself is no longer treated as the unresolved root cause.

## Stand-up / pose control

**VERIFIED BASELINE**

`STAND_UP` has been verified on the real robot with `robot_mode=3`, `ctrl_mode=1`, and zero reported error/warning state after transition.

A recurring generic idle HOLD that could repeatedly inject zero commands has been deduplicated while explicit STOP, LiDAR, bubble, stall and custom safety abort paths remain active.

## SHOW / Custom Moonwalker

**IN DEVELOPMENT — NOT YET PHYSICALLY VALIDATED**

A custom Moonwalker V1 sequence has been implemented using normal motion control rather than manufacturer automation mode. The choreography includes backward motion with alternating left/right components and remains intentionally conservative.

The custom path now has internal start and runtime gates requiring fresh body state, standing mode, controller authority and zero error/warning state. STOP and safety HOLD paths can abort the sequence.

The first live trigger attempt did **not** execute the choreography: the command reached the NX mode manager and motion-request stage, but controller confirmation timed out before the X3 custom sequence was confirmed active. No successful physical Moonwalker movement is claimed yet.

## Battery / power

**HARDWARE REDESIGN IN PROGRESS**

A separate battery/power upgrade is being developed. Final public specifications will follow when stable.

## Media

The current real-robot INTERACT video is linked from the main README and the INTERACT documentation. Additional real-robot media will be added as functions reach verified physical milestones.
