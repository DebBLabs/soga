# SOGA Stable Interfaces v0.1

Status: Sprint 8 Launch Package  
Purpose: Define the stable interface contracts exposed by the SOGA reference implementation.

## Scope

This document defines interface boundaries, not deployment topology.

SOGA may be implemented as a library, service, gateway, policy layer, or integrated governance component.

## Interface Summary

```text
Human Intent
     |
     v
Mission Intake API
     |
     v
Canonical Mission Representation
     |
     v
Runtime Envelope API
     |
     v
Governance API
     |
     v
Canonical Decision Package API
     |
     v
PEP / Execution API1. Mission Intake API

Purpose:

Convert human intent into a Canonical Mission Representation.

Consumes:

* Human intent
* Optional subject representation
* Optional mission context
* Optional sector knowledge

Produces:

* Canonical Mission Representation
* Validation finding if the mission cannot be represented safely

Stable contract:

* Mission Intake performs representation only.
* Mission Intake does not produce ALLOW, RESTRICT, or DENY.
* Mission Intake does not perform governance reasoning.
* Invalid or incomplete missions produce findings, not malformed CMRs.

2. Canonical Mission Representation

Purpose:

Represent the mission that governance will later evaluate.

Carries:

* Mission identifier
* Subject identifier
* Objective
* Allowed actions
* Forbidden actions
* Bounds
* References
* Metadata

Stable contract:

* CMR is the boundary between mission representation and governance evaluation.
* CMR is not a governance decision.
* CMR may be produced from human intent or mission files.
* CMR may be projected into protocol-specific artifacts.

3. Protocol Adapter Interface

Purpose:

Normalize delegation or authority evidence from external protocols into SOGA-compatible runtime inputs.

Consumes examples:

* AAuth Mission Statement
* UCAN-shaped capability evidence
* ZCAP-shaped capability evidence
* Other authorization or delegation artifacts

Produces:

* Runtime Envelope input
* Authority evidence
* Mission evidence
* Subject state assertions where available

Stable contract:

* Protocol adapters do not produce governance outcomes.
* Protocol adapters do not alter PDP behavior.
* Protocol-specific inputs must converge on the same governance path.
* Protocol changes must not change governance semantics.

4. Runtime Envelope API

Purpose:

Carry execution-time governance inputs into the PDP.

Consumes:

* Canonical Mission Representation or projected mission evidence
* Authority or delegation evidence
* Subject Agency State
* Reachability
* Execution context
* Policy context
* Advisory agent evidence

Produces:

* Runtime Envelope

Stable contract:

* Runtime Envelope is input to governance.
* Runtime Envelope is protocol-independent.
* Runtime Envelope may contain zero or more advisory agent inputs.
* Conflicting advisory evidence is allowed.
* Conflicting advisory evidence is evaluated by governance; it is not a competing governance outcome.

5. Advisory Evidence Interface

Purpose:

Allow advisory agents to contribute governance-relevant evidence.

Consumes:

* Agent identifier
* Evidence type
* Evidence content
* Provenance
* Confidence

Produces:

* Advisory evidence records
* Review signals where disagreement, uncertainty, or contradiction is present

Stable contract:

* Advisory agents are evidence contributors only.
* Advisory agents do not produce ALLOW, RESTRICT, or DENY.
* Advisory agents do not produce Canonical Decision Packages.
* Advisory agents do not override the PDP.

6. Governance API

Purpose:

Evaluate execution-time legitimacy.

Consumes:

* Runtime Envelope
* Mission inputs
* Authority inputs
* Subject Agency State
* Reachability
* Execution context
* Policy
* Advisory evidence signals

Produces:

* ALLOW
* RESTRICT
* DENY
* Dimension evaluations
* Restriction mode where applicable
* Governance rationale

Stable contract:

* The PDP is the sole governance authority.
* The six governance dimensions remain locked.
* RESTRICT is a real execution path, not a softened DENY.
* One authoritative governance determination exists per execution event.
* The PDP remains protocol-independent.

7. Canonical Decision Package API

Purpose:

Package the governance result as the canonical artifact for downstream consumers.

Consumes:

* Governance determination
* Dimension evaluations
* Authority inputs
* Subject Agency State
* Reachability
* Mission
* Execution context
* Policy
* Execution receipt
* Provenance
* Restrict mode where applicable

Produces:

* Canonical Decision Package

Stable contract:

* The CDP is the API boundary for downstream systems.
* Execution, audit, visualization, and future consumers read the CDP.
* Consumers must not reconstruct governance logic.
* One CDP exists per execution event.

8. PEP / Execution API

Purpose:

Enforce or execute according to the governance result.

Consumes:

* Decision Package
* Governance directives
* Restrict mode
* Execution context

Produces:

* Execution status
* Execution receipt
* HOLD / EXECUTE / DENY behavior as applicable

Stable contract:

* PEP enforces; it does not govern.
* PEP does not override the PDP.
* PEP does not reinterpret protocol evidence.
* RESTRICT may result in supervised execution, holding, bounded continuation, or other constrained execution modes.

Non-Goals

SOGA stable interfaces do not define:

* Production deployment topology
* Distributed service architecture
* Multi-hop wire protocol
* Cloud scaling strategy
* Specific identity provider requirements
* Required authorization protocol

Core Principle

Protocols carry evidence.

SOGA evaluates legitimacy.

The PDP governs.

The CDP is the API.

