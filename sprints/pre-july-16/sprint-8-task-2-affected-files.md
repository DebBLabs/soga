# Sprint 8 Task 2 — Runtime Bridge / Stub Replacement
# Affected Files

Date: 2026-06-27

Status: Draft for Gate 1 Review

---

## Task

Replace the temporary AAuth governance stub path with a real SOGA runtime governance invocation.

---

## Purpose

Use the AAuth Execution Adapter output as canonical runtime input, pass it through RuntimeGovernanceEngine, and produce a real Canonical Decision Package.

---

## Affected Files

### New

- engines/aauth_execution_runtime_bridge.py

### Modified

- external-repos/aauth-full-demo/scripts/start-infra.sh

### Planned Next Modification After Gate 1

- external-repos/aauth-full-demo/backend/app/services/soga_governance_stub.py

---

## Current Verification

Manual bridge verification completed.

Input:

- agent_url: http://supply-chain-agent.localhost:3000
- user_id: guest
- message: Optimize laptop supply chain

Result:

- governance_determination: ALLOW
- reason: All governance dimensions passed at execution time.
- canonical_decision_package.governance_determination: ALLOW
- canonical_decision_package.reachability: REACHABLE

---

## Architectural Conformance

The bridge:

- consumes RuntimeEnvelope produced by AAuthExecutionAdapter
- invokes RuntimeGovernanceEngine
- invokes CanonicalDecisionPackageAdapter
- preserves protocol independence
- does not pass AAuth-shaped inputs directly to RuntimeGovernanceEngine
- keeps the adapter projection-only
- keeps the AAuth backend interface stable

---

## Note on Reachability Default

AAuth execution requests may omit live reachability.

For the initial ALLOW path, omitted reachability is treated as Reachable inside the runtime bridge.

Explicit UNKNOWN or UNREACHABLE values still flow through to RuntimeGovernanceEngine and may produce REVIEW / RESTRICT or FAIL according to existing runtime logic.

---

## Gate 1 Request

Please review before replacing the live AAuth stub implementation.

