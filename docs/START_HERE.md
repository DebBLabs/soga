# Start Here

This repository contains the SOGA reference implementation.

SOGA means **Subject-Oriented Governance Architecture**.

SOGA is an execution-time governance layer that evaluates whether a requested action remains legitimate when execution is requested.

It is not an identity protocol.

It is not an authorization protocol.

It is not a delegation protocol.

SOGA consumes evidence from those systems and produces a Canonical Decision Package.

## Core Principle

Protocols carry evidence.

SOGA evaluates legitimacy.

The PDP governs.

The CDP is the API.

## Recommended Reading Order

1. `README.md`
2. `docs/canonical_decision_package_v0_1.md`
3. `docs/service_map_v0_1.md`
4. `docs/stable_interfaces_v0_1.md`
5. `docs/repository_curation_v0_1.md`
6. `docs/future_deployment_considerations_v0_1.md`
7. docs/service_map_v0_1.md
8. docs/stable_interfaces_v0_1.md

## Primary Demonstrations

Run:

python3 -m tools.protocol_independence_demo
python3 -m tools.subject_agency_state_demo
python3 -m tools.mission_to_cdp_demo
Supporting Proofs

For protocol-specific review:
python3 -m tools.aauth_runtime_envelope_v0_1_proof
python3 -m tools.pep_end_to_end_proof
Regression

Run:
python3 -m tools.cdp_regression

Expected results
CDP REGRESSION PASS: 10 use cases, 38 canonical decision packages
What This Repository Demonstrates

* Protocol changes do not change governance outcomes.
* Subject Agency State changes do change governance outcomes.
* RESTRICT is a first-class execution path.
* The Canonical Decision Package is the governance artifact.
* Execution and visualization consume the CDP; they do not reconstruct governance logic.

Scope

This repository is a reference implementation of SOGA governance semantics.

It does not prescribe production deployment topology, distributed service architecture, or network-scale implementation strategy.
