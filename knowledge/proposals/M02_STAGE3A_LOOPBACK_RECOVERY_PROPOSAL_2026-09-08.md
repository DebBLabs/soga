# M02 Stage 3A-R Proposal — Source-Supported Loopback Recovery

Date: 2026-09-08
Status: DRAFT FOR INDEPENDENT REVIEW — NOT AUTHORIZED FOR EXECUTION OR CODE
Prepared from checkpoint: `main @ f55551d282e33bef415a7d2a10f4e8ed44950517`

## Purpose

Resolve the narrow Stage 3A negative finding without patching the selected WAS
teaching-server source or relaxing the literal-loopback boundary. This recovery
phase asks only whether the exact selected packages can be composed and made
reachable on `127.0.0.1` using interfaces their own source explicitly exports.

Stage 3A-R is not Stage 3B. It creates no wallet-to-Person-Server adapter,
credential interpretation, WAS client orchestration, positive handoff, or
integration test.

## Verified problem

At WAS teaching server `2090a606f2723e4d57ef0090db55fd1bdab9427e`, the
standalone executable calls `fastify.listen({ port: config.port, host:
'0.0.0.0' })` at `src/start.ts:66`. The documented environment configuration
does not expose a host override. D-038 prohibited wildcard binding and source
modification, so Stage 3A correctly stopped before service startup.

## Source-supported seam

The same exact package deliberately supports downstream composition:

- `src/index.ts` exports `createApp`, `fastifyWas`, and `FileSystemBackend`;
- `src/server.ts:29` implements `createApp(options)` without opening a socket;
- `docs/consuming-server-as-library.md` describes both `createApp` and
  `fastifyWas` as supported library surfaces and states that the downstream
  Fastify composition owns startup;
- `Fastify.listen` therefore receives its host from the downstream caller; and
- the documented filesystem backend accepts an explicit data directory and
  requires neither Postgres nor Docker.

The documentation's minimal example happens to show `0.0.0.0`; that example is
not a requirement of the exported API. The proposed caller will use literal
`127.0.0.1` and an exactly matching `serverUrl`, because WAS zCap invocation
targets compare the full host and port.

## Options considered

1. **Patch `src/start.ts` or add an upstream environment variable.** Rejected
   for this phase. It modifies the selected source and would require a separate
   upstream-development and licensing disposition.
2. **Use a firewall to compensate for `0.0.0.0`.** Rejected. The process would
   still violate the explicit wildcard-bind prohibition and the evidence would
   depend on machine-global state.
3. **Run the exact package through its exported library composition.**
   Recommended. It preserves the selected source, uses its documented public
   seam, and makes the network boundary an explicit, testable caller choice.
4. **Select another WAS revision or substitute another server.** Rejected. It
   would abandon the reviewed exact-source selection rather than answer the
   observed limitation.

## Proposed authorization boundary

Authorize a Stage 3A-R reproduction harness only. The harness may be a small,
reviewable SOGA-owned research launcher whose sole responsibilities are:

1. import `createApp` and `FileSystemBackend` from the already built exact WAS
   checkout;
2. create an explicit temporary filesystem data directory under a new Stage
   3A-R temporary root;
3. supply `serverUrl` using literal `http://127.0.0.1:<ephemeral-port>`;
4. supply finite storage, upload, Space, Collection, and Resource limits;
5. call `listen` with host `127.0.0.1` and the same port;
6. record the actual bound address and verify that `/health` and the selected
   documented WAS interface return source-supported responses over loopback;
7. serve the already built exact Freewallet static output from the same Node
   harness, using only `node:http` and `node:fs`, on a separate literal-loopback
   port; verify only its root document and local asset reachability;
8. run the entire Node harness under the verified OS-level network-containment
   profile described below; and
9. close both servers in `finally`, then prove with an external socket tool that
   neither candidate port remains bound.

The launcher must not duplicate, alter, or reinterpret WAS protocol logic. A
temporary harness-local `node_modules/was-teaching-server` symlink may point to
the exact detached checkout so that Node resolves the package's declared root
export without copying, publishing, or modifying it. The launcher must import
`was-teaching-server`, not a private `dist/` path. It must not be described as
upstream behavior: the package supplies the WAS application; SOGA supplies only
the bounded research composition and process lifecycle.

If package self-resolution through that explicit symlink does not work, stop.
Do not install or publish the package and do not bypass the export map with a
private `dist/` import. If the existing exact checkouts or dependencies are no
longer present, reacquisition and lockfile-frozen installation require renewed
explicit authority; this proposal does not silently inherit package-registry
access from D-038.

## Runtime boundary

- Bind only to literal `127.0.0.1`; reject `localhost`, DNS names, IPv6
  wildcard, `0.0.0.0`, and every non-loopback address.
- Run the single Node harness with macOS `/usr/bin/sandbox-exec` under a
  temporary, reviewable profile that denies all network operations by default
  and permits only TCP bind, inbound, and outbound operations whose local or
  remote address is literal `127.0.0.1`. The profile path, complete contents,
  command, process identifier, and stderr are evidence. `sandbox-exec` is
  deprecated, so availability alone is not treated as proof that enforcement
  works.
- Before importing either candidate or opening either candidate port, run a
  separate synthetic preflight under the exact same profile. It must prove all
  three properties: a temporary `127.0.0.1` listener and client can exchange a
  nonce; a bind to `0.0.0.0` is denied; and a TCP connection to the IANA
  TEST-NET-1 address `192.0.2.1` is denied locally. The last test is an expected
  OS denial, not authorized external traffic. Record the typed errors. If any
  expected allow or denial is absent, stop before candidate startup.
- Treat the OS sandbox as containment, not as a complete record of attempted
  destinations. Record any denial surfaced to the harness or stderr, but do not
  infer that an empty log proves no attempt occurred. During the bounded hold
  window, use `lsof` to confirm the harness exposes only the two expected
  literal-loopback listeners.
- Use generated test identifiers and temporary storage only.
- Do not set a remote WAS URL, KMS URL, CORS proxy, DID resolver, telemetry
  endpoint, callback, redirect, or proxy.
- Application runtime external-network access remains prohibited and is
  blocked by the preflight-verified OS profile, not merely by policy.
- Do not open a graphical browser, install browser binaries or extensions, run
  Playwright, invoke WebAuthn/WebCrypto ceremonies, create a wallet account, or
  claim a completed Freewallet interaction.
- No Postgres, Docker, system keychain, production credential, personal data,
  payment, camera, microphone, QR scan, or public exposure.
- No Person Server, SOGA permission endpoint, participant session, governance
  decision, or execution surface is part of this recovery phase.
- No Misty access, physical actuation, R3, G28, or G29.

## Required evidence

- exact origin, SHA, package version, license, and lockfile hashes remain those
  accepted under D-039;
- tracked source diffs remain empty before and after execution;
- the launcher imports only documented package-root exports;
- the containment preflight succeeds before either candidate is imported or
  served, including positive loopback exchange and negative wildcard-bind and
  TEST-NET connection controls;
- the actual WAS and static-server socket addresses are `127.0.0.1`;
- `/health`, one non-mutating WAS interface response, the Freewallet root, and
  one local built asset are observed over literal loopback;
- any unavailable interface or surfaced sandbox denial is recorded without
  substitution or a claim of complete attempt logging;
- hold-window `lsof` evidence shows only the two expected listeners owned by
  the sandboxed harness;
- after shutdown, external `lsof -nP -iTCP:<port> -sTCP:LISTEN` checks return no
  listener for either selected port, and the harness process is absent; and
- a standalone evidence report receives Gate 1 and Gate 2 review before PI
  disposition.

Success means only that the exact built packages can be reached through a
source-supported, locally composed process boundary. It does not establish a
wallet interaction, WAS authorization, storage write, cross-service handoff,
AAuth conformance, person identity, authority, consent, mission permission,
action execution, or readiness for Stage 3B.

## Stop conditions

Stop without expansion if:

- package-root import cannot address the exact checkout without source or
  dependency modification;
- either listener is not provably bound to literal `127.0.0.1`;
- `/usr/bin/sandbox-exec` or the exact containment profile is unavailable, or
  the preflight fails to allow loopback, deny `0.0.0.0`, or deny the TEST-NET
  connection before candidate startup;
- the runtime attempts any external connection;
- a required interface needs a graphical browser, WebAuthn/WebCrypto ceremony,
  remote DID resolution, external context retrieval, Postgres, Docker,
  production credential, or undocumented trust;
- tracked upstream source changes;
- shutdown leaves a candidate process or listener running; or
- meaningful evidence would require Stage 3B code or semantics.

## Holdpoint

This proposal authorizes nothing. It must receive independent Gate 1 and Gate 2
review, followed by explicit PI authorization, before any launcher is written
or any service is started. Stage 3B remains unauthorized regardless of the
Stage 3A-R result.
