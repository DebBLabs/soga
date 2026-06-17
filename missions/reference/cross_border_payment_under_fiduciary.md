# Reference Mission: Cross-Border Payment Under Fiduciary

## Status

Reference Mission v0.1

---

## Scenario

Bob has delegated limited fiduciary authority to a Subject Agent to execute an approved payment to a family member living in another country. The payment may occur after changing financial or regulatory conditions.

---

## Objective

Execute the authorized payment while preserving the Subject's financial interests and complying with delegated authority.

---

## Preferences

- Minimize transaction fees.
- Prefer previously approved payment channels.
- Complete the payment promptly.
- Preserve an auditable record.

---

## Hard Constraints

- Never exceed the authorized payment amount.
- Never change the recipient.
- Never change the destination account.
- Never violate applicable legal or regulatory restrictions.

---

## Fallback Behaviors

If exchange rates exceed acceptable limits:

- Hold execution.

If additional approval is required:

- Escalate to the authorized fiduciary.

If the Subject becomes unreachable:

- Continue only within previously delegated authority.

If execution violates hard constraints:

- Return DENY.

---

## Governance Questions

- Fiduciary duty
- Execution-time authorization
- Runtime financial context
- Delegated authority boundaries
- RESTRICT versus DENY

---

## Notes

This mission demonstrates that possessing authority to make payments does not imply authority to alter payment semantics or exceed delegated boundaries.
