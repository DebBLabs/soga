# Sprint 10 — Regression Strategy

Status: Planning only. No code authorized.

## Required baseline

Run:

python3 -m tools.regression_baseline

Expected:

- AAuth ACTIVE → ALLOW / EXECUTING
- UCAN ACTIVE → ALLOW / EXECUTING
- ZCAP ACTIVE → ALLOW / EXECUTING
- AAuth IMPAIRED → RESTRICT / HOLDING
- UCAN IMPAIRED → RESTRICT / HOLDING
- ZCAP IMPAIRED → RESTRICT / HOLDING

## New checks after implementation authorization

Add only after code authorization:

- envelope without interaction_context behaves unchanged
- envelope with interaction_context is accepted
- interaction_context does not alter decision semantics unless policy uses it
