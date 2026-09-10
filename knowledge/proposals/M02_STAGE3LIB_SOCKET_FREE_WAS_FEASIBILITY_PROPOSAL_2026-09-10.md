# M02 Stage 3-Lib Proposal — Exact-Source Socket-Free WAS Feasibility

Date: 2026-09-10
Status: PHASE 0 AUTHORIZED UNDER D-058 — PHASES 1–2 NOT AUTHORIZED
Prepared from checkpoint: `main @ ff16893c148bf4a7a7b19e42d0a9d364739ed18a`

## Purpose

Determine whether the exact selected Wallet Attached Storage (WAS) teaching
server can supply useful storage and protocol behavior as an imported library,
without starting its standalone executable or opening any network listener.

Stage 3-Lib is a further Stage 3A recovery attempt, not Stage 3B and not a new
top-level phase. It produces no Stage 3B code or tests. It tests a
source-supported composition seam, not a new SOGA storage
protocol. It precedes any Person Server composition and any Freewallet
interaction. Its result must be useful even if Freewallet cannot run headlessly:
either the real WAS library behavior is reproducible without sockets, or the
boundary is recorded precisely and the candidate is not represented as usable.

## Established evidence and current boundary

Accepted Stage 3A runtime evidence records:

- WAS teaching server origin
  `https://github.com/interop-alliance/was-teaching-server.git`;
- exact commit `2090a606f2723e4d57ef0090db55fd1bdab9427e`, version
  `0.27.0`, and lockfile SHA-256
  `edda1bc47d02a673e0994e2b184886e02f581f00c85958879b15225e4c7b7884`;
- successful frozen-lockfile installation and build from that source, after the
  first build's `tsx` metadata step was denied access to a temporary local IPC
  pipe and the identical build succeeded with local-process permission;
- the standalone executable's hardcoded `0.0.0.0` listener.

Accepted library-surface evidence appears in the reviewed Stage 3A-R and R2
proposals, D-040, and the accepted Stage 3A-R evidence. It records documented
package-root exports including `createApp`, `fastifyWas`, and
`FileSystemBackend`, with downstream composition owning startup. Those source
claims must nevertheless be reverified at the reacquired exact revision before
Phase 1 because that revision is no longer present locally.

Stage 3A-R (D-041), R2 (D-043), R3 (D-048 and D-051), and R4 (D-054 and D-057)
all ended in accepted negative results without candidate startup. This proposal
sets aside the macOS- and Docker-containment line for a socket-free experiment.
It reverses none of those results and authorizes no rerun, diagnosis, or change
to any prior containment attempt. It is the separately reviewed new direction
required by the current stop recorded in `CURRENT_STATE.md`.

The temporary exact-source checkout used by Stage 3A no longer exists. The
repository's older reference clone is at a different revision and does not
contain the selected commit object. No later phase may imply that the exact
checkout or installed dependency tree remains available.

## Selected experiment

Use the exact WAS revision only through its documented package-root library
surface. Select `createApp`, rather than the smaller `fastifyWas` surface,
deliberately: `createApp` is the composition used by the standalone executable
and includes the health route, so it provides higher fidelity to the candidate
whose startup was blocked. Fastify injection is a facility of the returned
Fastify instance, not a WAS-documented interface; using it bypasses neither the
package export nor WAS route logic. Construct the application in process with
test-only temporary filesystem storage and exercise it through injection. Do
not call a network `listen`, create a TCP, UDP, or TLS network connection,
publish a port, or start the WAS standalone executable.

The work is divided into holdpoints:

### Phase 0 — exact-source reacquisition and verification

After independent review and explicit PI authorization, a clean temporary
detached checkout may be reacquired from the recorded origin at the exact
commit under one named temporary root fixed in the authorization record. Use a
plain detached checkout with no submodule or LFS fetch. Only the network
operations intrinsic to that exact Git acquisition are permitted. The origin,
full commit, package version, license, and lockfile hash must match the accepted
Stage 3A evidence before proceeding.

If the exact dependency tree is not already reproducibly available, one
lockfile-frozen installation may be performed using exactly the recorded
`pnpm@11.20.0`, `--frozen-lockfile`, and a runner cache confined inside the
checkout. The observed Node version must be recorded. Package-registry access
is permitted only for that installation. No update, substitution,
mutable-version selection, audit-fix, or unrelated package operation is
permitted.

The known `tsx` build-metadata local IPC pipe is not a network listener. If it
recurs, record it explicitly and do not include it in any claim about network
sockets.

Phase 0 ends with a standalone acquisition-and-build evidence record containing
the origin, full commit, version, license, lockfile hash, exact commands, clean
status before and after, observed Node version, and any `tsx` IPC-pipe event.
Both gates must review that record and the PI must disposition it before any
Phase 1 file is created. Phase 0 authorization does not authorize Phase 1. Any
mismatch or source modification stops the phase.

### Phase 1 — create-only harness and tests

Creation of any Phase 1 harness or test requires its own prospective PI
authorization after Phase 0 acceptance. Create, but do not execute, SOGA-owned
files under `tools/m02_stage3lib/` that:

1. contain reviewed code that, only during the separately authorized Phase 2
   execution, creates a temporary
   `tools/m02_stage3lib/node_modules/was-teaching-server` symlink to the exact
   detached checkout immediately before dynamic import, then imports only the
   bare `was-teaching-server` package specifier and its documented package-root
   exports. Phase 1 commits harness source only; the symlink and harness-local
   `node_modules` must never be staged or committed;
2. construct the exact WAS application with `FileSystemBackend` rooted in a
   newly created temporary test directory;
3. configure finite byte, upload, Space, Collection, and Resource limits;
4. contain no harness call to `listen`, as verified by complete-file review;
5. before importing WAS, install fail-closed SOGA-side detection
   instrumentation over `net.Server.prototype.listen`, `dgram.createSocket`,
   and Node network/TLS connection entry points; record and abort on any
   attempt rather than suppressing it. This patches no file or upstream source
   and is detection for an experiment authorizing no listener—not a substitute
   for OS containment of an authorized listener as prohibited in R2. WAS must
   be loaded by dynamic import only after these guards are active;
6. set and record an explicit literal-loopback `serverUrl` used only as WAS
   configuration for generated URLs and invocation targets; make no connection
   to it;
7. use Fastify injection to exercise only exact source routes and schemas;
8. begin with a health or other non-mutating source-supported request;
9. if the exact source supports it using only permitted local test material,
   exercise one bounded temporary resource write and read;
10. if supported by the exact source, exercise any conditional-write
   behavior, including one successful `If-None-Match: *` creation and one
   conflicting replay that fails with the source-defined response;
11. record request class, status, relevant response headers, and state
   transition without recording secrets or unrestricted response bodies; and
12. close the application and remove the harness-created data, temporary
    symlink, and harness-local `node_modules` in `finally`.

Both independent reviewers must read the complete harness and tests and return
PASS before either is committed. Execution requires the separate authorization
in Phase 2.

### Phase 2 — one bounded socket-free execution

Only after a separate PI authorization may the exact reviewed and committed
harness execute once. Before execution, record the exact inspection commands.
The authorization record must fix an exact maximum of 15 seconds for the
pre-import observation holdpoint and 60 seconds for the complete execution.
After installing the guards and before creating the temporary module symlink or
dynamically importing WAS, the harness emits a recorded readiness marker on
stdout and blocks until the external observer creates the specified completion
marker or the 15-second deadline expires. Deadline expiry aborts through the
same unconditional `finally` cleanup; it never proceeds to import.

An external observer must enumerate the harness PID's network sockets during
that synchronized pre-import holdpoint, immediately before process exit, and
after exit; the first two observations must be empty and the last must confirm
that the PID is absent. Take a whole-host listener inventory immediately before
process creation and immediately after exit; the two inventories must be
identical. A pre-existing listener does not stop the run and must not be
identified, inspected, or removed. Any listener delta stops the run and is
recorded only as a non-identifying count and fact of change; do not investigate
listener ownership. This objective comparison makes no attribution claim. The
60-second overall deadline is fail-closed and invokes unconditional cleanup.
The run must produce a standalone evidence report and independent cleanup
verification. Both gates must review the report before adoption or a
composition decision.

## Source-first rules

- Do not create a synthetic wallet endpoint, `/_test/wallet-evidence` route,
  SOGA interpretation layer, or replacement WAS contract.
- Do not bypass package exports with private deep imports.
- Do not modify, patch, copy into SOGA, or present upstream source as SOGA code.
- Permitted credential material is limited to keys and tokens generated locally
  and accepted by the exact unmodified source through its own documented
  provisioning and authorization path without remote DID resolution or a
  network call. Prohibited are stubs, bypasses, disabled verification,
  hand-built tokens the source would not validate, or substitution for any
  verification step. If an attempted operation requires `did:webvh` or another
  remotely resolved controller, stop without promoting the Space or resolving
  it remotely.
- The `net.Server.prototype.listen` guard must record enough of the attempted
  argument shape to distinguish a network port/host from a local IPC path or
  handle. Either attempt remains fail-closed, but evidence must classify an IPC
  stop separately and must not report it as a network-socket attempt.
- Treat AGPL licensing as a recorded source fact, not as a legal conclusion.
  This local research experiment authorizes neither redistribution nor a
  deployment decision.
- Derive any future Person Server storage interface only from observed exact
  input/output behavior after this experiment; do not design that interface in
  advance and force WAS to resemble it.

## Required evidence

- exact origin, commit, version, license, and lockfile hash;
- clean source status before and after build and execution;
- complete acquisition and frozen-install commands, if used;
- exact package-root imports and source lines establishing them as public;
- proof that the harness contains no network `listen` call, that the fail-closed
  network-attempt guards were active before WAS import, and that PID-scoped
  socket observations and whole-host before/after inventories met their
  objective conditions; any non-network `tsx` IPC pipe is reported separately;
- route and storage behavior observed through injection;
- precise classification of any skipped write, read, precondition, or
  authorization behavior and the source boundary that prevented it;
- temporary-storage contents summarized without secret or unrestricted body
  disclosure; no generated private key, seed, or onboarding-token value may be
  recorded, and key identifiers may appear only as truncated or hashed
  references;
- successful application close and immediate removal of harness-created data,
  the temporary module symlink, and harness-local `node_modules`; repository
  `git status --porcelain` recorded before and after the run; and
- independent Gate 1 and Gate 2 reviews of both the pre-execution package and
  post-run evidence.

The Phase 0 disposition must preserve the exact checkout, dependency tree, and
runner cache unchanged through Phase 1 review and the single Phase 2 execution.
They are removed at one named point only: after the Phase 2 evidence passes both
gates and the PI accepts it. That acceptance must explicitly authorize removal,
and the final synchronization must record independent verification of removal.

## Success and negative-result meanings

Success establishes only that useful behavior of the exact WAS teaching server
can be exercised through its documented in-process library surface without a
network listener. It does not establish a wallet interaction, production
storage, Person Server integration, AAuth conformance, person identity,
authority, consent, mission permission, participant-session behavior, or
action execution.

A negative result is also valid if it identifies the exact point at which the
library requires network startup, remote resolution, unsupported credentials,
source modification, or another prohibited dependency. It must not be repaired
by inventing an endpoint or replacing the source behavior.

No later phase may assume that the Phase 0 checkout, dependency tree, cache, or
temporary module-resolution link still exists; each must verify its inputs.

## Explicit exclusions

This proposal authorizes nothing by itself. Until separately authorized it
permits no Git acquisition, dependency installation, code, test, build, import,
candidate execution, listener, Docker use, browser, Freewallet execution,
wallet interaction, Person Server integration, Stage 3B work, external service,
personal data, payment, Misty access, physical actuation, R3 protocol work,
G28, or G29.

Freewallet's exact headless presentation/signing boundary will be investigated
as a later, separately scoped source-first phase. It is intentionally excluded
from this first experiment so that a browser limitation cannot obscure whether
WAS itself supplies a usable storage seam.

## Holdpoint

Independent Gate 1 and Gate 2 must review this proposal against the repository
and accepted Stage 3 evidence. The PI must then explicitly authorize the next
phase. No acquisition, implementation, or execution may begin from this draft.
