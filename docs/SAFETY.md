# Safety Architecture

> **Status:** VERIFIED BASELINE / ACTIVE DEVELOPMENT

Safety is treated as an **architecture layer**, not as a single emergency button.

Motion commands are evaluated against current robot state, sensor information and mode permissions before they are allowed to reach the robot.

## Current safety concepts

- LiDAR safety zones can block movement when obstacles enter protected areas.
- Release hysteresis helps prevent rapid stop/release oscillation.
- Vision depth can block forward motion when the center path is too close.
- FOLLOW and autonomous behavior require explicit permission states.
- `HOLD_NO_MOVE` is used as the safety hold command when movement must stop.
- Motor-stall protection can detect commanded motion without wheel movement under high load and force a hold.

## Current LiDAR baseline

The current verified baseline uses approximately:

- **stop:** 0.30 m
- **release:** 0.38 m

These values may evolve with continued real-robot testing.

## Safety publication rule

Public documentation describes the safety concepts and verified behavior. It does not expose credentials, private deployment details or unnecessary machine-specific configuration.
