# M01 Mission Formation — Governed Misty A QR Action Precursor

Date: 2026-09-05  
Status: PROPOSED — awaiting constitutional Gate 1 and Gate 2 review  
Authority: D-028, Mission Formation only  
Prepared by: Codex/CG, Implementation Lead  
Review target: `main @ efec4b17f73a9f94331ac51ef96fdbc1def8c1ae`

## Mission intent

Establish a bounded, target-bound path in which a QR-originated request is
evaluated through the existing SOGA/AAuth governance path and, only after all
later authorizations and safety preconditions are satisfied, produces one
finite C1 expressive action on Misty A with truthful, independently reviewable
evidence.

This formation artifact defines the proposed mission. It does not instantiate
an approved mission, authorize implementation, or permit Misty power, network
connection, discovery, status query, command dispatch, or actuation.

## Native AAuth Mission candidate

The native immutable AAuth `Mission` and append-only mission log remain the
only authoritative mission representation.

| Field | Proposed value or required disposition |
|---|---|
| `approver` | **UNESTABLISHED:** Deb's canonical Person Server identifier must be adopted before Mission Authorization. |
| `agent` | Proposed semantic identifier: `soga-m01-misty-a-qr-agent-v1`; Gate review and Deb adoption required. This identifies the mission agent, not Codex, Claude, or AGy. |
| `approved_at` | **UNSET:** actual instant of Deb's later Mission Authorization; must not be backfilled. |
| `approved_tools` | The three versioned semantic actions in catalog `m01-c1-v1-candidate` below; final inclusion depends on Gate review and Deb authorization. |
| `description` | "Permit the M01 mission agent to process a QR-originated request for one catalog-bounded, governed C1 expressive action on the explicitly bound Misty A platform, subject to current authorization, safety, cardinality, and truthful-receipt requirements." |
| `s256` | **UNSET:** calculated by the native AAuth implementation only after the canonical fields above are adopted. |

No placeholder identifier, approval time, or hash may be represented as an
approved mission value.

## Candidate semantic-action catalog: `m01-c1-v1-candidate`

The catalog is intentionally limited to non-navigational, non-contact,
non-identifying expression. Every entry remains a physical candidate until its
exact Misty A primitive, bounds, interruption behavior, and neutral transition
are locally verified.

| Semantic action | Requested outcome | Cardinality | Required neutral result | Current evidence status |
|---|---|---:|---|---|
| `m01.signal_light` | Show one fixed, allowlisted LED color for a bounded interval | At most once per authorized session | Return to an adopted neutral LED state | Historical command shape only; present Misty A behavior unverified |
| `m01.show_expression` | Show one fixed, allowlisted non-identifying display/eye expression | At most once per authorized session | Return to an adopted neutral/blank expression | G27 permits fixed C1 display candidates; exact asset and present behavior unverified |
| `m01.speak_phrase` | Speak one fixed, allowlisted, non-personalized phrase | At most once per authorized session | Silence | Historical command shape only; present Misty A behavior and safe volume unverified |

The initial physical acceptance run shall authorize exactly one catalog entry;
the other two remain unexercised candidates. A QR
request selects a semantic action, never a raw endpoint, asset URL, free-form
text, actuator value, IP address, or robot target.

## QR intake and session lifecycle

M01 inherits the adopted G27 single-use grant and session lifecycle; it does
not define a new QR session mechanism. The QR artifact carries or resolves only
an opaque, integrity-protected grant reference bound to the mission hash,
catalog/policy and notice versions, canonical platform, issuer, expiry, and
intended session service. Validation and atomic consumption occur before
session creation. One grant creates at most one session; replay returns an
existing status or terminal receipt and cannot repeat execution. The adopted
hard and idle expiry semantics, one-live-session constraint, ephemeral channel
binding, withdrawal, terminal-state, and fail-closed rules remain binding.

The QR payload does not carry authority by itself and does not directly name a
Misty endpoint, network address, primitive, or free-form action. The exact
grant integrity, issuer, storage, and service-owner instantiations remain
implementation decisions to be proposed and reviewed inside the later Mission
Authorization envelope; none may weaken the inherited G27 properties.

## Explicit prohibitions

- No base, arm, or head motion in the initial catalog.
- No navigation, following, approach, contact, photography, camera or
  microphone capture, identity or emotion inference, participant tracking, or
  retained participant data.
- No participant-supplied text, image, URL, audio, endpoint, primitive,
  actuator value, target, or network address.
- No broadcast, discovery, first-device selection, last-connected target,
  mutable global target, hardcoded fallback, or reuse of a prior `ALLOW`.
- No direct-dispatch legacy path and no copying of historical Misty code as an
  authorized implementation input.
- No claim that HTTP acceptance, dispatch, or robot self-report proves physical
  completion.
- No implementation before Mission Authorization; no physical access before
  Physical Execution Authorization.

## Required bindings and invariants

Before implementation can be authorized, Gate review must confirm that the
mission is sufficiently bounded and identify every unresolved decision. Before
physical execution can be requested:

1. Deb adopts a canonical Misty A `platform_id`, verified against admissible
   local evidence; it is never inferred from IP address or availability.
2. The adapter target is explicitly allowlisted and bound to that platform;
   the final adapter rechecks the binding immediately before dispatch.
3. Mission, catalog, platform, session, request, decision, policy, safety state,
   and receipt references are mutually bound and current.
4. The inherited G27 grant is integrity-protected, unexpired, target-bound,
   atomically consumed, and creates at most one live session with the adopted
   hard/idle expiry and withdrawal behavior.
5. Per-action and per-session cardinality are enforced independently of
   single-use grant and request-idempotency controls.
6. Replay, wrong-target, stale decision, late `ALLOW`, timeout, network loss,
   conflicting execution, and safety-halt cases fail closed and do not resume
   an old action automatically.
7. The independent local safety halt is physically available and verified; it
   does not depend on governance or network availability.
8. The action's exact primitive, finite bounds, safe interruption/completion
   behavior, and neutral transition are measured and recorded on Misty A.
9. Misty B remains unpowered/unaffected and its state and command surface do
   not change.

## Evidence and receipt requirements

The evidence chain must distinguish at least:

`request received → governance decision → dispatch attempted → dispatch
acknowledged/rejected → physical start unknown/observed → physical completion
unknown/observed → neutral unknown/observed`

Every record names the mission hash, catalog version, semantic action,
platform, session, request and decision references, adapter, receipt source,
and timestamp. A software or HTTP success may establish dispatch only.
Physical outcome remains `unknown` unless independently observed and bound to
the request. For the first authorized run, Deb may provide recorded human
observation; that evidence must remain labeled human observation.

## Proposed implementation and validation envelope

If Deb later grants Mission Authorization, Codex may implement only:

- QR request parsing into the finite semantic catalog;
- a new target-bound Misty A adapter with no fallback or discovery;
- cardinality, replay, freshness, wrong-target, late-decision, timeout,
  concurrency, network-loss, and safety-inhibit controls;
- fake and loopback surfaces, positive and negative tests, and evidence
  generation; and
- the pre-physical review package.

Mission Authorization would not permit powering, connecting, discovering,
querying, or actuating Misty. Those actions require a later Physical Execution
Authorization.

## Acceptance criteria

### Mission Formation exit

1. Claude/Gate 1 and AGy/Gate 2 independently review this frozen package.
2. Every blocking finding is corrected or explicitly escalated; all rework and
   dispositions remain durable.
3. The approver identifier and mission-agent identifier receive explicit PI
   disposition before native mission approval.
4. Deb receives a decision packet stating exactly what Mission Authorization
   would and would not permit.

### Pre-physical implementation exit

1. All existing tests and the new positive/negative suite pass from a clean
   checkpoint.
2. Gate 1 and Gate 2 independently reproduce material checks and issue
   advisory rulings against the same checkpoint.
3. The canonical Misty A identity, isolated network placement, hardware/battery
   inspection, operator stop, target binding, catalog primitive, bounds,
   interruption behavior, cardinality, and neutral behavior are evidenced.
4. The packet preserves the distinction between permission, dispatch, physical
   start, physical completion, and neutral outcome.
5. Deb is asked for Physical Execution Authorization only after these results
   and unresolved risks are presented.

### Physical mission acceptance

1. Exactly one authorized QR request produces at most one dispatch to the
   explicitly bound Misty A target and none to Misty B.
2. Deb observes and records whether the selected visible/audible outcome and
   neutral transition actually occur.
3. Replays, wrong targets, stale decisions, and inhibited actions produce no
   additional physical action.
4. Receipts state only what their evidence source establishes.
5. Gate findings and Deb's final `ACCEPT`, `REWORK`, or `FAIL` disposition are
   preserved without inferring acceptance.

## Known unresolved decisions and risks

- Deb's canonical Person Server identifier is not established in the current
  repository.
- The proposed mission-agent identifier is not yet adopted.
- Misty A's canonical platform identifier, present network address, physical
  condition, and endpoint behavior are not established by current repository
  evidence.
- Exact LED neutral state, display asset, spoken phrase, volume, durations, and
  primitive interruption behavior remain to be verified and adopted.
- Current G27 state, receipts, and coordination are process-local and do not
  establish durable production operation.
- The temporary shared-file reviewer queue carries evidence only and provides
  no cryptographic identity, durable delivery, or authorization.

## Requested independent reviews

- **Claude / constitutional Gate 1:** architectural conformance, authority
  boundaries, native AAuth mission fidelity, inherited G27 safety/isolation,
  implementability, and missing requirements.
- **AGy / constitutional Gate 2:** independently attempt to falsify coherence,
  demonstrability, acceptance criteria, nonclaims, catalog boundedness, and the
  sufficiency of the proposed evidence package.

Both rulings are advisory. Neither authorizes implementation or physical work.
