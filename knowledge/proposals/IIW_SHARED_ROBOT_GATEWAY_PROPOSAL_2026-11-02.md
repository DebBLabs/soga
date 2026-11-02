# IIW Shared Robot Gateway Proposal

Date: 2026-11-02  
Status: PROPOSED — SOURCE ONLY; NOT ACCEPTED; NOT EXECUTABLE  
Repository basis: SOGA `072cabefcdd4a12bc2d65cd69ee3e0fb7707a461`  
Presentation basis: Permission to Speak `c943e594270045daa64694f44c33e3602a8181e6`

## Purpose

Prove that the accepted Permission to Speak decision can be enforced through
one target-bound gateway across more than one embodied endpoint without making
the accepted laptop/iPad demonstration depend on either robot.

The gateway is the stable enforcement boundary. Misty and mBot2/CyberPi are
separate adapters behind it. A decision bound to one platform cannot operate
the other platform, and participant devices never receive a robot address,
credential or direct route.

## Preserved accepted baseline

The following remain byte-identical and outside implementation scope:

- the D-191 accepted Beryl/iPad v11 evidence;
- the D-192 public launcher and operator checklist;
- all accepted AAuth `fcf656d`, approval-pending, fictional-parent and Flow A
  sources;
- the PI-locked visitor-visible Flow A screens and wording;
- the existing M01 physical evidence and its exhausted D-032 authority.

The new work is additive. Failure or delay of either robot adapter cannot alter
or disable the accepted laptop/iPad demo.

## Separate public and robot modes

The accepted D-192 public mode remains the guaranteed robot-free demonstration.
It may not dispatch through the robot gateway. While that mode serves any
visitor-visible statement that no robot acts or is connected, the gateway must
remain unconstructed and robot dispatch must be impossible.

Robot dispatch requires a later, separately reviewed **robot mode** with its own
explicit visitor wording. That wording must say that a locally configured robot
may ask exactly one bounded invitation question after the local AAuth/SOGA
decision permits it. It must also disclose that the visitor's input remains
unverified fictional-parent role-play input and does not establish identity,
parenthood, legal authority or consent.

The robot-mode wording and the adapter command must contain the same exact
question bytes. No accepted or legacy text such as `Hello! Would you like to
hear a song?` may authorize or describe `Would you like to dance?`. Static tests
must prove both exact equality and that robot mode cannot start while any served
screen says that no robot acts or is connected.

## Exact semantic boundary

Flow A permits only a bounded invitation question. It does **not** authorize a
dance, locomotion, approach, photography, sensing, recording, free-form speech
or any other robot behavior.

The first shared action is:

`pts.ask_dance_question.v1`

Its exact visitor-facing content is:

`Would you like to dance?`

The robot then pauses for exactly five seconds for a clear natural response.
The gateway does not infer or classify a child response. Any later
dance action requires a separate, explicit decision and is outside this phase.

The existing M01 pink-to-yellow Misty signal-light sequence may be used only in
a separately authorized connectivity and neutral-return probe. It is not the
Flow A invitation action and may not be described as one.

## Shared invocation contract

Reuse the existing immutable `g27_tip_jar.adapter.Invocation` fields rather than
creating a second decision-binding shape:

- `request_id`;
- `decision_reference`;
- `mission_s256`;
- `session_id`;
- `platform_id`;
- `agent_id`;
- `action`;
- `catalog_version`.

The gateway receives an invocation only after the accepted Flow A path reaches
terminal `ALLOW`. It must reject missing fields, an unknown platform, an action
outside the finite catalog, a changed decision binding, a repeated request with
different bytes, or a caller-supplied platform that differs from the immutable
gateway binding.

No raw token, pending capability, participant lease, browser identifier,
fictional-parent receipt or free text crosses the robot boundary.

## Invocation producer and lifecycle channel

A new internal `RobotInvitationCoordinator`, not a participant-facing endpoint,
is the sole invocation producer. A later implementation proposal must name the
exact additive integration seam; it may not poll `/api/state`, `/api/table-state`
or another participant surface to trigger physical action. The accepted bridge
remains unchanged in this proposal. If the coordinator ultimately requires a
bridge hook, that exact bridge change and its complete lifecycle event contract
must receive separate prospective review before implementation.

The producer constructs each field from fixed internal sources:

- `request_id`: a fresh internal identifier for this one invitation attempt;
- `decision_reference`: the terminal local decision reference emitted by the
  approved internal lifecycle seam;
- `mission_s256`: the verified mission value from that decision context;
- `session_id`: the active bounded presentation session;
- `platform_id`: the operator's immutable preconfigured target;
- `agent_id`: the fixed reviewed demo agent identity;
- `action`: exactly `pts.ask_dance_question.v1`;
- `catalog_version`: the fixed reviewed gateway catalog version.

The lifecycle seam emits only fixed internal events: `ALLOW_OPEN`, `LEAVE`,
`FINISH`, `WITHDRAW`, `EXPIRE`, `ERROR` and `SHUTDOWN`. `ALLOW_OPEN` may reserve and dispatch only
while the presentation remains `TERMINAL_ALLOW`, `presentation_outcome` is
`NONE`, and the completion window remains open. Every event is bound to the
same session and decision reference; mismatched, duplicate, stale or reordered
events fail closed.

Dispatch begins when the reservation is taken for adapter invocation and ends
at the adapter's terminal receipt. `LEAVE`, `FINISH`, `WITHDRAW`, `EXPIRE`,
`ERROR` or `SHUTDOWN` observed before dispatch begins cancels the reservation,
consumes the decision reference and guarantees zero dispatch. The same event
observed during or after dispatch invokes `stop_to_neutral` and prevents any
later dispatch. The event must not wait for `dispatch()` to return. If stop or
neutral fails or times out, the receipt records that failure, physical outcome
remains `unknown`, the gateway accepts no further dispatch until an operator
reset, and the operator's independent local stop applies.

`ALLOW_THEN_WITHDRAW` retains the historical ALLOW decision and records
`presentation_outcome=STOPPED`; that value describes only closure of the
presentation interaction, never the physical state of a robot. The robot receipt
separately records `dispatch_status=NOT_DISPATCHED` when withdrawal preceded
dispatch, or records `stop_status=ACKNOWLEDGED`, `FAILED` or `TIMED_OUT` when
withdrawal occurred during or after dispatch. Physical outcome remains `unknown`
unless separately observed and attested. A failed or timed-out stop therefore
cannot imply that the robot stopped. Withdraw must never rewrite ALLOW as DECLINE.
Finish and expiry likewise cannot claim that an already acknowledged command was
never sent. On the accepted bridge, Leave is reachable only before ALLOW and
therefore has no decision reference; the coordinator treats it as a pre-dispatch
session cancellation. `EXPIRE` means the robot-mode completion window lapsed; it
is not the accepted bridge's separate `TERMINAL_EXPIRED` no-ALLOW result.

## Known target-binding gap

The accepted Flow A authorization request binds the participant, mission and
scope `misty.address_participant`; it does not carry a stable physical-platform
identifier. Therefore the current AAuth/SOGA result does not itself prove that
the decision selected Misty rather than mBot2.

For this bounded prototype, the operator configures exactly one active physical
target before a visitor turn. On first dispatch the local gateway atomically
binds the decision reference and session to that configured platform. A later
attempt to reuse the decision reference for another target fails closed. The
participant cannot choose or alter the target.

This is local composition, not protocol-level target binding. The evidence and
UI must say so. A later phase should evaluate whether the target belongs in the
signed action request, authorization token, transaction context, capability or
another binding artifact. That question is part of the AAuth/GNAP/Transaction
Token roadmap and is not resolved here.

## Immutable target registry

The gateway is constructed with an immutable map:

`platform_id -> adapter`

Initial logical targets:

- `urn:debblabs:misty-<unit>:<verified-serial>` — unresolved until the physical
  handoff identifies whether Misty A or Misty B is selected and verifies its
  serial, MAC and current Beryl address; if Misty A is selected, its known
  identity is `urn:debblabs:misty-a:20221304273`;
- `urn:debblabs:mbot2-iiw:<verified-device-id>` — unresolved until the physical
  handoff verifies CyberPi identity and the supported control interface.

Addresses and transports are configuration supplied at construction. They are
not discovered, accepted from participant input, copied from QR content or
silently replaced at runtime. IP addresses are locations, not identities.

## Gateway dispatch behavior

For each request, the gateway must:

1. validate the complete invocation;
2. verify exact target and action binding;
3. atomically reserve the request identifier;
4. dispatch once to the bound adapter;
5. return the same receipt for an identical replay without redispatch;
6. reject a replay whose invocation differs;
7. return a truthful bounded failure receipt when the adapter is unavailable;
8. never fall back to another robot, transport, address or simulated success.

Success and failure receipts are stored under the reservation before it is
released. An adapter exception therefore cannot leave the request reusable or
permit a retry to redispatch. A new request identifier for an already consumed
decision reference is rejected even on the same target; only an exact replay of
the original invocation returns the original receipt.

Only one physical invitation may be active across all robot adapters at a time.
The reservation is released only after a terminal adapter receipt or an
explicit local safety stop. A permission result does not override physical
safety.

## Adapter contract

Every adapter implements the same narrow operation:

`dispatch(invocation, *, bound_platform_id) -> receipt`

and the independent bounded stop operation:

`stop_to_neutral(invocation, *, bound_platform_id) -> receipt`

`stop_to_neutral` is idempotent and callable while `dispatch` is in flight. It
has finite time and output limits and does not depend on dispatch returning.

The receipt contains only:

- request and platform identifiers;
- catalog action and decision reference;
- adapter status;
- command acknowledgement status;
- neutral/stop status when applicable;
- physical outcome: `unknown` unless separately observed and attested;
- execution surface identifier.

Transport acknowledgement must never be reported as observed speech or motion.
Exceptions are converted to fixed error codes; exception text, credentials,
addresses and device responses are not exposed to participant surfaces.

## Misty adapter path

The implementation may reuse the proven M01 patterns:

- explicit platform and API-base construction;
- strict POST-only JSON transport;
- no discovery, redirects, retry or fallback target;
- bounded timeout and response size;
- idempotent request binding;
- exception-safe return to neutral.

The M01 action and mission authorization are not reusable. A new invitation
adapter must use only the exact invitation action and an independently reviewed
Misty speech or display endpoint. Before that exists, the old signal-light
adapter may establish connectivity and neutral return only under separate
authority.

Misty identity must be verified by serial and MAC. The current Beryl IP must be
observed fresh and bound for the run. Opening Misty Studio is not a read-only
network check because its default page may start camera and telemetry reads.

## mBot2/CyberPi adapter path

The adapter must use the supported interface established by the physical
handoff. Candidate transports are a bounded local USB/serial seam or a
preloaded CyberPi receiver reachable only from the robot-side network. The
proposal does not choose between them before the device inventory and harmless
control test are complete.

The first adapter may display or speak the exact invitation and may use a fixed
light indication. Motor movement remains prohibited in this phase. Any receiver
program must fail safe on malformed, unknown, stale or repeated input and must
have a local stop/neutral path independent of the gateway.

The Makeblock mobile app, preset remote and any separate controller are setup
tools only. They are not part of the governed execution path and must not be
available as an undisclosed alternate control during a governed test.

## Network topology

Final intended topology:

- participant phone/iPad and one laptop participant-side interface on a
  participant network;
- Beryl as the private robot network containing the laptop robot-side interface
  and explicitly named robot endpoints;
- no participant route to Beryl or either robot;
- IP forwarding and bridge mode disabled between the laptop interfaces;
- only application-layer gateway dispatch crosses the boundary.

The accepted D-191 topology placed the controlled iPad on Beryl temporarily to
prove the interaction. Changing to the dual-network topology is a separate
integration and test phase; it is not silently claimed by this proposal.

Until that dual-network phase is accepted, **no robot may be associated with
Beryl while a participant device is associated with Beryl**. Physical stages
1-6 below may run on Beryl only with every participant device disconnected, or
after the reviewed dual-network topology is established. The D-192 operator
checklist requires the operator to confirm that exactly the laptop and
controlled iPad A are associated and to stop if a third client appears; this is
a manual control, and the launcher does not detect it. The launcher also binds
to the literal Beryl address and cannot serve the future participant network
without a separately reviewed serving/binding change. No physical gateway test
may weaken or bypass these controls. Static tests may prove only gateway or
configuration enforcement, not actual Beryl association state.

## Required static and synthetic tests

The implementation proposal must cover at least:

1. exact Misty dispatch through a fake transport;
2. exact mBot2 dispatch through a fake transport;
3. unknown platform rejection;
4. Misty-bound decision presented to mBot2 rejection;
5. mBot2-bound decision presented to Misty rejection;
6. action and catalog mismatch rejection;
7. missing decision reference rejection;
8. identical replay returns the prior receipt without redispatch;
9. changed replay fails closed;
10. adapter unavailable produces no fallback or success claim;
11. concurrent cross-robot requests permit at most one physical invitation;
12. transport acknowledgement leaves physical outcome `unknown`;
13. timeout or safety stop prevents later dispatch;
14. no participant secret, address, token or receipt enters a robot command;
15. all accepted Flow A and SOGA baselines remain byte-identical.
16. the first local decision/session-to-platform binding is atomic and cannot
    be changed after creation;
17. no test or evidence describes the local platform binding as an AAuth token
    or SOGA decision property.
18. public robot-free mode cannot construct or call the gateway, and any served
    `No robot acts` / `no robot or camera connected` statement blocks robot mode;
19. robot-mode visitor wording and the dispatched invitation bytes are exactly
    `Would you like to dance?` with no legacy song/greeting substitution;
20. the invocation producer uses only the internal lifecycle seam and never a
    participant-facing state endpoint;
21. each of leave, finish, withdraw, expiry, error and shutdown before dispatch
    produces no dispatch and consumes the session or decision as applicable;
22. each of those events during dispatch calls `stop_to_neutral`, prevents later
    dispatch and records the truthful terminal state; withdraw preserves ALLOW,
    records presentation outcome STOPPED, records stop status separately and
    leaves physical outcome `unknown`;
23. each of those events after dispatch calls `stop_to_neutral` and prevents all
    later dispatch;
24. a repeated stop event is idempotent and cannot reactivate dispatch;
25. stale, reordered or cross-session lifecycle events fail closed;
26. adapter exception records a stable failure receipt and an identical replay
    cannot redispatch;
27. a new request identifier cannot consume an already used decision reference;
28. robot association is prohibited while a participant device shares Beryl
    before the dual-network phase;
29. the invitation response/neutral window is exactly five seconds, matching
    the visitor-visible robot-mode explanation.
30. stop failure or timeout records physical outcome `unknown`, blocks later
    dispatch until operator reset, never claims a physical stop and preserves
    the independent local stop.

## Staged physical validation

Physical work requires separate prospective authority after implementation and
blind review:

1. verify robot identity and current address/interface read-only;
2. run a harmless connectivity/neutral probe;
3. run the exact invitation on one robot with no motion;
4. confirm truthful receipt and neutral/stop state;
5. repeat on the second robot through the same gateway;
6. prove cross-target rejection;
7. only then propose any bounded movement.

Each attempt is single-use, has finite limits, no automatic retry and an
operator stop. Robot action is never required for the accepted public demo.

## Proposed implementation boundary

After the physical handoff resolves identities and transports, a later PI
decision may authorize create-only implementation in a new additive package,
tentatively:

- `robot_gateway/__init__.py`;
- `robot_gateway/gateway.py`;
- `robot_gateway/misty_invitation.py`;
- `robot_gateway/mbot2_invitation.py`;
- `tests/test_robot_gateway.py`;
- `tools/robot_gateway/run_static_and_synthetic_tests.py`;
- a runtime manifest and README.

Exact files, hashes, dependency pins and test count must be fixed before
implementation review. No existing accepted source may be modified unless a
later proposal identifies the exact file and reason.

## Current authorization boundary

This document is a proposal only. It authorizes no implementation, dependency
operation, import, compilation, lint, test, listener, network change, device
discovery, Beryl access, Misty access, mBot2/CyberPi access, speech, light,
sensor read, movement or physical execution. The unrelated PI routine-tool
proposal remains excluded, unread and untouched.
