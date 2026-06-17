# Reference Mission: Incident Response Investigation

## Status

Reference Mission v0.1

---

## Scenario

An enterprise delegates authority to a Subject Agent to investigate a suspected cybersecurity incident. The investigation may continue for hours or days while system conditions evolve.

---

## Objective

Determine the scope and impact of the incident while preserving evidence and minimizing operational disruption.

---

## Preferences

- Minimize impact to production systems.
- Preserve forensic evidence.
- Prefer automated collection where possible.
- Prefer notification before disruptive actions.

---

## Hard Constraints

- Never destroy or alter evidence.
- Never exceed the delegated investigation scope.
- Never access systems outside the approved boundary.
- Never initiate remediation actions without separate authorization.

---

## Fallback Behaviors

If additional privileges are required:

- Hold execution.

If the investigation scope expands beyond authorization:

- Escalate for additional approval.

If the incident is resolved before execution:

- Terminate the mission.

If execution can no longer be justified:

- Return RESTRICT or DENY.

---

## Governance Questions

- Mission versus session
- Execution-time legitimacy
- Scope expansion
- Long-running missions
- RESTRICT versus DENY

---

## Notes

Authority granted at mission creation does not guarantee that execution remains legitimate throughout the lifetime of the investigation. Governance must be evaluated continuously at execution time.
