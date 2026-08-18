# ROS 2 Component Status

> 🚧 **LIVE DEVELOPMENT STATUS**
>
> DIABLO X3-NX is tested continuously on real hardware.
>
> Status can change as functions are improved, replaced or revalidated.

| Area | Current status | Notes |
|---|---|---|
| DIABLO controller interface | VERIFIED / ACTIVE DEVELOPMENT | Controller communication and telemetry path active; DDS delivery diagnostics ongoing |
| Motion bridge | VERIFIED | High-level request to DIABLO MotionCmd path |
| RPLIDAR C1 | VERIFIED | `/scan` available |
| LiDAR safety | VERIFIED / ACTIVE DEVELOPMENT | Used for movement safety |
| RealSense D435 runtime | VERIFIED | Runtime camera management |
| Vision target tracking | VERIFIED / ACTIVE DEVELOPMENT | Target direction and depth information |
| FOLLOW | VERIFIED / ACTIVE DEVELOPMENT | Physical forward / left / right behavior demonstrated |
| TRACK | IN DEVELOPMENT | Target tracking layer |
| CAM | VERIFIED / ACTIVE DEVELOPMENT | On-demand camera functionality |
| AUTO | IN DEVELOPMENT | Supervised autonomous behavior |
| INTERACT basic intents | VERIFIED | STOP, STAND_UP, SIT_DOWN |
| INTERACT short motions | IN DEVELOPMENT | Runtime path currently being diagnosed |
| SHOW | IN DEVELOPMENT | Demonstration-oriented functions |
| UWB | EXPERIMENTAL | Additional positioning / tracking work |
| X3 touch UI | VERIFIED / ACTIVE DEVELOPMENT | Continues to evolve |
| Battery V2 integration | IN DEVELOPMENT | Separate hardware development |

## What VERIFIED means

VERIFIED does not mean that development has stopped.

It means that the stated behavior has been demonstrated on the physical
DIABLO robot.

A verified component may still receive:

- tuning
- safety improvements
- architecture changes
- performance improvements
- new capabilities

## What IN DEVELOPMENT means

The function exists in the development project but should not be interpreted
as a finished public product or stable API.

## Why unfinished work is shown

The purpose of this repository is not only to present final results.

It is also intended to make the technical direction understandable and allow
other developers to follow the evolution of the project.

Constructive technical discussion and suggestions are welcome.
