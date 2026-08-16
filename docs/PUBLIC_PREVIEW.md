# DIABLO X3-NX - Public Preview

**Independent ROS 2 robotics development project by GVM**

DIABLO X3-NX extends the Direct Drive Technology DIABLO two-wheel robot platform with a D-Robotics RDK X3 and an NVIDIA Jetson Xavier NX.

The project combines real-hardware robotics, perception, interaction and safety functions in a compact X3-NX architecture.

> Status: Active development. Public documentation will describe only functions that have been verified on the real robot.

## Project direction

DIABLO X3-NX is being developed as a real robotics platform rather than a software-only demonstration. The goal is to combine edge control, ROS 2 high-level logic, perception, safety and interaction while keeping the system understandable and practical.

## Core platform

- **Robot base:** Direct Drive Technology DIABLO
- **Edge controller:** D-Robotics RDK X3
- **High-level compute:** NVIDIA Jetson Xavier NX 16GB
- **LiDAR:** RPLIDAR C1
- **Depth / RGB camera:** Intel RealSense D435
- **Audio:** ReSpeaker XVF3800
- **UWB:** Ai-Thinker BU04
- **Middleware:** ROS 2

## Development areas

### FOLLOW
Person-following behavior with controlled motion and safety gating.

### LiDAR safety
Obstacle-zone detection used to block or release robot motion according to the current safety state.

### Vision
RealSense-based target and depth perception used by higher-level robot logic.

### INTERACT
On-demand voice interaction for short, controlled robot actions.

### X3 touch UI
Direct robot-side status and mode control on the RDK X3 display.

## High-level architecture

```text
Sensors <-> RDK X3 <-> Jetson Xavier NX <-> ROS 2 decision and safety layers
```

The public documentation will explain the functional architecture while avoiding credentials, private network information, machine-specific access details and unnecessary deployment secrets.

## Planned public demonstrations

- FOLLOW demo - approximately 30-60 seconds
- LiDAR safety demo - approximately 30-45 seconds
- Vision demo - approximately 30-60 seconds
- INTERACT demo - approximately 30-60 seconds
- X3 touch UI demo - approximately 20-30 seconds
- DIABLO X3-NX overview - approximately 2-3 minutes

## Publication principles

Only current and verified project information should become public. Obsolete experiments, backup history, credentials, private data, unreviewed third-party source code and internal production configuration remain outside the public package.

Selected software components may be published later after licensing, security and technical review.

## Attribution

**Project creator & engineering:** GVM  
**AI-assisted development:** ChatGPT and Codex by OpenAI  
**Robot platform:** Direct Drive Technology DIABLO  
**Core compute platforms:** D-Robotics RDK X3 and NVIDIA Jetson Xavier NX

The names above identify technologies and tools used by the project. They do not imply official sponsorship, endorsement or partnership unless such a relationship is confirmed separately.

## Current status

DIABLO X3-NX is in active development. Photos, architecture diagrams and short real-robot demonstration videos will be added as the public presentation is prepared.

---

**GVM | DIABLO X3-NX**
