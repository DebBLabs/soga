# Canonical Subject Agency State Registry

Status: Draft

Purpose:

Define the common Subject Agency States used across SOGA demonstrations,
use cases, proofs, and governance scenarios.

The goal is to keep state language consistent while missions and authority
relationships vary.

---

## ACTIVE

Meaning:

The subject can act independently.

Governance Implication:

Routine mission steps may proceed if authority requirements are satisfied.

Typical Outcome:

ALLOW

---

## SUPERVISED

Meaning:

The subject can participate, but some actions require delegate or caregiver approval.

Governance Implication:

Authority may exist, but execution may require additional oversight.

Typical Outcome:

RESTRICT

Common Restriction:

Approval Required

---

## IMPAIRED

Meaning:

The subject cannot independently authorize certain actions.

Governance Implication:

Execution may be restricted or denied depending on mission requirements,
available delegates, and policy.

Typical Outcomes:

RESTRICT or DENY

---

## UNREACHABLE

Meaning:

The subject cannot be contacted for confirmation.

Governance Implication:

Execution depends on mission urgency, fallback rules, and delegated authority.

Typical Outcomes:

RESTRICT, DENY, or ALLOW under predefined fallback rules

---

## EMERGENCY

Meaning:

A time-sensitive condition changes normal governance thresholds.

Governance Implication:

Policy may allow emergency execution, require escalation, or narrow permitted actions.

Typical Outcomes:

ALLOW, RESTRICT, or DENY depending on emergency policy

---

# Usage Rules

1. Use these states consistently across scenarios.

2. Do not create new states unless the scenario requires a materially different condition.

3. Record the Subject Agency State used for each governance decision.

4. Treat state as a runtime input, not a permanent identity attribute.

5. State should be evaluated when a governed mission step requires current condition evidence.

