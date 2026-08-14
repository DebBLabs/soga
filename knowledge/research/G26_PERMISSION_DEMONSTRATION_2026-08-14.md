# G26 Permission Demonstration Record

Date: 2026-08-14

Command: `python3 tools/g26_permission_demo.py`

Canonical test: same action (`schedule_appointment`) + same immutable mission
(`s256` identical) + different subject agency state.

| State/phase | SOGA outcome | AAuth endpoint result |
|---|---|---|
| Independent | `ALLOW` | HTTP 200, `permission: granted` |
| Supervised, no evidence | `RESTRICT`, authorized `HOLDING` | HTTP 202, `requirement=approval` |
| Supervised, valid PS assertion | re-evaluated `ALLOW` | HTTP 200, `permission: granted` |

RESTRICT path exercised: **HOLDING through AAuth approval deferred response**.
The authorized constraint is `gate-supervision-required`, requires
`supervisor_confirmation`, and references `authority-caregiver-001`.

The approval record is explicitly
`provisional-g26-approval-evidence-v1`, with convergence obligation
`future-canonical-stage-gate-clearance-evidence-schema`. It records the Person
Server as asserting/authenticating party and states that approval is attributed
to a holder of the referenced authority. `Beth` is retained as supplied human
attribution; the durable event is not represented merely as “Beth approved.”

The demonstration preserves the same mission, `schedule_appointment` action,
and `SUPERVISED` subject through re-evaluation. The mechanism-specific tests
show that absent evidence, a wrong authority reference, a different constraint,
or agent-supplied forged evidence does not cause `ALLOW` or `granted`.

Mission-log entries are separate for the originating SOGA decision, AAuth
deferred projection, provisional approval evidence, SOGA re-evaluation
decision, and final AAuth projection. Explicit decline remains a polling error and does
not rewrite the originating SOGA `RESTRICT` as `DENY`.

The demonstration configures a 300-second expiry solely as demonstration
configuration. It is not a caregiver liveness-policy decision. General expiry
selection and escalation semantics remain Future Research.
