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
