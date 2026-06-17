# SOGA Service Map v0.1

Status: Sprint 8 Launch Package  
Purpose: Map the notional SOGA architecture to the current reference implementation.

## Scope

This document describes SOGA reference implementation service boundaries.

It does not define a required production deployment topology.

SOGA may be deployed as libraries, services, gateways, policy components, or integrated governance infrastructure.

## Architecture Flow

```text
Human Intent
     |
     v
Mission Intake Service
     |
     v
Canonical Mission Representation
     |
     v
Protocol Adapter Layer
     |
     v
Runtime Envelope Service
     |
     +--> Subject / Person State Boundary
     +--> Authority Evidence
     +--> Advisory Agent Evidence
     |
     v
Governance PDP Service
     |
     v
Canonical Decision Package Service
     |
     v
Execution / PEP Service
Mission Intake Service

Purpose:

Convert human intent into a Canonical Mission Representation.

Boundary:

Representation only. No governance decision.

Current implementation:

* intake/*
* builders/mission_builder.py
* intake/cmr_builder.py
* intake/cmr_source.py

Protocol Adapter Layer

Purpose:

Normalize protocol-specific delegation or authority evidence into SOGA-compatible inputs.

Boundary:

Protocols carry delegation and authority evidence. They do not decide governance outcomes.

Current implementation:

* input_adapters/*
* builders/protocol_projection.py

Runtime Envelope Service

Purpose:

Carry mission, subject, delegation, execution context, and advisory evidence into governance evaluation.

Boundary:

The Runtime Envelope is input to governance. It is not itself a governance decision.

Current implementation:

* verify/runtime_envelope.py
* verify/runtime_envelope_model.py

Subject / Person State Boundary

Purpose:

Represent Subject Agency State, reachability, and subject capability context.

Boundary:

Current implementation is local/reference only. Person Server integration is a future boundary.

Current implementation:

* verify/runtime_envelope_model.py
* engines/subject_capability_loader.py
* data/subjects/*

Advisory Agent Evidence Service

Purpose:

Carry advisory agent evidence, disagreement, confidence, and provenance.

Boundary:

Evidence only. No governance authority.

Current implementation:

* advisory/*

Governance PDP Service

Purpose:

Evaluate execution-time legitimacy and produce governance determinations.

Boundary:

The PDP is the sole governance authority.

Current implementation:

* verify/governance_pdp.py
* engines/runtime_governance_engine.py
* engines/runtime_dimension_evaluator.py
* engines/restrict_mode_selector.py

Canonical Decision Package Service

Purpose:

Package governance determinations into the Canonical Decision Package artifact.

Boundary:

The CDP is the API boundary for downstream consumers.

Current implementation:

* verify/canonical_decision_package.py
* verify/decision_package_builder.py
* engines/canonical_decision_package_adapter.py

Execution / PEP Service

Purpose:

Enforce or execute based on the governance result.

Boundary:

Execution consumes governance decisions and CDPs. It does not reconstruct governance logic.

Current implementation:

* execution/simple_pep.py
* engines/execution_orchestrator.py
* engines/restrict_execution_engine.py

Regression and Use Case Runner

Purpose:

Run the frozen use cases and confirm CDP generation across domains.

Current implementation:

* tools/run_use_case.py
* tools/cdp_regression.py
* use_cases/*

Public Demonstration Surface

Purpose:

Demonstrate the primary SOGA claims.

Current implementation:

* tools/protocol_independence_demo.py
* tools/subject_agency_state_demo.py
* tools/restrict_visibility_demo.py
* tools/mission_to_cdp_demo.py
* tools/multi_agent_cdp_demo.py

Supporting Proofs

These files remain useful as supporting protocol and execution proofs, but are not the primary README path.

* tools/aauth_runtime_envelope_v0_1_proof.py
* tools/ucan_runtime_envelope_v0_1_proof.py
* tools/zcap_runtime_envelope_v0_1_proof.py
* tools/pep_end_to_end_proof.py
* monitor.py

Historical / Review Classification

These files are retained for history or dependency review but are not part of the launch path.

* tools/input_adapter_proof.py
* tools/runtime_proof.py
* verify/run_demo.py
* verify/phase1b_core.py

Note: verify/phase1b_core.py still has active dependencies and should not be removed until dependencies are extracted.

Locked Boundaries

* Protocols carry delegation and authority evidence.
* SOGA evaluates execution-time legitimacy.
* Advisory agents contribute evidence only.
* The PDP is the sole governance authority.
* The CDP is the canonical output.
* One authoritative CDP exists per execution event.
* Execution and visualization consume the CDP; they do not recreate governance logic.

Production Deployment Note

This repository is a reference implementation of SOGA governance semantics.

It does not prescribe production service topology, distributed deployment architecture, multi-hop network architecture, or scaling strategy.
