# Design Decisions

> **Status:** LIVING DOCUMENT

This page records important design choices so that future readers can understand not only **what** DIABLO does, but **why** the project is structured this way.

## Two-computer architecture

Keep robot-near control on the D-Robotics RDK X3 while using the Jetson Xavier NX for heavier perception and higher-level behavior.

## On-demand voice runtime

Do not keep the full voice stack running at boot. Start it only when INTERACT is requested.

## Safety ownership

Use clearly owned safety topics and explicit permission states to reduce ambiguous or duplicated control authority.

## Minimal-node preference

Extend existing services and nodes when practical instead of creating unnecessary permanent processes.

## Real-robot verification

A software path is not considered complete only because messages or code look correct. Physical behavior is verified on the real robot when motion is involved.

## Public documentation first

Explain architecture, modes and interfaces before releasing large amounts of source code. This gives engineers direction while reducing the risk of publishing obsolete, private or third-party material without review.

## Changes are expected

A design decision can be replaced when testing proves a better approach. When that happens, the public documentation should explain the new direction instead of pretending the older approach never existed.
