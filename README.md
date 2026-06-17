# SOGA

**Subject-Oriented Governance Architecture**

SOGA is an execution-time governance layer that evaluates whether delegated authority remains legitimate at the moment of execution.

SOGA is not an identity system.

SOGA is not an authorization protocol.

SOGA sits above delegation, authorization and identity systems and evaluates whether a requested action should still be allowed, restricted, or denied when execution is requested.

## Core Principle

Protocols carry evidence.

SOGA evaluates legitimacy.

The PDP governs.

The CDP is the API.

## The Problem

Most authorization systems answer:

- Who are you?
- What are you allowed to do?

SOGA evaluates a third question:

- Should this still be allowed now?

Execution-time legitimacy may depend on:

- Subject Agency State
- Mission status
- Reachability
- Execution context
- Policy constraints
- Authority evidence

These conditions can change after delegation is issued.

## Three Claims

### 1. Protocol changes do not change governance outcomes

The same governance evaluation should produce the same result regardless of whether delegation evidence arrives through AAuth, UCAN, ZCAP, or another protocol.

### 2. Subject Agency State changes do change governance outcomes

Governance outcomes may change when the subject's condition changes, even when authority evidence remains unchanged.

### 3. RESTRICT is a real execution path

RESTRICT is not a softened DENY.

It is a first-class governance outcome that enables constrained execution, supervision, bounded continuation, or holding behavior when execution remains possible under additional governance conditions.

## Architecture

Human Intent

↓

Mission Intake

↓

Canonical Mission Representation

↓

Protocol Adapters

↓

Runtime Envelope

↓

Governance PDP

↓

Canonical Decision Package

↓

Execution / PEP

The Canonical Decision Package (CDP) is the authoritative governance artifact produced for each execution event.

## Specification

The normative specification is:

`docs/canonical_decision_package_v0_1.md`

Additional architecture documents:

- `docs/service_map_v0_1.md`
- `docs/stable_interfaces_v0_1.md`
- `docs/repository_curation_v0_1.md`
- `docs/agent_evidence_model_v0_1.md`
- `docs/mission_working_representation_v0_1.md`

## Demonstrations

Protocol Independence
python3 -m tools.protocol_independence_demo

Subject Agency State
python3 -m tools.subject_agency_state_demo

Mission Intake to CDP
python3 -m tools.mission_to_cdp_demo

Additional demonstrations:

* tools/restrict_visibility_demo.py
* tools/multi_agent_cdp_demo.py

AAuth, UCAN, and ZCAP Proofs

Supporting protocol proofs are available for reviewers interested in protocol integration:

* tools/aauth_runtime_envelope_v0_1_proof.py
* tools/ucan_runtime_envelope_v0_1_proof.py
* tools/zcap_runtime_envelope_v0_1_proof.py
* tools/pep_end_to_end_proof.py

These proofs demonstrate protocol-specific evidence entering the same Runtime Envelope and Governance PDP.

Regression

Run the frozen regression suite:

python3 -m tools.cdp_regression

The regression suite validates governance behavior across the frozen use cases and confirms Canonical Decision Package generation across domains.

Status

Current repository status:

* Protocol-independent Governance PDP
* Canonical Decision Package architecture
* Subject Agency State governance model
* Mission Intake pipeline
* Multi-agent advisory evidence support
* Frozen regression suite

Protocol Ecosystem Alignment

Current protocol proofs include AAuth, UCAN, and ZCAP.

SOGA does not depend on any particular delegation, authorization, or identity protocol. Protocol-specific authority evidence is normalized into a common Runtime Envelope before governance evaluation.

The Governance PDP evaluates execution-time legitimacy independently of the originating protocol, allowing the same governance semantics to be applied across heterogeneous ecosystems.

Additional protocol adapters, including OAuth/OIDC/OIDF-aligned authority artifacts, GNAP-style authorization models, agent interoperability frameworks, and emerging delegated authority ecosystems, may be added without changing Governance PDP semantics, Canonical Decision Package structure, or Policy Enforcement Point behavior.

Community-contributed protocol adapters are encouraged. New delegation, authorization, identity, or agent ecosystems may be integrated by implementing the Runtime Envelope contract and demonstrating equivalent governance outcomes through the Governance PDP.

This repository is a reference implementation of SOGA governance semantics.

It does not prescribe production deployment topology, distributed service architecture, or network-scale implementation strategy.

