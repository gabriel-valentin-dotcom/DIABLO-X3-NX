# INTERACT

> **Status:** VERIFIED REAL-HARDWARE FUNCTIONS / ACTIVE DEVELOPMENT

INTERACT is the on-demand voice-interaction mode for short, controlled robot actions.

## Current design

- Voice runtime is started only when requested.
- The voice stack is not intended to consume robot resources continuously at boot.
- Verified basic safe intents include `STOP`, `STAND_UP` and `SIT_DOWN`.
- Short controlled motion intents are part of the active real-hardware development path.
- Continuous free-driving by voice is **not** the design goal.
- Pose and short-motion requests are gated by the current INTERACT state; safety/STOP behavior remains available.

## Safety principle

Voice commands must not bypass robot-state and safety gating. INTERACT is intentionally disabled before selected SHOW/custom-motion tests so late or stale voice pose requests cannot interfere with the test state.

## Media

▶️ **[DIABLO X3-NX — INTERACT Voice Command Test | Real Robot](https://www.youtube.com/watch?v=1tYXHSDjvRE)**

This video shows the INTERACT voice-command path on the physical DIABLO X3-NX robot during active development.
