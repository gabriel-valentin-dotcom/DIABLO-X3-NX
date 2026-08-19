# DIABLO X3-NX — ROS 2 Source Area

> 🚧 **WORK IN PROGRESS — ACTIVE ROBOT DEVELOPMENT**
>
> This area is intended for reviewed source snapshots from the real DIABLO X3-NX ROS 2 development workspace.
>
> The codebase is still evolving. Files published here may change as the robot is tested, diagnosed and extended.

## Publication model

DIABLO X3-NX is being developed as a real multi-computer ROS 2 system. The productive workspace is referred to internally as `diablo_ws`.

The long-term goal is to make the project source available openly. During active development, this repository may contain development snapshots before a stable release exists.

A development snapshot is published to show:

- real package structure
- real nodes and interfaces
- interaction between X3 and Jetson NX
- safety and permission logic
- mode implementation direction
- current engineering state

It should **not** be interpreted as a finished plug-and-play release.

## What will not be copied blindly

The public source area should exclude or separately review:

- `build/`, `install/` and `log/`
- local backups
- credentials or private data
- temporary diagnostic captures
- machine-specific secrets
- third-party/vendor code without publication rights

## Current source status

The first source area is [`examples/armed_state/`](examples/armed_state/).

Its real implementation snapshot has not yet been added. No synthetic replacement code is used.

Future reviewed snapshots may include larger parts of the real workspace so developers can understand how the components operate together.

## Stable release later

A future stable release will be explicitly tagged and documented separately from ongoing development. Until then, `main` should be read as a living development history.

The final open-source license will be selected before the first formal open-source release.
