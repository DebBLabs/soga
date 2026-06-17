# Reference Mission: Birthday Gift Purchase

## Status

Reference Mission v0.1

---

## Scenario

Bob wishes to purchase a birthday gift for his niece.

He delegates this task to his personal agent.

---

## Objective

Purchase an appropriate birthday gift and arrange delivery before the birthday.

---

## Preferences

- Stay near the target budget.
- Prefer highly rated items.
- Prefer delivery before the birthday.
- Prefer a gift consistent with prior purchases.

---

## Hard Constraints

- Do not exceed $100 without additional authorization.
- Do not change the shipping address.
- Do not purchase prohibited items.
- Do not disclose personal information beyond what is necessary.

---

## Fallback Behaviors

If no acceptable gift exists within the preferred budget:

- Search for equivalent alternatives.

If only acceptable options exceed the preferred budget:

- Hold execution.
- Request confirmation from the subject or designated delegate.

If the subject is temporarily unreachable:

- Follow previously authorized fallback rules.

If the subject is in a governance state that prohibits autonomous execution:

- Return a RESTRICT or DENY decision as appropriate.

---

## Governance Questions

This mission tests:

- Preference vs. hard constraint
- Execution-time evaluation
- Subject reachability
- Fallback behavior
- RESTRICT vs. DENY outcomes

---

## Notes

This mission is intentionally protocol-independent.

It should be projectable into AAuth, UCAN, ZCAP, and future delegation mechanisms while preserving its governance semantics.
