# M02 Stage 3A-R3 Corrected Diagnostic Preflight Evidence

Date: 2026-09-09

Executed commit: `bd7619642b005d180543984f182667fae060a664`

Decision boundary: D-050

Result: **NEGATIVE CONTAINMENT RESULT WITH POSITIVE CAUSAL DISCRIMINATION**

## Scope

D-050 authorized one execution of the exact committed, independently reviewed
`tools/m02_stage3ar3/preflight.py`. The run used only the previously accepted,
cached, full-digest Node image and synthetic resources. It did not run
`candidate_startup.py` or mount, import, serve, start, or contact Freewallet or
WAS.

## Command and status

```text
python3 tools/m02_stage3ar3/preflight.py
```

Process exit status: `1`.

## Complete bounded output

```json
{"control": "internal_network", "gateway": "172.19.0.1", "result": "PASS"}
{"attempt": 1, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 4, "result": "WAIT"}
{"attempt": 2, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 205, "result": "WAIT"}
{"attempt": 3, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 409, "result": "WAIT"}
{"attempt": 4, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 614, "result": "WAIT"}
{"attempt": 5, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 820, "result": "WAIT"}
{"attempt": 6, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 1022, "result": "WAIT"}
{"attempt": 7, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 1224, "result": "WAIT"}
{"attempt": 8, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 1427, "result": "WAIT"}
{"attempt": 9, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 1632, "result": "WAIT"}
{"attempt": 10, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 1834, "result": "WAIT"}
{"attempt": 11, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 2038, "result": "WAIT"}
{"attempt": 12, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 2243, "result": "WAIT"}
{"attempt": 13, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 2448, "result": "WAIT"}
{"attempt": 14, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 2650, "result": "WAIT"}
{"attempt": 15, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 2855, "result": "WAIT"}
{"attempt": 16, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 3060, "result": "WAIT"}
{"attempt": 17, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 3263, "result": "WAIT"}
{"attempt": 18, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 3468, "result": "WAIT"}
{"attempt": 19, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 3668, "result": "WAIT"}
{"attempt": 20, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 3873, "result": "WAIT"}
{"attempt": 21, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 4076, "result": "WAIT"}
{"attempt": 22, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 4281, "result": "WAIT"}
{"attempt": 23, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 4483, "result": "WAIT"}
{"attempt": 24, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 4688, "result": "WAIT"}
{"attempt": 25, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 4893, "result": "WAIT"}
{"attempt": 26, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 5095, "result": "WAIT"}
{"attempt": 27, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 5301, "result": "WAIT"}
{"attempt": 28, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 5504, "result": "WAIT"}
{"attempt": 29, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 5709, "result": "WAIT"}
{"attempt": 30, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 5913, "result": "WAIT"}
{"attempt": 31, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 6118, "result": "WAIT"}
{"attempt": 32, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 6323, "result": "WAIT"}
{"attempt": 33, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 6529, "result": "WAIT"}
{"attempt": 34, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 6731, "result": "WAIT"}
{"attempt": 35, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 6933, "result": "WAIT"}
{"attempt": 36, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 7138, "result": "WAIT"}
{"attempt": 37, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 7339, "result": "WAIT"}
{"attempt": 38, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 7543, "result": "WAIT"}
{"attempt": 39, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 7745, "result": "WAIT"}
{"attempt": 40, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 7950, "result": "WAIT"}
{"attempt": 41, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 8151, "result": "WAIT"}
{"attempt": 42, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 8353, "result": "WAIT"}
{"attempt": 43, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 8559, "result": "WAIT"}
{"attempt": 44, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 8763, "result": "WAIT"}
{"attempt": 45, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 8968, "result": "WAIT"}
{"attempt": 46, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 9171, "result": "WAIT"}
{"attempt": 47, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 9374, "result": "WAIT"}
{"attempt": 48, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 9578, "result": "WAIT"}
{"attempt": 49, "category": "ConnectionRefusedError", "control": "nonce_attempt", "elapsed_ms": 9783, "result": "WAIT"}
{"control": "containment_preflight", "error": "loopback nonce endpoint did not become ready", "result": "FAIL"}
{"binding": "{\"46321/tcp\":[{\"HostIp\":\"127.0.0.1\",\"HostPort\":\"46321\"}]}", "binding_status": 0, "control": "container_diagnostic", "logs": "LISTENING_OK", "logs_status": 0, "result": "OBSERVED", "state": {"error": "", "exit_code": 0, "oom_killed": false, "running": true}, "state_status": 0}
{"category": "nonce_match", "control": "container_self_readiness", "detail": "", "exit_status": 0, "result": "PASS"}
{"control": "cleanup", "result": "PASS"}
```

## Findings

The corrected timing defect is no longer a plausible explanation: the host
made 49 bounded attempts over approximately 9.8 seconds and every attempt
received `ConnectionRefusedError`.

The synthetic server itself was healthy at the diagnostic point:

- Docker state reported the container running, exit code `0`, not OOM-killed,
  and no recorded container error;
- Docker recorded the requested host binding as
  `127.0.0.1:46321` to container port `46321/tcp`;
- the bounded container logs contained `LISTENING_OK`;
- the bounded self-readiness probe received the expected nonce and passed.

Within this exact tested topology, the server was serving inside its container
while the host could not establish the published literal-loopback connection.
This discriminates the observed failure as a host-publication-path failure for
the combination tested: Docker Desktop on this host, the internal bridge,
literal-loopback publication, exact image digest, script commit, and controls.

The run does not establish which Docker Desktop component or rule refused the
host connection. It does not establish that all internal Docker networks behave
this way on other hosts or versions, and it does not authorize weakening the
internal-network boundary.

Because the host nonce never became ready, the script failed before the later
non-loopback-host and container-egress negative controls. The complete
containment preflight therefore did not pass, and no candidate may start.

## Independent cleanup verification

After process exit, separate read-only checks confirmed:

- no container matching `soga-m02-r3` remained;
- no Docker network matching `soga-m02-r3` remained;
- no TCP listener remained on host port `46321`;
- no TCP listener remained on host port `46322`.

Local HEAD and `origin/main` both remained at the executed commit
`bd7619642b005d180543984f182667fae060a664`. The only remaining working-tree
item before this report was the unrelated untracked PI routine-tool-approval
proposal. It was not read or modified by the diagnostic.

The exact digest-pinned Node image remains cached as the accepted D-046 input,
and Docker Desktop remains running.

## Boundary after execution

The one D-050 execution has been consumed. Candidate startup remains
prohibited. Any script modification, additional diagnostic or preflight run,
non-internal comparison, alternative containment design, or candidate access
requires separately reviewed and prospectively authorized work. Stage 3B and
all D-050 exclusions remain in force.
