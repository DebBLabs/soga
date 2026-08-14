# G26 Permission Demonstration Record

Date: 2026-08-14

Command: `python3 tools/g26_permission_demo.py`

Canonical test: same action (`schedule_visit`) + same immutable mission
(`s256` identical) + different subject agency state.

| Subject agency state | SOGA outcome | AAuth endpoint result |
|---|---|---|
| Independent | ALLOW | HTTP 200, `permission: granted` |
| Supervised | RESTRICT (`supervised_execution`) | HTTP 202, pending interaction |

RESTRICT path exercised: **AAuth deferred response**. The response contains
`status`, `pending_id`, `pending_url`, and `requirement: interaction`. It does
not contain or imply a timeout.

The emitted mission log records the complete SOGA decision and provenance next
to, but independently from, the AAuth projection. Separate tests demonstrate
the internally discharged restriction path and the authorized `denied` plus
`reason` fallback. The fallback test verifies that its mission-log SOGA outcome
remains `RESTRICT`, not `DENY`.
