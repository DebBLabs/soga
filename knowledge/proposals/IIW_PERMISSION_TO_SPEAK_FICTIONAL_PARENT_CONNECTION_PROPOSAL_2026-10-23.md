# IIW Permission to Speak — Fictional-Parent QR Connection Proposal

Date: 2026-10-23  
Status: PROPOSED — no implementation or execution authority  
Repository basis: `fbded4930a9c78300f5eb1848bd5f5b009601b5a`

## Purpose

Connect a new, explicitly fictional-parent QR scenario to the accepted
approval-pending AAuth/SOGA demonstration without changing or reinterpreting
the D-148 adult-participant fixture.

The table visitor is an adult who knowingly role-plays the parent of a fictional
child for this demonstration. The input is always labeled unverified simulation.
It proves neither identity nor a real relationship, parental or legal authority,
consent, assent or public-event safety.

## Why a separate package is required

D-145 through D-148 deliberately bind the existing QR package to an adult
participant choosing whether a response may be directed to that same
participant. Its fixed mission, action, participant and page text expressly
exclude a parent scenario. Mapping that event directly to an asserted parent
receipt would change its meaning after collection and violate the accepted
boundary.

The fictional-parent case therefore receives a separate additive package. The
accepted D-148 package remains byte-identical and available as its own future
participant-choice path.

## Accepted inputs that remain unchanged

| Input | SHA-256 |
|---|---|
| `m02_aauth_fcf656d/approval_pending.py` | `18717f7b64007c92f6fb893498f1329b8ed049bb6636eb586a44267588bea47b` |
| `m02_aauth_fcf656d/demo_operator.py` | `b65160deffccf80220a0f466384a98ad1c3d21101dc44a1ee3b5d8099bf238a3` |
| `m02_aauth_fcf656d/other_party_approval.py` | `c5a244da3ef5e6694df663af2ff0fb5cd83cdf928fa49c1ab708b197c35d78b0` |
| `iiw_qr_session/package.py` | `3f079c3bd7c834758a1062926f5083d556497ab8013a2426ea5bef95584495c9` |

The new code may use `BindConfiguration` and private-IPv4 validation from the
accepted QR package. It must not import the D-148 participant session or treat
its `ParticipantChoice` as representative input.

## Phase 1 — create-only package

Create exactly these additive files:

1. `iiw_fictional_parent/session.py` — one-use, capability-bound fictional
   scenario state;
2. `iiw_fictional_parent/gateway.py` — bounded participant HTTP page and
   submission codec;
3. `iiw_fictional_parent/connection.py` — the sole mapping into the accepted
   `DemoOperatorAdapter.record_held_input()` seam;
4. `iiw_fictional_parent/__init__.py` — explicit public surface only;
5. `tests/test_iiw_fictional_parent.py` — focused static and behavioral tests;
6. `tools/iiw_fictional_parent/run_static_and_loopback_tests.py` — bounded
   future test controller; and
7. `iiw_fictional_parent/README.md` — operator and claim-boundary record.

No accepted source may be modified.

## Exact scenario semantics

The fixed scenario is:

- scenario: `permission-to-speak-fictional-parent-v1`;
- proposed action: `address_fictional_child`;
- affected subject: `fictional-child-1`;
- visitor role: `fictional-parent-roleplay`;
- choices: `APPROVE_FICTIONAL_DIRECTED_RESPONSE` and
  `DECLINE_FICTIONAL_DIRECTED_RESPONSE`;
- assurance carried into the accepted adapter:
  `unverified-demo-input`.

The exact accepted-seam mapping is:

| Scenario term | Accepted seam field/value |
|---|---|
| fictional child | agent action-body `participant` = `fictional-child-1` |
| fictional child | `DemoOperatorAdapter.participant` = `fictional-child-1` |
| scenario | surface and adapter `mission_s256` = `mission-sha256` |
| proposed directed response | action-body and adapter `scope` = `misty.address_participant` |

`permission-to-speak-fictional-parent-v1` is a scenario identifier, not an
AAuth mission hash. `address_fictional_child` is human-facing scenario text,
not the accepted scope value. Because Misty is excluded, the UI must describe
`misty.address_participant` as the accepted legacy name for a simulated directed
response by the demo resource; it must not imply robot execution.

The Phase 1 composition factory constructs the accepted surface and adapter
from these same constants. It refuses construction if any supplied scenario,
participant, mission or scope differs. Approve must poll to terminal `200` with
reason `approval_active`; an intentionally mismatched binding must poll to
terminal `403` with the exact accepted mismatch reason.

The page must state, before either choice:

> You are an adult participating in a fictional demonstration. You are
> role-playing the parent of a fictional child. This does not verify your
> identity, establish any real relationship or legal authority, or record
> consent for a real person.

The buttons must name the fictional effect. Leaving without choosing is always
permitted and produces no approval input.

## State and capability controls

- One session accepts at most one choice.
- Lifetime is exactly 30 seconds under the same injected integer clock callable
  used by the accepted pending store and adapter. The held request is created
  first; the composition records the clock value when its `202` and pending path
  are received and must create the QR session without advancing that clock.
  Thirty seconds is therefore strictly shorter than the held record's accepted
  120-second lifetime and its verified auth-token remainder.
- The capability contains 32 bytes of generated entropy, appears only in the
  URL fragment and is removed from the visible URL before controls enable.
- Capability comparison is digest-based and constant-time.
- Choice, scenario, action, fictional subject, role-play label and gateway
  instance are exact immutable bindings.
- Invalid, expired, cancelled, replayed and already-consumed sessions are
  publicly indistinguishable.
- The callback fires exactly once only after all bindings pass.
- No capability, receipt identifier, token, key or signature may appear in
  logs, errors, response bodies or durable evidence.

## Connection to the accepted approval-pending flow

The connection is deliberately narrow:

1. a Phase 1 test composition of the accepted AAuth/SOGA stack first produces
   one live held request with `requirement=approval` and captures the `Location`
   pending path from the public `202` response;
2. `connection.py` receives only the shared integer clock, accepted store and
   policy needed to construct its `DemoOperatorAdapter`, the public pending
   path, the exact bindings above and a receipt-ID factory. It does not read
   private store state. The new QR session is created for that held request in
   the same clock tick;
3. the adult visitor sees the complete fictional-role disclosure and submits
   one bound choice;
4. `connection.py` validates the exact fictional-parent event and maps only:
   - approve -> `DemoOperatorAdapter.record_held_input(pending_path,
     "APPROVED")`;
   - decline -> `DemoOperatorAdapter.record_held_input(pending_path,
     "WITHDRAWN")`;
5. the agent learns the result only through the accepted signed polling path;
6. the QR choice consumes the session even if the adapter refuses it. An
   adapter refusal (`pending_not_live`, `operator_capacity`, `invalid_input` or
   `operator_state_unavailable`) makes the connection terminal, produces the
   same public `404 {"status":"session unavailable"}` response, creates no
   second receipt and authorizes no retry; and
7. session state, pending path and any adapter event are cleared from the test
   composition after a terminal result.

The complete public poll outcomes are: `200 approval_active` for the exact
approved binding; `403 approval_withdrawn` for decline; `403` with the accepted
fixed mismatch reason for a receipt/action binding mismatch; `408 expired` when
an unresolved held request ages out; `410 gone` when already completed; and
indistinguishable `404 not_found` for invalid path, signature, token or binding
provenance. Before expiry, no-choice departure leaves the held request at `202
pending`; it supplies no receipt and later reaches `408` if polled after expiry.

The new connection must never call `replace_standing_input()`. No choice may
authorize a later child, encounter, mission or action. It must never inspect
private store internals or use `last_decision`.

For each encounter, the composition factory creates one adapter and transfers
its only reference to one connection object. No presentation control, second
connection or other component receives that adapter or may call
`record_held_input()` for the pending path. The connection serializes choice
handling under one lock, consumes its pending path before invoking the adapter
and rejects every later call. This process-local exclusive ownership prevents
the accepted store's replace-on-resolve behavior from overwriting the visitor's
choice. Tests must prove a second and concurrent input cannot reach the seam.

Phase 1 contains only this test composition. It does not use or modify the
external Permission to Speak presentation. Wiring the reviewed connection into
that bridge requires a separate proposal after the package passes execution.

`DemoOperatorAdapter` remains the component that creates the fixed
`asserted_role="parent"`, `assurance="unverified-demo-input"` receipt. The new
package characterizes that value only as a fictional scenario assertion, not
an authenticated or legally meaningful claim.

The accepted receipt also fixes `source="local-operator-demo-control"`, which
the signed-poll decision exposes as `approval_source`. In this profile that
value identifies the accepted local adapter seam through which the QR choice
was conveyed; it does **not** identify or authenticate the visitor and is not a
claim that the local operator made the choice. The page, README, test evidence
and any later presentation must state that distinction verbatim. A focused test
must assert the exact observed source value and the accompanying disclaimer.

## HTTP and network boundary

Phase 1 creates source only and opens no listener.

For a later separately reviewed synthetic run, every bind and connect must be
literal `127.0.0.1`. A later real-phone proposal may select one exact private
IPv4 address on the Beryl network, but must separately review interface
identity, host-header binding, QR origin, firewall/reachability, device cleanup,
public-event privacy and G29. No wildcard, hostname, DNS, external route,
internet service, TLS claim or ambient LAN trust is permitted here.

Every response must include `Cache-Control: no-store`, `Referrer-Policy:
no-referrer`, `X-Content-Type-Options: nosniff` and a restrictive CSP. Request
bodies, headers, concurrency, queue depth and timeouts must be finite. Early
refusals close the connection without draining untrusted bodies.

## Required Phase 1 tests

The focused suite must cover at least:

1. exact disclosure and button text;
2. fragment removal before controls enable;
3. approve mapping to one held `APPROVED` input;
4. decline mapping to one held `WITHDRAWN` input;
5. no standing-policy mutation;
6. no callback on no-choice departure;
7. expiry, cancellation, replay and duplicate submission;
8. every binding mismatch and unknown choice;
9. concurrent submissions consuming at most once;
10. exclusive adapter ownership: a second or concurrent caller cannot overwrite
    the visitor's receipt;
11. pending-path absence, mismatch, expiry and terminal-state refusal through
    public seams only, with a consumed QR session, public `404`, no second
    receipt and no retry after adapter refusal;
12. signed polling returning every accepted `200`, `202`, `403`, `404`, `408`
    and `410` outcome described above;
13. exact field mapping, approve -> `200 approval_active`, deliberate mismatch
    -> `403` with its named reason, and the exact
    `approval_source="local-operator-demo-control"` disclosure;
14. exact security headers, host checks, body and framing limits;
15. refusal of wildcard, loopback aliases, hostname and unassigned addresses;
16. no secret or capability leakage;
17. cleanup of server thread, listener, session and temporary state; and
18. regression of the accepted D-140/D-144 approval-pending/operator tests and
    the accepted D-148 QR fixture tests without modifying their sources.

The future controller must pin every source hash, exact runtime identity,
interpreter and test count; use finite time/output limits; verify repository
immutability; write to a new absent durable evidence directory; stop all
listeners and children; and permit no automatic retry. It must reuse the
accepted provider-runtime manifest and full static provider verification before
any signed AAuth path imports `cryptography` native code. The new runtime
manifest must also pin the explicit namespace-package loading of
`iiw_qr_session/package.py` without importing the D-148 participant session.

## Review sequence

1. Both blind gates review this complete proposal.
2. With prospective PI authorization, Phase 1 creates the seven files but does
   not import, compile, lint, test or execute them.
3. Both blind gates review every complete created file.
4. A separate proposal and PI authorization are required for synthetic
   loopback execution.
5. A separate proposal, privacy/safety review and G29 disposition are required
   before a phone, Beryl network, public event or real QR is used.

## Exclusions and claim boundary

This proposal does not authorize implementation, import, compilation, lint,
test, execution, listener, QR generation, phone or device contact, Beryl/LAN or
external access, personal data, a real child, verified identity, parental or
legal authority, consent or assent, wallet/WAS, presentation modification,
Misty, physical action, G28 or G29.

No participant age is inferred or verified. The later table procedure must
restrict this role-play interface to an adult visitor; that public-event control
is not established by Phase 1 code.

It defines a truthful fictional-parent demonstration path only. It does not
claim that AAuth `fcf656d` defines representative authority; the pinned source
audit found that it does not. The other-party approval lifecycle is an
application profile layered beside the bounded AAuth flow, and the UI and
evidence must keep that distinction visible.

The unrelated PI routine-tool proposal remains excluded, unread and untouched.
