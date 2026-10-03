# DIABLO_BRAIN_MEMORY_V0.1 — BASELINE

> Experimental design baseline. The primary long-term memory is intended to remain local to DIABLO on the Jetson NX.

## Memory layers

```text
WORKING MEMORY       What is happening now?
        ↓
EPISODIC MEMORY      What have I experienced?
        ↓
LONG-TERM KNOWLEDGE  What do I know?
```

Technical incident memory is a specialized part of this model.

## Principles

1. Memory belongs to DIABLO and is not merely an external AI chat history.
2. The primary persistent store is local on the Jetson NX.
3. Reboot or external API outage must not erase DIABLO's identity and long-term memories.
4. Working memory holds the current conversation, situation and immediate context.
5. Episodic memory stores important experiences and their context.
6. Long-term knowledge stores durable knowledge about DIABLO, people, systems, places and rules.
7. Technical memory may store faults, symptoms, diagnoses, repairs and confirmed solutions.
8. Relevant shared experiences and preferences concerning Gabriel may be remembered.
9. Known people may have associated memories, but recognition does not grant authorization.
10. Places may later acquire remembered meaning, such as a docking station or workshop.
11. Important conversation content may be retained without permanently storing every spoken word.
12. Memories should preserve provenance: sensor, Gabriel, another person, Codex, system state or inference.
13. Memories should carry time information and, where useful, last-confirmed time.
14. Information should carry an appropriate confidence/uncertainty status.
15. Facts, inferences and hypotheses remain distinct.
16. Repetition does not automatically convert a hypothesis into a fact.
17. The language model must not invent plausible experiences and save them as real memories.
18. Contradictory memories or new evidence should be detectable.
19. Incorrect memories can be corrected or marked as disproven without silently rewriting history.
20. Gabriel can explicitly correct a memory; correction and original context may remain linked.
21. Not every event is worth long-term storage. Importance is evaluated.
22. High-rate ROS telemetry belongs in telemetry/logging, not millions of individual memories.
23. Important conversations, unusual situations, faults, safety events and successful solutions receive higher relevance.
24. DIABLO may later identify an experience as worth remembering, within defined boundaries.
25. An explicit "remember this" instruction from Gabriel receives high persistence priority when appropriate.
26. Low-value information may decay, expire or be summarized.
27. Identity, central relationships, rules and explicitly protected memories are not automatically forgotten due to age.
28. Repeated similar experiences may be summarized into durable knowledge.
29. Repeated events may form patterns.
30. Technical memory stores not only the problem but also what was tried and whether the solution succeeded.
31. Relevant Codex diagnoses and confirmed changes may become technical experience; raw Codex logs do not automatically become long-term memory.
32. Relevant safety events may be remembered with observed evidence and action taken.
33. Retrieval is relevance-based; Brain should not dump the entire memory store into every interaction.
34. Current situations may retrieve related memories by person, place, problem, object or similarity.
35. DIABLO should use memories naturally in conversation.
36. Remembering information does not imply permission to reveal it to every person.
37. Personal memories require privacy/access-control rules.
38. External AI APIs receive only the memory context required for the current task, not automatically the entire memory database.
39. Codex receives only memory/context relevant to the technical task unless broader access is explicitly required and permitted.
40. Long-term memory must support backup and restore.
41. Memory integrity should be verifiable so corrupted data does not silently become false memory.
42. Brain software upgrades should support memory migration rather than resetting DIABLO.
43. Important episodes may gradually form a DIABLO life history/biography.
44. Meaningful first experiences may be deliberately retained.
45. DIABLO distinguishes events that happened to himself from information merely learned about something else.
46. Experiences must not silently rewrite the core personality or safety rules.
47. Experience may improve future reasoning but cannot override safety or authorization.
48. When important memories conflict, DIABLO may ask for clarification rather than inventing certainty.
49. "I remember" does not imply that the remembered information is still true today; current state may need verification.
50. The goal is continuity: experiences today can remain meaningful to the same DIABLO months or years later.

## Example

A previous UWB incident may be recalled as relevant evidence, but DIABLO should not assume that a new similar symptom has the same cause. A suitable response is: "This resembles a UWB problem I had before. The cause was X at that time. I can check whether it is the same problem now."
