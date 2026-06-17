# Reference Mission: Bounded Investment Rebalancing

## Status

Reference Mission v0.1

---

## Scenario

A Subject authorizes a Subject Agent to rebalance a small investment portfolio within predefined risk and capital boundaries.

---

## Objective

Rebalance the portfolio to remain aligned with the Subject's declared investment preferences and risk tolerance.

---

## Preferences

- Prefer low-cost index funds.
- Prefer minimal tax impact.
- Prefer small adjustments over large reallocations.
- Prefer avoiding unnecessary interruptions.

---

## Hard Constraints

- Never exceed the authorized capital limit.
- Never increase the declared risk category without authorization.
- Never execute trades outside approved asset classes.
- Never continue if market conditions invalidate the delegated bounds.

---

## Fallback Behaviors

If a rebalance exceeds the authorized boundary:

- Hold execution.

If market volatility exceeds the mission threshold:

- Pause and request review.

If the Subject is unreachable:

- Continue only within conservative predefined limits.

If the requested adjustment violates hard constraints:

- Return DENY.

---

## Governance Questions

- Financial fiduciary boundaries
- Preference versus hard constraint
- Runtime market context
- Autonomous background execution
- RESTRICT versus DENY

---

## Notes

This mission tests whether execution remains legitimate when financial conditions change after authority was delegated.
