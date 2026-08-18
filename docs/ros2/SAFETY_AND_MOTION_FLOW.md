# Safety and Motion Flow

> ⚠️ **ACTIVE SAFETY DEVELOPMENT**
>
> This document explains the architecture concept.
>
> It is not a certification document and does not describe DIABLO X3-NX as a
> safety-certified autonomous system.

## Design principle

Higher-level behavior should not have unrestricted direct ownership of the
robot motors.

A movement decision passes through several layers.

## Simplified motion flow

```text
FOLLOW / AUTO / INTERACT / other behavior
                   |
                   v
          behavioral decision
                   |
                   v
           safety conditions
                   |
             allowed?
              /    \
            no      yes
            |        |
            v        v
     HOLD_NO_MOVE   motion request
                       |
                       v
             /diablo_motion_request
                       |
                       v
              X3 motion bridge
                       |
                       v
               /diablo/MotionCmd
                       |
                       v
                DIABLO controller
```

## Safety information

Different subsystems contribute information to movement permission.

Examples include:

- LiDAR obstacle state
- vision depth
- target state
- operating mode
- FOLLOW permission
- AUTO permission
- robot state
- movement timeout
- motor-stall detection

## LiDAR safety

The LiDAR layer evaluates different regions around the robot.

The current baseline uses approximately:

- stop distance: 0.30 m
- release distance: 0.38 m

The difference between stop and release distance provides hysteresis.

These values are development parameters and may change after further
real-robot testing.

## Vision safety

Depth information from the RealSense camera can add an additional forward
movement constraint.

Vision is not intended to silently replace the LiDAR safety layer.

The sensors provide complementary information.

## FOLLOW safety

FOLLOW movement requires more than just detecting a person.

Typical conditions include:

- FOLLOW active
- movement allowed
- usable target
- acceptable target depth
- LiDAR safe
- vision safe
- valid robot state

If required conditions are not met, movement should not continue.

## Motor-stall protection

A separate protection concept observes situations where:

- movement is commanded
- wheel movement remains near zero
- motor load is high
- an obstacle condition is present

The intended response is a controlled hold rather than continued force.

## HOLD_NO_MOVE

`HOLD_NO_MOVE` is an important project-level safety command.

It is used when the system should explicitly remain stationary instead of
continuing a previous movement request.

## Development philosophy

Safety behavior is verified on the physical robot wherever practical.

A ROS 2 message reaching a node does not by itself prove that the real robot
behaves correctly.

For DIABLO X3-NX:

**software evidence + runtime evidence + real-robot behavior = verification**

## Current status

The safety architecture is operational but continues to evolve as additional
modes and hardware are integrated.
