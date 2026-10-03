# DIABLO_Brain — Experimental Architecture V0.1

> **Status:** EXPERIMENTAL / RESEARCH  
> **Implementation:** Work in Progress  
> **Project:** DIABLO X3-NX

DIABLO_Brain is the experimental high-level intelligence architecture for DIABLO.

The goal is not to place a generic chatbot next to the robot. The goal is to give DIABLO a persistent identity, personality, memory, self-model, perception and self-diagnostics layer that can use the robot's real state and sensors.

**Core principle:** DIABLO remains DIABLO. External AI systems may help DIABLO, but they are not DIABLO's identity.

## Design status

| Component | Version | Status |
|---|---:|---|
| Identity | V0.1 | Defined |
| Personality | V0.1 | Defined |
| Memory | V0.1 | Defined |
| Self Model | V0.1 | Defined |
| Perception | V0.1 | Defined |
| Diagnostics | V0.1 | Defined |
| INTERACT | V0.1 | Next design step |

## Implementation status

The documents in this directory describe the current design direction. They **do not imply that all described capabilities are implemented on the physical robot**.

- DIABLO_Brain runtime: not implemented
- Persistent Brain memory: not implemented
- OpenAI API integration: not implemented
- Brain self-diagnostics: not implemented
- Codex integration: not implemented
- Person recognition: not implemented

Existing DIABLO functions such as FOLLOW, TRACK, camera/vision, LiDAR safety, BMS and AUTO remain separate from this experimental Brain design.

## Architecture

```text
IDENTITY       Who am I?
PERSONALITY    How do I behave?
MEMORY         What do I remember?
SELF MODEL     What belongs to me and what can I do?
PERCEPTION     What do I perceive right now?
DIAGNOSTICS    How do I investigate my own problems?
INTERACT       How do people naturally communicate with me?   [next]
```

INTERACT is intended to become the personal AI/conversation interface for Brain. AUTO remains a separate autonomous physical operating mode.

## Safety boundary

DIABLO_Brain must not bypass the existing motion safety and permission layers. Perception, reasoning or an external AI response does not directly authorize motor movement. Safety remains independent of personality, memory and external AI availability.

## Documents

- [Identity V0.1](IDENTITY_V0.1.md)
- [Personality V0.1](PERSONALITY_V0.1.md)
- [Memory V0.1](MEMORY_V0.1.md)
- [Self Model V0.1](SELF_MODEL_V0.1.md)
- [Perception V0.1](PERCEPTION_V0.1.md)
- [Diagnostics V0.1](DIAGNOSTICS_V0.1.md)

## Development note

This architecture is intentionally being defined before implementation. Components may change during experiments and validation on the real DIABLO robot.
