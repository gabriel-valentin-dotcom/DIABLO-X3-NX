# DIABLO_BRAIN_DIAGNOSTICS_V0.1 — BASELINE

> **Status:** Experimental design baseline  
> Diagnosis is separated from repair. The default diagnostic path is read-only.

## Core principle

DIABLO should be able to investigate questions about his own technical state using real current system evidence, relevant perception and confirmed memory rather than producing generic AI answers.

```text
QUESTION / EVENT
      ↓
SELF MODEL
      ↓
CURRENT STATE
      ↓
PERCEPTION
      ↓
DIAGNOSTICS
      ↓
RELEVANT MEMORY
      ↓
CAUSE CONFIRMED?
   ├── yes → explain
   └── no  → deeper read-only diagnosis
                    ↓
               CODEX_REQUEST
               when necessary
```

## Baseline principles

1. DIABLO can investigate his own technical state using real data.
2. Natural questions such as "Diablo, do you have a problem?" can trigger self-diagnosis without requiring ROS commands.
3. Targeted questions should primarily inspect the relevant subsystem rather than indiscriminately checking everything.
4. A general health question may trigger a defined system health check.
5. Current state is checked before relying on historical memory.
6. Memory may then help interpret current symptoms.
7. Symptoms and root causes remain distinct.
8. DIABLO does not state a root cause as fact without sufficient evidence.
9. UNKNOWN is a valid diagnostic result.
10. Diagnostic evidence must be fresh enough for the conclusion being made.
11. LiDAR diagnosis may inspect scan activity/freshness, relevant service/node state and safety state.
12. Camera and vision processing may be diagnosed separately.
13. UWB diagnosis may inspect stream activity, freshness and plausible range state.
14. Battery/BMS diagnosis may inspect reachability, SOC, voltage, cell information, temperature and available fault/protection state.
15. Relevant X3 services and states may be part of diagnosis.
16. Relevant Jetson NX services, processes and resources may be part of diagnosis.
17. ROS 2 nodes, topics, services, publisher/subscriber activity and data freshness may provide diagnostic evidence.
18. Operating modes matter: a disabled sensor path may be intentionally disabled rather than faulty.
19. Permission may legitimately block movement and must not automatically be interpreted as a defect.
20. A safety block is a valid safety state, not automatically a system failure.
21. Where evidence allows, Brain distinguishes movement requested, permitted, forwarded and actually executed.
22. DIABLO understands important subsystem dependencies so upstream failures can be distinguished from downstream symptoms.
23. Brain attempts to distinguish probable root cause from secondary effects.
24. Multiple faults may exist simultaneously.
25. Diagnostic severity may be normalized as OK, INFO, WARNING, ERROR, CRITICAL or UNKNOWN.
26. Safety-critical problems receive highest attention.
27. Short transient packet loss does not immediately become a hardware-failure claim; expected rates and time windows matter.
28. Persistent faults are treated differently from isolated transient events.
29. DIABLO recognizes recovery as well as failure.
30. Duration and recurrence may be relevant diagnostic evidence.
31. Current symptoms may be compared with confirmed historical incidents.
32. Similar symptoms do not prove the same historical cause.
33. A previously successful solution may be presented as a relevant lead, not automatic proof.
34. Technical evidence may include states, measurements, logs and relevant events.
35. Gabriel normally receives a natural-language summary rather than raw logs.
36. Technical detail can be provided when requested.
37. DIABLO may proactively report an important new problem.
38. Minor transient/self-healing events should not create constant interruptions.
39. Investigation is initially read-only. Diagnosis does not automatically authorize repair.
40. Brain first uses its own available local state and diagnostic information.
41. If that is insufficient, DIABLO may recognize the need for deeper technical investigation.
42. Brain may create a structured CODEX_REQUEST containing symptom, context, relevant evidence and checks already performed.
43. Codex should receive the relevant technical context so it does not need to start from zero.
44. A Codex diagnosis is technical analysis, not automatically proven truth.
45. The first Codex step for an unknown fault should normally be read-only investigation rather than immediate code modification.
46. A proposed repair is a separate action from diagnosis.
47. Motion, safety, permission, BMS, motor-controller and other critical areas must not be modified solely from an unverified Brain/Codex hypothesis.
48. Where authorization is required, DIABLO asks Gabriel clearly before the change is executed.
49. Emergency STOP remains independent and must never wait for Brain, external AI, Codex or confirmation.
50. After the cause and successful solution are confirmed, the incident may become technical memory.

## Diagnostic escalation levels

```text
LEVEL 0   Observe
    ↓
LEVEL 1   Brain self-check
    ↓
LEVEL 2   Local read-only diagnosis
    ↓
LEVEL 3   Codex read-only diagnosis
    ↓
          Cause identified
    ↓
LEVEL 4   Repair proposal
    ↓
          Authorization where required
    ↓
LEVEL 5   Controlled change
    ↓
          Verification
    ↓
          Technical memory
```

## Example

If `/scan` stops updating, DIABLO should not immediately say "My LiDAR is broken."

A truthful progression is:

1. "I am not receiving current LiDAR data."
2. Inspect freshness and relevant service/node/safety state.
3. If the stream remains absent while the service is running: "My LiDAR data stream has stopped. The service is still running, so I do not yet know the cause."
4. Relevant previous incidents may be recalled as leads without assuming an identical cause.
5. If local evidence is insufficient, create a deeper read-only technical investigation request.

## Safety boundary

Diagnosis may explain safety behavior but never bypass it. Emergency stopping remains independent of the Brain and external AI path.
