# SPRINT ROADMAP — G0 through G30
## Deb B Labs Embodied Governance Research Program

Status: DRAFT v0.1 — proposed for adoption via the G0 initialization commit
Precedence: subordinate to `knowledge/working/CURRENT_STATE.md`

Naming note: sprint and guardrail identifiers share the G-namespace by
established repository convention (G23 is both). "G0" is a deliberate
pre-sequence marker for program initialization, not a guardrail.

---

## G0 — Program Initialization

**Purpose.** Transition the repository from component-driven development
to a research-driven program. No architectural research; no new runtime
behavior.

**Deliverables — repository governance**
- `CURRENT_STATE.md` amended: new phase, G0 active, sprint sequence
  authorized, HEAD field corrected
- Repository drift resolved to zero known items
- `tools/live_governance_workbench.py` dispositioned (commit, document,
  defer, or remove — recorded in the decision log)
- Updated sprint roadmap published (this document)

**Deliverables — strategy artifacts** (`knowledge/strategy/`)
- `PROGRAM_CHARTER.md`
- `SPRINT_ROADMAP_G0_G30.md`
- `TRACKS.md` (continuous track registers, seeded)
- `DECISION_LOG.md` (seeded with the July 20 decisions)

**Gate 1 exit criteria** (verified by Claude, advisory; activation of
G24 authorized by the PI)
1. Repository synchronization complete; zero known drift.
2. Operating model internally consistent: charter, roadmap, tracks, and
   CURRENT_STATE.md contain no contradictions; precedence rule stated.
3. Roadmap approved by the PI.
4. Research questions well-formed: every primary hypothesis in the
   charter is stated falsifiably and mapped to the sprint expected to
   produce its first Observed evidence.
5. No unresolved architectural contradictions on record.

---

## G24 — Research Synchronization

**Purpose.** Close current research threads before inspection begins.
(Repository-governance items formerly listed here moved to G0.)

**Deliverables**
- PIC report and feedback completed
- Why PIC review completed
- AAuth office-hour findings reconciled
- Research notes synchronized

No architecture or runtime changes.

**Exit criterion.** Current research state accurately reflects
everything learned during recent standards discussions.

---

## G25 — AAuth Integration Investigation

**Purpose.** Observe the implementation boundary before designing
against it. (Per the standing CURRENT_STATE.md objective.)

**Inspect**
- Christian's connector
- Person Server integration
- Governance Server consultation point
- Deferred interaction flow
- CTAP2 / User Presence / User Verification
- External governance interface
- Current Mission representation and adapter behavior

**Outputs**
- Verified implementation findings; Observed execution path
- Gap analysis; integration-hook candidates
- Unresolved questions classified Hypothesis or Future Research

No connector implementation.

---

## G26 — Mission and Orchestration Research

**Purpose.** Define what Mission is architecturally — and what it is
not. Clarity, not renaming.

**Candidate models (minimum three, evaluated on evidence)**
1. Mission as the top-level orchestration and authority contract
2. Mission as an AAuth/domain concept beneath a separate orchestration
   abstraction
3. A standards-mapped hybrid

**Tested against.** Observed AAuth implementation (G25 outputs), AAuth
terminology, PMI terminology, current Stage Gate behavior,
delegated-authority requirements, embodied/multi-agent scenarios,
ecosystem continuity and switching costs.

**Exit artifacts.** Terminology crosswalk; bounded conceptual model;
architecture decision record with selected model, rationale, and
explicit repository consequences — including "no change" if warranted.

---

## G27 — Embodied Capability and Physical Safety Model

**Purpose.** Model governed physical execution before connecting
Misty B.

**Per-capability definition** (movement/pose, speech/sound,
camera/perception, display, attention cues, companion-device
interaction): risk class, required authority, relevant context,
interruptibility, revocation behavior, safe degraded state, audit
requirements, local-vs-remote decision requirements.

**Additional required outputs**
- Misty A / Misty B state-isolation specification (testable property)
- Mid-actuation interruption semantics
- Network-partition behavior
- Threat-model extension for non-delegating affected subjects,
  including bystanders

Latency remains Hypothesis-class until measured. Taxonomy is modeled
against Misty B's perception envelope; Misty A serves as the
lower-capability comparative control.

---

## G28 — Governed Misty B Runtime Prototype

**Entry criteria.** G27 state-isolation specification exists;
interruption semantics defined; G26 decision record adopted.

**Purpose.** Route selected Misty B actions through the canonical
pipeline: orchestration context → Stage Gate → RuntimeEnvelope →
Governance Policy Server → Canonical Decision Package → Capability
Registry → Misty actuation.

**Measure.** Decision latency by capability and risk class;
interruption behavior; degraded-state transitions; network-loss
behavior; logging completeness; isolation from Misty A.

This sprint produces the first Observed evidence for H1 and H3.

---

## G29 — Living Laboratory Methodology

**Purpose.** Define how a real event produces research evidence.
Deliberately precedes any public demonstration.

**Scope.** Observational metrics; evidence-classification rules for
live (non-repeatable) events; instrumentation; intervention and
exception logging; consent; bystander treatment; video/audio handling;
retention and deletion; privacy boundaries; repeatability limits;
criteria distinguishing anecdote from evidence.

---

## G30 — First Controlled Embodied Event

**Entry criterion.** G29 methodology adopted.

**Purpose.** Small, instrumented event with Misty B in a host or
performance-support role.

Success is not that the robot performs without error. Success is that
the event yields interpretable evidence on authority evaluation,
governed physical execution, latency, interruptions, safe-state
behavior, environmental effects, human interaction, and the adequacy of
the methodology itself.

---

## Standing Note

Continuous program tracks (Research, Implementation, Standards,
Funding & Partnerships, Living Laboratory & Outreach) run across every
sprint and are
governed by the charter and `TRACKS.md`, not by this roadmap.
