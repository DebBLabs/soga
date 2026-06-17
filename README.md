# SOGA

## Subject-Oriented Governance Architecture

SOGA is an execution-time governance layer.

It evaluates whether delegated authority remains legitimate when execution is requested.

SOGA does not replace identity, authorization, or delegation systems.

Instead, SOGA evaluates whether delegated authority should still be exercised now.

---

## The Problem

Authentication answers:

Who are you?

Authorization answers:

What are you allowed to do?

Governance answers:

Should this still be allowed now?

Execution-time legitimacy may depend on:

- Subject Agency State
- Mission status
- Reachability
- Execution context
- Policy constraints
- Authority evidence

These conditions may change after delegation is issued.

---

## Three Claims

### 1. Protocol changes do not change governance outcomes

The same governance evaluation should produce the same result regardless of whether delegation evidence arrives through AAuth, UCAN, ZCAP, or another protocol.

### 2. Subject Agency State changes do change governance outcomes

Governance outcomes may change when the subject's condition changes, even when authority evidence remains unchanged.

### 3. RESTRICT is a real execution path

RESTRICT is not a softened DENY.

It is a first-class governance outcome that enables constrained execution, supervision, bounded continuation, or holding behavior when execution remains possible under additional governance conditions.

---

## Start Here

For a first-time review, begin with:

1. docs/START_HERE.md
2. Governance Overview
3. Canonical Caregiver Scenario
4. Governance View Pattern Verification
5. Repository Inventory

These artifacts explain:

- Why SOGA exists
- How it works
- What governance decisions look like
- How the model generalizes across missions

---

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

Canonical Decision Package (CDP)

↓

Execution / Policy Enforcement Point (PEP)

The Canonical Decision Package (CDP) is the governance artifact produced for each execution event.

---

## Demonstrations

Protocol Independence

python3 -m tools.protocol_independence_demo

Subject Agency State

python3 -m tools.subject_agency_state_demo

Mission Intake to CDP

python3 -m tools.mission_to_cdp_demo

Additional demonstrations

python3 -m tools.restrict_visibility_demo

python3 -m tools.canonical_caregiver_scenario

python3 -m tools.governance_view_demo

---

## Regression

Run the frozen regression suite:

python3 -m tools.cdp_regression

Expected result:

CDP REGRESSION PASS: 10 use cases, 38 canonical decision packages

---

## Current Status

Current repository status:

- Protocol-independent Governance PDP
- Canonical Decision Package architecture
- Subject Agency State governance model
- Mission Intake pipeline
- Multi-agent advisory evidence support
- Frozen regression suite

---

## Specifications

Primary specification:

docs/canonical_decision_package_v0_1.md

Additional architecture references:

docs/service_map_v0_1.md

docs/stable_interfaces_v0_1.md

docs/repository_curation_v0_1.md

docs/agent_evidence_model_v0_1.md

docs/mission_working_representation_v0_1.md

---

## Protocol Ecosystem Alignment

Current protocol proofs include:

- AAuth
- UCAN
- ZCAP

SOGA does not depend on any particular delegation, authorization, or identity protocol.

Protocol-specific authority evidence is normalized into a common Runtime Envelope before governance evaluation.

The Governance PDP evaluates execution-time legitimacy independently of the originating protocol, allowing the same governance semantics to be applied across heterogeneous ecosystems.

Additional protocol adapters may be added without changing:

- Governance PDP semantics
- Canonical Decision Package structure
- Policy Enforcement Point behavior

Community-contributed protocol adapters are encouraged.

---

## Scope

This repository is a reference implementation of SOGA governance semantics.

It does not prescribe:

- Production deployment topology
- Distributed service architecture
- Approval service design
- Notification architecture
- Network-scale implementation strategy

