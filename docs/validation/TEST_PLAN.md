# Real-World Test Plan

> 🚧 **ACTIVE DEVELOPMENT — TEST MATRIX EVOLVING**

The purpose of this test plan is to define repeatable real-robot validation instead of relying only on isolated successful actions.

## Planned validation areas

### Boot and recovery

- cold boot
- ROS 2 graph availability
- controller communication
- sensor availability
- defined behavior after component restart or reconnect

### Motion and safety

- stand / sit transitions
- controlled forward and backward movement
- controlled turning
- obstacle stop behavior
- release hysteresis
- explicit hold behavior
- motor-stall protection

### FOLLOW

- target acquisition
- target loss
- center / left / right response
- distance control
- obstacle interaction
- repeated start/stop cycles

### Vision and LiDAR

- LiDAR sector behavior
- depth-based forward blocking
- conflicting or missing sensor information
- sensor recovery after runtime interruption

### INTERACT

- on-demand voice runtime
- basic intents
- safety gating
- repeated enable/disable cycles

### Power

- runtime under realistic load
- behavior near low-power limits
- stand-up and motion reserve
- future Battery V2 validation

## Evidence to collect

Where practical, tests should record:

- software version / commit
- hardware configuration
- test duration
- number of repetitions
- pass / fail result
- observed limitations
- relevant ROS 2/runtime evidence
- real-robot behavior

## Current status

This document defines the direction of validation. It is not yet a completed certification or release test report.
