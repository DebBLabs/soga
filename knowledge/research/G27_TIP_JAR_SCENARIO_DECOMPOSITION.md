# G27 Tip Jar Mission and Scenario Decomposition

Status: DRAFT — analysis input; not a Stage Gate finding or implementation authorization

Date: 2026-08-18

## Scope, provenance, and evidence discipline

This artifact analyzes the established Tip Jar use case before any G27 physical
connection or G28 implementation. It does not authorize powering, networking,
configuring, or contacting either Misty, and it does not authorize robot code,
wallet integration, MCP, zCaps, or physical execution.

**PI-attested provenance:** Deb states that Tip Jar predates G27 and the current
Person Server/authority findings and is the established first embodied use case.
The QR-initiated bounded-session model is a refinement of that use case, not a new
use case selected to fit G27. It is used here to test the adopted model, not to
confirm it. No Tip Jar mission, scenario, constraint, or execution record was
found in the repository at the review checkpoint
`main @ c60953b36553f325ec1d8404451bdc836eb80625`.

Evidence labels used below:

- **REPOSITORY EVIDENCE** — present in a canonical or executable repository artifact.
- **PI-ATTESTED OBSERVATION** — reported directly by Deb but not independently
  reproduced from the repository.
- **INFERENCE** — derived for scenario analysis and not yet verified.
- **POLICY HYPOTHESIS** — a proposed G27 decision rule tested by the scenarios;
  not operative until PI disposition.
- **UNRESOLVED** — required information or mechanism is not established.

Under RM-01/RM-02, a needed scenario capability is not treated as physically
available merely because Misty's API or the scenario names it. A governance
permission is not evidence that physical execution occurred.

## 1. Approved mission

### Semantic mission statement

**PI direction, expressed semantically:** the mission principal authorizes the
mission agent to offer one bounded social interaction with Misty II. After notice,
a participant explicitly consents/grants access by scanning the QR code. The scan
initiates one fixed interaction session; the participant's phone may serve as its
access/control point. The QR/phone mechanism is an access point to the governed
session, not a separate governance system, and does not establish identity, legal
status, guardianship, or general authority.

The general pattern is:

`mission authorized → notice → QR consent/grant → bounded session → governed
semantic actions → embodied execution → session termination`.

**PI-selected allocation:** one persistent Tip Jar mission governs multiple
participant interactions. Each interaction uses a distinct, single-use
participation credential to create separate bounded session state outside the
mission. A fresh native mission instance per participant session is not the
selected G27 model. This allocation does not make the QR/phone mechanism a
separate governance system and does not authorize any semantic action without
its own governance evaluation.

The allocation is required by the use case rather than chosen only for object
convenience. A native mission is an immutable, `s256`-bound authorized artifact.
Minting a mission for each participant would therefore require the mission
principal to create and approve a new mission for every person who approaches
Misty, which does not scale to the intended farmers-market setting. It would
also misstate authority by making the participant an approver of a new mission
rather than a participant entering the principal's already authorized mission.
The distinct credential/session layer expresses that participation without
transferring mission-approval authority.

The authorization does not allow Misty to infer identity from perception,
authority from identity or apparent relationship, approval from a gesture,
sufficient authorization from mission alignment, or physical execution from a
permission result. Session initiation establishes intentional participation in
that session, not identity or authority beyond what the modeled action requires.
A child or other bystander is not assumed to have authority; a person described
as a guardian is not treated as such until any relationship and authority required
for the proposed child-directed action are established. Missing evidence,
unavailable governance, an expired session, and safety interruption must not
result in an action being represented as authorized or completed.

Within that session the initial Tip Jar mission authorizes only the bounded
semantic action envelope below:

- greet the participant;
- offer the limited choice `dance` or `sing`;
- perform the selected bounded dance or song;
- acknowledge and thank the participant if a tip is received;
- conduct only brief conversation bounded by the mission;
- close the interaction and return to neutral.

Coordinated eyes/expression, head and arm gestures, speech, and small bounded
forward/back expressive movement are candidate physical realizations of those
semantic actions, not independent mission permissions or raw commands in the
mission. A recorded tip observation may condition thanks, but this mission does
not authorize Misty to execute a payment/value transfer.

Vision-derived consent or identity, nod approval, autonomous emotion recognition,
photography, retained participant data, open-ended conversation, navigation, and
richer physical interaction are not required or authorized. They remain candidate
future actions or missions. The same Misty platform may later run a separately
bounded IIW discussion or participant-requested photography mission; this does not
enlarge Tip Jar.

### Native AAuth mission representation

D-013 and D-019 adopt the immutable native AAuth shape: `approver`, `agent`,
`approved_at`, `approved_tools`, and `description`, bound by `s256`. The object
has no fields for subject, beneficiary, authority relationship, evidence,
interaction context, constraints, lifecycle, or steps. Evolution is retained in
an append-only mission log.

The following is the exact adopted shape populated only to the point supported
by current evidence. Angle-bracketed values are unresolved and make this a
non-instantiated draft, not a valid approved object:

```json
{
  "approver": "<UNESTABLISHED_CANONICAL_IDENTIFIER_FOR_DEB>",
  "agent": "<UNESTABLISHED_CANONICAL_IDENTIFIER_FOR_TIP_JAR_AGENT>",
  "approved_at": "<UNESTABLISHED_APPROVAL_TIMESTAMP>",
  "approved_tools": [
    {
      "name": "greet_participant",
      "description": "Give the participant in one valid bounded Tip Jar session a visibly embodied greeting."
    },
    {
      "name": "offer_tip_jar_choice",
      "description": "Offer the session participant the fixed choice of a bounded dance or bounded song."
    },
    {
      "name": "perform_selected_dance_or_song",
      "description": "Perform only the dance or song selected within the current bounded session."
    },
    {
      "name": "acknowledge_tip",
      "description": "Acknowledge and thank the participant when receipt of a tip is established."
    },
    {
      "name": "brief_bounded_conversation",
      "description": "Conduct only conversation bounded by this Tip Jar mission and session."
    },
    {
      "name": "close_tip_jar_session",
      "description": "Close the interaction and return Misty to the defined neutral state."
    }
  ],
  "description": "Offer one noticed, fixed, QR-consented Tip Jar social session containing only the bounded greeting, dance-or-song choice and performance, tip acknowledgement, brief bounded conversation, and close-to-neutral actions under applicable governance and physical-safety conditions.",
  "s256": "<UNAVAILABLE_UNTIL_ALL_CANONICAL_FIELDS_ARE_ESTABLISHED>"
}
```

`approved_tools` is required protocol structure. It names the semantic operation
at the permission boundary; it is not a list of robot primitives and does not by
itself encode the authorization conditions above. `s256` cannot truthfully be
calculated while the approver, agent, and approval time are unresolved.

**G27 representation finding:** the existing mission object can preserve the
semantic description and name a semantic approved tool. It cannot itself express:

- the QR session identifier or its fixed bounds;
- which participant is bound to a particular session;
- whether that attendee is a child or affected bystander;
- a guardian relationship or its scope;
- an authority source or holder;
- evidence requirements or evidence satisfaction;
- proof of intentional session initiation or attribution of later input;
- interaction freshness, concurrent participants, latency, or walk-away state;
- a `HOLDING` path or physical-safety condition.

Those values would have to enter permission evaluation as authority evidence,
policy, subject/current state, and execution context outside the immutable mission.
The current architecture has such evaluation categories, but no Tip Jar-specific
authorized constraint or evidence artifact is established.

### G27 Tip Jar policy model

This section models the policy that would be required for the first mission. It
does not add fields to the AAuth mission. All rules below are **POLICY HYPOTHESES**
pending PI disposition.

The ordinary QR participant is age and identity unknown. The policy does not use
"low risk" as an unstated category. Instead, it enumerates the exact conditions
for each action. The mission identified by its approved `s256` is the authority
artifact authorizing the agent to offer these actions. No participant authority
artifact is required for an action that the policy explicitly makes available to
an age/identity-unknown participant. QR consent is session participation evidence,
not an authority artifact.

| Semantic action | Constraints | Required evidence/consent/authority | Missing-condition result | Unknown age/identity? |
|---|---|---|---|---|
| `greet_participant` | Active session; scripted, non-personalized greeting; no contact, recording, identification, or navigation; safety state permits embodiment | Authorized mission `s256`; adequate-notice record; valid session-scoped QR consent/grant; current session reference; current safety context. No participant authority reference | No `ALLOW`; fail closed at the missing stage. Withdrawal/termination still closes without a new decision | **POLICY HYPOTHESIS: yes**, because the action is available to any consenting session participant and neither identifies nor acts legally for them |
| `offer_tip_jar_choice` | Active session; exactly the finite `dance`/`sing` choice; no open request | Same mission/session/notice evidence as greeting. No participant authority reference | No `ALLOW`; do not solicit or accept an out-of-envelope choice | **POLICY HYPOTHESIS: yes**, on the same enumerated non-identifying, non-contact basis |
| `perform_selected_dance_or_song` | Active session; one recorded in-session `dance` or `sing` selection; selected item is in the PI-approved finite catalog; current conceptual safety rules satisfied | Mission/session/notice evidence plus selection evidence bound to the session. No participant authority reference | No `ALLOW`; remain safely pending only if an authorized prerequisite exists, otherwise fail closed | **POLICY HYPOTHESIS: yes**, provided the identical safety and content bounds apply regardless of participant age |
| `acknowledge_tip` | Active session; fixed acknowledgement/thanks; no claim about payer identity, amount, ownership, or transfer authority | Mission/session/notice evidence plus authoritative-enough observation that a tip was received, bound to the session. No participant authority reference | No `ALLOW` for acknowledgement; no tip is inferred from QR scan or identity | **POLICY HYPOTHESIS: yes**, because it acknowledges an established event without performing a transfer |
| `brief_bounded_conversation` | Active session; only PI-approved scripted prompts/responses needed for greeting, fixed choice, selected performance, thanks, and closure; finite turns/duration; no personal-data solicitation or retention | Mission/session/notice evidence and any input bound to that session. No participant authority reference | Out-of-catalog input receives no conversational action beyond safe closure; no open-ended continuation | **POLICY HYPOTHESIS: yes** only under these scripted bounds; a free-form conversation is outside mission |
| `close_tip_jar_session` | Active session; fixed closure; terminal consumption; calm/neutral return | Current session reference. Normal completion may be governed; participant withdrawal, expiry, distress stop, and safety halt may force termination without a new permission | Terminate safely; do not reopen or execute queued actions | **Yes for closure**; stop availability cannot depend on age or identity |

Where a future action actually requires guardian authority, the policy would need
an explicit authority reference and evidence binding the asserted guardian,
child, scope, action, session, freshness, and provenance. No such authority
artifact/reference or evidence shape is established for Tip Jar. Therefore the
first policy does not authorize a scanner to extend the session to another person.
A claimed parent/guardian may initiate for self, but child inclusion remains a
policy hypothesis requiring separate PI disposition; any path that requires
guardian authority fails closed at Authority establishment.

The policy projection remains SOGA-shaped: satisfied conditions permit evaluation
to produce `ALLOW`; absent required evidence produces no grant. An authorized
`HOLDING` path would have to be declared explicitly under D-020. This draft does
not infer one for Tip Jar.

### Notice and bounded-session rules

These are **POLICY HYPOTHESES** pending PI disposition:

1. **Adequate notice precedes consent.** Notice identifies the Tip Jar mission's
   finite action envelope, that actions are governed before execution, that the
   scan creates one bounded session rather than identity, that no participant data
   is intentionally retained by this mission, and how to stop/close.
2. **QR consent/grant is explicit and session-scoped.** A valid scan after notice
   requests exactly one new session. The phone may carry the session reference,
   bounded choices, status, and stop control; it is not a PDP or governance system.
3. **Duration is event-bounded plus expiry-bounded.** A session begins only after
   validation and ends at the earliest of normal closure, participant/parent stop,
   distress stop, safety termination, or configured expiry. It cannot remain
   indefinitely live. The actual expiry duration requires PI decision; no number
   is invented here.
4. **Initiation is single-use.** Each accepted initiation creates one session
   reference. Replaying the same initiation evidence cannot create a second
   session, reopen a terminated session, or repeat an action. Exact cryptographic
   and storage mechanics are G28 implementation concerns after this rule is adopted.
5. **Actions are session-bound.** Selection, tip event, governance request,
   permission, and execution record bind to the same current session. A grant for
   one action is not a grant for another or for another participant.
6. **Withdrawal terminates ordinary interaction.** Explicit participant/parent
   stop immediately inhibits further ordinary actions without a new permission
   decision. It is session termination, not revocation and not SOGA `DENY`.
7. **Nothing carries forward between participant sessions.** QR consent,
   selections, action permissions,
   participant/parent claims, inclusion attempts, and tip observations expire with
   the session. Under the PI-selected allocation above, the mission itself
   persists across participant sessions, but no participant authorization or
   session state carries into a later scan.
8. **Terminal behavior is legible.** Pending, allowed/executing, declined/failed,
   expired, withdrawn, safety-stopped, and normally closed states must not be
   conflated. Exact presentation and transport are not selected here.

## 2. Baseline QR-session interaction

The baseline is a participant who receives notice of the bounded offer,
intentionally scans the QR code, and enters one fixed Tip Jar session. It does not
use Misty's cameras to discover the participant or infer approval. The functional
chain is:

`perception/observation → session initiation → identity if required → authority or
consent if required → governance → semantic action → physical execution`.

The required seven-stage walkthrough maps that chain without collapsing its
boundaries:

1. **Observation** — The participant is presented notice of the bounded Tip Jar
   offer and the system receives a QR-session initiation request. This is
   protocol/session input, not camera recognition and not yet proof that the
   request is valid, current, or responsive to adequate notice.
2. **Interpreted evidence** — The request is validated as one explicit
   consent/grant to start the offered fixed session: correct notice/offer,
   unused/fresh initiation, and bounded session context. The scan establishes
   participation in that session only. The notice contents, QR/session format,
   phone binding, and validation mechanism are **UNRESOLVED**.
3. **Attribution** — The interaction is attributed to the QR-session participant,
   not to a person selected from camera observations. For an anonymous greeting,
   stable civil identity is not required; the necessary attribution is the binding
   between the request and this session participant. How subsequent requests bind
   to the same session is **UNRESOLVED**.
4. **Authority establishment** — Under the modeled action-by-action policy, the
   mission `s256` authorizes the offer and the noticed QR initiation supplies
   session-scoped consent. The policy requires no participant identity or general
   authority for its exactly enumerated, non-identifying, non-contact actions.
   Action-specific evidence still applies: a recorded selection precedes
   performance and established tip receipt precedes `acknowledge_tip`.
5. **Governance decision** — SOGA evaluates the same mission, requested semantic
   action, valid/current session evidence, policy, execution context, and safety
   state. It may return `ALLOW` only if an authorized Tip Jar policy recognizes
   the session participation evidence and the physical safety conditions are met.
   That Tip Jar policy is not yet present in the repository.
6. **Permitted semantic action** — A resulting `ALLOW` permits only the requested
   action in the mission envelope for this session. A selection of `dance` or
   `sing` is bounded session input, not permission for arbitrary performance.
   Permission does not separately authorize each primitive or any future action.
7. **Physical execution** — The execution surface composes the permitted semantic
   action from approved bounded primitives and independently records success,
   failure, withdrawal, safety interruption, and return to neutral. The session
   then continues within its bounds or terminates.

**Positive-control finding:** the fixed-session policy hypothesis justifies why
identity and general participant authority are not required for its exactly
enumerated actions. It therefore supplies a coherent candidate path, using
`greet_participant` as the minimal positive control:

`mission authorized → intentional QR session validated → no additional identity
or authority required for greet_participant → governance ALLOW →
greet_participant → bounded physical execution`.

The path is not yet an operative positive path. It stops at stage 5 until the PI
adopts or rejects the policy hypothesis and its notice/session/safety rules. It is
also not repository-executable or evidence-complete. This is not a manufactured
`ALLOW`: the model now provides an explicit rule capable of supporting `ALLOW`,
while preserving policy authorization as the remaining G27 blocker.

Within a future valid session, the same analysis repeats per semantic action:

- `offer_tip_jar_choice` requires an active session and fixed choice set.
- `perform_selected_dance_or_song` additionally requires a recorded selection and
  action-specific safety context.
- `acknowledge_tip` additionally requires evidence that a tip was received; it
  does not authorize or execute the transfer.
- `brief_bounded_conversation` requires enforceable topic/turn/duration bounds,
  which are not yet defined.
- `close_tip_jar_session` terminates the session and returns to neutral.

### Resulting positive and negative paths

**Candidate modeled positive path (minimal):** authorized mission → adequate
notice → valid QR consent/grant → current bounded session → policy requires no
identity or additional authority for `greet_participant` → SOGA `ALLOW` → bounded
embodied greeting → return/continue safely within session → session termination.
This path is coherent but stops at governance until the policy hypothesis and
conceptual safety rules are adopted.

**Unresolved parent/child hypothesis:** authorized mission → notice to claimed
parent → QR consent/grant and attempted child inclusion → current bounded session.
The path then stops: the scan proves neither parent status nor guardian-child
authority, the current evidence shape does not establish the relationship, and
"low risk" is not a policy category. A future policy could enumerate a specific
child-directed action and justify a sufficient consent/authority rule, but no
positive child-inclusion path is established here.

**Defined negative paths:** inadequate notice or invalid/stale/replayed scan stops
at Interpreted evidence; no session binding stops at Attribution; a heightened
child-directed action lacking required guardian evidence stops at Authority
establishment; absent/unavailable governance stops at Governance decision; missing
tip-receipt evidence prevents `acknowledge_tip`; a late result cannot authorize an
expired session; participant/parent withdrawal or distress stops ordinary
interaction without a new permission; physical safety halt interrupts execution
without converting the governance decision to `DENY`.

## 3. Required variations

Each variation explicitly retains all seven stages or identifies its stopping
stage.

### V1 — Age/identity-unknown participant initiates for self only

1. **Observation:** a QR-session initiation request arrives.
2. **Interpreted evidence:** it is validated as one intentional, fresh session start.
3. **Attribution:** the request binds to this session participant; age and identity
   remain unknown and are not inferred.
4. **Authority establishment:** the modeled policy requires the mission `s256`,
   notice, QR consent, current session, and safety context, but no participant
   identity or authority reference for `greet_participant`.
5. **Governance decision:** `ALLOW` is possible only if that policy is adopted and
   all enumerated conditions are satisfied.
6. **Permitted semantic action:** `greet_participant` for this session only.
7. **Physical execution:** bounded greeting primitives execute and return neutral.

**Current stopping stage:** 5 — the model has a coherent candidate path, but the
proposed Tip Jar policy and conceptual physical-safety rules require PI adoption
before the model can treat an `ALLOW` as legitimate.

### V2 — Child independently initiates; bystander does not initiate

1. **Observation:** either a child independently scans, or a child/bystander is
   merely near Misty. The system does not infer age through vision.
2. **Interpreted evidence:** ambient presence is not initiation. A valid child scan
   is session consent, although the system still receives it as age/identity unknown.
3. **Attribution:** a scan can bind the anonymous participant to the session; a
   bystander without a scan has no session.
4. **Authority establishment:** the policy hypothesis explicitly makes the six
   enumerated, non-contact, non-identifying actions age-neutral. It does not infer
   adulthood. If the PI does not adopt that rule, the child path has no substitute
   age/parent evidence and fails closed.
5. **Governance decision:** applies the actual participation policy; it must not
   infer adulthood or parental consent from the scan.
6. **Permitted semantic action:** only the explicitly enumerated actions whose
   age/identity-unknown participation conditions are established for this session.
7. **Physical execution:** only the allowed bounded action; otherwise none.

**Outcome:** a bystander without a scan stops at session initiation. A child scanner
has the same candidate path as any unknown participant only if the PI adopts the
explicit age-neutral action rules; otherwise the path stops at Governance decision.

### V3 — Claimed parent/guardian initiates and includes a child

1. **Observation:** a person claiming to be a parent/guardian scans after notice
   and explicitly attempts to include a child in the fixed session.
2. **Interpreted evidence:** a valid session consent/grant and explicit inclusion
   are distinguished; the scan does not prove legal guardianship.
3. **Attribution:** the request binds to the adult session participant and names or
   otherwise session-binds the intended child without using vision as identity.
4. **Authority establishment:** the scan establishes neither parent status nor
   guardian-child authority. The current evidence shape does not establish the
   relationship, and the first policy contains no child-inclusion rule.
5. **Governance decision:** fail closed for extending the session to the child. An
   authorized deferred path could be used only if later explicitly declared.
6. **Permitted semantic action:** none directed to the child under the current
   modeled policy; the scanner's self-only session remains separable.
7. **Physical execution:** no child-directed execution.

**Current result:** stops at stage 4. Parent/child inclusion remains an unresolved
policy hypothesis, not a positive path.

### V4 — Participant attempts to extend the session to another person

1. **Observation:** a participant initiates for self and later requests an action
   directed to another person, child or adult.
2. **Interpreted evidence:** the valid self session and extension request are
   distinguished; proximity does not join the other person.
3. **Attribution:** the request binds to the scanner's session; no session consent
   from the other person is established.
4. **Authority establishment:** the scanner's QR consent cannot be transferred.
   No relationship or authority artifact authorizes action for the other person.
5. **Governance decision:** fail closed for the extension; the self-only session
   may continue within its own bounds.
6. **Permitted semantic action:** none directed to the other person.
7. **Physical execution:** no extended-person execution.

**Stopping stage:** 4 — consent and authority cannot carry from the scanner to
another person.

### V5 — Ambiguous gesture

1. **Observation:** an ambiguous gesture occurs near an offered or active session.
2. **Interpreted evidence:** it remains ambiguous ambient input and is not used to
   initiate the session or approve `greet_participant`.
3. **Attribution:** unnecessary for the initial path; session attribution comes
   from the QR initiation.
4. **Authority establishment:** derives only from conditions applicable to the
   requested action, not the gesture.
5. **Governance decision:** ignores the gesture as approval evidence.
6. **Permitted semantic action:** depends on the valid QR request and governance,
   never on the ambiguous gesture.
7. **Physical execution:** occurs only after the independent governed path.

**Outcome:** the gesture no longer creates a stopping point because it is not in
the initial approval path. Without a valid QR session, the scenario stops at
session initiation.

### V6 — False-positive nod or gesture

1. **Observation:** sensor records unrelated movement.
2. **Interpreted evidence:** a classifier may falsely label it a nod, but that
   label is outside session initiation and initial authorization.
3. **Attribution:** no QR session is created or transferred by the label.
4. **Authority establishment:** no authority or consent follows from it.
5. **Governance decision:** receives no valid `greet_participant` request on that basis.
6. **Permitted semantic action:** none on that basis.
7. **Physical execution:** none on that basis.

**Stopping stage:** session initiation. The QR model removes this false positive
from the positive-control authorization path.

### V7 — Missing required evidence

1. **Observation:** a QR-session request or child-directed request occurs.
2. **Interpreted evidence:** session evidence is incomplete, invalid, stale, or
   lacks an action-specific prerequisite.
3. **Attribution:** session binding may exist but does not repair missing evidence.
4. **Authority establishment:** declared evidence requirement is unsatisfied.
5. **Governance decision:** no `ALLOW`; use only an authorized `HOLDING`/deferred
   path, otherwise fail closed under D-020.
6. **Permitted semantic action:** none while evidence is missing.
7. **Physical execution:** none.

**Stopping stage:** 4 — required evidence is absent.

### V8 — Concurrent child, guardian, and another attendee

1. **Observation:** three people are present and one or more QR-session requests arrive.
2. **Interpreted evidence:** each valid initiation creates one fixed session; mere
   group presence or overlapping gestures do not join anyone to it.
3. **Attribution:** each request and later input must bind to its session. One
   participant's scan is not automatically another attendee's session.
4. **Authority establishment:** guardian authority, the child's affected status,
   and the other attendee's independent authority must be evaluated separately.
5. **Governance decision:** one person's valid evidence must not authorize an
   action attributed to another; the repository has no Tip Jar correlation model.
6. **Permitted semantic action:** only an actor-bound outcome, if independently allowed.
7. **Physical execution:** only that outcome, with no spillover representation
   that all present agreed.

**Stopping stage:** 3 if session/input correlation is absent; stage 4 also remains
unresolved for any child-directed action requiring guardian authority.

### V9 — Governance unavailable

1. **Observation:** QR-session initiation arrives.
2. **Interpreted evidence:** session evidence may be valid.
3. **Attribution:** the request may be bound to the session participant.
4. **Authority establishment:** may be available but cannot substitute for a
   governance determination.
5. **Governance decision:** unavailable; no decision is produced.
6. **Permitted semantic action:** none requiring governance.
7. **Physical execution:** no governed Tip Jar action; enter a defined safe
   degraded presentation state once one is authorized.

**Stopping stage:** 5 — the PDP/governance service is unavailable.

### V10 — Network partition

1. **Observation:** QR-session input may arrive on one side of the partition.
2. **Interpreted evidence:** session validation may continue only if its required
   dependencies are reachable; their placement is not yet established.
3. **Attribution:** session binding may fail if its source is across the partition.
4. **Authority establishment:** may fail if authoritative evidence cannot be
   obtained or freshness checked.
5. **Governance decision:** may be unreachable or lack required current inputs;
   no cached grant is assumed.
6. **Permitted semantic action:** none unless a future authorized degraded-state
   rule expressly supports it.
7. **Physical execution:** no governed Tip Jar outcome; local physical safety
   controls remain operative.

**Stopping stage:** the earliest unavailable dependency among 2–5. Current
topology and caching policy are unestablished, so a single later stage cannot be
selected without inventing architecture.

### V11 — Governance reachable but response exceeds the interaction latency bound

1. **Observation:** participant initiates a persistent bounded QR session.
2. **Interpreted evidence:** session evidence is validated.
3. **Attribution:** request binds to the session participant.
4. **Authority establishment:** authority inputs are prepared or requested.
5. **Governance decision:** the session remains pending in a safe, legible state;
   a response eventually arrives after the session's validity or human usability
   bound has expired.
6. **Permitted semantic action:** the late permission must not be treated as live
   permission for the expired interaction without a fresh request/context check.
7. **Physical execution:** none for the expired interaction.

**Stopping stage:** 6 — a decision existed, but its execution context was no
longer current. This differs from unavailable governance.

### V12 — Physical safety halt during an interaction

1. **Observation:** interaction and a physical hazard/halt signal occur.
2. **Interpreted evidence:** safety signal is classified independently of social
   or authority evidence.
3. **Attribution:** social evidence may remain attributed; the safety halt does
   not require guardian attribution to stop hazardous actuation.
4. **Authority establishment:** prior authority does not override the halt.
5. **Governance decision:** any existing permission remains distinct from the
   physical enforcement state and cannot compel continued actuation. No new
   permission decision is required to honor the halt.
6. **Permitted semantic action:** no new physical action while halt is active;
   whether a non-physical acknowledgement remains permitted is unestablished.
7. **Physical execution:** the local safety mechanism stops/inhibits actuation and
   records the interruption; completion is not reported.

**Outcome:** reaches stage 7 as an interrupted physical execution, not successful
completion and not necessarily governance revocation.

### V13 — Participant or parent withdraws, interaction ends, or person walks away

1. **Observation:** the participant or initiating parent withdraws, explicitly
   ends the session, the fixed session expires, or loss of engagement/presence is
   otherwise observed.
2. **Interpreted evidence:** termination is validated against the session rules.
3. **Attribution:** termination binds to the same QR session.
4. **Authority establishment:** previously supplied authority or consent does not
   establish continuing participation after withdrawal.
5. **Governance decision:** withdrawal terminates/inhibits the interaction without
   requiring another permission decision. A pending evaluation must not silently
   become a new interaction; cancellation/expiry semantics are not established.
6. **Permitted semantic action:** no late attendee-directed outcome after the
   interaction context expires.
7. **Physical execution:** stop/return to a neutral state; exact expression is
   unestablished.

**Stopping stage:** 6 for any late permission; the interaction-bound semantic
action is no longer current. Pending termination semantics are a G27 finding.

### V14 — Included child becomes distressed

1. **Observation:** the parent or child communicates distress or asks to stop.
   Autonomous emotion recognition is not required or relied upon.
2. **Interpreted evidence:** an explicit stop/withdrawal signal is associated with
   the active parent/child session; no emotional diagnosis is made.
3. **Attribution:** the stop binds to the active session and may be supplied by
   either the child or initiating parent.
4. **Authority establishment:** no additional authority evidence is required to
   stop the interaction.
5. **Governance decision:** ordinary interaction stops without awaiting a new
   permission decision; this does not imply SOGA `DENY`.
6. **Permitted semantic action:** only session closure and calm/non-stimulating
   return to neutral; autonomous comforting or emotional intervention is outside
   the mission.
7. **Physical execution:** stimulating speech, dance, song, and expressive motion
   stop; Misty enters the defined calm neutral state.

**Outcome:** reaches stage 7 as participant/parent withdrawal and safe closure,
not as autonomous emotion governance or intervention. The explicit stop input and
calm neutral state remain unimplemented/unestablished.

## 4. Guardian and third-party authority findings

The mission is Deb's mission. Neither child nor guardian is assumed to be a party
to its delegation chain. Deb's approval can authorize Misty to conduct a class of
interaction, but cannot by itself establish that an adult has authority to act
for a particular child in a particular encounter.

Current architecture distinguishes human relationship, normalized delegate role,
authority evidence, and governance evaluation. `project/roles.md` explicitly says
family relationship alone does not define authority and that authority must be
declared and evidenced. The G26 trust boundary recognizes an authority holder
only through an authenticated Person Server assertion referring to a declared
authority artifact; G26 does not resolve or authenticate the human independently.

For any child-directed action whose policy requires guardian authority, an
authoritative source would have to supply evidence binding at least:

- the asserted guardian or authorized adult;
- the affected child;
- the relevant relationship or legal authority;
- the scope covering the exact Tip Jar semantic decision;
- validity/freshness and provenance;
- the request/interaction to which the assertion applies.

No current repository artifact supplies that evidence. The native mission object
cannot represent this relationship. The provisional G26 approval-evidence object
can bind an assertion to mission hash, action, constraint, authority reference,
asserting Person Server, human attribution, result, and re-evaluation, but it does
not represent a guardian-to-child relationship or establish that its scope covers
Tip Jar. Reusing it without an authorized Tip Jar constraint and authority
artifact would invent semantics.

**Finding:** the QR scan establishes neither legal guardianship nor general
guardian authority. The current evidence shape does not establish a
guardian-child relationship, and "low risk" is not an established governance
category or decision rule. Parent-initiated child inclusion therefore remains an
unresolved policy hypothesis, not a positive path. The first modeled policy does
not permit the scanner to extend the session to another person, so the current
child-inclusion path stops at Authority establishment. If a later policy permits
a particular child-directed action under a specific consent or authority rule,
that rule must be explicit and justified. Where guardian authority is required
and cannot be established, the path remains fail-closed. A future wallet or
Person Server might supply an artifact, but no wallet behavior, credential,
delegation, or authority structure is assumed here.

## 5. Latency and degraded-state findings

The QR scan creates a persistent but fixed and bounded session. Latency is no
longer derived from recognizing a nod before a fleeting gesture ends. It remains
a human-relative and session-relative bound rather than a justified fixed number:

- Notice must remain available long enough for an intentional scan, and the
  response must arrive while the same QR session, participant binding, evidence,
  and execution context remain current.
- A conversational pause must not be so long that the attendee reasonably treats
  the exchange as failed or leaves.
- If the person walks away, that observed termination overrides any remaining
  usefulness of a later permission for that interaction.
- The bound may differ for initial session acknowledgement, governance decision,
  guardian evidence presentation, and physical execution. No single value is yet
  supported.

The model requires a safe, legible intermediate state while governance is
pending. The participant must be able to distinguish at least "session received,
decision pending" from permission, denial, execution, and failure. The phone may
serve as that session control/status point, but this is not yet selected or
implemented. The pending state may not begin embodied action, imply approval, or
continue past the session bound. Its exact sensory expression is not yet
authorized; it must also remain distinguishable from Misty's charging and safety
indications.

Three failure classes remain distinct:

1. **Governance unavailable:** no governance result can be obtained. Stop at
   Governance decision and enter a safe, non-committal degraded state.
2. **Network unavailable/partitioned:** one or more session, authority,
   governance, logging, or execution dependencies may be separated. Stop at the
   earliest missing required dependency. Local-versus-remote placement is not
   decided.
3. **Governance reachable but too slow:** a result exists, but the human
   interaction context has expired. Do not execute it as if timely; require a new
   interaction/evaluation if the person re-engages.

**G27 requirement:** G28 must measure end-to-end stage timestamps and preserve an
interaction correlation identifier outside the immutable mission. What creates
that identifier and the exact expiry rule remain unresolved; this artifact does
not add them to the mission schema.

## 6. Derived capability requirements and physical-safety rules

The following capabilities are derived only after the scenarios. Evidence status
describes this repository/project, not Misty's published product specification.

| Semantic need | Minimum primitive or external dependency | Evidence status | Boundary/finding |
|---|---|---|---|
| Present bounded-session notice | QR-adjacent and/or phone-visible notice of scope, duration, actions, and stop control | assumed/unverified for modeling | Notice must precede consent/grant; exact content and presentation are unresolved. |
| Initiate one intentional session | QR presentation plus session-validation path | assumed/unverified for modeling | Scan creates a bounded session, not identity or authority. This need is not necessarily a Misty-native function. |
| Bind requests to the session | Session correlation and freshness state | assumed/unverified for modeling | Must prevent replay, cross-session input, and late execution; representation remains unresolved. |
| Accept bounded participant control | Phone/session input for `dance` or `sing`, withdrawal, and close | assumed/unverified for modeling | Access/control point only; not a governance system. |
| Show pending state | Legible non-committal display/eyes, sound, or other signal | assumed/unverified for modeling | Must not imply permission or conflict with charging/safety indications. |
| Speak greeting | TTS/speech output | repository-confirmed | Repository contains optional `POST /api/tts/speak` code, but no retained physical-run evidence. |
| Present attentive expression | Display/eyes | assumed/unverified for modeling | Candidate primitive for the single semantic greeting. |
| Nod/attend | Bounded head pose | assumed/unverified for modeling | Output primitive, not participant approval input. |
| Give bounded gesture | Bounded arm movement | assumed/unverified for modeling | Output primitive, not a separate mission permission. |
| Express embodiment through motion | Small forward/back drive with bounded distance and speed | assumed/unverified for modeling | Expressive motion, not navigation; conceptual safety rules are modeled, while measured bounds remain G28 work. |
| Perform bounded dance | Prebounded composition of expression, head/arms, sound, and expressive motion | assumed/unverified for modeling | Must be selected in-session and independently governed as the semantic action. |
| Perform bounded song | Prebounded audio/speech and optional expression composition | assumed/unverified for modeling | Must be selected in-session; no open catalog is implied. |
| Establish that a tip was received | Tip-event evidence source bound to the session | assumed/unverified for modeling | Conditions `acknowledge_tip`; scan and participant identity do not prove receipt. |
| Bound brief conversation | Enforceable topic, turn, duration, and stop limits | assumed/unverified for modeling | Open-ended conversation is outside scope; actual bounds are unresolved. |
| Indicate coarse system state | Chest LED | repository-confirmed | Repository sends `POST /api/led`; no retained physical-run evidence. Charging may independently use orange LED. |
| Camera/vision perception | Presence, attention, or richer-interaction sensing | not required | Removed from initial session/approval path; future capability only. |
| Receive spoken response | Microphone/audio capture and interpretation | not required | Not required for the initial fixed greeting; may support future conversation. |
| Produce guardian/authority evidence | External authoritative evidence source/Person Server boundary | assumed/unverified for modeling | Not a Misty perception function; current Tip Jar source and shape are absent. |
| Obtain governance decision | Network/API path to the same SOGA PDP with current context | repository-confirmed | G26 proves permission-boundary governance, not Misty execution or Tip Jar inputs. |
| Enforce physical safety halt | Local immediate halt/inhibit mechanism | assumed/unverified for modeling | Must remain effective during governance/network failure. |
| Honor withdrawal/distress stop | Explicit participant/parent stop path to calm neutral | assumed/unverified for modeling | Requires no new permission and performs no autonomous emotional intervention. |
| Record stage provenance | Correlated observation, evidence, decision, permission, execution, and interruption log | assumed/unverified for modeling | G26 mission log is process-local and does not prove physical execution. |
| Navigation | Mapping/path planning/docking navigation | not required | Expressive forward/back motion is not navigation. |
| Camera image retention | Stored photo/video | not required | Presence/gesture sensing does not imply retention; G27 must treat capture and retention separately. |
| Payment/value transfer | Payment capability | not required | Outside the Tip Jar mission; only evidence of receipt conditions `acknowledge_tip`. |

### Semantic-action-to-physical-primitive mapping

These are candidate realizations, not separate mission permissions. Optional
primitives may be omitted only if the remaining composition still satisfies the
semantic action and the adopted safety rules. "Repository-confirmed" below means
code support was found; it does not establish successful physical exercise.

| Semantic action | Candidate physical primitives | Not required | Evidence status |
|---|---|---|---|
| `greet_participant` | Short speech; eye/display expression; head orientation/nod; bounded arm gesture; optional small forward/back expressive motion; return to neutral | Navigation, vision-derived identity, touch | Speech is repository-confirmed; all other listed primitives are assumed/unverified for modeling |
| `offer_tip_jar_choice` | Short speech; eye/display expression; optional head orientation and bounded arm gesture | Base motion, navigation, vision | Speech is repository-confirmed; display/head/arm are assumed/unverified for modeling |
| `perform_selected_dance_or_song` | For dance: prebounded eye/display, head, arm, sound, and optional small expressive base-motion composition. For song: prebounded speech/audio and optional expression/head/arm composition. Both return to neutral | Navigation, contact, open-ended performance selection | Speech is repository-confirmed; display/head/arm/audio composition/base motion are assumed/unverified for modeling |
| `acknowledge_tip` | Short speech; eye/display expression; optional head or bounded arm gesture | Base motion, navigation, payment transfer | Speech is repository-confirmed; display/head/arm are assumed/unverified for modeling |
| `brief_bounded_conversation` | Scripted speech; eye/display expression; optional head orientation | Base motion, navigation, open-ended dialogue, retained participant data | Speech is repository-confirmed; display/head and bounded dialogue enforcement are assumed/unverified for modeling |
| `close_tip_jar_session` | Short closure speech; calm eye/display state; return head, arms, and base to neutral | Navigation, further participant-directed actuation | Speech is repository-confirmed; display and physical neutral return are assumed/unverified for modeling |

Expressive forward/back motion is not navigation. No physical availability or
successful actuation is established merely because a primitive appears in this
mapping.

### G27 conceptual physical-safety rules

G27 retains the rules that determine when actuation may occur; it does not invent
measured limits:

- A physical safety halt bypasses governance and immediately inhibits actuation.
- Actuation must not occur despite a governance `ALLOW` when the session has
  ended or been withdrawn, the permission is absent/stale/wrong-session, a
  required primitive is faulted or unavailable, a concurrent actuation conflicts,
  the required safety state is unavailable, or safe completion/return to neutral
  cannot be established.
- Motion must not begin when the required obstruction/hazard state cannot be
  established. This is a conceptual fail-safe rule, not a claim that a particular
  sensor or obstruction algorithm exists.
- Safe degradation means omitting an unsafe optional primitive and using only a
  separately safe composition, or performing no embodied action if the semantic
  action cannot still be satisfied safely.
- Success, failure, timeout, withdrawal, and interruption require a calm/safe
  neutral outcome conceptually; the actual pose and measured values are not
  established.
- Participant withdrawal/session termination inhibits ordinary interaction
  without another permission decision. It remains distinct from the physical
  safety mechanism that preempts hazardous actuation.

Actual reach, speed, distance, force, measured latency, obstruction response that
requires hardware measurement, and verified neutral poses are G28 measurement and
validation requirements after the G27 rules are adopted. They are not G27 numeric
exit blockers. No numeric envelope or verified physical primitive is asserted by
this draft.

**PI-attested historical observations relevant to capability evidence:** Deb reports
that physical segmented-network testing occurred before the project shifted to a
controlled mockup. That observation supports neither a particular Misty primitive
nor a Tip Jar execution result. No PI-attested LED, TTS, display, head, arm,
camera, microphone, or drive exercise is recorded in this artifact.

## 7. Separate interruption mechanisms

### Participant withdrawal/session termination

Purpose: end the current participant's bounded interaction when the participant
or initiating parent explicitly requests stop, the session completes or expires,
or the modeled distress stop is invoked. It inhibits further ordinary actions
without another permission decision and returns Misty to the calm/neutral state.
It is session termination, not revocation, not a physical safety determination,
and not by itself SOGA `DENY`.

### Physical safety halt

Purpose: immediately stop or inhibit unsafe physical actuation. It belongs at the
physical enforcement boundary, must remain effective if governance or networking
is unavailable, and records an interrupted execution. It does not by itself
revoke authority, invalidate the mission, or produce SOGA `DENY`.

### Capability revocation (for example WAS/zCap)

Purpose: make a previously available capability or delegation unavailable for
future invocation according to that capability system. The repository has not
connected WAS/zCap to Misty or Tip Jar. Revocation behavior is not assumed, and
this artifact does not authorize it.

### Governance or post-grant revocation

Purpose: change whether previously granted authority may still be exercised under
current mission, policy, evidence, and state. G26 explicitly leaves post-grant
obligations and live revocation outside its implementation. No Tip Jar mechanism
is defined. It must not be represented by a physical halt or capability revocation
unless a future decision establishes the relationship.

## 8. Unresolved and falsifying cases

These are in-scope G27 findings requiring disposition before G27 exit:

1. The initial semantic envelope is now bounded to six named actions; the exact
   notice, QR/session representation, phone control, and validation mechanism are
   not established.
2. Canonical approver identifier, agent identifier, approval timestamp, and
   therefore mission `s256` are unestablished.
3. The native mission cannot encode interaction-specific subject, guardian-child
   relationship, authority, evidence, constraints, latency, or safety state.
4. This artifact now defines a proposed Tip Jar policy/constraint model for
   session consent, six action bounds, required evidence, absent-evidence behavior,
   and age/identity-unknown participation. It is a policy hypothesis awaiting PI
   disposition, not an operative authorization. It deliberately does not authorize
   parent/child inclusion or invent a RESTRICT path.
5. No mechanism establishes session correlation, freshness, replay resistance,
   or binding of subsequent input to the same participant/session.
6. The proposed policy makes specified non-identifying, non-contact actions
   available without identity, age, or general participant authority, but the PI
   has not adopted that rule. Parent inclusion remains unresolved: the scan does
   not establish parent status, the evidence shape does not establish the
   guardian-child relationship, and no child-inclusion rule is defined.
7. Gesture assent is removed from the initial path; no future gesture-evidence
   rule is established.
8. Session end, withdrawal, replay, non-carry-forward, and terminal-consumption
   rules are modeled, but the fixed duration/expiry and pending-cancellation
   mechanism still require PI disposition and later implementation.
9. No measured human interaction latency bound exists.
10. Network-partition dependency placement is unestablished, so the earliest
    failed stage varies by topology.
11. No safe, legible pending/degraded presentation behavior or phone control/status
    behavior is authorized.
12. No repository evidence establishes QR-session handling, participant choice,
    tip receipt, conversation bounds, display, head, arm, dance/song composition,
    expressive drive, calm/neutral return, withdrawal stop, or safety-halt behavior.
13. Governed permission is not yet connected to or evidenced as physical Misty
    execution; that remains G28 scope.

A model that silently supplies any of these missing values fails the stated
falsification criterion.

## 9. Questions produced by the model

These questions arise from the walkthrough and are not assumptions used to close it:

1. What exact observable completion record proves each requested semantic action
   executed within bounds and returned or progressed safely within the session?
2. What canonical identifiers and approval instant instantiate Deb's immutable
   AAuth mission and its `s256`?
3. Who or what is the AAuth `agent` for this mission: a stable orchestration agent,
   a Misty-specific agent, or another already-established actor?
4. Will the PI adopt the proposed action-specific policy that treats notice plus
   valid QR consent as sufficient participation evidence for enumerated actions
   despite unknown age/identity? Parent inclusion is not included; what separately
   justified rule and evidence, if any, would permit a named child-directed action?
5. For any future action that actually requires guardian authority, what
   authoritative source can bind the guardian to the child and scope that
   authority to the action?
6. What session mechanism binds initiation and subsequent input to the correct
   participant when several people are present, without requiring identity when
   the action does not need it?
7. What validates a QR initiation as fresh, single-use, and bound to one fixed session?
8. What event or bound ends the session, and how are pending evaluations cancelled
   or rendered stale?
9. What human-derived latency distribution and bound result from controlled
   observation of the interaction?
10. Which dependencies must remain available during a network partition, without
    yet deciding their local or remote placement?
11. What safe, legible pending/degraded response is permitted while governance is
    deciding or cannot decide in time?
12. Which physical actions require immediate interruption, and what independently
    verifiable signal proves the halt took effect?

13. What measured space, distance, speed, obstruction, and return-to-neutral
    limits make the small forward/back movement safe and expressive rather than
    navigational?

14. What finite dance, song, and conversation catalog/bounds belong to this
    mission, and what evidence establishes a participant's selection?

15. What session-bound event establishes that a tip was received without turning
    this mission into a payment system?

16. What notice is sufficient before the QR consent/grant, and which stop/status
    controls must remain available on the participant's phone?

## 10. Future semantic-action catalog — recorded, not modeled

The bounded governed-session pattern may later support a separately authorized
IIW discussion session, participant-requested photography, richer conversation,
bounded physical interaction, vision-mediated interaction, and other Misty
assistance. Each would require its own semantic authorization, action-specific
policy/evidence analysis, privacy and safety conditions, and scenario
decomposition. Recording the catalog does not add those actions to the Tip Jar
mission or authorize implementation.

## 11. Disposition of findings from the first draft

### Changed

- The initial envelope changes from one `greet_participant` positive control to a
  fixed sequence/catalog of six bounded semantic actions, while retaining the
  greeting as the minimal positive control.
- The QR scan changes from session initiation alone to explicit participant
  consent/grant following notice; it still proves neither identity nor general authority.
- The participant's phone becomes a possible session access/control/status point,
  not a separate governance system.
- Participant discovery/approval changes from camera/gesture inference to
  intentional QR-session initiation.
- Ordinary-participant attribution changes from unresolved physical-scene
  identity to session-bound attribution; civil identity is not required for the
  anonymous greeting.
- Ordinary-participant authority changes from presumed external self-authority
  evidence to a proposed action-specific rule requiring no identity/general
  authority for the enumerated age/identity-unknown participant actions, subject
  to PI adoption.
- Parent initiation and explicit child inclusion remain an unresolved hypothesis,
  not a positive path. The scan proves neither parent status nor guardian-child
  authority, and the current evidence shape cannot establish the relationship.
- Latency changes from a fleeting gesture/conversational-turn problem to a fixed,
  persistent-session bound with a required pending state.
- Drive changes from not required to a candidate bounded expressive primitive;
  navigation remains not required.

### Survives

- The native mission cannot carry notice/consent state, session state,
  guardian-child relationship, action-specific authority evidence, latency, or
  physical-safety context.
- The mission still lacks canonical approver/agent identifiers, approval time,
  and calculable `s256`.
- Guardian relationship and scoped authority remain unresolved whenever a
  child-directed action's policy requires them.
- Missing evidence, governance unavailability, network partition, late response,
  participant/parent withdrawal, safety halt, and session termination remain
  distinct cases.
- Permission remains distinct from physical execution, and participant/session
  termination, physical safety halt, capability revocation, and governance or
  post-grant revocation remain four separate concepts.
- No physical Misty capability or safety envelope is established merely by this model.

### Merged

- Physical-scene actor attribution, concurrency, freshness, withdrawal, and walk-away issues
  merge into the narrower requirement for session correlation, freshness,
  participant binding, and termination across concurrent sessions.
- Ambiguous and false-positive gesture findings merge into one boundary: ambient
  gestures are outside the initial session/approval path and cannot create a request.
- The former undefined degraded response and slow-governance questions merge into
  the requirement for a safe, legible pending/degraded state within the session bound.

### Disappears from the initial path

- Camera-based participant discovery and nod/gesture approval.
- A requirement to identify an ordinary participant solely to greet them.
- A requirement for ordinary-participant identity or general-authority evidence
  beyond noticed intentional participation, unless later authorized policy
  introduces one for a particular action.
- Payment/value transfer as a possible interpretation of the initial action.

These disappear only from the initial positive-control path. They are not findings
about future photography, conversation, physical interaction, vision-mediated
interaction, payment, or other missions.

### Becomes a G28 implementation/validation requirement after G27 disposition

- Demonstrate notice, QR consent/grant, one-session correlation, bounded phone
  control, and terminal session consumption without treating them as identity or
  governance systems.
- Demonstrate the same governance boundary separately for greeting, choice,
  selected performance, tip acknowledgement, bounded conversation, and closure.
- Validate physical primitive availability and measure reach, speed, distance,
  force, latency, obstruction response, halt behavior, degradation, and neutral
  return against the G27 conceptual safety rules.
- Preserve distinct evidence for session consent, governance decision, semantic
  permission, physical execution, interruption, and session termination.
- Measure end-to-end and per-stage latency against the G27-approved session bound.

These are not authorized by this draft; they become G28 requirements only after
their G27 models and policies are dispositioned.

### Requires PI decision before an instantiated mission or G28 execution

- Canonical mission approver, agent identifier, approval time, and resulting `s256`.
- Exact notice and fixed session duration/expiry; the draft already models
  withdrawal, replay, non-carry-forward, and terminal-consumption rules.
- The finite dance, song, and brief-conversation catalogs/limits.
- Whether to adopt the action-specific rules that permit enumerated actions for an
  age/identity-unknown participant without additional identity or authority.
- Whether child participation remains excluded from the first mission or a
  separately justified child-inclusion rule and evidence requirement must be
  modeled; QR initiation alone is insufficient.
- The session-bound event accepted as evidence that a tip was received.
- The intended pending, calm/non-stimulating, degraded, and neutral states after
  their safety implications are modeled.

No item in this list authorizes a mission-schema extension.

### Positive-control conclusion and remaining G27 exit blockers

The model now contains a coherent candidate positive path for
`greet_participant`: authorized mission → adequate notice → valid single-use QR
consent/grant → current bounded session → the proposed policy requires no age,
identity, or additional authority for this enumerated action → governance `ALLOW`
→ bounded embodied greeting → safe continuation or termination. The absence of
identity evidence is not silently repaired; it is addressed by the explicit
action-specific policy hypothesis.

That path is **not yet an authorized legitimate positive path**. It stops at
Governance decision until the PI adopts or rejects the proposed policy and its
conceptual session/safety rules. Remaining G27 exit blockers are:

1. PI disposition of the action-by-action policy, especially availability to an
   age/identity-unknown participant and explicit exclusion or separate treatment
   of child inclusion.
2. PI disposition of adequate notice, fixed duration/expiry, terminal states,
   phone control/status scope, and the non-carry-forward/replay rules.
3. Canonical mission approver, agent identifier, approval instant, and calculated
   `s256` without extending the native AAuth mission schema.
4. Finite dance/song/conversation bounds and the session-bound tip-receipt
   evidence rule.
5. PI adoption of the conceptual no-actuation, degraded-state, halt, withdrawal,
   and neutral-return rules. Numeric physical measurements remain G28 work, not
   G27 blockers.

Parent/child inclusion is not silently required to make the ordinary-participant
positive control work. If child inclusion is required within the first mission,
its presently unresolved consent/authority rule is an additional G27 blocker; if
it is excluded, that exclusion must be explicit in the adopted policy.

## RM-01 search record and evidence limits

Repository-native searches covered `tip jar`, `tip-jar`, `tipjar`, `QR`,
`notice`, `session`, `expiry`, `replay`, `withdrawal`, `age`, `identity`, `child`,
`guardian`, `bystander`, `nod`, `gesture`, `Misty`, `approved_tools`,
`authority_reference`, `required_evidence`, `restrict_path`, `HOLDING`,
`semantic action`, `physical primitive`, `interaction`, `latency`, `network
partition`, `revocation`, and `safety halt`
across the current tree and the adopted decision/model artifacts.

Primary repository bases were D-013, D-019, D-020, the G26 mission/permission
decision, `aauth_permission/models.py`, `project/roles.md`, the G27/G28 roadmap,
and the previously verified Misty wrapper/sanity code. No Tip Jar-specific file or
history evidence was found. This draft therefore establishes model boundaries and
questions; it does not establish physical capability, guardian authority, or a
complete executable mission.
