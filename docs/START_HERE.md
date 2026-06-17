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

For a first-time review, read these five artifacts in order:

1. `docs/governance_overview.md`
2. `docs/north_star_governance_lifecycle.md`
3. `canonical_caregiver_scenario.md`
4. `sprints/gate-3/pattern_verification.md`
5. `docs/repository_inventory_v0_1.md`

This sequence answers:

1. Why does this matter?
2. How does it work?
3. Show me.
4. Does it generalize?
5. Where does it live?

---

## Core Principle

Authentication answers:

Who are you?

Authorization answers:

What were you permitted to do?

Governance answers:

Should that authority still be exercised now?

---

## What This Repository Demonstrates

- Mission steps are the primary unit of governance.
- Protocol artifacts provide supporting evidence.
- Subject Agency State can change governance outcomes.
- RESTRICT is a first-class governance path.
- RESTRICT is not a degraded ALLOW.
- Execution consumes governance decisions; it does not recreate governance logic.

---

## Primary Review Commands

Run:

```bash
python3 -m tools.restrict_visibility_demo
python3 -m tools.subject_agency_state_demo
python3 -m tools.pep_end_to_end_proof
python3 -m tools.canonical_caregiver_scenario
python3 -m tools.governance_view_demo
python3 -m tools.cdp_regression
Expected regression result:
CDP REGRESSION PASS: 10 use cases, 38 canonical decision packages
Scope

This repository is a reference implementation of SOGA governance semantics.

It does not prescribe production deployment topology, distributed service architecture, approval service design, notification architecture, or network-scale implementation strategy.

