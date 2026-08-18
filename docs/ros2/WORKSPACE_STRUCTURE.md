# ROS 2 Workspace Structure

> 🚧 **WORK IN PROGRESS — ACTIVE ROBOT DEVELOPMENT**
>
> This document describes the current logical structure of the DIABLO X3-NX
> ROS 2 environment.
>
> The project is being developed and tested continuously on the real robot.
> Package boundaries, nodes, topics and implementation details may change.
>
> This is an architecture overview — not yet a complete plug-and-play workspace.

## Why this page exists

DIABLO X3-NX uses two computers with different responsibilities:

- D-Robotics RDK X3
- NVIDIA Jetson Xavier NX

The goal of this page is to help ROS 2 developers understand where different
robot functions live and how the project is organized.

## Development workspace

The main ROS 2 development environment is referred to internally as:

`diablo_ws`

The complete private development workspace contains production code,
diagnostics, experiments, backups and temporary development material.

The public repository therefore does **not** mirror the complete workspace.

Only reviewed architecture information and selected source components are
published.

## Logical structure

Conceptually the system is divided into the following areas:

```text
DIABLO robot base
        |
        v
RDK X3
├── robot controller interface
├── motion bridge
├── robot telemetry
├── LiDAR
├── LiDAR safety
└── touch UI
        |
        | ROS 2
        v
Jetson Xavier NX
├── mode management
├── camera management
├── vision / perception
├── FOLLOW logic
├── AUTO supervision
├── safety supervision
└── INTERACT / voice runtime
```

## RDK X3 role

The RDK X3 stays close to the physical robot.

Typical responsibilities include:

- communication with the original DIABLO controller
- robot telemetry
- low-level motion command interface
- LiDAR runtime
- robot-side safety information
- X3 touch UI
- ROS 2 communication with the Jetson NX

## Jetson Xavier NX role

The Jetson NX handles higher-level and compute-intensive tasks.

Typical responsibilities include:

- camera runtime
- computer vision
- person tracking
- FOLLOW behavior
- autonomous decision logic
- safety supervision
- voice / interaction
- higher-level mode management

## Public source-code policy

Architecture and interfaces can be documented before all source code is public.

Source code is published selectively after review.

Before a source component becomes public it should be checked for:

- technical relevance
- current development status
- credentials and private information
- machine-specific data
- third-party licensing
- obsolete experiments
- real-robot verification where applicable

## Status

This structure represents the current development direction.

It is expected to evolve.
