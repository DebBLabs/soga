# M01 Strict HTTP Transport — Preparation Evidence

Date: 2026-09-05  
Role: Codex, Implementer  
Scope: localhost validation only

The prepared `StrictJsonPostTransport` makes one explicit JSON POST with no
discovery, redirect following, or automatic retry. It requires a bounded
timeout in `(0, 5]` seconds, bounds responses to at most 65,536 bytes, requires
a 2xx JSON-object response, and reports transport failures without claiming a
physical outcome. Target, endpoint, semantic action, idempotency, neutral
return, and truthful physical-state handling remain enforced by the reviewed
`MistySignalLightAdapter` and runtime.

The transport was exercised only against an ephemeral `127.0.0.1` HTTP server.
No request was sent to Misty during implementation or tests.

Before physical execution, the exact checkpoint must pass both independent
gates and the PI must authorize the current run binding and visible LED action.

## Exact terminal construction path

`scripts/run_m01_physical.py` wires the reviewed mission, adopted platform ID,
strict transport, signal adapter, one-second wait, and terminal confirmation.
It requires an explicit API base URL and the future Physical Execution
Authorization identifier `D-032`; without both, it exits before constructing a
session or sending any request. The only physical-run confirmation text accepted
is `EXECUTE m01.signal_light`.
