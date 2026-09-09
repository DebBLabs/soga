# M02 Stage 3A-R4 IPv6 Control Diagnosis Proposal

Date: 2026-09-09

Status: **PROPOSED — NOT AUTHORIZED FOR IMPLEMENTATION OR EXECUTION**

Governing checkpoint: `254d2fe1b662c01a1cba5bd9dbe663c89f2f26d3`

Governing decision: D-054

## Purpose

Determine which condition produced the accepted R4 `ipv6_present` category
without testing reachability, starting a server, publishing a port, or accessing
either candidate.

The diagnosis is limited to distinguishing:

- non-loopback IPv6 address records;
- IPv6 default-route records associated with `lo`;
- IPv6 default-route records associated with a non-loopback interface; and
- the kernel IPv6-disable settings visible inside the diagnostic container.

It does not decide that loopback-associated state is safe, relax the R4 control,
or authorize another R4 preflight. Any policy change requires a later proposal
grounded in the diagnostic evidence.

## Evidence basis

D-054 accepts the single R4 run as a negative result. Docker network inspection
reported `Internal=true`, `Attachable=false`, and `EnableIPv6=false`. Server
endpoint inspection found no Docker-reported IPv6 address or gateway. The
separate kernel probe then returned `ipv6_present`, a combined category produced
when either `/proc/net/if_inet6` contains a non-`lo` address or
`/proc/net/ipv6_route` contains any default-route record.

Because the route check did not filter by interface, a loopback-associated
kernel route record could trigger the same category as a non-loopback default
route. The accepted evidence does not establish which condition occurred or
that any usable IPv6 reachability existed.

Docker's current networking documentation confirms that Docker Desktop has
separate default-networking-mode and DNS-resolution settings and that custom
bridge IPv6 can be enabled or disabled. Configuration labels therefore remain
evidence about Docker configuration, not a substitute for the in-container
kernel observation.

Primary Docker references:

- <https://docs.docker.com/desktop/features/networking/networking-how-tos/>
- <https://docs.docker.com/engine/network/drivers/bridge/#use-ipv6-in-a-user-defined-bridge-network>

## Environmental changes since the accepted run

After D-054 evidence collection, the PI manually created and attempted to start
the Docker-generated container `nifty_hawking` from the already cached Node
image. Read-only inspection found it stopped normally with exit status `0`, no
mounts, no published ports, and the ordinary Docker `bridge` network. It is not
an R4 resource and must not be started, removed, inspected beyond the bounded
preflight inventory, or treated as evidence for this diagnosis.

The PI also enabled Docker MCP Toolkit and signed into Docker Desktop. Docker's
documentation states that its MCP Gateway may run automatically in the
background and may start isolated MCP-server containers when a configured tool
is invoked. No conclusion is made that enabling the setting created a visible
container or affected the R4 result.

Primary Docker MCP references:

- <https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/>
- <https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/>

These are environmental deltas. Any authorized diagnosis must record a bounded
pre-start inventory. The objective environmental holdpoint is zero
pre-existing running Docker containers and zero Docker-published host ports;
either nonzero count stops the diagnosis before creation. This bounded check
does not identify an MCP component, inspect MCP-private state, or prove that no
background MCP component exists. It must not invoke
`docker mcp`, enable or disable a feature, open a catalog or profile, install or
start an MCP server, use a Docker MCP tool, log in, log out, or contact Docker
Hub or another external service.

## Proposed sequence

### Phase 1 — Create a diagnostic script only

After this complete proposal receives PASS from both gates and the PI
prospectively authorizes Phase 1, create—but do not execute—a new diagnosis
script distinct from every R3 and R4 preflight script.

The script must:

1. use the exact cached, full-digest `linux/arm64` Node `v24.20.0` image accepted
   under D-046 with `--pull=never`;
2. use fixed diagnostic names distinct from R3, R4, `nifty_hawking`, and the
   legacy A2A/GNAP resources;
3. perform a bounded read-only inventory of Docker containers, networks, and
   Docker-published host ports before creation. The script may list resources
   internally only to compute normalized counts, fixed-name collisions, the
   count of pre-existing running Docker containers, and the count of
   Docker-published host ports. It may identify `nifty_hawking` only by the
   fixed name already supplied by the PI. It must emit only those counts and
   fixed-name collision categories; it must not emit arbitrary user resource
   names, images, labels, ports, addresses, credentials, profiles, or MCP data;
4. stop before creation if any fixed diagnostic resource exists, any
   pre-existing Docker container is running, or any Docker-published host port
   exists. These are the complete objective environmental holdpoints; the
   script must not try to classify a resource as MCP-related. Zero counts must
   be recorded only as observations, not proof that no background MCP
   component exists;
5. create one non-attachable `Internal=true`, IPv6-disabled bridge and one
   disposable, non-root, read-only, capability-free diagnostic container with
   no host publication, additional network, namespace sharing, Docker socket,
   host mount, server, client, or long-running application. The bounded procfs
   read is the container's own single command; it emits the normalized result
   and exits rather than being kept alive or inspected with a later exec;
6. apply `no-new-privileges`, bounded tmpfs, CPU, memory, PID, subprocess, and
   total execution-time limits;
7. read only `/proc/net/if_inet6`, `/proc/net/ipv6_route`, and
   `/proc/sys/net/ipv6/conf/*/disable_ipv6` inside the container;
   require exactly six whitespace-delimited fields for every nonblank
   `if_inet6` record and exactly ten for every nonblank `ipv6_route` record;
   treat the final field as the interface name only after the complete record
   shape passes validation;
8. emit only normalized categories and counts:
   - count of non-loopback IPv6 address records;
   - count of default-route records whose interface field is `lo`;
   - count of default-route records whose interface field is not `lo`;
   - whether `disable_ipv6` is `0`, `1`, missing, or unreadable for `all`,
     `default`, `lo`, and each non-loopback interface, using a redacted stable
     interface index rather than an interface name;
9. emit no IPv6 address, route destination, gateway, source prefix, metric,
   flags, interface name other than literal `lo`, raw procfs line, raw Docker
   output, host address, body, token, credential, profile, or personal data;
10. fail closed on malformed field counts, an unknown route format, an
    unbounded interface set, unreadable non-absent input, output above its cap,
    subprocess timeout, or cleanup uncertainty; and
11. remove the diagnostic container and network unconditionally and make any
    success dependent on independent absence verification.

The complete script must receive PASS from both gates before commit or
execution.

### Phase 2 — One diagnosis execution

Only after the exact Phase 1 script is committed, both full-file reviews pass,
and the PI separately authorizes execution may it run once.

The result may establish only which normalized R4 condition was observed in the
new diagnostic container under the then-current Docker Desktop configuration.
It may not be represented as proof of the condition present in the already
removed D-053 containers. Consistency with the prior result is not identity with
it.

Any environmental difference from the D-053 checkpoint—including a
PI-reported Docker setting or feature change, image change, or an objective
inventory holdpoint—must be recorded and may require stopping rather than
comparison. This reporting duty does not reinstate script-side classification
of resources as MCP-related.

## Interpretation boundaries

- Non-loopback address count above zero: the strict R4 address condition is
  reproduced; usability and reachability remain untested.
- Non-loopback default-route count above zero: the strict R4 route condition is
  reproduced outside `lo`; usability and reachability remain untested.
- Only `lo` default-route records above zero: consistent with the hypothesis
  that the original combined category was triggered by loopback-associated
  kernel route state; it does not prove what occurred in the removed D-053
  container and does not by itself justify changing the R4 pass rule.
- All three counts zero: the prior result is not reproduced; no transient cause
  may be selected without further evidence.
- Any malformed, unreadable, ambiguous, or environmentally confounded result:
  diagnosis fails closed and no R4 policy changes.

Route usability, rejection, metrics, and flags are deliberately outside this
diagnosis. The result distinguishes which interface class carries a textual
default-route record; it does not determine whether that record could carry
traffic. Any usability or reject-route classification requires a separate
reviewed step.

## Required evidence

Any authorized execution must produce a standalone report containing the exact
commit, bounded pre-start inventory, complete bounded output, exit status,
interpretation, environmental differences, and independent cleanup checks.
Both gates must review the evidence. No result authorizes another preflight or
candidate access.

## Explicit nonauthorization

This proposal authorizes nothing. It permits no file creation or modification,
Docker execution, container or network creation, image or dependency operation,
MCP command, MCP tool or server use, Docker sign-in change, feature change,
external service, port publication, socket reachability probe, server, client,
candidate startup or access, Freewallet or WAS execution, wallet interaction,
Person Server integration, Stage 3B code or tests, personal data, payment,
Misty power or access, physical actuation, R3 protocol work, G28, or G29.

Phase 1 requires both proposal reviews and explicit PI authorization. Phase 2
requires both complete-script reviews, a committed exact script, and a separate
explicit PI authorization. Any R4 control change or additional execution
requires another reviewed proposal and PI decision.
