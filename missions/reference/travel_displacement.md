# Reference Mission: Travel Displacement

## Status

Reference Mission v0.1

---

## Scenario

Alice delegates travel management to a Subject Agent. During travel, weather and airline disruptions require replanning while the Subject is temporarily unreachable.

---

## Objective

Maintain the overall travel mission while minimizing disruption and preserving previously expressed preferences.

---

## Preferences

- Prefer direct flights.
- Prefer existing hotel reservations.
- Minimize additional cost.
- Minimize unnecessary interruptions to the Subject.

---

## Hard Constraints

- Never exceed the authorized travel budget.
- Never change the final destination.
- Never extend the trip without authorization.
- Never disclose unnecessary personal information.

---

## Fallback Behaviors

If the original flight is unavailable:

- Search for equivalent alternatives.

If all alternatives exceed the authorized budget:

- Hold execution.

If the Subject is unreachable:

- Continue only within delegated limits.

If no compliant solution exists:

- Return RESTRICT or DENY.

---

## Governance Questions

- Preferences versus hard constraints
- Fallback behavior
- Subject reachability
- Dynamic execution context
- Mission continuity

---

## Notes

This mission illustrates that execution-time governance must evaluate changing environmental conditions while preserving the Subject's delegated intent.
