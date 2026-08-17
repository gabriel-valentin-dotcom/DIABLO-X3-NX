# INTERACT

> **Status:** VERIFIED BASIC FUNCTIONS / ACTIVE DEVELOPMENT

INTERACT is the on-demand voice-interaction mode for short, controlled robot actions.

## Current design

- Voice runtime is started only when requested.
- The voice stack is not intended to consume robot resources continuously at boot.
- Verified basic safe intents include `STOP`, `STAND_UP` and `SIT_DOWN`.
- Additional short-motion intents are under development and diagnostics.
- Continuous free-driving by voice is **not** the design goal.

## Safety principle

Voice commands must not bypass robot-state and safety gating.

## Media

**Planned.** Interaction videos will be added when time allows.
