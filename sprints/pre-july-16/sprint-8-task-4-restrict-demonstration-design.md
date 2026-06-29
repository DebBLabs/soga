# Sprint 8 Task 4 — RESTRICT Demonstration Design

Date: 2026-06-27

Status: Draft for Gate 1 Review

---

## Objective

Demonstrate that SOGA produces a real RESTRICT determination from a live AAuth execution request when Subject Agency State changes.

This task proves that execution-time governance is state-sensitive.

---

## Core Claim

The same live AAuth request can produce different governance outcomes solely because runtime governance inputs changed.

The delegation does not change.

The protocol does not change.

The agent does not change.

The mission does not change.

Only Subject Agency State changes.

That is the point of the demonstration.

---

## Scenario

Alice delegates authority to Beth.

Beth attempts the same delegated action under two different runtime states.

---

## Run 1 — ALLOW

Subject:

    Alice

Subject Agency State:

    Independent

Expected Result:

    ALLOW

Expected Execution Behavior:

    Execution proceeds.

Expected CDP:

    Governance Determination: ALLOW
    Subject Agency State: INDEPENDENT
    Reachability: REACHABLE

---

## Run 2 — RESTRICT

Subject:

    Alice

Subject Agency State:

    Supervised

Expected Result:

    RESTRICT

Expected Execution Behavior:

    Execution enters HOLDING.

Expected Reason:

    Subject requires supervision or runtime review before execution may proceed.

Expected CDP:

    Governance Determination: RESTRICT
    Subject Agency State: SUPERVISED
    Restrict Mode: present
    Reason: visible

---

## Required Path

Both runs must use the same architectural path:

    Live AAuth execution request
        -> AAuth Execution Adapter
        -> RuntimeEnvelope
        -> Runtime Bridge
        -> RuntimeGovernanceEngine
        -> CanonicalDecisionPackageAdapter
        -> governance result

---

## Evidence Required

Task 4 evidence must include:

- RuntimeEnvelope evidence
- RuntimeGovernanceEngine decision
- Canonical Decision Package
- Backend logs
- ALLOW run evidence
- RESTRICT run evidence
- Execution proceeds for ALLOW
- Execution enters HOLDING for RESTRICT
- Regression confirmation

---

## Out of Scope

This task does not implement:

- new governance dimensions
- per-hop governance evaluation
- approval workflow
- production notification service
- Mission Builder changes
- Workbench UI changes
- caregiver application UI

---

## Design Constraint

Do not fake RESTRICT.

Do not hardcode the final governance determination.

The RESTRICT result must be produced by RuntimeGovernanceEngine from canonical runtime inputs.

---

## Success Criteria

Task 4 succeeds when:

1. A live AAuth execution request enters SOGA governance.
2. RuntimeGovernanceEngine produces RESTRICT.
3. CanonicalDecisionPackageAdapter produces a real RESTRICT CDP.
4. Logs show the Subject Agency State that caused RESTRICT.
5. Execution enters HOLDING.
6. The same baseline ALLOW path still works.
7. Regression passes with all baseline cases.

---

## Demonstration Message

Execution-time governance is state-sensitive.

SOGA complements AAuth by evaluating whether delegated authority should still be exercised at the moment of execution.

