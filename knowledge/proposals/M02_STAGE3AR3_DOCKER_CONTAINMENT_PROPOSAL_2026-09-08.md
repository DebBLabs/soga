# M02 Stage 3A-R3 Proposal — Docker Containment Characterization

Date: 2026-09-08
Status: AUTHORIZED UNDER D-044 — EXECUTION NOT YET STARTED
Prepared from checkpoint: `main @ 53f917b45690feb184f3a2fe291dbc301ea0c858`

## Purpose

Determine whether the already-installed Docker Desktop can contain the exact
Freewallet `8e806c0` and WAS teaching server `2090a60` build outputs without
weakening M02's host-facing literal-loopback or application-runtime
external-network boundaries.

The selected WAS executable binds `0.0.0.0`. In this experiment that wildcard
bind would occur only inside a disposable container network namespace. Docker
would publish the candidate port only on host `127.0.0.1`. A Docker-internal
wildcard bind is not treated as equivalent to a host wildcard bind; the
preflight must prove the actual host exposure and egress properties before any
candidate starts.

Stage 3A-R3 is containment research only. It is not Stage 3B and contains no
wallet interaction, Person Server integration, credential interpretation,
storage write, governance decision, or execution surface.

## Evidence basis and unresolved facts

- Docker CLI `28.5.2` is installed at `/usr/local/bin/docker` on this arm64
  macOS host. Whether Docker Desktop and its daemon are currently running is
  unverified because the initiating Codex sandbox could not query the user
  Docker socket.
- Docker documents that a port published with an explicit `127.0.0.1` host
  address is host-local. Docker also documents that versions before 28.0.0 had
  a same-L2 localhost-publication exposure; the installed CLI is later, but the
  daemon version must be checked independently before reliance.
- Docker documents Compose `internal: true` and `docker network create
  --internal` as externally isolated networking. It also documents that the
  network gateway may remain reachable from containers. Therefore
  `--internal` is a candidate control, not proof of complete host isolation.
- Both exact source checkouts, dependency trees, and build outputs already
  exist under `/private/tmp/m02-stage3a-20260908`. R3 authorizes no source
  reacquisition, rebuild, dependency installation, or registry access.

Primary Docker documentation used for this proposal:

- <https://docs.docker.com/engine/network/port-publishing/>
- <https://docs.docker.com/reference/compose-file/networks/#internal>
- <https://docs.docker.com/reference/cli/docker/network/create/#network-internal-mode---internal>

## Fixed names and ports

- Docker project prefix: `soga-m02-r3`
- Synthetic/candidate host port: `127.0.0.1:46321`
- Freewallet host port, if candidates are reached: `127.0.0.1:46322`
- Container network: a newly created, non-attachable internal bridge bearing
  the fixed project prefix
- Temporary evidence/data root: a fresh directory under
  `/private/tmp/m02-stage3ar3-20260908`

No substitute port, project name, network, image, source revision, or checkout
is permitted during the run.

## Phase 0 — Docker readiness and local-image inventory

After explicit PI authorization, Docker Desktop may be opened if the daemon is
not already available. Any macOS password, privileged-helper, license,
subscription, upgrade, network-access, or security prompt is a PI holdpoint;
Codex may not answer it on the PI's behalf.

The operator must then record:

1. client and server versions and architecture;
2. Docker context and daemon identity;
3. currently running containers and existing resources bearing the fixed
   project prefix;
4. whether ports `46321` and `46322` are free; and
5. locally cached images, by immutable image ID and platform, that already
   contain Node 24 or later and can run a bounded JavaScript preflight.

Use `--pull=never`. If no suitable local image exists, stop and report that
separate image acquisition would require a new reviewed decision. Do not pull,
build, tag, load, import, or alter an image in R3.

## Synthetic preflight

Nothing may mount, import, serve, or execute either candidate until every
synthetic control passes. Using only the selected locally cached image:

1. Create the fixed-name internal bridge network and verify its inspected
   configuration, including `Internal=true` and no attachment to an unrelated
   network.
2. Start one disposable synthetic container with `--pull=never`, read-only root
   filesystem, a bounded tmpfs, all Linux capabilities dropped,
   `no-new-privileges`, finite memory/CPU/PID limits, no Docker socket, no host
   namespace, no host directory mount, and only the internal network.
3. Inside the container, bind the synthetic server to `0.0.0.0:46321`. Publish
   it only as `127.0.0.1:46321:46321/tcp` on the host.
4. Prove a nonce exchange succeeds through host `127.0.0.1:46321`.
5. Inspect Docker's port mapping and host listeners. Any `0.0.0.0`, `::`, or
   non-loopback host publication fails the preflight.
6. Enumerate the host's active non-loopback IP addresses and prove the nonce
   endpoint is unreachable through each at port `46321`. Distinguish refusal or
   timeout from successful reachability and record the result.
7. From inside the container, characterize routes and name resolution, then
   prove connection attempts to TEST-NET-1 `192.0.2.1:46321` and a second
   unallocated external test address fail locally without reaching an external
   service. No public hostname is queried.
8. Characterize `host.docker.internal` and the internal-network gateway. If
   either supplies broader host reachability than the reviewed boundary allows,
   or the result cannot be demonstrated without opening a new host listener,
   stop and report the uncertainty; do not infer containment.
9. Stop and remove the synthetic container and project network, then verify the
   fixed ports, container, process, and network are absent.

The preflight report must distinguish Docker configuration, empirical success,
empirical denial, ordinary connection failure, and untested behavior. An
`internal` label or loopback-looking mapping is not sufficient by itself.

## Candidate reachability holdpoint

Only if every synthetic control passes may R3 create two fresh disposable
candidate containers, one for WAS and one for the Freewallet static surface,
using the same reviewed image ID, internal network, and controls. The containers
must not share a PID, IPC, user, or host namespace. Any synthetic preflight or
candidate-startup script created after authorization must be independently
reviewed in full before execution. The candidate containers may:

- mount each exact checkout read-only;
- mount a fresh temporary WAS data directory read-write;
- run the exact built WAS executable with its filesystem backend and explicit
  finite `capacityBytes`, `maxUploadBytes`, `maxSpacesPerController`,
  `maxCollectionsPerSpace`, and `maxResourcesPerSpace` values recorded in the
  execution evidence, allowing its existing `0.0.0.0` bind only inside the
  container;
- serve the exact built Freewallet static output without a graphical browser;
- publish only `127.0.0.1:46321` and `127.0.0.1:46322` on the host;
- fetch WAS `/health`, one documented non-mutating WAS route, the Freewallet
  root, and one same-origin built asset; and
- record status, content type, bind state, and shutdown evidence without
  recording response bodies, credentials, tokens, or personal data.

The candidate holdpoint is finite and may last no more than 30 seconds after
both services become ready. No wallet action, WAS write, browser execution,
WebAuthn/WebCrypto ceremony, Person Server call, or cross-service handoff is
permitted.

## Stop conditions

Stop before candidate startup if:

- Docker Desktop cannot start without an unreviewed prompt or change;
- daemon version is below 28.0.0 or differs materially from the reviewed
  capability assumptions;
- an existing fixed-name resource or fixed-port listener is present;
- no suitable local Node 24+ image is available by immutable ID;
- Docker attempts a pull, build, registry request, update, login, or external
  service access;
- the internal network, host mapping, non-loopback-host test, container-egress
  test, or host-gateway characterization is absent, ambiguous, or broader than
  expected;
- either exact checkout, tracked source, lockfile, dependency tree, or build
  output is absent or changed;
- candidate startup would require source modification, copying into SOGA,
  rebuilding, installing, Postgres, production credentials, undocumented
  trust, or a new image;
- any host publication is not literal `127.0.0.1` on the fixed ports;
- cleanup cannot prove all R3 containers, networks, processes, temporary
  listeners, and fixed-name resources are gone; or
- any earlier authorization or safety boundary is reached.

On every stop, retain a standalone evidence report, remove any unadopted
research machinery after review if it would invite unsafe reuse, and leave
Docker Desktop running or stop it only according to the PI's explicit direction.

## Required review and evidence

Before execution, Claude Gate 1 and Gemini/AGy Gate 2 must independently review
this proposal against D-038 through D-043, the accepted Stage 3A/R/R2 evidence,
the exact-source state, and current Docker documentation. After execution, both
must review the standalone evidence and independently check cleanup.

Success would establish only bounded local reachability of the two exact built
candidates inside the tested Docker configuration. It would not establish
wallet usability, WAS conformance, Person Server composition, or Stage 3B.

## Explicit nonauthorization

This proposal authorizes nothing. It permits no Docker startup, daemon access,
container or network creation, image pull/build/load/import, registry access,
source change, dependency operation, candidate execution, Stage 3B code or
tests, wallet interaction, Person Server integration, external exposure,
personal data, payment, Misty access, physical actuation, R3 protocol work,
G28, or G29.

Execution requires independent Gate 1 and Gate 2 PASS results followed by an
explicit PI decision.
