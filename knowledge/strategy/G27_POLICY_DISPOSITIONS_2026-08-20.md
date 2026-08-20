# G27 Policy Dispositions and Prototype Boundary

Date: 2026-08-20

Status: PI APPROVED — conceptual and policy authorization; not implementation
authorization and not G27 exit

Scope: These dispositions convert the Tip Jar policy hypotheses into the
authorized conceptual model for G27. They preserve the implementation-neutral
session-grant contract committed at `dc50ea2`. A/B isolation, network placement,
capability/safety modeling, the positive control, and the remaining G27 exit
work are still required before G28 entry. Neither Misty may be powered or
connected until the required isolation and network-placement controls exist.

## 1. Age- and identity-unknown participant policy

A participant may enter a bounded Tip Jar session without establishing identity
or age. The following actions may be governed positively without identity, age,
or guardianship evidence because their authority does not depend on those
attributes:

- receive the versioned notice;
- initiate one bounded session through the participation credential;
- receive a neutral greeting;
- receive the finite `dance` or `sing` choice;
- select one offered action;
- receive the selected bounded performance;
- participate in brief catalog-bounded conversation;
- stop or close the session.

`acknowledge_tip` additionally requires an authoritative, session-correlated
tip-receipt event.

Identity, age, appearance, apparent relationship, gesture, proximity, or
possession of the participant's phone does not establish broader authority. An
action whose policy actually requires age, identity, guardianship, or
third-party authority remains `RESTRICT` or `DENY` until the required
authoritative evidence exists.

## 2. Notice, credential, session, replay, termination, status, and concurrency

The version-bound participation notice states:

- the bounded interaction offered;
- the available action categories;
- that scanning initiates one session but does not establish identity;
- that every action remains independently governed;
- that the participant may stop at any time;
- applicable retention and observation boundaries; and
- what the phone controls and does not authorize.

Each participation credential is bound to the persistent mission, notice
version, and session-policy version. It expires ten minutes after issuance, may
create at most one session, is atomically consumed, and cannot be replayed,
renewed, or used to revive a terminal session.

Each live session has one unique identifier and one consumed credential. The
session has a five-minute hard maximum and a one-minute inactivity timeout.
Valid participant-originated activity may reset the inactivity timer but never
extend the hard maximum. Internal polling, retries, governance processing,
robot telemetry, and invalid or repeated requests do not reset inactivity.

At timeout or other terminal transition:

- the session records a distinct terminal cause;
- pending decisions and actions become stale;
- no new physical action may begin;
- Misty returns to the neutral state;
- the credential and phone binding cannot revive the session; and
- later requests return terminal status without creating another session.

The persistent mission may authorize multiple participant sessions over its
approved operating period. The first implementation permits only one live
physical Misty interaction at a time. Concurrent scans must not create
concurrent physical sessions or consume a credential unless a session is
actually created.

The phone is bound through an ephemeral session/channel key, not a persistent
device fingerprint or identity claim. One credential creates at most one
session; one ephemeral phone binding has at most one live session. Repeated
identical requests return the existing status or receipt and do not repeat
physical execution. Excessive requests are rate-limited and recorded without
creating extra mission, credential, session, permission, or execution
artifacts. This is a channel/session control, not proof that the same human
cannot use another browser or device.

The first action catalog constrains cardinality: greeting once; choice
presentation once; selection once; one selected dance or song; tip
acknowledgment once per authoritative tip event; conversation to its finite
turn limit; and close once.

Status distinguishes at least: offered, expired, invalid, consumed, session
live, action pending, action permitted, action declined, session withdrawn,
session safety-stopped, session normally closed, and session failed.

The one- and five-minute values are initial prototype values. Later revision
requires measured evidence and PI disposition.

## 3. Canonical mission instantiation

The first Tip Jar mission uses one immutable native AAuth mission object with:

- `approver`: the PI's canonical Person Server identifier;
- `agent`: the canonical Tip Jar mission-agent identifier;
- `approved_at`: the actual PI approval instant;
- `approved_tools`: only the versioned semantic Tip Jar action catalog;
- `description`: the approved bounded Tip Jar mission statement; and
- `s256`: calculated over the canonical AAuth form.

The mission persists across participant sessions. Credentials, sessions,
selections, observations, evidence, decisions, and execution receipts remain
outside the mission and correlate through `mission_s256`. No placeholder
identifier, timestamp, catalog reference, or hash may be represented as
canonical evidence. The actual values must be instantiated before the mission
is represented as approved or executable.

## 4. Finite action catalogs

Every positively governable semantic action references a finite, versioned
catalog. The first mission contains finite greeting, dance, song,
brief-conversation, closing, and tip-acknowledgment sets.

Catalog entries bind semantic actions to permitted physical realizations and
limits. Free-form movement, unrestricted song selection, open-ended
conversation, navigation, photography, identity inference, emotion inference,
and raw actuator commands are outside the first mission. Mutable catalog
contents must not silently enlarge an approved mission; a changed catalog
requires a new version and a governance decision about mission coverage.

## 5. Conceptual safety, degraded behavior, and neutral state

Physical safety is an independent local boundary. It does not wait for
governance or network availability. The physical safety halt may be manually
operated, but it may not be mocked, simulated, scripted as an ad hoc governance
step, or depend on the provisional service chain.

A safety halt immediately inhibits affected execution, supersedes pending or
granted semantic-action permission, and records a distinct safety outcome. It
does not manufacture SOGA `DENY`, participant withdrawal, or capability
revocation.

Missing, stale, conflicting, or unverifiable mission, credential, session,
policy, authority, freshness, network, governance, or safety evidence fails
closed for the affected action. The safe degraded presentation performs no
requested physical action, makes no success claim, preserves stop controls,
provides only a short bounded explanation when safely available, and transitions
to neutral.

Neutral permits only minimum safe and legible behavior. It does not continue
the prior action, improvise a substitute, approach a participant, or infer
authorization from previous success. Timeout values for governance or network
failure are not invented here; they require measurement and PI authorization.

Permission and execution remain separate. Dispatch success is not physical
execution evidence. The PEP/runtime must record `STARTED`, `COMPLETED`,
`INTERRUPTED`, or `FAILED` evidence for an attempted physical action before a
corresponding execution claim is made.

## 6. Child inclusion

The first mission does not require age determination and does not exclude a
participant merely because age is unknown. A child may participate only in the
same low-risk, age-independent envelope available to every unknown-age
participant.

The system does not infer child, adult, parent, or guardian status from
appearance, proximity, speech, or scanning behavior. No guardian relationship
or authority is presumed. Child-directed actions requiring guardian authority,
identity, age, special data processing, physical contact, photography,
navigation, payment authority, or expanded interaction are outside the first
mission unless separately authorized through evidenced policy.

This establishes the G27 positive-control candidate without weakening a
boundary:

`valid mission → valid notice-bound credential → one live session →
unknown-age/unknown-identity participant → finite selected semantic action →
authority established for that age-independent action → permission may be granted`

Current context, local safety, session state, action-specific evidence, and
execution controls still apply.

## Prototype qualification and evidence boundary

The first Misty demonstration is real-first: use actual conformant services to
the greatest extent currently available. A mock, local, temporary, or manually
coordinated component is permitted only for an explicitly identified missing
function needed to make the interaction runnable and observable.

Every provisional component must be named in a per-component manifest, state
what it substitutes for, and identify the claims its use prevents. Prototype
data shapes carry an explicit convergence obligation and do not become
canonical through use. Atomic single-use consumption and terminal non-revival
must be real properties even when their implementation is provisional.

The prototype must preserve the approved governance semantics, authority
boundaries, action-by-action evaluation, session isolation, failure behavior,
independent physical safety, correlation, and evidence attribution. It must
include negative controls for replayed/consumed credentials, wrong-session
actions, expired/terminal sessions, repeated requests, and safety halt during
actuation.

Results are reported as Observed prototype evidence with every mock boundary
enumerated. They do not establish production readiness, platform invariance,
bystander safety in an unconstrained environment, live mid-actuation revocation,
validated perception, or a complete external service chain unless those
properties are separately demonstrated.

Once actual services satisfy the contract, the next mission holds the Tip Jar
scenario constant and runs from real mission creation and approval through
credential issuance, session state, permission, enforcement, physical execution
receipt, and termination evidence. Prototype shortcuts create no architectural
precedent.

Photography remains outside the first mission and is deferred until the G29
living-laboratory privacy, bystander, retention, and deletion methodology is
adopted.

## Immediate consequence

These dispositions authorize the G27 conceptual model, not implementation,
robot connection, or physical execution. Immediate work is:

1. define the Misty A/Misty B isolation property;
2. define network placement and partition behavior;
3. complete the per-capability authority, context, interruptibility,
   degradation, locality, and audit model;
4. define the positive-control and negative-control acceptance criteria; and
5. submit the completed G27 model to its exit gate.
