# Operator runtime draft

This package implements injected synthetic integration only. physical_mode=True
refuses construction. The accepted switching-r3 modules are dependencies and
remain unchanged. No concrete AAuth authorizer, robot event source, device
transport or host-lock implementation is supplied as live authority.

The factory checks canonical endpoint keys, obtains one injected host lease per
binding and wraps adapter stops to publish bounded stop progress. A supervisor
and serialized tick worker have distinct threads. Supervisor heartbeat checks
run before consume and consume repeats the gate under the switcher owner lock.
Record persistence occurs outside the supervisor mutex, with an outer pending
record preventing selection and dispatch until a durable append succeeds.
CLOSED blocks further interaction. Host leases remain held until explicit
power-off confirmation after worker shutdown.

The issued-allow repository must atomically consume a fresh matching grant.
The test repository is an in-memory synthetic fixture. It is never AAuth.
Boot-bound observations are injected; the runtime exposes no event transport.
Physical target locks require a later reviewed implementation and an operator
procedure excluding nonparticipating tools and other controllers.

The runtime retains bounded-session history, rejects stale heartbeat and
uses 5.5 seconds as the reviewed Misty stop job budget. Each future adapter
must supply its own separately reviewed stop bound. A supervisor/worker crash
cannot enforce a physical stop; manual power removal remains required.
Health rescue runs on a separate daemon thread; a callback that holds the
owner lock may prevent rescue from starting, so the latched outer lock must
be treated as requiring immediate operator action. Unattended use is excluded.

All files are draft and unexecuted. The test/controller manifest pins sources
and dependencies without a hash cycle. A committed exact execution request
and prospective PI approval are required before any synthetic run. The
accepted public Flow A and existing gateway/coordinator files are unchanged.

## Revision 2 corrections and preload inventory
The controller preloads __future__, copy and collections.abc before audit.
Source imports are g27 adapter (future/copy/dataclasses/threading/typing);
strict_json_post (future/json/socket/time/collections.abc); Misty adapter
(future/copy/hashlib/threading/typing); accepted gateway
(future/copy/dataclasses/threading/types/typing); unavailable adapter
(future/copy/threading); owned gateway (the same plus accepted gateway);
switching (copy/dataclasses/threading and cached project modules); operator
runtime (copy/dataclasses/queue/threading/time/typing and cached modules);
test files (unittest, dataclasses, unittest.mock, threading and cached project
modules). Controller imports cache every stdlib module in that inventory.
No package filesystem import is needed after audit.

Health/shutdown revocation invalidates every registered platform's unconsumed
grants on a separate revocation thread. Outer gates latch before revocation;
recovery refuses until revocation completion and cannot bypass its failure.
Worker death and queued-job age are supervised. Phase and active bindings
refresh after every operator-call exit, including errors. Lifecycle events for
other sessions/decisions revoke only those grants and cannot terminate the
current interaction. ERROR is supported for the matching active binding.

Persistence pending state survives health mode changes. Recovery retries it
outside the supervisor mutex, before reopening gates. Shutdown stops driver
threads in finally even if finish fails. Startup records explicitly distinguish
zero-I/O placeholder inference. Session exhaustion closes through shutdown;
pending active cleanup remains operator-controlled and never issues two stops.

The synthetic test count is pinned in the manifest. All accepted CyberPi
package files and the accepted runtime proposal are protected. The watchdog
uses worker request/stop progress for bounded legitimate stop waits, and
refuses new grant consumption without fresh runtime readiness after recovery.

## Revision 3 recovery and test isolation
A health latch blocks scheduled new jobs. If operator recovery finds
WAIT_NEUTRAL, it first drives the owner's tick directly, which can only
settle that deadline to LOCKED, then uses recover with fresh neutral proof;
before the deadline it still uses neutral. No dispatch/selection is enabled
by this cleanup. CLOSED never reopens, including after a persistence failure.
Dead armed workers must be restored/restarted before health recovery succeeds.

Failure has precedence over incarnation exhaustion if a stale queued job is
also present. The exhaustion test drains its synthetic queue first to isolate
that path. The real-worker stop test drives supervisor boundaries manually,
and the test repository now serializes grant operations to avoid a test-only
revocation/consume race. These are unexecuted test-design corrections.
