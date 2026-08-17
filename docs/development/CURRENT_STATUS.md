# Current Development Status

**Last updated:** 17 August 2026

> The project changes frequently. This page describes the current public development picture, not a final release state.

## FOLLOW

**VERIFIED / ACTIVE DEVELOPMENT**

Core FOLLOW behavior has been verified on the real robot. Continued tuning and integration work remains possible.

## LiDAR safety

**VERIFIED / ACTIVE DEVELOPMENT**

LiDAR safety is active and used as an authoritative motion-safety input.

## Vision

**ACTIVE DEVELOPMENT**

Target direction and depth information are used by higher-level behavior and safety logic.

## INTERACT

**VERIFIED BASIC FUNCTIONS / ACTIVE DEVELOPMENT**

The on-demand voice runtime is active. Basic safe intents have been verified. Additional short-motion intents remain under diagnosis and development.

## X3 touch UI

**ACTIVE**

The current UI includes INTERACT and SHOW areas and continues to evolve. A current presentation image is available under `media/images/ui/`.

## Controller telemetry / DDS diagnostics

**ACTIVE DEVELOPMENT**

Internal X3 controller telemetry and ROS publish paths are being audited against actual DDS user-data delivery behavior. This work is diagnostic and should not be interpreted as a finished root-cause conclusion until the remaining delivery path is proven.

## Battery / power

**HARDWARE REDESIGN IN PROGRESS**

A separate battery/power upgrade is being developed. Final public specifications will follow when stable.

## Media

More images and real-robot videos are planned when time allows.
