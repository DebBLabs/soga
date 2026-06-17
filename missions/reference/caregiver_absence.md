# Reference Mission: Caregiver Absence Response

## Status

Reference Mission v0.1

---

## Scenario

Alice depends on a designated caregiver and a Subject Agent to coordinate daily activities. The designated caregiver becomes temporarily unreachable while the Subject Agent continues operating.

---

## Objective

Continue supporting the Subject safely while remaining within previously delegated authority.

---

## Preferences

- Minimize unnecessary interruptions.
- Continue routine activities when safe.
- Preserve the Subject's dignity and independence.
- Prefer previously established routines.

---

## Hard Constraints

- Never exceed delegated authority.
- Never create new medical or financial commitments.
- Never disclose sensitive information unnecessarily.
- Never assume new authority because the caregiver is unavailable.

---

## Fallback Behaviors

If the caregiver cannot be reached:

- Continue only previously authorized activities.

If an action exceeds delegated authority:

- Hold execution.

If another authorized delegate exists:

- Escalate according to the delegation plan.

If no safe path exists:

- Return RESTRICT or DENY.

---

## Governance Questions

- Subject reachability
- Delegated authority boundaries
- Escalation paths
- RESTRICT versus DENY
- Execution-time governance

---

## Notes

The absence of the caregiver does not automatically expand the authority of the Subject Agent. Governance must be evaluated at execution time.
