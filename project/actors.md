# Canonical Actor Registry

Status: Draft

Purpose:

Provide a consistent set of actors used across demonstrations,
use cases, proofs, and governance scenarios.

The goal is to expose governance invariants by keeping actors
constant while missions, states, and authority relationships vary.

---

## Alice

Role:
Subject / Principal

Description:

Alice is the person on whose behalf actions are performed.

Examples:

- Purchase gifts
- Schedule appointments
- Manage finances
- Participate in research

Subject Agency State may vary:

- ACTIVE
- SUPERVISED
- IMPAIRED
- UNREACHABLE
- EMERGENCY

---

## Beth

Role:
Caregiver Delegate

Description:

Beth assists Alice with daily activities and may approve
restricted actions when governance requires additional oversight.

Examples:

- Purchase approval
- Appointment confirmation
- Escalation recipient

Typical Governance Relationship:

RESTRICT
→ Beth Approval Required

---

## Carol

Role:
Financial Delegate

Description:

Carol has bounded financial authority on behalf of Alice.

Examples:

- Bill payment
- Budget management
- Limited financial transactions

Typical Governance Relationship:

Financial mission steps.

---

## David

Role:
Healthcare Delegate

Description:

David has authority related to healthcare coordination.

Examples:

- Appointment scheduling
- Provider coordination
- Care management activities

Typical Governance Relationship:

Healthcare mission steps.

---

## Evelyn

Role:
Governance Reviewer

Description:

Independent reviewer, auditor, compliance officer,
or governance observer.

Purpose:

Review governance decisions, audit trails,
and mission outcomes.

---

# Usage Rules

1. Reuse actors whenever possible.

2. Avoid creating new actors unless required by the use case.

3. Demonstrate governance by changing:

   - Mission
   - Mission Step
   - Subject State
   - Authority Evidence

   rather than changing actors.

4. Actors provide continuity across demonstrations.

