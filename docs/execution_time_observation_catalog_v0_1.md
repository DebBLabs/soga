# Execution-Time Observation Catalog v0.1
**Subtitle:** Candidate Evidence Inputs for Governance Normalization Research

**Status:** Research Artifact
**Date:** 2026-07-01
**Sprint:** Execution-Time Observation Catalog Sprint
**Gate 1:** APPROVED (Claude)
**Gate 2:** APPROVED WITH CONDITIONS (Gemini)

No architectural decisions are made by this document.

---

## Scope

This catalog records execution-time observations identified through
cross-disciplinary literature synthesis.

It documents observations only.

**Out of scope:**
- Classification functions
- Governance normalization algorithms
- Evidence weighting
- Runtime decision logic
- Architectural mappings
- RuntimeEnvelope modifications
- Protocol modifications
- Implementation guidance
- Mission Builder integration

---

## Related Repository Artifacts

- docs/governance_evidence_taxonomy_v0_1.md
- docs/agent_evidence_model_v0_1.md
- specifications/runtime-envelope/v0.1/runtime-envelope-specification-v0.1.md
- docs/stable_interfaces_v0_1.md
- knowledge/research/RESEARCH_OBSERVATIONS.md
- knowledge/research/METHODOLOGICAL_CONSTRAINTS.md

---

## Catalog Schema

Each observation is recorded using seven fields:

1. Observation Name
2. Originating Discipline / Platform
3. Measurement / Generation Method
4. Standardization Level [Standardized | Implementation-Specific | Research-Only]
5. Structural Coupling Dependency [Hardware-Bound | Protocol-Neutral]
6. Candidate SOGA Governance Dimension(s)
7. Authoritative Source

---

## Domain: HCI and Human Factors
*Observations 001–008 — Synthesized by Claude*

---

### Observation 001

| Field | Value |
|---|---|
| Observation Name | operator_workload |
| Originating Discipline | Human factors / HCI |
| Measurement Method | NASA-TLX subjective rating scale; secondary task performance; physiological measures (EEG, fNIRS, heart rate variability) |
| Standardization Level | Standardized — NASA-TLX is an established validated instrument |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | subject_agency_state, reachability |
| Authoritative Source | Hart and Staveland (1988); NASA-TLX manual |

---

### Observation 002

| Field | Value |
|---|---|
| Observation Name | situation_awareness_level |
| Originating Discipline | Human factors |
| Measurement Method | SAGAT (Situation Awareness Global Assessment Technique) query freezes; SART rating scale; real-time SA probes |
| Standardization Level | Standardized — SAGAT is widely validated across aviation, military, and healthcare domains |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | subject_agency_state, execution_context |
| Authoritative Source | Endsley (1995); Endsley and Garland (2000) |

---

### Observation 003

| Field | Value |
|---|---|
| Observation Name | attention_state |
| Originating Discipline | HCI / cognitive psychology |
| Measurement Method | Eye tracking dwell time; gaze direction; blink rate; response latency to attention probes |
| Standardization Level | Implementation-Specific |
| Structural Coupling Dependency | Hardware-Bound at source; Protocol-Neutral at projection boundary |
| Candidate Dimension(s) | reachability |
| Authoritative Source | Salvucci and Goldberg (2000); Iqbal and Bailey (2004) |

---

### Observation 004

| Field | Value |
|---|---|
| Observation Name | breakpoint_proximity |
| Originating Discipline | HCI / interruption research |
| Measurement Method | Task structure analysis identifying subtask completion boundaries; real-time task state monitoring |
| Standardization Level | Research-Only |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | reachability |
| Authoritative Source | Monk et al. (2004); Iqbal and Bailey (2005) |

---

### Observation 005

| Field | Value |
|---|---|
| Observation Name | trust_calibration_state |
| Originating Discipline | Human factors / automation trust research |
| Measurement Method | Complacency monitoring via monitoring frequency drop; intervention latency; trust scale instruments (Jian et al.) |
| Standardization Level | Research-Only |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | authority |
| Authoritative Source | Lee and See (2004); Parasuraman and Manzey (2010) |

---

### Observation 006

| Field | Value |
|---|---|
| Observation Name | handoff_state |
| Originating Discipline | HCI / joint activity research |
| Measurement Method | Mutual predictability assessment; directability monitoring; control transfer acknowledgment signals |
| Standardization Level | Research-Only |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | authority, subject_agency_state |
| Authoritative Source | Klein et al. (2004); Sheridan (2002) |

---

### Observation 007

| Field | Value |
|---|---|
| Observation Name | procedure_compliance |
| Originating Discipline | Human factors / safety engineering |
| Measurement Method | Task sequence monitoring against authorized procedure; deviation detection via process tracing |
| Standardization Level | Standardized — operationally standardized in aviation (LOSA) and healthcare (surgical checklists) |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | policy |
| Authoritative Source | Helmreich et al. (1999) LOSA; Haynes et al. (2009) surgical checklist |

---

### Observation 008

| Field | Value |
|---|---|
| Observation Name | shared_situation_awareness |
| Originating Discipline | Team human factors |
| Measurement Method | Cross-team SA probe alignment; communication analysis; shared mental model assessment |
| Standardization Level | Research-Only |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | execution_context |
| Authoritative Source | Salas et al. (1995); Endsley and Robertson (2000) |

---

## Domain: Robotics and Embodied AI
*Observations 009–012 — Synthesized by Gemini*

---

### Observation 009

| Field | Value |
|---|---|
| Observation Name | interaction_f_formation |
| Originating Discipline | Social Robotics / Embodied Conversational Agents (ECAs) |
| Measurement Method | Sensor fusion (LiDAR, computer vision, depth sensing) calculating spatial geometry, body orientation vectors, and gaze intersection among human-robot groupings |
| Standardization Level | Research-Only — built on Kendon's F-formations; metrics are platform-specific |
| Structural Coupling Dependency | Hardware-Bound at source; projects as Protocol-Neutral spatial state arrays |
| Candidate Dimension(s) | execution_context, reachability |
| Authoritative Source | Kendon (1990); Althaus et al. (2004) |

---

### Observation 010

| Field | Value |
|---|---|
| Observation Name | agent_bdi_state |
| Originating Discipline | Autonomous Multi-Agent Systems / Embodied AI |
| Measurement Method | Real-time extraction of active Beliefs, Desires, and Intentions from agent execution stack |
| Standardization Level | Implementation-Specific — natively parsed in BDI languages (Jason, Jadex) |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | mission, authority |
| Authoritative Source | Rao and Georgeff (1995); Bordini et al. (2007) |

---

### Observation 011

| Field | Value |
|---|---|
| Observation Name | dialogue_act_classification |
| Originating Discipline | Conversational Agents / Natural Language Processing |
| Measurement Method | Real-time classification of user communication turn using DAMSL or ISO 24617-2 dialogue act schema |
| Standardization Level | Standardized — DAMSL and ISO 24617-2 |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | execution_context, authority |
| Authoritative Source | Core and Allen (1997) DAMSL; Bunt et al. (2010) ISO Standard |

---

### Observation 012

| Field | Value |
|---|---|
| Observation Name | associative_context_relevance |
| Originating Discipline | LLM Agent Frameworks / MCP Context Runtimes |
| Measurement Method | Semantic proximity or vector embedding distance between incoming execution request and active memory stream |
| Standardization Level | Implementation-Specific |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | mission, policy |
| Authoritative Source | Park et al. (2023) Generative Agents; Anthropic MCP Specification (2025) |

---

## Domain: Industrial Control Systems / Aviation / Automotive Robotics
*Observations 013–016 — Synthesized by Gemini*

---

### Observation 013

| Field | Value |
|---|---|
| Observation Name | speed_separation_distance |
| Originating Discipline | Collaborative Industrial Robotics / Safety Engineering |
| Measurement Method | Real-time laser scanners, light curtains, or safety-rated vision systems calculating distance vector between autonomous robot and human worker |
| Standardization Level | Standardized — ISO 10218 and ISO/TS 15066 |
| Structural Coupling Dependency | Hardware-Bound at source; projects as normalized safe/unsafe flag |
| Candidate Dimension(s) | execution_context, policy |
| Authoritative Source | ISO/TS 15066 (2016) |

---

### Observation 014

| Field | Value |
|---|---|
| Observation Name | automation_mode_state |
| Originating Discipline | Aviation Systems / Human-Automation Interaction |
| Measurement Method | Extraction of active autopilot, Flight Management System (FMS), or automated driver-assist (ADAS) mode registers |
| Standardization Level | Standardized — aviation FMA displays; SAE J3016 Levels 0–5 |
| Structural Coupling Dependency | Protocol-Neutral |
| Candidate Dimension(s) | subject_agency_state, authority |
| Authoritative Source | Sarter and Woods (1995); SAE J3016 |

---

### Observation 015

| Field | Value |
|---|---|
| Observation Name | operator_takeover_latency |
| Originating Discipline | Automotive Robotics / Manned-Unmanned Teaming (MUM-T) |
| Measurement Method | Time elapsed between automation Takeover Request and physical engagement of human control mechanisms |
| Standardization Level | Standardized — autonomous driving telemetry and aerospace human performance standards |
| Structural Coupling Dependency | Protocol-Neutral — projected as millisecond integers |
| Candidate Dimension(s) | reachability, subject_agency_state |
| Authoritative Source | Merat et al. (2014); Aerospace Human Factors Standards |

---

### Observation 016

| Field | Value |
|---|---|
| Observation Name | intervening_override_frequency |
| Originating Discipline | Industrial Control Systems / Safety Instrumented Systems |
| Measurement Method | Audit trail processing counting manual operator overrides, setpoint rollbacks, or safety trips per unit of operational time |
| Standardization Level | Standardized — ISA-18.2 / IEC 62682 alarm management frameworks |
| Structural Coupling Dependency | Protocol-Neutral — exposed via discrete transaction logs |
| Candidate Dimension(s) | subject_agency_state, policy |
| Authoritative Source | ANSI/ISA-18.2; IEC 62682 |

---

## Catalog Summary

Total observations: 16
Domains covered: 4
- HCI and Human Factors: 8 observations
- Robotics and Embodied AI: 4 observations
- Industrial Control / Aviation / Automotive: 4 observations
- Agent Frameworks and MCP: included within Robotics domain (Obs 012)

Standardization distribution:
- Standardized: 7 (001, 002, 007, 011, 013, 014, 015, 016)
- Implementation-Specific: 3 (003, 010, 012)
- Research-Only: 6 (004, 005, 006, 008, 009, 016)

Structural coupling distribution:
- Protocol-Neutral: 11
- Hardware-Bound at source / Protocol-Neutral at projection: 5

---

## Open Research Questions

Carried forward from Research Synthesis Sprint:

- Should Interaction Evidence remain a separate taxonomy block?
- Is handoff a property of the interaction boundary or a
  cross-dimensional governance event?
- What classification functions transform heterogeneous observations
  into governance evidence?
- How should confidence, provenance, explainability, and
  auditability be measured?
- Does governance normalization constitute a distinct scientific
  construct separate from semantic normalization?
  (See RESEARCH_OBSERVATIONS.md RO-001)

---

## Repository Inspection Required

Repository Inspection Gate must be completed before this artifact
is committed to the repository.

CG shall verify:
- All 16 observations are present
- All seven fields are preserved for each observation
- No architectural drift introduced
- No normalization functions introduced
- No unintended changes to approved source material
- Document structure, provenance, and references are correct

Repository Curator (Deb) authorizes commit after inspection.
