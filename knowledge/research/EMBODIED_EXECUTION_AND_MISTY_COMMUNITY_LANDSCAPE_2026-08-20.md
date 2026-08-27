# Embodied Execution and Misty II Community Landscape

Date: 2026-08-20  
Revised: 2026-08-27  
Status: Research Note — not implementation authorization, robot-connection
authorization, G28 entry, or evidence of physical behavior.  
Evidence Classification: claim-level labels below  
Cross-Reference: `knowledge/strategy/PROGRAM_CHARTER.md`,
`knowledge/strategy/SPRINT_ROADMAP_G0_G30.md` (G27/G28),
`knowledge/research/G27_CAPABILITY_SAFETY_MODEL_2026-08-20.md`

---

## 1. Adopted Architectural Boundary

**REPOSITORY EVIDENCE.** The active G26/G27 model uses one immutable,
step-free native AAuth mission to express approved intent and scope. Session,
participant, evidence, and lifecycle state remain outside that mission in
separate session state and append-only records. Governance evaluates each
proposed action against the mission and the other runtime inputs; the mission
does not itself authorize execution. See D-013, D-019, D-021, and
`knowledge/research/G27_SESSION_GRANT_PERSON_SERVER_CONTRACT_2026-08-18.md`.

**REPOSITORY EVIDENCE.** SOGA produces an execution-time governance
determination. It does not own the independent physical safety halt. The local
physical enforcement and safety boundary must remain effective without SOGA,
the network, an adapter process, or a late governance result. See
`knowledge/research/G27_CAPABILITY_SAFETY_MODEL_2026-08-20.md` and
`knowledge/research/G27_AB_ISOLATION_NETWORK_REQUIREMENTS_2026-08-20.md`.

## 2. Product and Stewardship Observations

**OBSERVED — PRIMARY SOURCE.** Furhat Robotics states that it acquired Misty
Robotics and subsequently explored Misty's use across research and innovation.
This establishes the stewardship relationship but does not establish the size,
activity, or composition of a present Misty developer community.
[Furhat Conference on Social Robotics, Spring 2022](https://www.furhatrobotics.com/furhat-conference-on-social-robotics-spring-22).

**OBSERVED — PRIMARY SOURCE.** The `MistyCommunity` GitHub organization hosts
the preserved Misty documentation and REST API examples. The documentation
describes commands delivered over local Wi-Fi and warns that the robot's own
hazard detection can still fail in some conditions. These sources support API
and platform inspection; they do not authorize connecting either SOGA research
robot.
[MistyCommunity organization](https://github.com/MistyCommunity),
[Misty II documentation](https://github.com/MistyCommunity/Documentation/blob/master/src/content/misty-ii/robot/misty-ii.md),
[REST API examples](https://github.com/MistyCommunity/REST-API).

## 3. Misty II Product Tiers and SOGA Platform Roles

**OBSERVED — PRIMARY SOURCE.** Preserved Misty documentation defines three
product tiers, not two:

| Capability | Basic | Standard | Enhanced |
| :--- | :--- | :--- | :--- |
| Depth hardware | No Structure Core depth sensor | Structure Core depth sensor | Structure Core depth sensor |
| Depth-dependent functions | Misty depth-dependent APIs, auto-docking, SLAM, and 3D imaging are unavailable | Depth-dependent APIs, auto-docking, SLAM, and 3D imaging are supported | Standard capabilities plus expanded mapping capacity |
| Android processor | Open-Q 820 | Open-Q 820 | Open-Q 820Pro |
| Mapping statement | No supported depth-based mapping | Approximately 5 minutes and 800–1000 square feet per map, subject to environmental variables | Approximately 10 minutes and 1600–2000 square feet per map, subject to environmental variables |
| Included charging equipment | Wired adapter; wireless pad sold separately | Wireless pad; wired adapter sold separately | Wireless pad; wired adapter sold separately |
| Shared interfaces | JavaScript SDK, beta .NET SDK, REST API, web tools; depth-dependent interfaces do not function on Basic | Same listed interfaces | Same listed interfaces |

Source: [Misty II specifications and model comparison](https://github.com/MistyCommunity/Documentation/blob/master/src/content/misty-ii/robot/misty-ii.md#misty-ii-specs).

**REPOSITORY EVIDENCE / FUTURE APPLICATION.** D-006 assigns Misty A (Basic)
as the lower-capability comparative control and Misty B (Enhanced) as the
higher-capability platform. That assignment is a planned SOGA experimental
role. It does not state that either platform is connected, powered, mapped, or
currently used by the G27 implementation.

## 4. Identified Community Software Examples

**OBSERVED — PRIMARY REPOSITORIES.** At least two third-party projects expose
Misty through ROS-related software: `R4Robotics/Misty-ROS` describes itself as
a ROS bridge, and `NSF-iSAT/misty_wrapper` provides ROS bindings for Misty II.
Their existence does not establish broad ROS adoption, ROS2 parity, current
maintenance, or a canonical topic model.
[R4Robotics/Misty-ROS](https://github.com/R4Robotics/Misty-ROS),
[NSF-iSAT/misty_wrapper](https://github.com/NSF-iSAT/misty_wrapper).

**OBSERVED — SINGLE PROJECT, NOT ECOSYSTEM EVIDENCE.** One public repository
describes a Misty II system using MediaPipe, Whisper, GPT-4o, a deterministic
executor, and hardware-free simulation tests. This is evidence of one concrete
foundation-model integration pattern, not evidence that the Misty community as
a whole has adopted that architecture.
[jyp-studio/misty-llm-embodied-agent](https://github.com/jyp-studio/misty-llm-embodied-agent).

**ABSENCE / FUTURE RESEARCH.** This review did not establish a primary-source
Misty implementation using MCP. MCP-to-Misty integration therefore remains a
future interoperability question, not an observed platform or community fact.
No Misty-specific voice-latency benchmark is claimed; latency remains to be
measured under G28 if G28 is authorized.

Search basis recorded 2026-08-27: `"Misty II" MCP robot`,
`site:github.com/MistyCommunity MCP`, and
`site:github.com "Misty II" "Model Context Protocol"`, followed by inspection
of the MistyCommunity organization, preserved Documentation, and REST-API
repository. No primary-source Misty/MCP implementation was found in that
bounded search; this is not a claim of universal absence.

## 5. Governance Research Intersection

**INFERENCE.** Misty's network API, physical actuators, sensors, and
model-dependent capability differences make it a useful candidate for testing
whether the same mission and governance semantics remain valid as the execution
surface changes. The testable SOGA question is whether a requested semantic
action can be evaluated, target-bound, dispatched, interrupted, and evidenced
without relaxing the adopted authority, isolation, degradation, and safety
boundaries.

**REPOSITORY EVIDENCE.** An SOGA ALLOW does not prove that a robot acted and
does not override local safety. The G27 recording adapter therefore reports the
physical outcome as unknown. Any later robot adapter must preserve separate
records for the request, governance decision, authorization projection,
dispatch, and observed physical result, while the independent local physical
safety mechanism retains precedence.

## 6. Explicit Nonclaims and Next Research

This note does not establish:

- the current size or activity of the Misty community;
- adoption by named laboratories not individually cited here;
- a universal historical lifecycle for Misty use;
- MCP support, sub-500 ms voice latency, or any other unmeasured performance;
- that an LLM, ROS bridge, SDK, or remote service is safe to connect to Misty;
- that SOGA implements the local physical safety halt;
- that either Misty has been powered, connected, queried, or actuated; or
- that D-025, G28 entry, public demonstration, or robot execution is authorized.

Future work, only after the applicable decision and gate, may inspect candidate
adapters, measure latency and interruption behavior, test A/B isolation, and
compare governance evidence across REST, ROS, MCP, or other execution surfaces.
