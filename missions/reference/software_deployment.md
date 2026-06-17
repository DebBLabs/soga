# Reference Mission: Software Deployment Under Approval

## Status

Reference Mission v0.1

---

## Scenario

Bob delegates software deployment to an enterprise deployment agent.

Deployment has been approved but execution may occur hours later.

---

## Objective

Deploy the approved software update safely.

---

## Preferences

- Minimize downtime.
- Deploy during maintenance window.
- Preserve rollback capability.

---

## Hard Constraints

- Never deploy outside the approved window.
- Never exceed approved scope.
- Never bypass required approvals.

---

## Fallback Behaviors

If the maintenance window closes:

- Hold execution.

If approval is revoked:

- Deny execution.

If deployment partially succeeds:

- Follow rollback policy.

---

## Governance Questions

This mission tests:

- Session versus mission
- Approval versus execution
- Execution-time governance
- Revocation
- RESTRICT versus DENY

---

## Notes

Authorization may have been valid when the mission was created.

SOGA evaluates whether execution remains legitimate at execution time.
