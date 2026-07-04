# Stage Gate Architecture v0.1

**Status:** Research Definition
**Date:** 2026-07-04
**Sprint:** Sprint C — Phase C1
**Gate 1:** APPROVED (Claude)
**Gate 2:** Pending

No architectural decisions are made by this document
beyond what is explicitly stated.
This document is a research definition, not a specification.

---

## 1. What is a Stage Gate?

A Stage Gate is an explicit governance checkpoint declared
within a mission execution flow. It designates a point at
which SOGA must evaluate whether execution may continue
before the next mission step proceeds.

A Stage Gate is not a governance decision.
It is a trigger for governance evaluation.

```
Stage Gate answers:
Has this mission reached a point where governance
evaluation must occur before execution continues?

GovernancePDP answers:
What is the governance decision?
```

These are distinct responsibilities that must never
be conflated.

---

## 2. Why Stage Gates Exist

Without explicit Stage Gates, governance evaluation is
implicit — it may occur at every step or at no step,
depending on implementation. Implicit governance creates
invisible decision points that cannot be inspected,
audited, or communicated to collaborators.

Explicit Stage Gates make governance checkpoints:

- **Visible** — declared in the mission package
- **Inspectable** — recorded in the CDP trail
- **Communicable** — named checkpoints a human author
  can reason about
- **Auditable** — every gate evaluation produces a CDP

---

## 3. Position Within the Execution Lifecycle

```
Mission Package
      ↓
Mission Step declared
      ↓
Stage Gate declared for this step?
      │
      ├── No  → Execute directly
      │
      └── Yes → Governance evaluation required
                      ↓
                RuntimeEnvelope assembled
                      ↓
                GovernancePDP evaluates
                      ↓
                Canonical Decision Package produced
                      ↓
          ┌───────────────────────────────────┐
          │ ALLOW                             │
          │ Execute. Continue mission.        │
          ├───────────────────────────────────┤
          │ RESTRICT                          │
          │ Three governed continuation paths:│
          │                                   │
          │ HOLDING                           │
          │   Wait for human clearance.       │
          │   Nothing executes until          │
          │   human acts.                     │
          │                                   │
          │ BOUNDED CONTINUATION              │
          │   Act within declared bounds      │
          │   while awaiting clearance.       │
          │   Example: may remind, may not    │
          │   reschedule.                     │
          │                                   │
          │ SUPERVISED EXECUTION              │
          │   Execute with human monitoring.  │
          │   Human may intervene but does    │
          │   not need to act first.          │
          ├───────────────────────────────────┤
          │ DENY                              │
          │ Do not execute.                   │
          │ Mission step fails.               │
          └───────────────────────────────────┘
```

---

## 4. The Four-Phase Stage Gate Lifecycle

### Phase 1 — Discovery Boundary

A mission step carries a stage_gate constraint declaration.
The gate condition is read from
`mission.constraints.stage_gate`.

The runtime identifies that governance evaluation is required
before this step executes.

The gate condition is already expressible using the Mission
Constraints data model established in the Mission Constraints
Sprint. Sprint C gives this field runtime behavior.

---

### Phase 2 — Interruption Request

The gate condition projects into the canonical
RuntimeEnvelope through the standard passive adapter
and normalization pipeline.

The GovernancePDP evaluates and produces:

```
Canonical Decision Package:
  decision: RESTRICT
  governance_reasoning_token: [identifies gate condition]
```

The GovernancePDP produces exactly what it produces today.
Nothing more. It remains completely unaware that an
interruption exists as a workflow concept.

**Execution Interruption Record (execution layer):**

When the CDP carries RESTRICT, the Mission Execution Engine
— not the GovernancePDP — creates an Execution Interruption
Record. This record lives in the execution layer and owns:

- interruption_instance_id (unique per gate instance)
- gate instance reference
- pending clearance state
- associated mission step
- reference to the triggering CDP

This separation is critical in multi-agent environments.
Multiple gates may be active simultaneously. The
interruption_instance_id allows a human supervisor to
identify precisely which gate instance requires clearance.

The CDP is not modified. The GovernancePDP is not modified.
The Execution Interruption Record is an execution-layer
concern owned by the future Mission Execution Engine
(Sprint E).

---

### Phase 3 — Clearance Capture

An authoritative external action satisfies the pending
gate condition. Examples:

- Human sign-off recorded
- Supervisor confirmation received
- Approval token issued
- Required evidence provided

The clearance is recorded as updated evidence associated
with the interruption_instance_id in the Execution
Interruption Record.

During this phase, the agent does not stop. It operates
within the bounds declared in the mission constraints:

```
supervision_required: true
  → SUPERVISED EXECUTION
  Agent executes with monitoring.
  Human may intervene.

bounded_continuation_allowed: true
  → BOUNDED CONTINUATION
  Agent acts within declared bounds.
  Example: may send reminder, may not reschedule.

subject_must_confirm: true
  → HOLDING
  Agent waits.
  Nothing executes until human acts.
```

The mission author defines the bounds.
The GovernancePDP enforces them.
The agent operates within them.

RESTRICT is not a stop sign. It is a governed continuation
with constraints.

---

### Phase 4 — Resubmission Pass

When clearance is received:

1. Execution Interruption Record is updated.
2. RuntimeEnvelope is rebuilt using updated evidence.
3. The same passive adapter and normalization pipeline
   executes. No bypass. No special path.
4. GovernancePDP evaluates the updated RuntimeEnvelope.
5. A new Canonical Decision Package is produced.
6. Decision: ALLOW. Execution proceeds.

This is RO-003 (Projection Pattern) applied to the
clearance lifecycle. The same pipeline. Updated evidence.
Natural evaluation. No governance memory. No special path.

---

## 5. Relationship to Mission Constraints

The Mission Constraints Sprint established:

```
mission.constraints:
  global:      apply throughout mission
  stage_gate:  apply at named execution boundaries
  delegation:  apply when authority passes to sub-agents
```

Sprint C makes `stage_gate` constraints first-class
executable checkpoints. The data model already exists.
Sprint C gives it runtime behavior.

Stage gate constraints may declare:

- Which steps require governance evaluation
- What RESTRICT path applies
  (HOLDING, BOUNDED CONTINUATION, SUPERVISED EXECUTION)
- What evidence satisfies the gate condition
- What the agent may do during RESTRICT

---

## 6. Relationship to GovernancePDP

The Stage Gate is a trigger.
The GovernancePDP is the evaluator.

The GovernancePDP is not aware of Stage Gates as a concept.
It receives a RuntimeEnvelope and produces a CDP.
The Stage Gate framework determines when to submit a
RuntimeEnvelope for evaluation.

Governance owns:
- execution-time legitimacy evaluation
- policy evaluation
- Canonical Decision Package generation

Mission Execution owns:
- waiting
- resumption
- interruption tracking
- human clearance workflow
- execution state

The GovernancePDP evaluates evidence.
It does not manage workflow.

---

## 7. Relationship to Mission Execution Engine (Sprint E)

The Execution Interruption Record is a Sprint E concern.
Sprint C defines Stage Gates conceptually and demonstrates
the RESTRICT/ALLOW lifecycle.

Sprint E implements:
- Execution Interruption Record infrastructure
- Interruption tracking across concurrent gate instances
- Clearance workflow integration
- Mission resumption after clearance

Sprint C does not implement the Execution Interruption
Record. It defines that such a record will exist and
that the execution layer owns it.

---

## 8. Non-Goals

Stage Gates are not:

- A replacement for GovernancePDP evaluation
- A human workflow system
- An approval routing system
- A notification system
- A protocol-specific construct
- A new governance dimension
- A modification to the CDP schema
- A mechanism for governance memory

Stage Gates declare when governance fires.
Everything else remains unchanged.

---

## 9. Architectural Invariants

All six invariants are preserved and strengthened
by the Execution Interruption Record revision:

```
□ GovernancePDP unchanged
□ RuntimeEnvelope unchanged
□ Canonical Decision Package unchanged
  — no additive metadata introduced
  — CDP remains the canonical governance decision
□ Passive Adapter boundary unchanged
□ Governance dimensions unchanged
□ Governance semantics unchanged
```

The CDP is not modified by Stage Gate architecture.
The interruption_instance_id lives in the execution layer.
The GovernancePDP remains completely unaware that an
interruption exists as a workflow concept.

---

## 10. Architectural Resolutions (Gate 2)

**Resolution 1 — Execution Interruption Record placement:**
The conceptual definition belongs in Sprint C.
The physical code implementation belongs in Sprint E.
No data-store structures, async tracking loops, or
event-bus files are introduced until Mission Execution
Engine (Sprint E) is formally authorized.

**Resolution 2 — RESTRICT path determination:**
The stage_gate constraint field specifies threshold rules.
The GovernancePDP evaluates whether runtime context
satisfies them. The execution engine reads the
governance_reasoning_token and maps it to the appropriate
operational state:
- HOLDING
- BOUNDED CONTINUATION
- SUPERVISED EXECUTION

The mission author declares the rules.
The GovernancePDP evaluates the evidence.
The execution engine implements the path.

**Resolution 3 — Stage Gate may produce ALLOW directly:**
Yes. A Stage Gate is a mandatory evaluation checkpoint,
not a mandatory blocking checkpoint.

If required clearance evidence is already present when
the gate is reached — for example, a supervisor
pre-approved the action — the GovernancePDP produces
ALLOW on the first pass. No interruption record is
created. Mission proceeds seamlessly.

Most well-governed missions with satisfied constraints
will produce ALLOW at Stage Gates without human
intervention.

---

## Repository Relationship

This document extends:
- Mission Constraints Sprint — stage_gate field defined
- docs/stable_interfaces_v0_1.md — interfaces unchanged
- docs/passive_adapter_specification_v0_1.md — unchanged
- knowledge/research/RESEARCH_OBSERVATIONS.md — RO-003
  Projection Pattern applies to Phase 4 resubmission

No existing document is modified by this research definition.
