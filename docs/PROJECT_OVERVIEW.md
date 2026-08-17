# Project Overview

> **Status:** WORK IN PROGRESS  
> **Last updated:** 17 August 2026

DIABLO X3-NX is an independent robotics development project focused on turning a compact two-wheel robot platform into a practical, observable and extensible real-hardware system.

The project combines robot-side control, higher-level compute, perception, safety, person following, user interaction and a touch interface.

## Project principles

- **Real robot first:** physical behavior is the final source of truth.
- **Safety before autonomy:** motion is gated and can be held immediately when required.
- **Minimal runtime:** prefer a small number of clearly owned nodes and services.
- **Verified claims only:** working features should be demonstrated on the real robot.
- **Development is visible:** changes, experiments and replaced approaches can be documented rather than hidden.
- **Human-readable architecture:** a technician should be able to understand the direction without reading the entire codebase.

## Public-project philosophy

This repository is intentionally being built while development continues. Some interfaces, parameters and implementation details will change over time.

The goal is not to present DIABLO as a finished product. The goal is to make the **idea, technical direction, current state and development history understandable**.

## Main technical areas

- Robot control and telemetry
- X3 ↔ Jetson NX ROS 2 architecture
- LiDAR safety
- Depth and RGB perception
- Person following
- Camera runtime
- Autonomous behavior experiments
- On-demand voice interaction
- X3 touch UI and demonstration modes

## Status vocabulary

- **VERIFIED** — demonstrated on the real robot.
- **IN DEVELOPMENT** — actively being developed; not presented as final.
- **EXPERIMENTAL** — exploratory and may be replaced.
- **PLANNED** — intended future work, not yet implemented.
- **DEPRECATED** — retained only for development history and no longer current.
