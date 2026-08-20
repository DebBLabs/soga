# G27 Minimal Session-Grant / Person Server Contract

Date: 2026-08-18

Gate/task: G27 — Tip Jar bounded-session modeling

Status: RESEARCH / PROPOSED ARCHITECTURE INPUT — not implementation authorization

## Scope and evidence labels

This artifact derives the minimum component contract required by the first Tip
Jar mission. It does not select a Person Server, wallet, session service, or
implementation technology; extend AAuth; extend the native mission; or authorize
G28 work.

- **REPOSITORY EVIDENCE** — established by a canonical decision, current G27
  artifact, or reached G26 implementation.
- **INFERENCE** — necessary consequence of the provisionally dispositioned G27
  lifecycle, not existing implementation.
- **PROPOSED CONTRACT** — minimum interface/state obligation for later review.
- **UNRESOLVED** — evidence does not select the value, mechanism, or owner.

The Mission 1 policy choices in
`knowledge/research/G27_TIP_JAR_SCENARIO_DECOMPOSITION.md` are treated here as
provisional G27 inputs subject to G28 validation. This artifact does not reopen
their HCI basis.

## 1. Repository baseline

**REPOSITORY EVIDENCE:** D-013 adopts the immutable native AAuth mission. D-019
requires the underlying SOGA decision and attribution to be preserved separately
from its lossy AAuth projection. D-020 requires authorized policy—not subject
state—to select an operational RESTRICT path and prohibits approval alone from
implying `granted` (`knowledge/strategy/DECISION_LOG.md:94-102,127-157`).

The mission contains `approver`, `agent`, `approved_at`, `approved_tools`,
`description`, and `s256`; it contains no session, participant, evidence,
constraint, or lifecycle fields (`aauth_permission/models.py:26-78`). The current
G27 model therefore places interaction-specific values in authority evidence,
policy, subject/current state, and execution context outside the mission
(`knowledge/research/G27_TIP_JAR_SCENARIO_DECOMPOSITION.md`, "G27
representation finding").

**PI-selected allocation:** one persistent Tip Jar mission governs multiple
participant interactions; a distinct, single-use participation credential
creates separate bounded session state for each interaction. A fresh native
mission instance per participant session is not the selected G27 model. The
contract below derives the required behavior for that selected allocation; it
does not reopen object allocation as an architectural alternative.
The selection rationale is recorded in
`knowledge/research/G27_TIP_JAR_SCENARIO_DECOMPOSITION.md`, "PI-selected
allocation."

G26 already demonstrates a permission request resolved against a mission,
execution-time SOGA evaluation, separate SOGA/AAuth logging, agent-bound deferred
polling, expiry, one-time terminal delivery, authoritative evidence intake, and
re-evaluation (`aauth_permission/service.py:57-90,107-219,224-264`). Those are
lineage/evidence patterns; a G26 approval record is not silently reused as a G27
session-grant schema.

## 2. Derived lifecycle

| Stage | Required state transition or evidence | Classification |
|---|---|---|
| 1. Approved mission | Resolve an immutable approved mission and its `s256`; resolve the authorized Tip Jar policy/action catalog | REPOSITORY EVIDENCE + PROPOSED CONTRACT |
| 2. Issue session grant | Create a fresh participation/session-bootstrap credential authorizing creation of exactly one bounded session under that mission and policy; record issuer, validity, and issuance receipt | PI DIRECTION + PROPOSED CONTRACT |
| 3. Expose through QR | Encode or reference the grant without adding it to the mission; present adequate notice before intentional initiation | PI DIRECTION + PROPOSED CONTRACT |
| 4. Participant initiates | Receive the grant through an intentional scan; do not infer identity, age, guardianship, or general authority | REPOSITORY EVIDENCE |
| 5. Validate and consume | Verify integrity/reference, mission/policy binding where applicable, validity, and unused state; atomically consume or reject | PROPOSED CONTRACT |
| 6. Establish session | Create a fresh live `session_id`, bind it to the consumed grant, mission, policy, initiating channel, and terminal rules | PROPOSED CONTRACT |
| 7. Govern actions | Bind each action request and its current evidence/context to that live session and evaluate it through SOGA/AAuth; no session-wide `ALLOW` is inferred | REPOSITORY EVIDENCE + INFERENCE |
| 8. Terminate/expire | Close on normal completion, withdrawal, configured expiry, distress stop, or safety termination; distinguish the cause | REPOSITORY EVIDENCE + PROPOSED CONTRACT |
| 9. Prevent reuse | Reject re-presentation of the consumed/expired grant and reject action requests for a non-live or wrong session | PROPOSED CONTRACT |

The lifecycle has two different one-time properties: the **grant** may create at
most one session, and a **terminated session** may not be revived. Neither property
means that only one semantic action may occur inside the session.

## 3. Minimal contract

### 3.1 Information required at issuance

**PROPOSED CONTRACT:** an issuer must have or resolve:

1. a stable `grant_id` or opaque grant handle with sufficient unpredictability;
2. the approved `mission_s256`;
3. an immutable or versioned Tip Jar policy/session-class reference only if the
   `mission_s256` alone does not distinguish the bounded interaction being
   instantiated;
4. a notice reference/version that is presented before initiation;
5. issuance time and not-before/expiry or equivalent validity bounds;
6. the single-use rule and terminal/non-carry-forward rule;
7. issuer identity and issuance provenance;
8. a status capable of at least `issued`, `consumed`, `expired`, and `invalidated`
   before session creation;
9. enough persistence/atomicity to prevent two scans from both consuming the
    same grant.

The participant's identity, age, phone identity, and guardian relationship are
not required issuance values for the provisional age/identity-unknown policy.
Their absence must not be converted into invented claims.

The baseline offer is available to any person who encounters adequate notice;
an ordinary browser may be sufficient to present and consume it. No participant
audience, specific phone application, or mission-agent binding is required in the
credential merely to restrict who may scan. A later channel-binding rule may be
needed to correlate subsequent browser inputs with the session it created, but
that is a session-correlation question and does not retroactively make audience
or application identity a mandatory credential field.

### 3.2 Bound to the grant versus resolved by reference

**PROPOSED CONTRACT:** the security result—not one token format—is required.
Two conforming patterns remain possible: an opaque unguessable reference whose
authoritative record carries the bindings, or a self-contained integrity-protected
artifact plus authoritative consumption state. The contract does not select one.

The following must be integrity-protected or structurally inseparable from the
authoritative grant record:

- `grant_id`/handle;
- `mission_s256`;
- policy/session-class reference and version only where needed to distinguish
  the bounded interaction being instantiated;
- issued-at and validity bounds;
- single-use semantics;
- issuer/provenance.

The complete mission, action descriptions, notice text, policy document, and
physical embodiment catalog may be looked up by immutable/versioned reference.
Validation must fail closed if a referenced object is absent, mutable without a
bound version/hash, or inconsistent with the grant. A bearer secret itself must
not be retained in audit logs; a stable identifier or digest is sufficient for
correlation.

**UNRESOLVED:** signature, MAC, capability proof, secure server-side lookup, key
format, QR encoding, and transport authentication. Cryptographic self-containment
is not required if an authenticated authoritative lookup provides equivalent
integrity and atomic consumption.

### 3.3 What the grant means

**PI DIRECTION + PROPOSED CONTRACT:** the artifact is precisely a **single-use, session-scoped
participation credential / session-bootstrap credential**. It authorizes creation
of one bounded Tip Jar interaction session and has these supporting roles:

- an **invitation/offer reference**, because it points to a pre-authorized
  bounded interaction and its notice;
- a **session bootstrap authorization**, because successful single-use
  consumption is authorized to create one live session;
- **evidence of intentional, session-scoped participant consent/grant**, because
  scanning after notice elects to enter that offered interaction;
- a **constrained authorization input**, only in the sense that the provisional
  policy may recognize valid session participation as a required condition for
  named actions.

It authorizes no Misty semantic action. It is not the approved mission, identity
proof, age proof, guardian proof, general authority, an AAuth permission response,
or permission for physical execution. Every semantic action still requires an
independent governance/AAuth evaluation. Whether an external capability
vocabulary can faithfully represent all or part of the credential is
**UNRESOLVED** and is not required to state this contract.

### 3.4 Minimum abstract operations

These names describe required effects, not an API design:

- **issue:** produce a fresh bound grant and issuance receipt;
- **inspect/resolve:** obtain notice and bound mission/policy information without
  consuming the grant, if notice delivery requires it;
- **initiate-and-consume:** validate and atomically consume a grant, then return a
  fresh session reference or a definite invalid/expired/reused result;
- **validate-session:** establish that a subsequent action request belongs to the
  same current live session;
- **terminate:** record a terminal cause and make further ordinary actions fail;
- **status/receipt:** return only the state appropriate to the caller without
  disclosing participant data or reusable bearer material.

Withdrawal and physical safety halt must be enforceable without awaiting another
permission decision. Withdrawal is a session terminal cause, not revocation or
SOGA `DENY`. Capability revocation and governance/post-grant revocation remain
separate and outside this contract.

### 3.5 Session-consumption trust boundary

**PROPOSED CONTRACT:** whichever component or coordinated components maintain
authoritative issuance, consumption, and live/terminal session state are trusted
for the integrity of participation. Ownership is not assigned here.

That trust is material. A compromised, incorrect, or inconsistent authority can:

- permit replay or concurrent double consumption;
- deny a legitimate unexpired credential;
- fabricate issuance or consumption that never occurred;
- create a session without valid participant initiation;
- bind an action to the wrong mission or session;
- terminate, revive, or leave a session live incorrectly;
- provide false freshness, status, or provenance evidence to governance.

The required trust properties are:

1. integrity of the mission, optional session-class/policy, issuer, validity, and
   single-use bindings;
2. authenticated or otherwise trustworthy access to authoritative state;
3. atomic consumption under concurrency;
4. durable, monotonic terminal state that cannot be rolled back into `issued` or
   `live`;
5. fail-closed behavior under missing, conflicting, stale, or unverifiable state;
6. attributable timestamps/provenance and tamper-evident correlation receipts;
7. separation of reusable bearer material from audit identifiers;
8. consistent propagation of withdrawal/termination so later permission or
   execution cannot treat a dead session as live.

These properties do not require the trusted function to be implemented by the
Person Server, wallet, application, governance service, or a separate service.

## 4. State and evidence model

### 4.1 Grant state

Minimum grant transitions:

`issued → consumed`

`issued → expired`

`issued → invalidated`

`consumed`, `expired`, and `invalidated` are terminal for initiation. A failed
validation does not reset or silently extend validity. Atomic consumption must
make concurrent second use fail. The exact invalidation authority and operational
recovery policy are **UNRESOLVED**; general revocation semantics are not introduced.

### 4.2 Session state

Minimum session transitions:

`created/live → normally_closed | withdrawn | expired | distress_stopped |
safety_stopped | failed`

All terminal states prohibit new ordinary action execution and prevent session
revival. Pending action evaluations must be cancelled or rendered stale when the
session terminates. Exact timeout duration and distributed consistency mechanism
remain **UNRESOLVED**.

### 4.3 Evidence presented for each permission evaluation

**PROPOSED CONTRACT:** the AAuth/SOGA action request must make available, directly
or by trusted reference:

- immutable mission reference: `mission_s256`;
- requested semantic action and requesting agent;
- live `session_id` and session status;
- grant issuance/consumption evidence: grant reference/digest, issuer, validator,
  issued/consumed times, validity result, single-use result, and provenance;
- adequate-notice version and evidence that the initiation path followed it;
- participant classification explicitly remaining age/identity unknown unless
  separate authoritative evidence says otherwise;
- applicable policy/constraint reference and version;
- action-specific evidence, such as a session-bound `dance`/`sing` selection or
  a separately established tip-receipt event;
- current execution and physical-safety context;
- freshness and correlation tying all inputs to the same session and action;
- prior terminal/withdrawal status sufficient to fail closed.

Possession of the session reference or grant does not itself produce SOGA
`ALLOW`. The policy evaluates these inputs for each action. Physical execution
requires both the permission result and the independent physical safety boundary.

### 4.4 Audit and receipts

Under the PI-selected allocation, session state is outside the immutable
mission, but its evidence must not become
an unrelated audit silo. An append-only audit relationship must distinguish
rather than collapse:

| Event | Minimum receipt evidence |
|---|---|
| Grant issued | event/reference; grant identifier/digest; mission and applicable policy/session-class references; issuer; issued/expiry times; notice version; provenance |
| Session initiated | session identifier; grant reference/digest; validation and atomic-consumption result; initiating channel attribution without invented identity; created time |
| Permission decision | session, mission, action, current evidence/context references; complete SOGA decision/provenance; distinct AAuth projection |
| Physical execution | permission/decision reference; execution-surface reference; attempted/completed/interrupted result; timestamp and observable receipt; safety outcome |
| Session terminated | session identifier; terminal cause; actor/source attribution; time; pending-action disposition; non-reuse outcome |

“QR scanned,” “permission granted,” and “Misty acted” are not interchangeable
events. Logs must not state execution merely because AAuth returned `granted`.

**PROPOSED CONTRACT:** the minimum correlation chain is:

`mission_s256 → grant_issuance_reference → grant_consumption/session_id →
governance_decision_reference + AAuth_projection_reference →
execution_evidence_reference → session_termination_reference`.

Every event must carry the stable identifiers needed to traverse this chain in
both directions without recording a reusable bearer secret. D-019's complete
SOGA decision and attribution remain distinct from the lossy AAuth projection.

**UNRESOLVED:** repository evidence does not select whether session events are
directly appended to the existing mission log, stored elsewhere and referenced
by mission-log entries, or correlated across append-only stores. Any conforming
choice must anchor the chain at `mission_s256`, preserve ordering/provenance, and
prevent grant/session events from becoming an uncorrelated audit silo.

## 5. Responsibility matrix

No row assigns a required responsibility to one mandatory owner. “Evidence for
owner” records an existing role or a functional fit, not a decision.

| Required responsibility | Plausible owner(s) | Evidence for owner | Unresolved |
|---|---|---|---|
| Hold/resolve approved mission and policy | Person Server; governance service; session service by trusted reference | G26 `PermissionService` currently stores missions and mission policies; D-019 describes SOGA as PS governance policy implementation | Durable authority and deployment boundary |
| Issue a mission/policy-bound single-use grant | Person Server; wallet; Misty/session application; separate session service | No repository component currently implements this; each candidate could potentially issue only if it can prove authorized mission/policy binding | Authorized issuer and trust basis |
| Present notice and QR | Misty/session application; phone-facing session service | G27 makes the phone an access/control/status point and notice part of the interaction, not governance | Display ownership and accessibility |
| Protect grant integrity and validity | Wallet; Person Server; session service | Functional security obligation only; no selected mechanism exists | Opaque lookup versus protected artifact; keys and authentication |
| Atomically validate/consume grant and prevent replay | Person Server; wallet with authoritative state; session service | Requires authoritative mutable single-use state; G26 one-time delivery is a pattern but not this function | Persistence, concurrency, failure recovery |
| Create and own live session state | Misty/session application; session service; Person Server | G27 session is interaction state outside the immutable mission; current G26 state is process-local and not a G27 implementation | Authoritative state owner and durability |
| Preserve participation-state integrity across issuance, consumption, and termination | Any coordinated owner(s) of the preceding state | Derived trust boundary in §3.5; no repository owner is selected | Trust anchors, consistency, auditability, failure domains |
| Bind phone inputs/action requests to session | Misty/session application; session service | The application receives participant choices and constructs action requests | Channel binding and cross-device transfer behavior |
| Validate current session for governance | Governance service using trusted session evidence; Person Server if it hosts governance | SOGA requires current policy/evidence/context; G26 constructs runtime input before evaluation | Push evidence versus trusted lookup |
| Decide action legitimacy | Governance service/SOGA behind AAuth permission boundary | D-019 and reached G26 path | Deployment location, not function |
| Project decision to AAuth | Person Server/AAuth permission service | D-014/D-019 and current `PermissionService` | Production PS implementation |
| Enforce permission at execution surface | Misty/session application/execution adapter | G27 distinguishes permission from physical execution | G28 adapter and receipt |
| Enforce immediate physical halt | Misty/local safety boundary | G27 requires halt independent of governance/network availability | Hardware mechanism and measured envelope |
| Terminate/expire session and stale pending work | Session-state owner; Misty application for immediate stop; governance service notified | G27 terminal rules require coordinated inhibition; no current component contract exists | Source of truth and distributed ordering |
| Preserve correlated append-only receipts | Person Server; governance/audit service; session service contributing events | G26 mission log proves separate SOGA/AAuth events but is in-memory | Durable store, disclosure, retention, privacy |

## 6. AAuth boundary analysis

### AAuth/reached G26 already provides

- the immutable mission and `s256` reference;
- semantic actions in required `approved_tools` protocol structure;
- a permission boundary that accepts a mission reference and requested action;
- terminal `granted`/`denied` projection distinct from SOGA's decision;
- deferred prerequisite mechanisms, including `approval`, when a particular
  action legitimately requires them;
- agent-bound polling, configured expiry, one-time terminal delivery, and
  evidence-driven governance re-evaluation in the G26 implementation;
- append-only separation of mission, SOGA decision, evidence, re-evaluation, and
  AAuth projection in the G26 model.

### Existing objects/mechanisms that can be reused without extension

- Use the native mission unchanged and reference it by `s256`.
- Submit each session action through the existing permission mechanism.
- Carry session/evidence/current-state inputs into the existing runtime
  governance categories outside the mission.
- Use an AAuth deferred requirement only when the action evaluation produces an
  authorized prerequisite matching that requirement. Session creation itself is
  not automatically `requirement=approval` or another deferred requirement.
- Preserve SOGA and AAuth artifacts separately in the audit chain.

### Nearest AAuth analogue: `requirement=interaction`

**REPOSITORY EVIDENCE:** the captured AAuth `-10` research says
`requirement=interaction` is a deferred prerequisite in which a user must act at
an interaction endpoint and the agent receives and relays the interaction URL
and code (`knowledge/research/AAUTH_PERMISSION_RESPONSE_2026-08-14.md:22-30`).
It is the nearest protocol analogue because both mechanisms direct a person to a
bounded interaction endpoint and return evidence/state needed to continue a
protocol-controlled flow.

The timing and unit of work are different:

- **AAuth interaction:** a permission request already exists; permission
  processing raises a deferred `interaction` requirement; the agent directs the
  user to satisfy it; completion allows that same pending permission flow to
  continue.
- **Tip Jar credential:** issuance and QR consumption occur before any semantic
  action permission request; consumption authorizes and creates the bounded
  session in which later, independently governed action permission requests may
  occur.

Therefore `requirement=interaction` does not cover the baseline bootstrap as
currently specified: there is no prior action permission request to defer, and
the result needed is creation of a multi-action bounded session rather than
satisfaction of a prerequisite for one already-pending permission request. This
does not make interaction irrelevant: a later action inside the live session
could use it if that action's SOGA result legitimately requires user-directed
interaction. It also does not establish that all bootstrap behavior is
categorically outside every possible AAuth deployment. No AAuth extension is
proposed.

### Application/PS/session-layer behavior outside the established AAuth boundary

- issuing and rendering QR grants;
- presenting adequate notice;
- atomic single-use consumption and replay prevention;
- creating, correlating, expiring, withdrawing, and closing a live interaction
  session;
- collecting bounded phone choices and tip-event evidence;
- enforcing local physical safety and invoking Misty primitives;
- recording a physical execution receipt.

### Cannot yet be classified

- whether a production AAuth Person Server API should expose grant/session
  operations;
- whether an existing wallet/capability object faithfully supplies the grant;
- whether grant or session status belongs behind one service boundary;
- transport authentication, proof format, keys, and persistent-store model.

No AAuth extension is proposed. After accounting for `requirement=interaction`,
the reviewed G26 material still contains no established AAuth session-grant
object, QR lifecycle, or single-use session bootstrap. That
absence is scoped to the repository's AAuth `-10` research and implementation,
not asserted as an exhaustive statement about future drafts or companion work.

## 7. Concrete implementation-neutral assessment contract

**Finding: YES.** The Tip Jar experiment now produces a concrete contract against
which a real Person Server or wallet implementation can later be assessed:

> A candidate component, alone or in a documented composition, must be able to
> issue or authoritatively resolve an integrity-protected, mission-bound,
> expiring single-use participation/session-bootstrap credential, with a bound
> policy/session class only where needed to identify the bounded interaction;
> present enough information for adequate notice; atomically validate and consume it;
> create or support creation of one correlated bounded session without asserting
> participant identity, age, or guardianship; provide trusted issuance,
> consumption, freshness, status, and provenance evidence to per-action
> governance; terminate the session on closure, withdrawal, expiry, or safety
> stop; prevent grant/session reuse; and preserve distinct receipts for issuance,
> initiation, SOGA/AAuth decision, physical execution, and termination.

The candidate need not own every function. It must expose verifiable behavior
and trust bindings for the functions it claims and interoperate with the owner of
the remaining required responsibilities.

### Later assessment criteria

1. Can it bind a credential to an immutable mission `s256`, issuer, validity
   period, single-use semantics, and—where needed—a versioned policy/session
   class?
2. Can it present or resolve the bound notice before consumption?
3. Can it prevent guessing, tampering, substitution, concurrent double use, and
   replay without logging reusable secrets?
4. Does it atomically produce an attributable issuance and consumption receipt?
5. Can it create or hand off a unique session reference and support authoritative
   live/terminal status?
6. Can later inputs and action requests be bound to the same session without
   claiming identity, age, or guardianship?
7. Can it provide provenance-bearing session evidence to the governance boundary
   and support action-specific evidence references?
8. Can withdrawal/closure/expiry render pending and later action requests stale,
   while remaining distinct from capability or governance revocation?
9. Can it preserve separate SOGA decision, AAuth projection, execution receipt,
   and terminal-session receipt?
10. Are durability, concurrency, privacy, retention, authentication, and failure
    behavior documented sufficiently to test the contract?

Capability revocation is not an assessment requirement for this G27 contract;
using it would touch a decision explicitly deferred by G26.

## 8. Unresolved questions

1. Who is authorized to issue grants, and what assertion proves that authority?
2. What exact policy/session-class identifier/version, if one is needed beyond
   `mission_s256`, and notice identifier/version are adopted?
3. What expiry duration and abandonment rule are adopted?
4. Is the QR an opaque handle or an integrity-protected self-contained artifact?
5. What authenticates the validator, session-state source, and evidence supplied
   to governance?
6. Which component owns atomic consumption and durable live/terminal session state?
7. What channel-binding rule, if any, governs phone refresh, browser closure,
   sharing, or
   transfer to another device?
8. What exact event establishes tip receipt?
9. What retention/privacy rule applies to grant, session, decision, and execution
    receipts, especially when participant identity is intentionally unknown?

## 9. RM-01 / RM-02 record

Repository-native terms searched across `knowledge/strategy`,
`knowledge/research`, `aauth_permission`, `engines`, and `docs` included:
`session grant`, `session bootstrap`, `single-use`, `replay`, `QR`, `invitation`,
`consume`, `consumed`, `withdrawal`, `mission`, `s256`, `permission`, `pending`,
`approval evidence`, `requirement=interaction`, `interaction endpoint`,
`AAuth-Requirement`, and `mission log`.

No implemented or canonical G27 session-grant object, issuer, atomic consumer,
durable session store, QR encoder, or replay-prevention mechanism was found. The
absence claim is limited to the current repository and the reviewed G26/AAuth
artifacts. The G26 pending record and one-time terminal delivery are
functionally relevant patterns but operate on a permission prerequisite, not on
the G27 participant session lifecycle.

RM-02 boundary: this artifact keeps verified repository behavior separate from
the inferred lifecycle and proposed contract. It makes no external component
replacement claim and no ownership or implementation decision.
