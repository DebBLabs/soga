# M02 Stage 3A-R4 Internal-Only Docker Containment Proposal

Date: 2026-09-09

Status: **PROPOSED — NOT AUTHORIZED FOR IMPLEMENTATION OR EXECUTION**

Governing checkpoint: `b981579bff99fda259e9e59a9b0854b70347bc8e`

Governing decision: D-051

## Purpose

Determine whether the exact Freewallet `8e806c0` and WAS teaching-server
`2090a60` build outputs can be characterized without publishing any container
port to the macOS host.

R4 replaces the failed R3 host-publication design with an internal-only Docker
network containing a synthetic server and a separate synthetic client. The
client is a test-only independent network peer; it does not settle where any
later integration-side caller will run. A successful R4 preflight would
establish only that two isolated containers can communicate over IPv4 on the
internal network while the specifically tested application-level host and
external paths remain closed. It would make no claim that Docker's embedded DNS
cannot forward queries upstream.

This proposal does not authorize a script, Docker execution, candidate access,
Stage 3B, or a production architecture.

## Evidence basis

The accepted D-051 evidence establishes, for the exact R3 topology:

- the synthetic Node server was running and returned the expected nonce to an
  in-container self-readiness probe;
- Docker recorded a literal `127.0.0.1:46321` publication request;
- the macOS host received 49 `ConnectionRefusedError` results over
  approximately 9.8 seconds;
- the later non-loopback-host and container-egress controls did not run; and
- cleanup removed the synthetic container, internal network, and fixed-port
  listeners.

The result localizes the observed failure to the tested host-publication path.
It does not identify a Docker Desktop component or rule, establish whether a
host-side listener was created, or justify weakening the internal-network
boundary.

R4 avoids that failed path rather than trying another host-publication
configuration. No host port is published. No comparison with a non-internal
Docker network is proposed.

## Proposed sequence

### Phase 1 — Create scripts only

After both gates pass this complete proposal and the PI prospectively
authorizes Phase 1, create—but do not execute—a new R4 synthetic preflight
script. Do not modify the accepted R3 preflight or candidate-startup scripts.

The complete R4 script must receive PASS from both gates before it may be
committed or executed. It must preserve:

1. the exact cached, full-digest `linux/arm64` Node `v24.20.0` image accepted
   under D-046, with `--pull=never`;
2. fixed R4 resource names distinct from all R3 names;
3. a newly created non-attachable Docker bridge with `Internal=true`;
4. two disposable containers—one synthetic server and one synthetic client—
   attached only to that internal network;
5. no `--publish`, `-p`, `-P`, host networking, Docker socket, host directory
   mount, additional network, host namespace, or namespace-sharing option such
   as `--network=container:...`, `--pid=container:...`, or
   `--ipc=container:...`;
6. read-only root filesystems, bounded tmpfs storage, non-root users, all
   capabilities dropped, `no-new-privileges`, and finite CPU, memory, PID, and
   execution-time limits;
7. nonce-based readiness and inter-container exchange without emitting bodies;
8. explicit subprocess and socket timeouts, bounded normalized diagnostics,
   unconditional best-effort cleanup, and failure if cleanup or absence
   verification fails. Pre-start collision or precondition failure must be
   reported separately from post-run cleanup failure; the script must never
   describe a pre-existing resource as a resource leaked by the attempted run.

### Phase 2 — One synthetic internal-only preflight

Only after the exact Phase 1 script is committed, both full-file reviews pass,
and the PI separately authorizes execution may it run once.

The synthetic preflight must prove all of the following:

1. the network exists with `Internal=true` and contains only the two expected
   containers. Docker inspection must also establish that IPv6 is disabled for
   the network, neither container has an assigned IPv6 address or default IPv6
   route, and the claimed result is explicitly IPv4-only;
2. neither container has a published port or an attachment to any other
   network;
3. the server becomes ready inside its container within a monotonic deadline;
4. the separate client resolves the server by its fixed container-network name
   and receives the exact nonce;
5. Docker reports no host port binding for either container, and host ports
   `46321` and `46322` remain without listeners. R4 assigns no host port; these
   inherited R3 ports are checked only to detect unintended publication or a
   conflicting pre-existing listener;
6. from both containers, bounded attempts to the two reviewed TEST-NET targets
   fail without contacting a public service;
7. the internal-network gateway and the fixed Docker Desktop alias set
   `host.docker.internal`, `gateway.docker.internal`,
   `docker.for.mac.host.internal`, `docker.for.mac.localhost`,
   `vm.docker.internal`, and `kubernetes.docker.internal` are characterized
   from both containers. Any alias in the `*.docker.internal` or
   `docker.for.mac.*` classes exposed through container configuration must be
   included. Any successful connection or response proving that a packet
   reached a gateway or host path—including `ECONNREFUSED` or another active
   refusal—constitutes disqualifying reachability. Only failure before the
   target is reachable, such as `ENETUNREACH`, `EHOSTUNREACH`, `EPERM`, or
   `EACCES`, may satisfy this control. Any broader host reachability,
   unresolved result, or need for a host listener fails the preflight;
8. DNS behavior is recorded only as bounded normalized resolution or
   no-resolution categories. Queries are limited to the server's internal
   container name, the fixed Docker Desktop aliases in control 7, and a
   reserved `.invalid` name. No public hostname may be queried. Docker's
   embedded DNS forwarder may use an upstream resolver even on an internal
   network; R4 does not characterize that forwarding path and makes no claim
   that DNS egress is absent. Any broader DNS characterization requires its own
   reviewed design and authorization. No resolved address, host LAN address,
   response body, token, credential, or personal data is emitted; and
9. both containers and the R4 network are removed and independent post-run
   checks find no R4 resource or fixed-port listener.

Ordinary refusal, timeout, absence of a route, and name-resolution failure must
remain distinguishable. Labels such as `Internal=true` are configuration
evidence, not proof of containment by themselves.

### Phase 3 — Candidate characterization holdpoint

Candidate startup is not authorized by this proposal. If every synthetic R4
control passes and both gates accept the evidence, a later proposal may request
one bounded candidate characterization using the same internal-only pattern.

That later proposal must decide how the exact candidate services and a
separate test client are placed, what read-only source/build mounts and
temporary storage are permitted, which non-mutating routes may be requested,
and how the absence of host publication and external reachability is verified.
It must retain the existing license, source-integrity, finite-limit, no-wallet-
interaction, no-write, no-Person-Server-integration, and cleanup boundaries.

An internal-only candidate result would not establish that a host process can
call the candidates. Any later SOGA or Person Server composition would require
a separately reviewed topology—potentially co-locating the bounded caller in
the internal network—and a new PI decision.

## Stop conditions

Stop without improvisation if:

- the exact digest-pinned image is absent or Docker attempts a pull, registry
  request, login, update, build, load, import, tag, or push;
- an R4 fixed-name resource already exists or either fixed host port is
  occupied;
- the network is not internal or either container joins another network;
- IPv6 is enabled, assigned, routed, or cannot be conclusively excluded from
  the R4 network and both containers;
- Docker creates any host port binding or listener;
- inter-container nonce exchange is absent, ambiguous, or exceeds its finite
  deadline;
- either container obtains unreviewed application-level host or external
  reachability;
- a gateway or Docker Desktop host-alias probe returns an active refusal or any
  other result proving target reachability, or its meaning is ambiguous;
- a DNS check would require a public hostname or the embedded resolver's
  upstream-forwarding behavior cannot remain outside the claimed result;
- a privilege, license, subscription, security, update, or network-access
  prompt appears;
- any script requires source modification, dependency work, production
  credentials, personal data, payment, or an external service; or
- cleanup cannot prove that every R4 container, network, process, and fixed-
  port listener is absent.

## Required evidence

Any authorized execution must produce a standalone report containing the exact
commit, command, full bounded output, exit status, interpretation, stop reason
if any, and independent cleanup verification. Both gates must review the
report. No successful synthetic result may be represented as candidate,
wallet, WAS, Person Server, Stage 3B, or physical-system integration.

## Explicit nonauthorization

This proposal authorizes nothing. It permits no file creation or modification,
Docker command, container or network creation, image or dependency operation,
host publication, candidate startup or access, Freewallet or WAS execution,
wallet interaction, Person Server integration, Stage 3B code or tests,
external service, public exposure, personal data, production credential,
payment, Misty power or access, physical actuation, R3 protocol work, G28, or
G29.

Phase 1 requires both independent proposal reviews followed by explicit PI
authorization. Phase 2 requires both full-script reviews, a committed exact
script, and a separate explicit PI authorization. Candidate characterization
requires a later proposal, both reviews, and another explicit PI decision.
