# M02 Stage 3B Proposal — Person Server / WAS Socket-Free Composition

Date: 2026-09-15
Status: PROPOSED — NOT AUTHORIZED FOR IMPLEMENTATION OR EXECUTION
Prepared at: `main @ 675cd3740914c76b4c6fe506604542bcc0024286`
Author/integrator: Codex
Proposed review classification: mandatory dual review under D-064 because the
work composes identity/authority evidence with third-party storage code.

## Purpose

Test the narrowest truthful composition between SOGA's bounded local Person
Server and the exact Wallet Attached Storage (WAS) library already proven under
D-063. The result sought is one test-only Person Server evidence record written
to and read from temporary WAS storage without starting either HTTP service or
opening a network listener.

This is not Freewallet integration. Dmitry Zagidulin reported that Freewallet is
browser-only and has no supported headless Node signing path. Freewallet and a
future wallet-facing exchange remain later work.

## Verified basis

- `m02_person_server` retains missions, signed test-only person tokens,
  permission results, pending state, revocation state, and correlated audit
  events in SQLite. It is a bounded local profile, not an AAuth-conformance
  claim.
- D-063 runtime-measured that exact WAS teaching-server commit
  `2090a606f2723e4d57ef0090db55fd1bdab9427e`, tree
  `540d85cea6cc7ab50ee6f00b0dead2084c1d65de`, can be imported through its public
  package root, constructed `FileSystemBackend`, served an injected health
  request, provisioned a Space through `createApp`, and verified it through
  `getSpaceDescription` without a harness listener or recorded network attempt.
- Source inspection of the exact commit's public types and filesystem backend
  shows `writeSpace`, `writeCollection`, `writeResource`, and `getResource`.
  Those four direct operations have not yet been runtime-exercised by this
  program. `writeResource` supports conditional `ifNoneMatch` create within one
  `FileSystemBackend` instance; its mutex is explicitly single-instance and is
  not an atomicity claim across processes or backend instances.
- The preserved build lacks `dist/build-info.json`; its provenance therefore
  remains the accepted D-061/D-063 evidence and the unchanged 298-file manifest.

## Proposed composition

Add one SOGA-owned Python adapter and one SOGA-owned Node worker under a new
`m02_was_composition` package. The Python adapter receives an already-completed
Person Server record, constructs a canonical non-secret storage envelope, and
invokes the finite Node worker as a child process using JSON over standard
input/output. The worker dynamically imports the exact package-root WAS export,
uses a caller-supplied temporary data root, and performs only the named backend
operations. One worker instance owns the backend and performs every operation
sequentially; no cross-process atomicity is claimed.

The worker creates one test Space and Collection, writes one evidence Resource
with `ifNoneMatch: true`, reads its bounded `resourceStream` back, verifies its
stored content type and version, and returns only bounded identifiers, hashes,
version, and equality results. The Space controller is one locally generated
test `did:key`. Space, Collection, and Resource identifiers must match
`^[A-Za-z0-9._~-]+$`, must not be `.` or `..`, and Collection/Resource IDs must
also reject the exact reserved sets in the selected source.

The worker does not use `createApp`, Fastify routes, onboarding tokens, zCaps,
HTTP, or a listener. Direct backend use deliberately bypasses the candidate's
route-level DID and identifier validation, onboarding and zCap authorization,
and request hooks; the worker mirrors only the named identifier constraints.
It proves storage-backend composition only, not WAS protocol authorization or
route behavior.

The minimal descriptions are `{id: spaceId, type: ["Space"], controller:
testDidKey}` and `{id: collectionId, type: ["Collection"]}`. The worker omits
`capacityBytes` because the selected backend implements that limit by spawning
`du`; finite envelope and temporary-root limits are instead enforced by the
Python adapter and controller.

The stored envelope contains:

- schema identifier and version;
- generated correlation identifier;
- Person Server issuer and test subject identifiers;
- mission hash, request identifier, action, permission projection, and terminal
  state;
- hashes of the complete Person Server result and any retained authority
  reference; and
- an explicit interpretation label: `person_server_evidence_only`.

It contains no compact person token, HMAC secret, operator credential, private
key, raw approval evidence, unrestricted mission document, personal data,
payment data, representative-authority claim, or affected-person assent claim.

## Implementation sequence

### Phase 3B-1 — create only

After PI authorization, create the complete adapter, worker, controller, and
tests without importing or executing WAS and without running tests. Both
eligible independent reviewers read the complete files. Any reviewer who
substantively corrects the package becomes a contributor and is replaced for
final independent review as required by D-064.

### Phase 3B-2 — one bounded execution

Only after both final reviewers PASS the exact source and the PI separately
authorizes execution, commit the reviewed source and execute one controller.
The socket-free controller runs only the focused source-contract and composition
tests. The complete SOGA test suite runs separately under its existing test
decisions and is excluded from the controller's socket-free claim. A standalone
evidence report receives independent review and PI disposition before the
result is accepted.

## Required controls

1. Verify exact SOGA HEAD, WAS commit/tree, public export, compiled manifest,
   clean tracked WAS state, `/usr/bin/python3` at Python 3.9.6, and
   `/opt/homebrew/Cellar/node/26.7.0/bin/node` at Node v26.7.0 before execution.
2. Use only generated test identifiers and temporary roots outside both
   repositories. Set finite storage, record-size, process-output, and timeout
   limits.
3. Install process-local guards before dynamic import for TCP/UDP listen and
   connect, TLS, fetch, child-process creation from Node, worker threads, and
   DNS. The Python adapter uses an exact executable and worker path, a minimal
   environment, no shell, bounded input/output, and a timeout with termination.
4. Each test may invoke at most one Node worker; invocations are sequential,
   each is limited to 10 seconds, and the complete focused run is limited to 24
   worker invocations and 180 seconds. Every invocation must be waited for and
   cleaned before the next. The Node worker may create no child process or
   worker thread. No package or build command is permitted.
5. Define one dependency-free restricted canonical JSON form in both languages:
   values may contain only objects with ASCII keys, arrays, ASCII strings,
   booleans, null, and integers within JavaScript's safe integer range; floats
   and every other value fail closed. Object keys are lexicographically sorted;
   UTF-8 output has no insignificant whitespace and uses JSON escaping. Python
   creates and hashes those canonical bytes. The worker independently
   canonicalizes the parsed value, requires the same bytes and hash, and stores
   those exact bytes as a bounded binary stream with
   `storedResourceType=application/json`. Readback is capped before buffering;
   its raw bytes, content type, and version must match, and Node must parse and
   canonicalize the readback again to the identical bytes and semantic value.
6. Create the Resource only if absent. On the selected backend's typed
   precondition failure, perform bounded readback: a duplicate identical
   request returns an explicit idempotent result only after full verification;
   changed content at the same identifier fails closed. For the duplicate and
   collision tests, one bounded worker mode performs the initial and second
   writes sequentially within one invocation and one backend instance.
7. Emit no secret or full stored envelope. Redact failures and report only
   bounded stage, error class, identifiers, hashes, and cleanup state.
8. Remove temporary data, module-resolution links, inputs, outputs, and child
   processes in `finally`. For each composition-worker test, use the accepted
   Phase 2 pattern: a synchronized pre-import PID observation, in-process API
   guards, process absence after wait, and unprivileged before/after user TCP
   listener snapshots. Record that these observations are not a privileged
   whole-host inventory and do not prove absence of every short-lived socket.
   Verify no surviving process or temporary path and no repository or WAS
   artifact change.

## Required tests

- successful bounded write/read with exact hash and semantic equality;
- altered readback or mismatched hash;
- duplicate identical request and changed-content collision;
- oversized, malformed, unknown-field, and secret-bearing envelopes;
- wrong mission/request/subject binding and unsupported interpretation label;
- missing or changed WAS commit, tree, export, or manifest;
- prohibited network, child-process, worker-thread, or DNS attempt, asserted at
  the patched API before a system call using only inert, non-routable test
  arguments;
- timeout, nonzero worker exit, excess output, partial write, and cleanup
  failure;
- proof that storage success cannot become permission, identity, authority,
  consent, participant admission, payment, or execution evidence; and
- regression coverage for all existing Person Server tests, run only in the
  separately invoked repository suite below because
  `tests/test_m02_person_server.py` binds a loopback listener;
- a separately invoked complete repository suite under its existing decisions,
  explicitly outside the socket-free composition controller and its socket
  observations because existing G26, M01, M02, and G27 tests bind loopback
  listeners.

Each negative test names and asserts its intended failure stage.

## Claim boundary

A positive result would establish only that a bounded SOGA Person Server
evidence projection can be preserved and recovered through the exact WAS
library backend without a network listener. It would not establish Freewallet
integration, wallet control or custody, WAS protocol/zCap conformance, AAuth
conformance, production persistence, external-service containment, legal
identity, representative authority, affected-person consent, participant
admission, mission permission, payment, dispatch, physical execution, or Misty
readiness. It would also not establish multi-process conditional-write
atomicity or any route-level WAS validation or authorization behavior.

## Stop conditions and exclusions

Immediately before Phase 3B-2, re-verify the non-durable candidate path
`/private/tmp/m02-stage3lib-20260910`, exact identity, public exports, and the
298-file manifest. Stop before implementation or execution if the exact
environment is absent or
changed; the public backend methods differ; safe composition requires a WAS
listener, route-level authorization bypass presented as conformance, dependency
or build activity, source modification, external access, or production data;
or the evidence envelope cannot remain non-secret and semantically bounded.
The unresolved AGPL-3.0-or-later boundary remains open; this local research
proposal makes no licensing disposition.

This proposal authorizes nothing. It does not authorize implementation,
execution, dependency or network activity, Freewallet, browser automation,
wallet interaction, Person Server HTTP startup, WAS application startup,
listeners, external services, personal data, payment, representative or
affected-person policy, participant-session work, Misty access, physical
actuation, G28, or G29. The unrelated PI routine-tool-approval proposal remains
excluded and untouched.
