# SOGA Governance Overview

Status: Reviewer Overview

## Purpose

SOGA (Subject-Oriented Governance Architecture) is an execution-time governance layer.

It evaluates whether delegated authority should still be exercised when execution is requested.

SOGA does not replace identity, authorization, or delegation systems.

Instead, it consumes authority evidence from those systems and produces governance decisions.

---

## The Core Question

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

## Governance Outcomes

SOGA produces three governance outcomes:

- ALLOW
- RESTRICT
- DENY

RESTRICT is a first-class governance outcome.

RESTRICT is not a softened DENY.

RESTRICT preserves mission continuity while preventing inappropriate execution until additional governance conditions are satisfied.

---

## Mission-Centric Governance

The mission step is the primary unit of governance.

Authority evidence is supporting input.

The governance evaluation occurs at execution time.

Mission Step
→ Governance Evaluation
→ Canonical Decision Package
→ Execution Status

---

## Repository Demonstrations

The repository demonstrates:

- Protocol-independent governance evaluation
- Subject Agency State also changing governance outcomes
- RESTRICT as a first-class execution path
- Canonical Decision Package generation
- Governance View pattern verification
- Regression across multiple domains
