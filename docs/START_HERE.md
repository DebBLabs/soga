# Start Here

This repository contains the SOGA Governance Laboratory and reference implementation.

SOGA means **Subject-Oriented Governance Architecture**.

SOGA evaluates whether delegated authority should still be exercised at execution time.

It is not an identity protocol.

It is not an authorization protocol.

It is not a delegation protocol.

SOGA consumes authority evidence and produces governance decisions.

---

## Read These First

For a first-time review, read these artifacts in order:

1. `docs/governance_overview.md`
2. `docs/north_star_governance_lifecycle.md`
3. `docs/passive_adapter_specification_v0_1.md`
4. `knowledge/research/RESEARCH_OBSERVATIONS.md`
5. `docs/RESEARCH_METHODOLOGY.md`

This sequence answers:

1. Why does this matter?
2. How does it work?
3. What architecture is stable?
4. What has been demonstrated?
5. How is research conducted?

---

## Core Principle

Authentication answers:

Who are you?

Authorization answers:

What are you allowed to do?

Governance answers:

Should that authority still be exercised now?

---

## What This Repository Demonstrates

- Mission steps are the primary unit of governance.
- Protocol artifacts provide supporting authority evidence.
- Subject Agency State changes governance outcomes.
- RESTRICT is a first-class governance outcome.
- Execution consumes governance decisions; it does not recreate governance logic.
- Governance evaluation remains invariant across representative protocol projections.

---

## Primary Demonstrations

Canonical Caregiver Scenario

Run:

    python3 -m tools.canonical_caregiver_scenario

Demonstrates:

    RESTRICT
    → HOLDING
    → approval or new evidence
    → full re-evaluation
    → ALLOW
    → EXECUTING

Governance Invariance

Run:

    python3 tools/governance_invariance_demo.py

Subject Agency State

Run:

    python3 -m tools.subject_agency_state_demo

Regression Baseline

Run:

    python3 -m tools.regression_baseline

---

## Stable Interfaces

The following interfaces are considered stable:

- RuntimeEnvelope
- Passive Adapter
- Governance Policy Server
- Canonical Decision Package
- Capability Registry
- REST / MCP / human execution surface

---

## Canonical Outcomes

The canonical governance outcomes are:

- ALLOW — execution may proceed
- RESTRICT — authority exists but execution is held pending additional conditions, evidence, or interaction
- DENY — execution may not proceed

RESTRICT is a persistent, first-class governance outcome.

It is not a softened DENY.

---

## Research Discipline

Repository architecture evolves only after research.

Research artifacts distinguish:

- Verified
- Observed
- Hypothesis
- Future Research

See:

`docs/RESEARCH_METHODOLOGY.md`

---

## Scope

This repository is a reference implementation of SOGA governance semantics and an executable research program.

It does not prescribe:

- production deployment topology
- distributed service architecture
- approval service implementation
- notification architecture
- protocol-specific deployment models

SOGA remains protocol-neutral.

Protocol ecosystems currently represented by repository fixtures include:

- AAuth
- UCAN
- ZCAP
- OAuth/GNAP
- AIIM-style mission representations

Representative fixtures demonstrate governance invariance.

They are not claims of complete live protocol implementations.

