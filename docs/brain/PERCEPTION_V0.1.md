# DIABLO_BRAIN_PERCEPTION_V0.1 — BASELINE

> Experimental design baseline. No perception result alone authorizes physical movement.

## Core principle

Brain should not reason directly over an uncontrolled mass of raw sensor values. Real sensor information is normalized into understandable, timestamped perceptions while preserving provenance and uncertainty.

```text
RAW SENSOR DATA
      ↓
NORMALIZED PERCEPTION
      ↓
CONTEXT / SENSOR FUSION
      ↓
ATTENTION / EVENTS
      ↓
BRAIN
```

## Principles

1. DIABLO has a common perception model combining information from different sensors.
2. Perceptions retain their source sensor/data source.
3. Perceptions carry timestamps.
4. Perceptions may carry confidence/uncertainty.
5. Stale sensor information is not treated as current perception.
6. UNKNOWN is valid.
7. Missing data is not automatically a fault.
8. Different sensors may disagree about the same situation.
9. Brain should detect meaningful disagreement rather than silently hiding it.
10. DIABLO should prefer explicit uncertainty to invented certainty.
11. RealSense/Vision may provide person/object detection, depth and relative position.
12. Person detection does not imply person identity.
13. Visual identity recognition must preserve confidence and uncertainty.
14. DIABLO may express uncertain identification naturally rather than claiming certainty.
15. UWB is a distance source, not a visual person detector.
16. UWB and vision may support each other when their observations are compatible.
17. A UWB range alone must not be verbalized as "I see Gabriel."
18. A useful distinction is: a known tag may be nearby even when the associated person is not visually perceived.
19. Microphone input, speech detection, speech-to-text, speaker recognition and semantic understanding are separate stages.
20. Speaker recognition alone does not grant privileged authorization.
21. LiDAR contributes spatial obstacle/range perception around DIABLO.
22. Spatial perception may be normalized into regions such as front, front-left, front-right, left, right and back.
23. Brain may understand states such as CLEAR, BLOCKED or UNKNOWN where supported by real evidence.
24. The existing safety system remains authoritative for movement decisions.
25. Internal state such as battery/BMS and subsystem health is also part of DIABLO's perception of himself.
26. Sensor fusion may combine vision, UWB, audio and memory to form a stronger contextual hypothesis.
27. Fused hypotheses still retain uncertainty and their underlying evidence.
28. Perception does not automatically become long-term memory.
29. Brain evaluates whether an event is important enough to become an episodic memory.
30. Brain has an attention concept so it can focus on a relevant person, event or technical problem without verbalizing everything it senses.
31. Attention may be empty; DIABLO does not need to continuously seek stimulation.
32. Changes are important perceptions: person appeared/left, range changed, sensor stream stopped/recovered, battery behavior changed, safety state changed.
33. Meaningful changes can be converted into normalized events.
34. Example events include PERSON_APPEARED, PERSON_LEFT, OBSTACLE_APPEARED, BATTERY_LOW, UWB_LOST, LIDAR_RECOVERED and SAFETY_STOP.
35. Important events may attract Brain attention and allow appropriate proactive communication.
36. Proactive communication should be relevance-controlled to avoid constant interruptions.
37. Sensor fusion must not turn correlation into certainty without sufficient evidence.
38. DIABLO should be able to explain the evidence behind important perception-based conclusions when useful.
39. Current perception and remembered information remain distinguishable.
40. Perception is stateful enough to understand meaningful transitions over time.
41. A sensor's technical availability and the semantic content it reports are separate concepts.
42. Perception quality may degrade gracefully when one sensor is unavailable.
43. Brain may use redundant information when available but must not fabricate missing measurements.
44. Identity estimation may later combine vision, UWB/tag context, speaker recognition and memory, while keeping authorization separate.
45. Environmental perception and self-perception share the same truthfulness rules: source, freshness, confidence and UNKNOWN.
46. Perception may inform self-diagnosis but is not itself proof of a root cause.
47. Sensor errors and environmental observations must be distinguishable where possible.
48. Safety-related perception should be available to Brain for explanation without allowing Brain to bypass the safety layer.
49. External AI receives only selected normalized perception/context needed for the task, rather than uncontrolled raw streams by default.
50. **Perception is separate from action.** Perceiving, understanding, remembering or speaking about something does not automatically create a motor command.

## Example fused situation

```text
Vision:      person detected, center, ~1.8 m
UWB:         known Gabriel tag, ~1.76 m
Audio:       speech detected
Speaker:     likely Gabriel
Memory:      Gabriel is a known person

Result:
PERSON_PRESENT = true
LIKELY_IDENTITY = Gabriel
CONFIDENCE = high
ATTENTION = Gabriel
```

Even this fused result does not by itself grant motion or administrative authorization.
