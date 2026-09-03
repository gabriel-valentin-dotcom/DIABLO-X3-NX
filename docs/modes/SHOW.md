# SHOW

> **Status:** ACTIVE DEVELOPMENT

SHOW is the controlled demonstration area of the X3 touch UI.

The goal is to provide selected visible robot demonstrations without mixing them with autonomous background behavior.

## Current direction

- Manual demonstration functions are grouped under one UI area.
- Current presentation targets include MOONWALK, JUMP, SPLIT and DANCE-style actions.
- SHOW remains intentionally separate from safety-critical autonomous logic.
- Demonstration actions must still pass the relevant robot-state and safety gates before motion is allowed.

## Custom Moonwalker V1

A custom Moonwalker V1 sequence has been implemented using normal motion control rather than manufacturer automation mode.

The sequence is internally gated by fresh body state, standing state, controller authority and zero error/warning state, and it can be aborted by STOP/safety HOLD paths.

**Physical validation is not complete.** The first live trigger attempt reached the NX command/motion-request path but timed out waiting for controller confirmation before the X3 custom sequence was confirmed active. Therefore no successful physical Moonwalker choreography is claimed yet.

## Media

SHOW UI and selected real-robot demonstrations will be published as their physical validation is completed.
