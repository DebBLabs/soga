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

