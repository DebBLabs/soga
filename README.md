# SOGA

## Subject-Oriented Governance Architecture

SOGA is an execution-time governance layer implemented as a
composable Governance Policy Server.

It evaluates whether delegated authority remains legitimate
when execution is requested — regardless of the protocol,
platform, or ecosystem that established that authority.

SOGA does not replace identity, authorization, or delegation
systems. It governs whether delegated authority should still
be exercised now.

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
- Mission status and constraints
- Reachability
- Execution context
- Policy constraints
- Authority evidence

These conditions may change after delegation is issued.

---

## Three Claims

### 1. Governance decisions are invariant across ecosystems

When authority, mission intent, constraints, and runtime state
are semantically equivalent, the governance decision is identical
regardless of mission origin or execution capability.

This has been demonstrated across five protocol ecosystems:
AAuth, UCAN, ZCAP, OAuth/GNAP, and AIIM-style missions.

### 2. Subject Agency State changes do change governance outcomes

Governance outcomes may change when the subject's condition
changes, even when authority evidence remains unchanged.

### 3. RESTRICT is a real execution path

RESTRICT is not a softened DENY.

It is a first-class governance outcome that enables constrained
execution, supervision, bounded continuation, or holding
behavior when execution remains possible under additional
governance conditions.

---

## Architecture

```
Ecosystem Payload (representative fixture)
        ↓
Passive Adapter (ecosystem-neutral projection)
        ↓
Canonical RuntimeEnvelope
(structured mission constraints + authority evidence)
        ↓
SOGA Governance Policy Server (GovernancePDP)
        ↓
Canonical Decision Package
(CDP + governance_reasoning_token)
        ↓
Execution / Policy Enforcement Point (PEP)
```

The Governance Policy Server evaluates the canonical
RuntimeEnvelope. It does not require knowledge of the
originating protocol, platform, or ecosystem.

Passive adapters absorb ecosystem specificity.
Governance evaluates canonical representations.

---

## Ecosystem Neutrality

SOGA is designed to remain ecosystem-neutral.

Current protocol adapters:

- AAuth
- UCAN
- ZCAP
- OAuth/GNAP
- AIIM-style (healthcare mission representation)
- MCP (capability surface)

Each ecosystem is projected through a passive adapter into
the canonical RuntimeEnvelope. The Governance Policy Server
evaluates the same canonical structure regardless of origin.

Additional protocol adapters may be added without changing:

- Governance Policy Server semantics
- Canonical Decision Package structure
- RuntimeEnvelope structure
- Policy Enforcement Point behavior

See: docs/passive_adapter_specification_v0_1.md

---

## Governance Invariance Demonstration

The primary demonstration verifies governance invariance
across five protocol ecosystems.

```bash
python3 tools/governance_invariance_demo.py
```

Expected output:

```
Governance Invariance Demonstration
Scenario: Caregiver Discharge Follow-Up

Origin                   Capability   Decision   Token
────────────────────────────────────────────────────────────
AAuth             REST         RESTRICT   supervision_required
UCAN              REST         RESTRICT   supervision_required
ZCAP              REST         RESTRICT   supervision_required
OAuth/GNAP        REST         RESTRICT   supervision_required
AIIM              REST         RESTRICT   supervision_required

Governance decision: INVARIANT
GovernancePDP:       UNCHANGED
RuntimeEnvelope:     UNCHANGED
```

This demonstration exercises:
- Real passive adapters for each ecosystem
- Real GovernancePDP evaluation
- Real Canonical Decision Package output
- Representative static payload fixtures

Only external transports and live protocol services
are represented by static fixtures.

---

## Additional Demonstrations

Behavioral demonstrations:

```bash
python3 -m tools.subject_agency_state_demo
python3 -m tools.canonical_caregiver_scenario
python3 -m tools.restrict_visibility_demo
python3 -m tools.governance_view_demo
```

Mission constraints demonstration:

```bash
python3 tools/mission_constraints_demo.py
```

---

## Regression

Run the verified regression baseline:

```bash
python3 -m tools.regression_baseline
```

Expected result:

```
AAuth ACTIVE:    ALLOW / EXECUTING
UCAN ACTIVE:     ALLOW / EXECUTING
ZCAP ACTIVE:     ALLOW / EXECUTING
AAuth IMPAIRED:  RESTRICT / HOLDING
UCAN IMPAIRED:   RESTRICT / HOLDING
ZCAP IMPAIRED:   RESTRICT / HOLDING

All baseline cases passed.
```

---

## Scientific Research Foundations

SOGA is developed as an executable research program.
The following research observations have been captured
and logged in knowledge/research/RESEARCH_OBSERVATIONS.md:

**RO-001 — Governance Normalization**
Governance normalization is a distinct scientific problem.
Adjacent work exists (Subjective Logic, policy reasoning,
runtime safety) but no existing framework addresses the
complete chain: heterogeneous observations → governance
significance → delegated authority context → execution-time
decision support.
Status: Confirmed research direction.

**RO-002 — Evidence Sufficiency for Governance Decisions**
When is there sufficient evidence to safely exercise
delegated authority? The required evidence threshold
scales with consequence severity.
Status: Captured. Deferred pending future research.

**RO-003 — The Projection Pattern**
A consistent structural pattern appears independently
across four architectural layers:
Authoring Representation → Projection →
Canonical Runtime Representation →
Governance Evaluation → Canonical Decision Package.
Status: Open research observation.

**RO-004 — Governance Invariance**
When authority, mission intent, constraints, and runtime
state are semantically equivalent, the governance decision
is identical regardless of mission origin or execution
capability. Demonstrated across five protocol ecosystems.
Status: Empirically demonstrated (Sprint A and Sprint B).

---

## Mission Constraints

Missions may carry explicit governance constraints:

```
mission:
  objective
  delegated_authority
  constraints:
    global         (supervision_required, execution_window)
    stage_gate     (named boundaries requiring human clearance)
    delegation     (redelegation_depth, sub-agent bounds)
  forbidden_conditions
```

Mission constraints are projected into the canonical
RuntimeEnvelope as soga_constraints and carry a
governance_reasoning_token identifying which constraint
triggered the governance decision.

---

## Stable Interface Documents

- docs/stable_interfaces_v0_1.md
- docs/passive_adapter_specification_v0_1.md
- docs/canonical_decision_package_v0_1.md
- docs/governance_evidence_taxonomy_v0_1.md
- docs/execution_time_observation_catalog_v0_1.md
- docs/governance_normalization_research_v0_1.md

---

## Representative Payload Fixtures

tests/fixtures/payloads/ contains representative
wire-format snapshots for each supported ecosystem.

Each fixture carries provenance identifying the
source specification and scenario it represents.

Payloads are static. Governance reports are generated
from actual CDP decisions.

---

## Start Here

For a first-time review:

1. docs/START_HERE.md
2. docs/governance_overview.md
3. tools/governance_invariance_demo.py
4. docs/passive_adapter_specification_v0_1.md
5. knowledge/research/RESEARCH_OBSERVATIONS.md

---

## Scope

This repository is a reference implementation of SOGA
governance semantics and an executable research program.

It does not prescribe:

- Production deployment topology
- Distributed service architecture
- Approval service design
- Notification architecture
- Network-scale implementation strategy

SOGA is designed to be composable. Each layer —
passive adapters, RuntimeEnvelope normalization,
Governance Policy Server, Canonical Decision Package,
PEP — may evolve independently while preserving
stable canonical interfaces.