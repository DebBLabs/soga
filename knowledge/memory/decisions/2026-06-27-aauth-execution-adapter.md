# Architectural Decision
# AAuth Execution Adapter

**Date:** 2026-06-27

**Status:** Accepted by Gate 1

---

## Decision

The AAuth Execution Adapter will be implemented as the first task of Sprint 8.

The adapter will reside inside the SOGA repository.

Proposed location:

    input_adapters/aauth_execution_adapter.py

---

## Rationale

SOGA is protocol independent.

AAuth produces delegation and authorization evidence but is not responsible for translating that evidence into SOGA's canonical runtime model.

The translation layer is therefore a SOGA responsibility.

This preserves the correct dependency direction:

    AAuth
        │
        ▼
Protocol-specific evidence
        │
        ▼
AAuth Execution Adapter
        │
        ▼
Canonical SOGA Runtime Inputs
        │
        ▼
Runtime Governance Engine
        │
        ▼
Canonical Decision Package

The Runtime Governance Engine never consumes AAuth-specific structures directly.

---

## Architectural Implications

This establishes the general adapter pattern for protocol integration.

Future protocol adapters follow the same architecture, including:

- AAuth
- UCAN
- ZCAP
- OAuth
- GNAP
- MCP
- Future protocol integrations

Each adapter produces the same canonical runtime representation.

Protocol independence is therefore demonstrated structurally rather than asserted.

---

## Gate 1 Ruling

Approved.

Implementation is deferred until Sprint 8.

No implementation work should begin before pre-Sprint closeout is complete.

---

## Sprint 8 Task 1

Implement:

    input_adapters/aauth_execution_adapter.py

Objectives:

- Translate AAuth execution requests.
- Produce canonical SOGA runtime inputs.
- Preserve protocol independence.
- Feed the Runtime Governance Engine.
- Produce the first live Canonical Decision Package from an AAuth execution request.

---

## Significance

This decision formalizes the execution-boundary integration strategy.

Protocol-specific systems remain external.

SOGA owns the canonical governance model and the translation into that model.

This preserves the architectural separation established in the Project Constitution and Architectural Principles.


---

## Gate 1 Boundary Test

The adapter's responsibility ends when it produces a RuntimeEnvelope.

The adapter should:

- Receive an AAuth execution request
- Extract mission context
- Extract delegation evidence
- Extract authorization context
- Extract subject identity
- Extract runtime conditions
- Translate each into SOGA canonical form
- Package everything into a RuntimeEnvelope
- Return the RuntimeEnvelope

The adapter should not:

- Evaluate Subject Agency State
- Apply policy
- Produce a governance determination
- Generate a Canonical Decision Package
- Make any ALLOW / RESTRICT / DENY decision

Those responsibilities belong to the Runtime Governance Engine and downstream CDP packaging.

## Architectural Test

The test question for the implementation is:

    Does AAuthExecutionAdapter return a RuntimeEnvelope and nothing else?

If yes, the boundary is correct.

If the adapter returns anything resembling a governance determination, policy evaluation result, or Canonical Decision Package, it has crossed the boundary and taken on Runtime Governance Engine responsibilities.

## Current Result

Sprint 8 Task 1 passes this boundary test.

The adapter returns a RuntimeEnvelope.

It does not evaluate governance.

It does not produce ALLOW, RESTRICT, or DENY.

It does not generate a Canonical Decision Package.

