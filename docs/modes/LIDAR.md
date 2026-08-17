# LIDAR

> **Status:** VERIFIED / ACTIVE DEVELOPMENT

The RPLIDAR C1 provides scan data used by DIABLO X3-NX for obstacle awareness and safety gating.

## Current concepts

- `/scan` provides LiDAR scan data.
- Filtered LiDAR safety state is used by higher-level motion logic.
- Safety sectors cover front, diagonal, side and rear areas.
- Stop/release hysteresis is used to avoid unstable boundary behavior.

## Ownership

The project separates raw sensor publication from the authoritative filtered safety state so that multiple parts of the system do not compete for safety ownership.

## Media

**Planned.** LiDAR-zone visualizations and real-robot safety demonstrations will be added later.
