# Reference Mission: Medication Refill

## Status

Reference Mission v0.1

---

## Scenario

Alice delegates medication refill management to her personal agent.

The agent may monitor refill status, communicate with the pharmacy, and arrange delivery.

---

## Objective

Ensure medication is refilled and delivered before the existing supply is exhausted.

---

## Preferences

- Prefer home delivery.
- Prefer the existing pharmacy.
- Minimize cost.
- Avoid unnecessary interruptions to the subject.

---

## Hard Constraints

- Never refill medications that require additional authorization.
- Never change prescribing physician.
- Never substitute medication without authorization.
- Never expose protected information unnecessarily.

---

## Fallback Behaviors

If delivery cannot occur:

- Attempt pickup alternatives.

If refill requires physician approval:

- Pause execution.
- Notify the appropriate party.

If the subject becomes unreachable:

- Continue only within previously authorized bounds.

If execution exceeds delegated authority:

- Return RESTRICT or DENY.

---

## Governance Questions

This mission tests:

- Long-running missions
- Subject reachability
- Execution-time evaluation
- Escalation paths
- Healthcare delegation

---

## Notes

The same mission should produce identical governance decisions regardless of whether execution is projected through AAuth, UCAN, ZCAP, or future protocols.
