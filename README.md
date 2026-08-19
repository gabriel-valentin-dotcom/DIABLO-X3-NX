# DIABLO X3-NX

**Independent real-hardware ROS 2 robotics development project by GVM**

> 🚧 **EARLY PUBLIC PREVIEW — WORK IN PROGRESS**  
> DIABLO X3-NX is intentionally documented while it is being developed. Architecture, interfaces, operating modes and implementation details may change as the real robot evolves.

DIABLO X3-NX extends the Direct Drive Technology DIABLO two-wheel robot platform with a D-Robotics RDK X3, an NVIDIA Jetson Xavier NX, ROS 2, LiDAR, depth vision, interaction and layered safety logic.

This repository is intended to become the **technical history of the project**: idea, hardware, architecture, user interface, ROS 2 structure, operating modes, verified tests, design decisions, development changes, real source snapshots and later real-robot media.

**Current principle:** only functions and capabilities that have been verified on the real robot are presented as working features.

## Explore the project

- [Project overview](docs/PROJECT_OVERVIEW.md)
- [System architecture](docs/ARCHITECTURE.md)
- [Hardware](docs/HARDWARE.md)
- [Safety](docs/SAFETY.md)
- [Operating modes](docs/modes/)
- [ROS 2 architecture and topics](docs/ros2/OVERVIEW.md)
- [ROS 2 source area](ros2/README.md)
- [Real NX development source snapshot](ros2/development_workspace/README.md)
- [Current development status](docs/development/CURRENT_STATUS.md)
- [Design decisions](docs/development/DESIGN_DECISIONS.md)
- [Human-AI development workflow](docs/development/HUMAN_AI_WORKFLOW.md)
- [Validation and release readiness](docs/validation/README.md)
- [Known limitations](docs/validation/KNOWN_LIMITATIONS.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [First public project preview](docs/PUBLIC_PREVIEW.md)

## Development source

Real code from the active NX `diablo_ws/src` workspace is now being published progressively under [`ros2/development_workspace/`](ros2/development_workspace/).

The first source batch contains complete project-specific ROS 2 packages for NX bringup, safety and UWB/tracker integration. Additional active packages will follow after publication review.

The public source is intended to show the **real architecture and implementation direction** while making it clear that `main` is not yet a stable plug-and-play release.

## Current X3 touch UI

The first current UI presentation image is available in [`media/images/ui/`](media/images/ui/).

More photos, UI images and real-robot demonstration videos will be added progressively when time allows.

## Community

Questions, technical discussion, ideas and suggestions are welcome through **GitHub Discussions**. The project is open for observation and discussion while remaining under active development.

External feedback is especially useful as the project moves from isolated verified functions toward repeatable full-system real-world validation.

---

**Project creator & engineering:** GVM  
**AI-assisted development:** ChatGPT and Codex by OpenAI

Technology names identify tools and platforms used by the project and do not imply sponsorship, endorsement or partnership.
