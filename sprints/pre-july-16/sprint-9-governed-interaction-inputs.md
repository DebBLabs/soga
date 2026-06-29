# Sprint 9 — Governed Interaction Inputs

Program: Pre-July 16 Program
Sprint: Sprint 9 — Governed Interaction Inputs
Status: Gate 1 APPROVED / Gate 2 CONDITIONAL CLEARANCE / Deb AUTHORIZED
Date: 2026-06-29
Commit Baseline: 71f78aa

---

## Research Question

What is the minimum information required to govern a Compaia interaction?

---

## Answer

The existing RuntimeEnvelope v0.1 is sufficient to govern a single-agent
execution request. To govern a Compaia interaction — a specialized execution
context in which a governed human subject engages with an autonomous participant
across a declared boundary — four additional inputs are required.

These four inputs are introduced as a provisional, optional nested block
inside execution_context:

execution_context.interaction_context

No existing RuntimeEnvelope fields are modified.
No Python files are modified in Sprint 9.

---

## Provisional Schema

{
  "execution_context": {
    "request_id": "...",
    "evaluated_at": "...",
    "guest_present": false,
    "operator_present": false,
    "source": "...",
    "interaction_context": {
      "interaction_id": "<generated UUID>",
      "participant_id": "<autonomous participant identifier>",
      "participant_type": "<agent | tool | robot | service>",
      "interaction_boundary": "<api_endpoint | agent_handoff | tool_invocation | physical_presence>"
    }
  }
}

interaction_context is optional. When absent, governance evaluation
proceeds as today. No existing baseline case is affected.

---

## Field Definitions

| Field | Purpose | Allowed Values | Status |
|---|---|---|---|
| interaction_id | Identifies this governed interaction as a distinct governance unit | Generated UUID | New |
| participant_id | Identifies the autonomous participant the subject is engaging | Any valid participant identifier | New |
| participant_type | Declares the nature of the autonomous participant | agent, tool, robot, service | New |
| interaction_boundary | Names the entry point being crossed at evaluation time | api_endpoint, agent_handoff, tool_invocation, physical_presence | New |

---

## Structural Invariants

The following are structural requirements the adapter must satisfy
before submitting an envelope for interaction governance.

Invariant 1 — mission_active

mission.lifecycle == ACTIVE

Invariant 2 — subject_can_intervene

subject.reachability == REACHABLE
AND
subject.governance_state != INDEPENDENT

The adapter is responsible for providing canonical subject state.
SOGA asserts these as policy inputs.

---

## Gate 2 Resolutions Adopted

1. interaction_context is nested inside execution_context.

2. No processing logic, evaluator code, flattening mechanics, or
Python implementation is authorized in Sprint 9.

---

## Files Modified

Repository documentation:

- sprints/pre-july-16/sprint-9-governed-interaction-inputs.md

No executable code modified.

The following files are explicitly NOT modified:

- verify/runtime_envelope.py
- verify/runtime_envelope_model.py
- Any adapter file
- Any regression test

---

## Regression Baseline

Verification command:

python3 -m tools.regression_baseline

Expected:

- AAuth ACTIVE
- UCAN ACTIVE
- ZCAP ACTIVE
- AAuth IMPAIRED
- UCAN IMPAIRED
- ZCAP IMPAIRED

All pass unchanged.

---

## Promotion Path

If authorized after Gate 2:

specifications/runtime-envelope/v0.1/interaction_context.md

Implementation targets (pending authorization):

- verify/runtime_envelope.py
- verify/runtime_envelope_model.py
- adapter projection
- regression additions

No implementation proceeds from this artifact alone.
