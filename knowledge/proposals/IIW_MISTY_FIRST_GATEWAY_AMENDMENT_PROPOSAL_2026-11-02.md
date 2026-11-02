# IIW Misty-First Shared Gateway Amendment Proposal

Date: 2026-11-02  
Status: PROPOSED — SOURCE ONLY; NOT ACCEPTED; NOT EXECUTABLE  
Repository basis: SOGA `17a1c3080aa848db30973b3b906832d7038b76ad`  
Parent decision: D-193  
Parent proposal SHA-256:
`31f529286303a8f49f214745f835b6412a806097552e4c8237883b421243f780`

## Purpose

Amend the implementation sequence and the Misty-specific completion boundary in
D-193 so that the shared gateway core and a Misty B invitation adapter may be
created and proved statically while the mBot2/CyberPi runtime interface remains
unresolved. This document is the exact D-193 implementation proposal for that
Misty-first create-only phase; no additional implementation proposal is required
before creation if the PI accepts it, but the complete created package and its
exact hashes still require blind dual implementation review before commit or
execution.

This does not weaken the shared architecture. The mBot2 target is represented by
an explicit unavailable adapter that always fails closed. There is no fallback
from Misty to mBot2, from mBot2 to Misty, or to simulation. No physical robot
access or execution is authorized by this proposal.

## Preserved accepted boundary

The following remain byte-identical and outside this amendment:

- the D-191/D-192 accepted public Flow A demonstration, launcher and evidence;
- all visitor-visible public-mode screens and wording;
- all accepted AAuth `fcf656d`, SOGA, approval-pending and fictional-parent code;
- the D-193 shared gateway semantics, lifecycle events, stop behavior, truthful
  receipt rules and network boundary;
- the M01 signal-light adapter, transport, evidence and exhausted authority.

Public mode remains robot-free. This phase creates no robot-mode screen, no
presentation hook and no lifecycle connection to Flow A.

## PI-reported Misty B target

Deb reported these values in this session on 2026-11-02 after physical handoff
work by Gemini (called G in the conversation), acting as the physical setup
assistant. Gemini reported reading the serial and CONFIG from the
unit/packaging, and the MAC, reserved address, firmware and battery from the
earlier local setup. They are PI-reported inputs, not independently re-read or
verified by this proposal:

- platform ID: `urn:debblabs:misty-b:20193802932`;
- serial: `20193802932`;
- MAC: `00:D0:CA:00:96:C3`;
- reserved Beryl address: `192.168.8.219`;
- firmware observed by the handoff: `2.0.2.11660`;
- model: Misty II, CONFIG `010-000002`.

The IP address is a proposed location, not identity. Any later physical request
must independently confirm the Beryl reservation and exact client boundary
without discovering or accepting another address.

## Authoritative API surface

The Misty II HTTP API documentation defines:

- invitation: `POST http://<robot-ip>/api/tts/speak`;
- stop: `POST http://<robot-ip>/api/tts/stop`.

The documented Speak fields used in this phase are `Text`, `Flush` and
`UtteranceId`. The exact payload is constructed internally:

```json
{
  "Text": "Would you like to dance?",
  "Flush": true,
  "UtteranceId": "<pts-hashed form defined below>"
}
```

The stop payload is an empty JSON object. A command acknowledgment requires an
HTTP 2xx JSON object whose `result` value is the JSON boolean `true`, with no
`error` member and with `status` either absent or exactly `Success`. The official
documentation describes successful Speak and StopSpeaking results as true. Any
other status, shape, value, ambiguity or transport outcome is failure. The first
harmless physical stage must record the actual StopSpeaking response and stop if
this strict parser does not accept it; it may not broaden the parser at runtime.

The official documentation labels
both commands Alpha and states that the HTTP API uses no keys or credentials;
any device able to reach Misty's address can issue commands. Therefore network
isolation, exact target binding and no participant route are safety controls,
not optional deployment preferences.

Sources, read 2026-11-02:

- https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#speak
- https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#stopspeaking
- https://docs.mistyrobotics.com/misty-ii/web-api/overview/

No camera, microphone, sensor, WebSocket, event subscription, drive, head, arm,
display, LED, asset, skill, update, discovery or network-management endpoint is
part of this phase. Misty Studio must not be opened.

## Misty invitation adapter

The adapter implements the D-193 interface:

`dispatch(invocation, *, bound_platform_id) -> receipt`

`stop_to_neutral(invocation, *, bound_platform_id) -> receipt`

Dispatch validates the exact platform, action
`pts.ask_dance_question.v1`, catalog version, mission, session, decision and
request bindings before constructing the fixed Speak payload. The adapter may
send exactly one request to the exact configured Speak URL. `Flush=true` prevents
older queued utterances from preceding the invitation. No caller supplies text,
URL, address, endpoint, payload field or utterance identifier. `UtteranceId` is
exactly `pts-` followed by the first 32 lowercase hexadecimal characters of
SHA-256 over the bounded internal request identifier; the raw identifier never
enters the payload.

`stop_to_neutral` may send exactly one request to the exact configured stop URL.
It is idempotent, bounded and independent of dispatch completion. Acknowledgment
means only that the HTTP/API request was acknowledged. Physical speech and stop
outcomes remain `unknown` unless separately observed and attested.

The adapter stores the invocation and stable success or failure receipt before
releasing its reservation. Exceptions become fixed codes. Exception text,
addresses, robot responses and internal identifiers are not exposed to visitor
surfaces. A Speak timeout, connection loss or ambiguous response records
`delivery=unknown`, never `not_sent`; it immediately makes one bounded
`stop_to_neutral` attempt and locks the target against later dispatch regardless
of that stop result until a local operator reset occurs outside participant
reach.

`RobotInvitationCoordinator` is the sole lifecycle-event receiver and invocation
producer in this phase. It owns the one-active reservation from before Speak
until the terminal invitation-window receipt. A successful HTTP acknowledgment
is nonterminal: it records only API acknowledgment. The five-second response
window starts only after an internal, matching `TextToSpeechComplete` signal for
the exact `UtteranceId`; it ends when five seconds on the injected monotonic clock
have elapsed or earlier on leave, finish, withdraw, expiry, error, shutdown or
stop. No event is interpreted as a child response.

The speech-completion deadline is exactly ten seconds on the injected monotonic
clock after API acknowledgment. If no matching completion arrives by that
deadline, the coordinator makes one bounded stop attempt, creates a terminal
receipt with `completion=missing` and physical outcome `unknown`, consumes the
decision and keeps the target locked until local operator reset. A stale,
reordered, duplicate, mismatched or cross-session completion signal is rejected
and cannot start a window or release a reservation.

A lifecycle stop event during speech makes one bounded stop attempt immediately
and, without waiting for speech completion, creates a terminal robot receipt that
records `stop_status=ACKNOWLEDGED`, `FAILED` or `TIMED_OUT` and
`physical_outcome=unknown`; it consumes that decision and cancels its response
window. `STOPPED` is used only as the presentation outcome for withdraw and never
as a robot or physical-outcome claim. A later completion signal for that
utterance is recorded as late and ignored. If the stop is acknowledged, the
target remains unavailable until the original ten-second speech deadline has
passed and then returns to available without reviving the decision. If stop
fails, times out or is ambiguous, the target remains locked until local operator
reset. No second dispatch is permitted during either interval.

Static and synthetic work uses an injected completion source and clock. Physical
Speak remains blocked until a later reviewed execution proposal defines and
pins the read-only Misty `TextToSpeechComplete` event transport. This is a
deliberate Misty-specific completion amendment to D-193, not a visitor-visible
wording change: the accepted statement that the robot speaks and then pauses for
five seconds remains literal.

## Transport

Create a new package-local JSON POST transport; do not modify the accepted M01
transport. It must enforce:

- literal `http://192.168.8.219/api/tts/speak` and
  `http://192.168.8.219/api/tts/stop` allow-list only;
- POST only, `application/json`, no redirects, discovery, retry, proxy, DNS,
  alternate address, authentication prompt or fallback;
- timeout no greater than two seconds per request;
- response body no greater than 65,536 bytes;
- JSON-object response only;
- fixed bounded request body and exact field/type validation;
- no environment-derived proxy use.

## mBot2 placeholder

`UnavailableMbot2Adapter` occupies the exact placeholder registry identifier
`urn:debblabs:mbot2-iiw:unavailable` until a real unit identity and runtime
interface are accepted. The identifier asserts no verified device. Both
`dispatch` and `stop_to_neutral` return a
stable unavailable receipt without network, USB, serial, Bluetooth or other
I/O. It can never fall back to Misty or simulation and cannot be configured with
an address or transport.

The mBot2 placeholder is not evidence of mBot2 compatibility or operation.

## Proposed create-only implementation boundary

After acceptance, a later PI decision may authorize creation only of:

- `robot_gateway/__init__.py`;
- `robot_gateway/gateway.py`;
- `robot_gateway/coordinator.py`;
- `robot_gateway/misty_invitation.py`;
- `robot_gateway/strict_json_post.py`;
- `robot_gateway/unavailable_mbot2.py`;
- `tests/test_robot_gateway_misty_phase.py`;
- `tools/robot_gateway/run_static_and_synthetic_tests.py`;
- `tools/robot_gateway/misty-phase-runtime-manifest.json`;
- `robot_gateway/README.md`.

No existing accepted source may be modified. Before implementation review, the
created package must fix every exact file and hash, dependency basis, exact test
count, interpreter, finite limits and initially absent evidence path. Those
values must also be pinned before any execution proposal. This preserves the
timing requirement in D-193 rather than postponing it until execution review.

## Required static and synthetic tests

The created package must prove at least:

1. exact Misty identity and platform binding;
2. exact action and catalog binding;
3. exact Speak URL and byte-equivalent fixed payload;
4. exact stop URL and empty-object payload;
5. no caller-controlled text, URL, address or endpoint;
6. no redirect, proxy, retry, discovery, DNS or fallback;
7. bounded timeout, response size and JSON response shape;
8. identical replay returns one stable receipt without redispatch;
9. changed replay and new request ID for a consumed decision fail closed;
10. dispatch acknowledgment leaves physical outcome `unknown`;
11. stop acknowledgment leaves physical outcome `unknown`;
12. stop failure or timeout records failure, blocks later dispatch and never
    claims a physical stop;
13. stop is callable and idempotent while dispatch is in flight;
14. all D-193 lifecycle events behave correctly before, during and after dispatch;
15. public robot-free mode cannot construct or call the gateway;
16. the mBot2 placeholder performs zero I/O and cannot fall back;
17. cross-target invocation fails closed;
18. concurrent requests allow at most one active invitation;
19. no secret, raw token, participant lease, browser identifier or fictional-
    parent receipt enters a robot payload;
20. all accepted Flow A, SOGA and M01 sources and evidence remain byte-identical.
21. API acknowledgment is accepted only for the exact success shape above;
22. a 2xx failure body is rejected and cannot produce an acknowledged receipt;
23. Speak timeout records delivery unknown, attempts one bounded stop and locks
    later dispatch regardless of the stop outcome;
24. API acknowledgment is nonterminal and the one-active reservation remains
    held while speech completion is pending;
25. only the exact matching completion signal starts the five-second window;
26. the injected monotonic clock proves the window is exactly five seconds after
    completion, and a second dispatch cannot occur within it;
27. missing, stale, duplicate, reordered and cross-session completion or
    lifecycle events fail closed;
28. local operator reset is not participant reachable and cannot revive a
    consumed decision;
29. `UtteranceId` has the exact bounded hashed form and exposes no raw request ID;
30. every parent D-193 test is retained, deferred or inapplicable exactly as
    mapped below.
31. the exact ten-second completion deadline expires into one bounded stop,
    terminal unknown physical outcome and operator-reset lockout;
32. lifecycle stop during speech creates a bounded terminal robot receipt with
    the exact stop status and physical outcome unknown, consumes the decision and
    never waits for speech completion; only withdraw records presentation outcome
    STOPPED;
33. late completion after lifecycle stop is recorded and ignored, with release
    only after the original deadline when stop was acknowledged;
34. failed, timed-out or ambiguous lifecycle stop remains locked until local
    operator reset.

## D-193 test mapping

- Parent tests 1, 3-18 and 20-30 are retained by this package, with tests 21-29
  above strengthening acknowledgment and completion behavior, subject to the
  explicit test-19 split below.
- Parent test 2, exact mBot2 dispatch through a fake transport, is deferred until
  the real mBot2/CyberPi identity and interface are accepted; the unavailable
  placeholder instead proves zero I/O and no fallback.
- Parent tests 4 and 5 remain applicable using the Misty platform ID and exact
  unavailable placeholder ID.
- Parent test 19's exact invitation-byte check is retained. Its visitor-visible
  robot-mode wording check is deferred because this phase creates no
  visitor-visible robot-mode screen and may not change public Flow A.
- Parent test 20 is implemented by `RobotInvitationCoordinator`, the sole
  lifecycle seam in this phase.
- Parent test 28 is static configuration enforcement only; actual Beryl client
  state remains a later physical holdpoint.
- Parent test 29 is proved synthetically from exact matching completion through
  five injected-clock seconds; no physical five-second claim is made before the
  completion-event transport is separately reviewed and executed.

## Later physical stages — not authorized

Physical work remains separate and prospective:

1. verify the laptop and Misty B are the only Beryl clients and the controlled
   iPad is disconnected;
2. verify the exact Misty identity and reservation without discovery;
3. execute a separately reviewed harmless stop-only request and record the exact
   response shape for the strict acknowledgment parser;
4. review its evidence;
5. separately propose, review and pin a read-only exact-utterance
   `TextToSpeechComplete` event transport and independent local stop;
6. execute one exact invitation with no motion, camera, sensor or listening;
7. execute one separately reviewed withdrawal/stop scenario;
8. review all evidence before any public robot mode.

Each physical attempt is single-use, finite, has no automatic retry and requires
an independent local stop. Failure never degrades the accepted public demo.

## Current authority

This amendment is a proposal only. It authorizes no implementation, import,
compilation, lint, test, listener, network change, Beryl access, Misty access,
mBot2/CyberPi access, HTTP request, speech, light, camera, sensor read, movement
or physical execution. The unrelated PI routine-tool proposal remains excluded,
unread and untouched.
