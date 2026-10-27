# IIW Fictional-Parent Presentation Connection Proposal

Date: 2026-10-27  
Status: PROPOSED — no implementation or execution authority  
SOGA basis: `0cd546ff515005fac896ab3f34e37d4ca6b10b1d` (D-156)  
Presentation basis: `/Users/debb/dev/permission-to-speak-work/permission-to-speak`
at commit `8aa6eec5d40eb671940b73238f8c08cc0c87be76`

## Purpose

Connect the independently reviewed and executed D-156 fictional-parent
role-play package to the existing Permission to Speak presentation so Deb can
see the proven decision flow operate through a visible, same-laptop interface.

This phase is presentation engineering. It does not modify any accepted SOGA
source, create program evidence, contact a phone, use a LAN, verify a parent or
control Misty.

## Established basis

D-156 accepts the bounded fictional-parent R2 execution: 128 of 128 tests
passed, including the preserved 93-test AAuth/SOGA baseline, 17-test QR
transport baseline and 18 fictional-parent tests. The accepted implementation
creates a one-use fictional-parent session only after the resource has returned
an AAuth `202 requirement=approval` held request. Its visitor choice reaches
only `DemoOperatorAdapter.record_held_input()`; the agent learns the outcome
only through the accepted signed polling path.

The presentation working copy is clean at commit
`8aa6eec5d40eb671940b73238f8c08cc0c87be76`. Its current live bridge predates
D-156 and directly exposes the D-140/D-144 standing and held-input controls.
The relevant starting hashes are:

| Presentation input | SHA-256 |
|---|---|
| `bridge.py` | `ca207c1165f2f2f5be25fd8a66bfa1184c554e59fa5d9a68a054e2b7cee9ff4f` |
| `index.html` | `0b349b11a6bdf03f1343d055ed996bd41453fcf1ed3ae3ce49d1d9220e4e09ac` |
| `README.md` | `374212c0adf2bedc9a45e3869861813926d5f772eee7de5ab840adecd32a52cc` |
| `CHECKLIST.md` | `5986a9b1978e48c9412095884c96e9bcf7da4af9932daa280ea28acc3679f867` |
| `warmup.sh` | `f2e2ab46024ffe50c0c3be08474dc9d9eaf3594c1b1df9b0a5cbbde7de806cc0` |

## Exact create-only change set

Modify only these files in the separate presentation repository:

1. `bridge.py` — replace the visible demo's direct parent-control path with a
   composition over the accepted D-156 public interfaces;
2. `index.html` — render the dynamic same-laptop invitation and truthful
   fictional-role disclosures, and display only sanitized state;
3. `README.md` — document the D-156 connection, operation and claim boundary;
4. `CHECKLIST.md` — add the exact operator rehearsal and reset checks;
5. `warmup.sh` — replace the obsolete standing-policy warm-up with the exact
   held-request fictional-parent rehearsal;
6. `test_fictional_parent_presentation.py` — focused presentation-connection
   tests; and
7. `run_fictional_parent_presentation_tests.py` — a bounded future controller
   that pins every input and output source but is not executed in this phase.

Do not modify the SOGA repository during implementation. Do not modify the
presentation photographs, slide order, speaker script, fallback history,
distribution archives or launchers. All five existing presentation inputs in
the table above must be hash-checked before editing. Any mismatch stops
implementation.

## Accepted SOGA surface

The bridge may import the public `iiw_fictional_parent` exports needed to call
`create_encounter()`, `handler_for()` and `server_for()`, including
`PARTICIPANT`, `SCENARIO`, `ACTION_LABEL`, `ROLEPLAY`, `MISSION_S256`,
`LEGACY_SCOPE`, `LIFETIME_SECONDS` and the two public unavailable exceptions.
It may import `BindConfiguration` and `validate_bind_configuration` from
`iiw_qr_session.package`, and `PARTICIPANT_PATH`, `DISCLOSURE`,
`SOURCE_DISCLOSURE` and `SCOPE_DISCLOSURE` from
`iiw_fictional_parent.gateway`. It may retain only the already accepted
D-140/D-144/AAuth components needed to create the held request and signed poll.
The `/enforce` participant must be the imported fictional-parent
`PARTICIPANT` (`fictional-child-1`), never the presentation's earlier
`participant-demo-1` value.

The accepted `participant_url()` is deliberately not called: its real-device
contract rejects loopback. Presentation code instead composes exactly
`http://127.0.0.1:4318` + `PARTICIPANT_PATH` + `#` + the active 64-character
lowercase-hex capability, after independently validating the fixed port, path
and capability form. This is explicitly a presentation-owned loopback URL, not
an extension or reinterpretation of accepted SOGA semantics.

Before importing, live mode must pin every D-156 fictional-parent source and
its accepted QR/AAuth dependencies to the exact hashes recorded in the D-156
evidence. It must continue complete provider-manifest and governance-tree
verification. A missing or changed source fails closed to the visibly labelled
simulated fallback; it must never silently use a partial live path.

No accepted SOGA source may be copied, edited, wrapped with substitute
semantics or reached through a private attribute. The bridge must not call
`replace_standing_input()`, `record_held_input()` directly or use
`last_decision`. The D-156 `FictionalParentConnection` remains the sole owner
of the held-input adapter and pending path.

## Visible flow

One clean presentation encounter is:

1. The simulated child-approach control asks the real bounded localhost
   AAuth/SOGA resource to evaluate the directed response. Immediately before
   every child-approach attempt, the bridge fully tears down any idle
   composition and builds a new person server, resource, store, policy, mission
   and agent token from the current shared clock. The approach may proceed only
   if that fresh composition is no more than five seconds old; otherwise it
   fails closed and requires another fresh construction. This keeps the
   300-second resource token, 1,800-second mission/supervision and longer token
   lifetimes from aging while Deb presents earlier slides.
2. The resource returns `202` with `requirement=approval` and one public
   pending path.
3. In the same frozen clock tick, the bridge calls `create_encounter()` and
   starts the accepted fictional-parent gateway on fixed literal
   `127.0.0.1:4318`. `BindConfiguration(address="127.0.0.1",
   interface_addresses=("127.0.0.1",), synthetic_loopback=True)` is validated
   before `server_for()` is called. The handler's exact Host is known in advance
   as `127.0.0.1:4318`; if either fixed port is occupied, live mode refuses.
4. The invitation slide links only to `GET /invitation` on the presentation
   bridge. While an encounter is live, that route returns `302` with
   `Cache-Control: no-store`, `Referrer-Policy: no-referrer`, an empty body and
   one `Location` header containing the presentation-owned loopback URL. When
   unavailable it returns sanitized `404`. This single redirect header is the
   only bridge output permitted to contain the capability. The capability is
   prohibited from `/api/state`, response bodies, logs, errors and durable
   files. The browser follows the redirect and the accepted fictional page
   removes its fragment before enabling controls.
5. An adult on the same laptop opens the page, reads the exact accepted
   disclosure and role-plays the parent of a fictional child. The accepted
   page removes the fragment before enabling its controls.
6. Approve or decline is submitted through the accepted gateway and connection
   only. The presentation observes the outcome only by signed polling:
   approval returns terminal `200 approval_active`; decline returns terminal
   `403 approval_withdrawn`.
7. Leaving without choosing supplies no input. At the 30-second choice expiry,
   the visible state becomes `choice expired` and the bridge performs the full
   teardown below. The accepted pending record's 120-second `408` remains
   proven by D-156 synthetic tests but is not claimed as visibly demonstrated
   here.
8. Reset, simulated child departure, navigation back to the invitation, choice
   expiry, any partial construction failure or shutdown calls
   `session.cancel()` when a session exists; calls gateway `shutdown()` and
   `server_close()` and joins its thread; then closes and reconstructs the whole
   live composition, including person server, resource, store and policy. No
   held request or decision carries forward and no old adapter path is used.

The visible labels must state:

- `LIVE LOCALHOST ROLE-PLAY` only when the accepted live path is active;
- `UNVERIFIED FICTIONAL-PARENT INPUT` beside the choice and result;
- `No identity, relationship, parental/legal authority or legal consent is verified`;
- `No robot acts`;
- `local-operator-demo-control names the software path, not the visitor`.

The interface must not use the words `real parent`, `parent verified`,
`consent granted`, `Misty allowed` or any equivalent claim.

## State and lifetime rules

- Only one encounter, held request, session, fictional gateway and outstanding
  invitation may exist at a time.
- One presentation-owned `EncounterClock` is the identical callable passed to
  the pending store, connection and fictional session. It derives nondecreasing
  integer seconds from `time.monotonic()` plus one captured epoch base. Under
  the bridge lock, its `freeze()` context returns one captured integer for all
  calls inside `create_encounter()`, guaranteeing the accepted same-tick
  invariant. On leaving the context it resumes wall-time derivation.
- `person_server.now` and every HTTP-signature `created` value are set from that
  same clock immediately before signing. The bridge performs at most one
  signed request for the same method, authority and path in any clock second;
  repeated browser state reads return cached sanitized state until the next
  second. This prevents replay-cache collisions without artificially advancing
  the session lifetime. Tests use an injected controllable implementation of
  the same callable contract.
- The accepted session's 30-second choice lifetime is the visible deadline.
  The accepted 60-second presentation ceiling remains unchanged as an absolute
  defense-in-depth ceiling but cannot extend the 30-second choice window. The
  120-second pending lifetime is a store cap only and cannot extend either
  visible deadline. No timer is reset by browser polling.
- If construction fails after the accepted connection claims a pending path,
  the bridge performs full teardown and constructs a fresh composition; it does
  not retry within that encounter or fall back to a standing/direct adapter
  path.
- The presentation state may expose only: mode, scenario label, pending/result
  status, sanitized HTTP status, fixed reason, revision and whether the
  invitation is available. It may not expose the capability, pending path,
  receipt identifier, token, key, signature or exception text.
- API requests and state transitions remain serialized under the bridge lock.
  A second or concurrent choice cannot reach the connection.
- Returning to the fictional-parent step always creates a fresh encounter; it
  never resurrects or reuses terminal state.
- Presentation startup may occur arbitrarily earlier, but a child approach
  always rebuilds the full composition immediately before its first signed
  request. No mission, supervision observation or token created at application
  startup is reused for the visible encounter.
- Because the accepted module retains claimed `(store, pending_path)` pairs for
  process lifetime, the presentation permits at most 64 encounter creations per
  process. At the cap it displays `LIVE RESTART REQUIRED`, refuses another
  encounter and instructs the operator to stop and restart the bridge. The
  checklist verifies this fail-closed behavior; it never approaches the
  accepted 1,024-claim ceiling.
- The old `/parent` page and `/api/parent` allow/withdraw route are removed or
  return the same sanitized `404` in both modes. The simulated fallback mirrors
  only the held-request sequence, is always labelled `SIMULATED`, and contains
  no standing allow state.

## Network and HTTP boundary

This phase is source creation only and opens no listener.

A future separately authorized test or rehearsal may bind only literal
`127.0.0.1`: the presentation remains on fixed port 4317 and the accepted
fictional gateway uses fixed port 4318. No hostname, wildcard,
private-LAN address, DNS, external route or device is permitted. All existing
host, origin, content-type, body-size, output and socket audit controls remain.
If either fixed port is occupied, live mode hard-stops with fixed operator
instructions; it does not silently select another port or label the result as
live. `CHECKLIST.md` requires both ports to be clear before rehearsal.

This proposal does not produce a scannable phone QR. The visible image may be a
clickable same-laptop invitation only and must be labelled accordingly. A real
phone/Beryl proposal requires separate interface, firewall, privacy, cleanup
and G29 review.

## Required focused tests

The create-only test module must cover at least:

1. exact D-156 source pins and refusal on every changed or missing source;
2. one held request followed by exactly one `create_encounter()` call;
3. no direct standing-input or held-input adapter calls by presentation code;
4. approve -> signed poll `200 approval_active`;
5. decline -> signed poll `403 approval_withdrawn`;
6. no choice -> `202`, then visible `choice expired` and full teardown at 30
   seconds under the injected clock; the unchanged D-156 baseline separately
   retains its synthetic 120-second `408` coverage;
7. exact disclosure, source disclaimer and `No robot acts` label;
8. capability confined to the single `/invitation` redirect `Location` fragment
   and then removed by the accepted page; absent from `/api/state`, response
   bodies, logs, errors and evidence;
9. pending path, receipts, tokens, keys and signatures absent from presentation
   state and output;
10. the specified shared/frozen wall clock; no same-second replay; 30-second
    visible expiry; unchanged 60-second ceiling; and no visible claim that the
    120-second store expiry was exercised;
11. application start followed by 1,900 injected seconds and then a child
    approach rebuilding a fresh composition and yielding `202`, plus refusal
    if the newly built composition is over five seconds old;
12. reset, child departure, navigation and shutdown canceling and closing all
    encounter state;
13. repeated and concurrent input reaching the accepted connection at most
    once;
14. literal-loopback-only binds and connects on 4317/4318, exact Host checks on
    both ports, presentation Origin checks, refusal of cross-origin posting to
    the gateway, and finite body/concurrency/time limits;
15. live-source mismatch producing only a clearly labelled held-request
    fallback, never a partial-live or standing-policy result; uniform refusal of
    the old `/parent` and `/api/parent` routes in both modes;
16. presentation navigation remains complete and no button is incorrectly
    highlighted after reset; and
17. full teardown and composition reconstruction after reset, departure,
    navigation, expiry and partial-construction failure; no listener remains;
    the 64-encounter cap refuses with restart instructions; and
18. no-choice expiry is recognized by a bridge-side timer or, at latest, the
    first state read within one second after the deadline, followed by full
    teardown; and
19. all 128 accepted D-156 tests remain selected by the future bounded
    controller without altering their source.

The future controller must pin the SOGA commit, presentation commit, every
complete source hash, runtime manifest and exact test count; enforce finite
time and per-stream limits; verify both repositories before and after; use a
new absent durable evidence directory; stop every child and listener; redact
all secrets; and prohibit automatic retry.

## Review and authorization sequence

1. Claude Gate 1 and AGy Gate 2 blindly review this complete proposal.
2. After prospective PI authorization, implement the seven-file create-only
   change in the separate presentation repository. Do not import or run it.
3. Both blind gates review every complete changed or added file.
4. A separate execution proposal and prospective PI authorization are required
   before tests or listeners run.
5. After a positive bounded test, a separate rehearsal authorization may let
   Deb see the localhost click-through.
6. Live phone QR/Beryl, presentation packaging and Misty remain separate later
   gates.

## Claim boundary and exclusions

A later positive result may establish only that the visible localhost
presentation is driven by the accepted fictional-parent role-play composition
and signed AAuth/SOGA decision path. It cannot establish complete AAuth
conformance, identity, relationship, real parental or legal authority, legal
consent, public-event safety, a live phone QR, LAN behavior, wallet/WAS, Misty
or physical execution.

This proposal authorizes no implementation, import, compilation, lint, test,
execution, listener, QR generation, device contact, Beryl/LAN or external
access, personal data, presentation packaging, wallet/WAS work, Misty access,
physical action, G28 or G29. The unrelated PI routine-tool proposal remains
excluded, unread and untouched.
