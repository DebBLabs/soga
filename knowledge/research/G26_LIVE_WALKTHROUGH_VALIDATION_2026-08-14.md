# G26 Continuous Live Walkthrough Validation

Date: 2026-08-14
Implementation checkpoint: `b92c18f2fe8f4ff80a827a577de42280e84dd065`
Method: one continuous in-memory `PermissionService` and loopback HTTP server;
the same mission, request, pending identifier, and agent identity were retained
through every boundary.

## Observed path

1. The canonical caregiver request retained action `schedule_appointment`,
   mission s256 `sc1Hyik6Dyhqt0qHKxwHgFOR1OszZogJYhAnXY8oi08`, and subject state
   `SUPERVISED`. SOGA returned `RESTRICT`; authorized policy selected
   `HOLDING`, `supervisor_confirmation`, and `authority-caregiver-001`.
2. The HTTP boundary returned `202 Accepted` with
   `AAuth-Requirement: requirement=approval`, same-origin unguessable
   `Location`, `Retry-After: 30`, `Cache-Control: no-store`, and the pending
   JSON body.
3. The first agent-bound GET returned the same `202` response. Deep copies of
   the complete pending record before and after compared equal; polling did not
   change pending state.
4. The scoped approval intake recorded a Person Server authenticated assertion
   attributed to Beth and to a holder of `authority-caregiver-001`. It claimed
   satisfaction of `gate-supervision-required` through
   `supervisor_confirmation` and was marked provisional with a convergence
   obligation to the future canonical Stage Gate clearance-evidence schema.
5. Approval triggered governance re-evaluation. Mission s256, action, and
   `SUPERVISED` state remained unchanged. The retained approval evidence
   satisfied the declared constraint, causing the subject-agency dimension to
   pass; all dimensions passed and SOGA returned `ALLOW`.
6. The next agent-bound poll delivered the stored terminal response exactly
   once: HTTP `200` with `{"permission": "granted"}`. Only `delivered` changed
   from `False` to `True`; no additional governance evaluation occurred.
7. A subsequent poll returned HTTP `410 Gone` with `error=invalid_code` and
   detail `Pending response already consumed.` The complete pending record and
   retained re-evaluation remained unchanged.

## Transport limitation observed

The mock server is implemented with Python `BaseHTTPRequestHandler` and emitted
response status lines using HTTP/1.0, including `HTTP/1.0 202 Accepted`,
`HTTP/1.0 200 OK`, and `HTTP/1.0 410 Gone`. The request client sent HTTP/1.1.
This is a mock-server transport limitation; the walkthrough did not establish
HTTP/1.1 response transport behavior.

No repository code was modified during the live walkthrough.
