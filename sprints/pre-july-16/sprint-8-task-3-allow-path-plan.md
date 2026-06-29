# Sprint 8 Task 3 — ALLOW Path Demonstration

Date: 2026-06-27

Status: Draft

## Objective

Demonstrate the live ALLOW path end to end.

A live AAuth execution request must pass through SOGA runtime governance, produce a real Canonical Decision Package, return ALLOW, and allow execution to proceed.

## Path

AAuth execution request
→ AAuth Execution Adapter
→ RuntimeEnvelope
→ RuntimeGovernanceEngine
→ Canonical Decision Package
→ ALLOW
→ AAuth execution proceeds
→ Optimization completes

## Success Criteria

- Live request completes successfully.
- Backend logs show SOGA EXECUTION BOUNDARY.
- Logs show Governance Determination: ALLOW.
- Logs show CDP Determination: GovernanceDetermination.ALLOW.
- Logs show Subject Agency State and Reachability.
- Optimization progress reaches completed / 100%.
- Regression baseline passes.

## Out of Scope

- RESTRICT path
- Caregiver scenario
- New governance dimensions
- Mission Builder changes
- Workbench UI changes


## Gate 1 Addition

The CDP produced during Task 3 must contain a real governance determination from RuntimeGovernanceEngine.

This must be distinguishable from the prior stub ALLOW response.

Evidence may come from:

- backend logs showing RuntimeGovernanceEngine-derived reason
- CDP determination value
- CDP Subject Agency State
- CDP Reachability
- successful execution after ALLOW

