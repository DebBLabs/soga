# Two-robot switching runtime integration revision 2
Date 2026-11-09. Proposal for create-only static review, with no execution authority.

## Basis and scope
CyberPi synthetic evidence is PI-accepted following 177/178. The staged
switching-r3 package passed 173/174 and remains unexecuted. Preserve the
accepted gateway/coordinator/Misty adapter and Flow A files. This proposal
defines an internal runtime around the separate OwnedRobotGateway path.

This package implements injected interfaces and synthetic integration only.
No live AAuth bridge, Misty event transport or mBot2 wire adapter is included.
Those require separately reviewed source/evidence and wiring. The service
refuses physical mode until concrete reviewed implementations exist.

## Exact create-only inventory and sequence
Stage outside the repository, eventually using these five relative paths:
1. robot_gateway/operator_runtime.py
2. tests/test_robot_gateway_operator_runtime.py
3. robot_gateway/OPERATOR_RUNTIME.md
4. tools/robot_gateway/run_operator_runtime_synthetic.py
5. tools/robot_gateway/operator-runtime-manifest.json

Include the four exact switching-r3 files only after separate PI acceptance.
No edit to accepted __init__, gateway, coordinator, Misty adapter, launcher
or presentation. Every complete file receives blind dual static review and
PI acceptance before commit. The manifest pins sources, dependencies and
protected artifacts but not itself/controller; the controller pins the manifest
and the external execution request pins the controller. A bounded synthetic
controller denies network/device/process/mutation capabilities in its child,
limits output/time and saves before/after hashes in a new absent evidence path.
The external request pins the actual test count and complete runtime before
blind dual review and prospective PI execution approval.

First reconcile accepted CyberPi evidence in canonical decision/current state
records. Before any proposal or runtime-file commit, separately review a
D-199 coexistence amendment for those exact new paths. Never silently widen
the six-addition rule. Any future execution request uses the actual committed
HEAD and reviewed protected hashes; historical accepted evidence stays tied
to its historical HEAD.

## Physical ownership and factory
One service owns the registry, switcher, authorizer, observations and driver.
It returns only operator methods, never adapters, transport, tokens or gateway.
Physical bindings are keyed by stable platform binding plus canonical endpoint
identity (literal IP/port for Misty; unit binding and manually pinned device
for mBot2). Reject two adapter instances or two different transport instances
that resolve to the same physical binding. Do not treat object identity as
physical identity.

The synthetic package models an injected host-lock interface. A future live
implementation must acquire exclusive nonblocking host locks per physical
binding before constructing transports and retain them until shutdown/power
confirmation. Legacy services/probes must use the same reviewed locks or be
excluded through a documented manual preflight. Host locks coordinate
participating programs, not arbitrary external HTTP clients. Before live use,
the PI verifies all robot studios, public robot controllers, legacy services,
D-198 probes and ad-hoc tools are closed, and that network access is restricted
to the intended laptop/controller. Without that check, live startup refuses.
These physical/network checks are future approved operator work, not performed
by this package. Factory tests cover distinct transports aimed at one endpoint
and failure to acquire a second physical-target lock.

## Decision repository interface and lifecycle mapping
Define IssuedAllowRepository as an injected protocol with atomic
consume(selected_platform_id, session_id, decision_reference, boot_id),
invalidate(session_id, reason), and invalidate_selection(platform_id).
Consume returns an immutable Invocation bound to exact platform, session,
decision, catalog/action, mission hash, agent and a fresh request id.
It refuses missing, expired, withdrawn, declined or consumed grants.
No repository means construction refusal. Provide only a bounded synthetic
in-memory implementation in tests, not a live store in operator_runtime.py.

A separately reviewed seam-identification artifact must name the actual
accepted AAuth/SOGA class/method and binding semantics before a live adapter
proposal is written. The QR fixture is explicitly outside that seam.
No synthetic repository is represented as AAuth authority.

Decline creates no grant. Decline and pre-dispatch withdraw/leave/finish
invalidate unconsumed grants without calling switcher.finish in IDLE.
For an active interaction, map only valid WITHDRAW/LEAVE/FINISH/ERROR events
to the switcher. STOPPING/WAIT_NEUTRAL/LOCKED never initiate a second stop.
Selection invalidates unconsumed grants for the old selection; approval
cannot transfer. Run-id freshness and repository consume prevent replay.
The health check and consume execute in the switcher's authorize callback
under the same owner critical section. A terminal health latch invalidates
all remaining unconsumed grants.

## Scheduling and independent health supervision
A supervisor thread runs with a maximum 100 ms period. It owns a separate
heartbeat and checks an independent serialized worker's progress. That worker
performs tick and any synchronous timer-triggered stop; no second worker
may invoke tick. The supervisor never calls a blocking tick itself.
Every operator entry checks supervisor heartbeat age (maximum 250 ms).
The authorize callback repeats the check atomically with grant consumption.

Before dispatching tick, the supervisor registers a single job and monotonic
start time. The worker reports entry, finish and current owner phase. A tick
that enters a legitimate STOPPING transition may take up to 5.5 seconds:
the reviewed adapter wait budget is at most 3 seconds plus its 2-second
transport bound, with 0.5-second scheduling margin. This bounded in-progress
stop is not a missing heartbeat and never schedules another stop. During
that job no new dispatch/selection is permitted. If the job exceeds 5.5
seconds, or a non-stop tick does not finish within 250 ms, latch health failure.
The supervisor heartbeat continues during a normal slow stop.

If the supervisor dies, the next operator entry/consume refuses on stale
heartbeat. An external supervisor/manual stop is still required for an active
robot when this whole process dies or cannot schedule; Python makes no
post-crash deadline claim. No unattended operation is proposed.

Tests cover a timer-driven EXPIRE stop slower than 250 ms without false
health failure, a non-stop tick stall, stop-budget overrun, supervisor
heartbeat loss, and concurrent dispatch versus a latched failure.

## Outer health, shutdown and persistence states
Runtime states are RUNNING, HEALTH_LOCKED, PERSISTENCE_LOCKED and CLOSED.
State latches block select/allow_open before any switcher call. On health
failure, atomically latch HEALTH_LOCKED and revoke pending grants.
For switcher DISPATCHING/WAIT_COMPLETION/RESPONSE_WINDOW schedule exactly
one finish(ERROR) through its existing one-stop path. For IDLE send zero
stops. For STOPPING/WAIT_NEUTRAL/LOCKED send zero further stops and retain
the outer lock. Recovery requires renewed health and explicit operator action.
If switcher is LOCKED, use its fresh-neutral recover after all operations
finish; if WAIT_NEUTRAL, use its fresh-neutral neutral before deadline, or
tick to its lock and then recover. In IDLE re-establish per-platform startup
neutrality after the health event before reopening the outer gate.

Shutdown latches CLOSED and revokes grants before scheduling work. In IDLE
send zero stops. In DISPATCHING/WAIT_COMPLETION/RESPONSE_WINDOW issue one
finish(SHUTDOWN). In STOPPING/WAIT_NEUTRAL/LOCKED do not send another.
Allow only bounded observation/cleanup and fresh neutral confirmation while
closed; never reopen or accept a new interaction. Join worker/supervisor
with explicit deadlines; a blocked driver ends in operator power-off handling.
No restart or compensating command is automatic.

Persist every completed terminal record before permitting a subsequent
interaction. All service operations pass an outer serialization gate that
stays blocked from observing the release until persistence succeeds.
The unchanged switcher may already have released its internal reservation;
this proposal does not claim that reservation remains held. If persistence
fails, latch PERSISTENCE_LOCKED, retain the terminal record in memory, block
selection and dispatch, and require explicit operator recovery and successful
durable append before reopening. Test failure on neutral, recover and
zero-I/O unavailable release separately. Never rewrite previous records.

Bound one service incarnation to 30 minutes or 100 consumed grants, whichever
comes first. At exhaustion block new grants, finish the active interaction
through the normal one-stop/neutral path, persist its terminal, close and
require a new boot id plus startup neutrality. Replay state is never cleared
within an active incarnation.

## Neutral truth and injected observation sources
Mint a fresh random boot id. Startup_neutral is once per platform per boot;
post-interaction neutrality is always required via neutral or recover before
another interaction. Do not relabel an ACK as neutral.

The strict unavailable mBot2 binding can use a synthetic startup-neutral fact
only when both the platform id equals MBOT2_UNAVAILABLE_PLATFORM_ID and the
registered object is the accepted UnavailableMbot2Adapter. Label it zero-I/O
inference, not a physical observation. Every non-placeholder adapter requires
a reviewed real observation source. This package implements injected verifier
interfaces and fake sources for tests only.

Misty completion binds UtteranceId derived from request_id, plus session and
decision. The text remains the accepted constant QUESTION; it is not derived
from request_id. A future event source must authenticate the unit and exact
event. Misty neutral means speech stopped and queued invitation cancelled.
mBot2 persistent screen/LED output requires separate completion and clear/
cancellation facts after accepted physical protocol evidence. No timer
fabricates device completion. No live event transport is included.

## Authority
No import, compilation, lint, tests, execution, device access, listener,
network probing, robot power-on or physical contact is authorized by this
proposal or a review PASS. Those require separate prospective PI approval.
Mission work remains outside this package.
