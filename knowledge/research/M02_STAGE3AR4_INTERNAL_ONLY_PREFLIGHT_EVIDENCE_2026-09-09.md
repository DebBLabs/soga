# M02 Stage 3A-R4 Internal-Only Synthetic Preflight Evidence

Date: 2026-09-09

Executed commit: `350e3b4287e588b659c382e3e3f84b6698183417`

Decision boundary: D-053

Result: **NEGATIVE CONTAINMENT RESULT — IN-CONTAINER IPV6 CONTROL STOP**

## Scope

D-053 authorized one execution of the exact committed, independently reviewed
`tools/m02_stage3ar4/preflight.py`. The run used only the previously accepted,
cached, full-digest Node image and synthetic resources. It did not run, mount,
import, serve, start, or contact Freewallet, WAS, a Person Server, either
candidate, Stage 3B, an external service, or either Misty robot.

## Command and status

```text
python3 tools/m02_stage3ar4/preflight.py
```

Process exit status: `1`.

## Complete bounded output

```json
{"control": "preconditions", "result": "PASS"}
{"control": "cached_image", "platform": "linux/arm64", "result": "PASS", "runtime": "node-v24.20.0-required"}
{"attachable": false, "control": "internal_ipv4_network", "expected_member_count": 0, "internal": true, "ipv6_enabled": false, "result": "PASS"}
{"attachable": false, "control": "internal_ipv4_network", "expected_member_count": 2, "internal": true, "ipv6_enabled": false, "result": "PASS"}
{"container_role": "server", "control": "container_isolation", "result": "PASS"}
{"category": "ipv6_present", "container_role": "server", "control": "container_ipv6", "result": "FAIL"}
{"control": "containment_preflight", "error": "IPv6 assignment or route not conclusively excluded: soga-m02-r4-server", "result": "FAIL"}
{"container_role": "server", "control": "container_diagnostic", "logs": "LISTENING_OK", "logs_status": 0, "result": "OBSERVED", "state": {"error": "", "exit_code": 0, "oom_killed": false, "running": true}, "state_status": 0}
{"container_role": "client", "control": "container_diagnostic", "logs": "CLIENT_READY", "logs_status": 0, "result": "OBSERVED", "state": {"error": "", "exit_code": 0, "oom_killed": false, "running": true}, "state_status": 0}
{"control": "cleanup", "result": "PASS"}
```

## Findings

The preconditions and exact cached-image check passed. Docker inspection
reported the newly created network as internal, non-attachable, and IPv6
disabled before container creation. After both containers started, a second
network inspection found exactly the two expected members and again reported
IPv6 disabled. Server inspection found only the expected network attachment,
no host port binding, no Docker-reported IPv6 address or gateway, and a running
container.

The next, independent in-container kernel check failed with normalized category
`ipv6_present`. In the committed script that category means at least one of two
conditions was observed in the server container:

- `/proc/net/if_inet6` contained an IPv6 address assigned to an interface other
  than `lo`; or
- `/proc/net/ipv6_route` contained a default-route record.

The bounded output intentionally records neither raw address nor raw route, and
the combined category does not identify which condition caused the failure.
The run therefore establishes a disagreement between the Docker-level IPv6
configuration/endpoint checks and the stricter in-container kernel control. It
does not establish usable IPv6 host or external reachability, the interface or
route involved, or whether a loopback-related kernel record contributed to the
result.

The control failed closed as required. Both synthetic processes were healthy at
the diagnostic point: the server log contained `LISTENING_OK`, the client log
contained `CLIENT_READY`, and both containers were running without an OOM or
recorded container error.

Because the first in-container IPv6 check failed, the script did not inspect the
client's isolation or IPv6 state, run the bounded server self-readiness check,
perform the separate-client nonce exchange, check the inherited ports during
the live topology, or execute any TEST-NET, gateway, Docker-host-alias, or DNS
controls. R4 containment therefore did not pass and no candidate may start.

## Independent cleanup verification

After process exit, separate read-only checks confirmed:

- no container matching `soga-m02-r4` remained;
- no Docker network matching `soga-m02-r4` remained;
- no TCP listener remained on host port `46321`;
- no TCP listener remained on host port `46322`.

Local HEAD and `origin/main` both remained at the executed commit
`350e3b4287e588b659c382e3e3f84b6698183417`. The only remaining working-tree
item before this report was the unrelated untracked PI routine-tool-approval
proposal. It was not read or modified by the preflight.

The exact digest-pinned Node image remains cached. Docker Desktop remains
running.

## Boundary after execution

The one D-053 execution has been consumed. Candidate startup and access remain
prohibited. Any script modification, additional preflight or diagnostic run,
IPv6-specific diagnosis, alternative containment design, candidate access, or
Stage 3B work requires separate review and prospective authorization. Every
D-053 exclusion remains in force.
