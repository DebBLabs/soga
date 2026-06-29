# Sprint 8 Task 4 — RESTRICT Path Evidence

Date: 2026-06-27

Status: Gate 1 Closeout Submission

---

## Objective

Demonstrate that SOGA produces a real RESTRICT determination from a live AAuth execution request when Subject Agency State is SUPERVISED.

---

## Live Request

Request ID:

    288e7e36-24e0-4113-81e8-55f87240ce97

Request included canonical runtime inputs through request parameters:

    subject_agency_state: SUPERVISED
    reachability: REACHABLE

---

## End-to-End Result

Optimization progress result:

    status: approval_pending
    progress_percentage: 0.0
    current_step: RESTRICT: Subject governance state requires supervision.

This confirms the execution did not fail. It entered a holding / approval-pending state because governance required supervision.

---

## SOGA Runtime Evidence

Backend log evidence:

    SOGA EXECUTION BOUNDARY
    User: guest
    Agent URL: http://supply-chain-agent.localhost:3000
    Execution Request Preview: Beth requests delegated caregiver action. with the following constraints: same request with supervised subject state.
    Governance Determination: RESTRICT
    Reason: Subject governance state requires supervision.
    CDP Determination: GovernanceDetermination.RESTRICT
    CDP Subject Agency State: SubjectAgencyState.SUPERVISED
    CDP Reachability: Reachability.REACHABLE

A2A boundary evidence:

    SOGA EXECUTION BOUNDARY decision=RESTRICT reason=Subject governance state requires supervision. user_id=guest agent_url=http://supply-chain-agent.localhost:3000

---

## Architectural Significance

This is a real RESTRICT path, not a hardcoded response.

The live request flowed through:

    AAuth execution request
        -> AAuth Execution Adapter
        -> RuntimeEnvelope
        -> Runtime Bridge
        -> RuntimeGovernanceEngine
        -> CanonicalDecisionPackageAdapter
        -> RESTRICT
        -> approval_pending / holding

The governance determination came from RuntimeGovernanceEngine.

The Canonical Decision Package was produced by CanonicalDecisionPackageAdapter.

---

## Core Demonstration Claim

The same live AAuth request can produce different governance outcomes solely because runtime governance inputs changed.

The delegation does not change.

The protocol does not change.

The agent does not change.

The mission does not change.

Only Subject Agency State changes.

---

## Verification

Regression baseline must be confirmed before commit:

    PYTHONPATH=. python3 tools/regression_baseline.py

Expected:

    All baseline cases passed.

---

## Gate 1 Request

Please review Sprint 8 Task 4 evidence.

If approved, Sprint 8 Task 4 closes.

