# FOLLOW

> **Status:** VERIFIED / ACTIVE DEVELOPMENT

FOLLOW is the person-following behavior of DIABLO X3-NX. It combines target state, controlled motion and safety gating.

## Current behavior

- Explicit arm/start behavior
- Target center-lock before forward motion
- Decision damping to reduce unstable left/right switching
- Forward and turn commands gated by permission and safety state
- Real-robot forward, left and right FOLLOW behavior verified

## Design principle

FOLLOW is not allowed to ignore the safety layer. Target tracking and motion permission remain separate concepts.

## Media

**Planned.** Current UI screenshots and real-robot FOLLOW demonstrations will be added when time allows.
