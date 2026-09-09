# M02 Stage 3A-R4 IPv6 Control Diagnosis Evidence

Date: 2026-09-09

Executed commit: `aac9b7d46d40bf27599d6a64866343e12111224d`

Decision boundary: D-056

Result: **NEGATIVE DIAGNOSTIC RESULT — PRE-START PUBLISHED-BINDING HOLDPOINT**

## Scope

D-056 authorized one execution of the exact committed, independently reviewed
`tools/m02_stage3ar4/ipv6_diagnosis.py`. The execution was consumed when the
process started. It stopped during bounded inventory before creating a
diagnostic network or container and before reading any in-container procfs
state.

The run did not execute the R4 preflight, test reachability, invoke MCP, start
or access a candidate, Freewallet, WAS, a Person Server, Stage 3B, an external
service, or either Misty robot.

## Command and status

```text
python3 tools/m02_stage3ar4/ipv6_diagnosis.py
```

Process exit status: `1`.

## Complete bounded output

```json
{"background_mcp_absence_proven": false, "container_count": 3, "control": "bounded_inventory", "diagnostic_container_collision": false, "diagnostic_network_collision": false, "docker_published_host_port_count": 2, "known_stopped_container_present": true, "network_count": 4, "result": "OBSERVED", "running_container_count": 0}
{"control": "precondition", "error": "Docker-published host port holdpoint", "result": "FAIL"}
{"control": "cleanup", "reason": "precondition_failed_before_creation", "result": "NOT_APPLICABLE"}
```

## Findings

The bounded inventory found three Docker containers, four Docker networks, no
running Docker container, no fixed diagnostic-name collision, and the known
stopped `nifty_hawking` container. It found two configured Docker host-port
bindings in the inspected container configurations. The exact reviewed script
counts `HostConfig.PortBindings` for both running and stopped containers, so
this is a conservative configured-binding finding; it is not evidence that two
host listeners were active.

The objective holdpoint requires both zero pre-existing running Docker
containers and zero Docker-published host-port bindings. The second condition
failed. The script stopped before image inspection, diagnostic network
creation, diagnostic container creation, or any IPv6 procfs read. It therefore
produced no IPv6 diagnosis and establishes nothing about the condition that
triggered D-053's combined `ipv6_present` category.

The output deliberately identifies no unrelated container, image, network,
port number, address, label, credential, profile, or MCP data. It also records
`background_mcp_absence_proven=false`; the zero running-container observation
does not prove that no background MCP component exists.

## Independent cleanup verification

After exit, separate fixed-scope read-only checks found:

- no container named `soga-m02-r4-ipv6-diagnosis-container`;
- no network named `soga-m02-r4-ipv6-diagnosis-network`;
- no TCP listener on inherited host port `46321`; and
- no TCP listener on inherited host port `46322`.

The cleanup record is `NOT_APPLICABLE` because the holdpoint fired before any
diagnostic resource was created. The independent absence checks confirm the
same boundary. Docker Desktop remains running. No unrelated container or
network was started, removed, renamed, or modified.

## Boundary after execution

The one D-056 execution is consumed. The result is a gated negative diagnostic
attempt, not an IPv6 finding. Any inspection intended to identify the unrelated
configured bindings, any environmental change or removal, any changed
holdpoint, script modification, additional diagnosis, R4 preflight, candidate
access, or Stage 3B work requires separate review and prospective PI
authorization. All D-056 exclusions remain in force.
