# G27 Tip Jar Capability and Conceptual Safety Model

Date: 2026-08-20

Status: ADOPTED — G27 requirements; not implementation authorization,
robot-connection authorization, or evidence of physical behavior

Gate/task: G27 — Embodied Capability and Physical Safety Model

## 1. Purpose and boundary

This artifact turns the PI-approved conceptual rules in D-023 into a
per-capability checklist for the first Tip Jar mission. It incorporates the
adopted A/B isolation and network requirements at `a52b7e8`. It does not reopen
the policy dispositions, choose physical measurements, prove a Misty primitive,
or authorize implementation or robot connection.

The roadmap requires each capability to state its risk, authority, relevant
context, interruptibility, revocation behavior, degraded state, audit evidence,
and local-versus-remote needs. The classes below are local to this mission; they
do not claim a repository-wide risk taxonomy:

- **C1 — bounded low-risk expression:** finite, non-contact, non-identifying,
  non-navigational behavior that can be safely omitted;
- **C2 — conditional embodied action:** bounded physical motion, active sensing,
  or device interaction requiring additional current safety/context evidence;
- **C3 — excluded:** behavior outside the first mission or lacking an adopted
  authority, privacy, safety, or measurement basis.

No governance `ALLOW` can override a missing physical-safety condition. A
safety halt can stop execution without changing the governance decision,
mission, authority, or participant status.

## 2. Common action gate

Before any requested physical primitive or composition begins, all of the
following must be true:

1. the mission, action catalog, policy, platform, credential, session, request,
   and decision references are current and mutually bound;
2. the action is finite, available on the named platform, and within its
   approved cardinality;
3. no withdrawal, expiry, terminal state, conflicting execution, safety halt,
   or stale decision exists;
4. every required local safety/context input is available and acceptable;
5. the primitive declares its interruption category, safe interruption or
   completion behavior, and conceptual neutral outcome;
6. the target-bound local adapter accepts the decision and can create an
   attributable execution receipt; and
7. the other Misty's state and command surface remain unaffected.

If any item is false or unknown, the requested action does not begin. The
system records the affected stage truthfully and uses the pending, degraded, or
neutral behavior defined below.

## 3. Per-capability model

### Movement and pose

- **First-mission use:** bounded head/arm gesture and optional small expressive
  forward/back base motion within a versioned composition; no navigation,
  following, approach, contact, or raw participant-supplied actuator command.
- **Risk:** head/arm expression is C1 only after physical bounds are measured;
  base motion is C2. Until G28 validates availability and bounds, both remain
  unverified physical candidates rather than executable facts.
- **Required authority:** current target-bound permission for the containing
  semantic action. Participant selection chooses only from the finite catalog;
  it grants no authority over raw motion.
- **Required context:** correct platform and session, local safety state,
  primitive availability, no conflicting actuation, and established
  obstruction/hazard state. Unknown required context blocks motion.
- **Interruption:** each composition declares immediate-interruptible,
  boundary-interruptible, or safe-completion-required behavior. Withdrawal and
  termination prevent the next primitive; physical safety may preempt the
  active primitive independently.
- **Revocation/expiry:** stale permission, terminal session, withdrawn session,
  or unavailable capability prevents new motion and invalidates queued motion.
  A late `ALLOW` never resumes it.
- **Degraded behavior:** omit optional motion only when the remaining
  composition still safely and truthfully performs the semantic action;
  otherwise perform no requested action.
- **Audit:** platform, semantic action, composition and primitive identifiers,
  decision, dispatch/start/result, interruption source, and whether neutral was
  observed or remained unknown.
- **Placement:** final target check, conflict prevention, interruption, safety
  halt, and neutral handling are local. Mission, policy, and governance may be
  remote but their absence blocks a new action.

### Speech and sound

- **First-mission use:** finite versioned greeting, choice, song, tip
  acknowledgment, bounded conversation, closure, and short unavailable message.
  No open-ended or participant-supplied performance content.
- **Risk:** finite non-personalized speech/sound is C1; content requiring
  identity, age, guardianship, sensitive inference, or unrestricted generation
  is C3.
- **Required authority:** current permission for the semantic action; tip
  acknowledgment also requires the authoritative session-correlated tip event.
- **Required context:** correct session, catalog/content version, cardinality,
  and a local determination that speech output is presently safe and available.
- **Interruption:** queued speech is canceled on withdrawal, termination, or
  halt. Active audio follows its declared stop boundary; no new phrase begins.
- **Revocation/expiry:** invalidates queued or future utterances and prohibits
  late replay. It does not rewrite already emitted sound as unspoken.
- **Degraded behavior:** silence is always permitted. One short, fixed,
  non-success unavailable/closing message may be used only when separately safe
  and authorized by the adopted degraded-state rule.
- **Audit:** content/catalog identifier rather than unnecessary participant
  speech content, plus platform, decision, start/result, interruption, and
  session correlation.
- **Placement:** content/policy selection may be remote; final volume/content
  allowlist, cancel/inhibit, and truthful receipt are enforced locally.

### Camera and perception

- **First-mission use:** none required for the positive Tip Jar path.
- **Risk:** passive safety inputs may become C2 after purpose, retention,
  access, and reliability are instantiated. Photography, identification,
  emotion inference, age inference, relationship inference, participant
  tracking, and retained participant imagery are C3.
- **Required authority:** no participant action or QR scan supplies authority
  for excluded sensing. A future safety sensor use requires a separately
  adopted purpose and data boundary; it cannot be repurposed as social evidence.
- **Required context:** sensor identity, local health/freshness, declared field
  and purpose, retention behavior, and bystander treatment.
- **Interruption:** excluded capture never starts. Any future permitted stream
  must have a local stop and bounded buffer-clearing rule independent of remote
  service availability.
- **Revocation/expiry:** stops future collection; it does not imply deletion of
  evidence subject to a separately adopted retention rule.
- **Degraded behavior:** do not infer missing perception. If a required hazard
  state cannot be established, block affected motion rather than substitute
  identity, proximity, or prior observations.
- **Audit:** sensor/purpose/version, freshness and availability result, whether
  collection occurred, and disposition of any bounded buffer; never claim an
  inference that was not established.
- **Placement:** the physical motion safety decision using a sensor must remain
  effective locally. Remote analytics or identity services are not part of the
  first mission.

### Display

- **First-mission use:** finite eye/display expressions for greeting, choice,
  performance, acknowledgment, closure, pending, degraded, and neutral states.
- **Risk:** fixed non-identifying expression is C1; participant imagery,
  identity-derived content, arbitrary remote content, and deceptive success
  presentation are C3.
- **Required authority:** current action permission for action-specific display;
  fixed pending/degraded/neutral safety presentation follows the adopted state
  rules and conveys no permission or success claim.
- **Required context:** correct platform/session/state and versioned display
  asset; no participant-supplied URL or arbitrary payload.
- **Interruption:** action-specific display changes to the declared degraded or
  neutral display at the earliest safe update boundary.
- **Revocation/expiry:** removes action-specific presentation and prevents
  replay; it does not display `DENY` unless governance actually returned it.
- **Degraded behavior:** calm, non-stimulating fixed presentation, or blank when
  display safety/availability is unknown.
- **Audit:** asset/state identifier, platform, transition cause, timestamps, and
  observed or unknown result.
- **Placement:** the final asset allowlist and neutral/degraded transition are
  local; remote state may request but cannot inject display content.

### Attention cues

- **First-mission use:** finite head orientation, eye/display cue, speech cue,
  or bounded arm gesture that makes the current interaction legible. No
  person-following, gaze-derived identification, persistent tracking, or
  inferred engagement.
- **Risk:** fixed non-tracking cue is C1 after physical validation; tracking or
  inference is C3.
- **Required authority:** current permission for the containing action. A cue
  does not establish participant consent, identity, attention, or authority.
- **Required context:** correct session and platform, safe primitive state, and
  catalog-bounded cue. No bystander is selected from appearance or proximity.
- **Interruption:** cancel queued cues and stop active physical cues according to
  their primitive interruption rule.
- **Revocation/expiry:** prohibits further cues and returns to degraded or
  neutral presentation.
- **Degraded behavior:** omit the cue; do not intensify, approach, repeat, or
  attempt to regain attention autonomously.
- **Audit:** cue identifier, containing action, platform, execution outcome, and
  interruption source; no unsupported claim that a person attended.
- **Placement:** final cue bounds and interruption are local; remote inference
  is excluded.

### Companion-device interaction

- **First-mission use:** the participant phone receives notice/status, presents
  the single-use credential, selects one finite offered action, sends bounded
  conversation choices, and can withdraw/close. It never addresses Misty
  directly.
- **Risk:** bounded session control is C1 at the semantic level; arbitrary robot
  addressing, raw commands, persistent fingerprinting, identity inference,
  payment authority, or cross-session control is C3.
- **Required authority:** valid credential for session creation; current
  ephemeral channel/session binding thereafter. Each physical action still
  requires its own governance result.
- **Required context:** notice and policy version, mission `s256`, credential
  state, channel binding, live session, action cardinality, rate limit, and
  target platform.
- **Interruption:** withdrawal/close immediately prevents new ordinary actions;
  it does not depend on a new permission. Loss of the phone does not disable the
  independent operator safety halt.
- **Revocation/expiry:** consumed credentials and terminal sessions do not
  revive. Repeated identical requests return prior status/receipt and do not
  repeat execution.
- **Degraded behavior:** report pending, unavailable, or terminal status without
  claiming success; do not retry physical actions automatically.
- **Audit:** credential consumption result, ephemeral binding reference, session
  state, request idempotency key, rate-limit result, decision/result references,
  withdrawal, and terminal cause—without creating a persistent phone identity.
- **Placement:** credential/session truth may be remote only with authoritative
  atomic state. Rate limiting and input validation occur at the session edge;
  target enforcement and safety remain local.

## 4. Plain-language operating states

These states describe what an observer and the system may truthfully expect.
Their exact lights, pose, volume, timing, and physical measurements remain G28
work.

### Pending

Misty has received a valid request but required governance or other current
evidence is not complete. She performs none of the requested physical action.
She may show one fixed calm pending indication and the phone may report
`pending`. Pending never extends the one-minute inactivity or five-minute hard
session limit through internal polling.

Pending has four explicit exit triggers, applied in this order:

1. **Safety halt:** enter `safety-stopped`; invalidate queued work and perform
   none of the requested action, regardless of any simultaneous or later
   result.
2. **Session termination:** on withdrawal, expiry, normal close, or another
   terminal transition, make the request stale, perform none of the requested
   action, record the terminal cause, and enter neutral when locally safe.
3. **Request becomes stale while the session remains live:** record the stale
   outcome, perform none of the requested action, and use the degraded-to-neutral
   path. A later result cannot revive that request.
4. **The common action gate resolves while the request is still current:** a
   target-bound `ALLOW` leaves pending only by passing every common-gate check
   and beginning the permitted action; `DENY`, `RESTRICT`, or an unsatisfied
   prerequisite performs none of the requested action and follows the
   degraded-to-neutral path.

The first applicable higher-priority exit wins. In particular, a safety halt
cannot lose a race to `ALLOW`, and a late decision cannot reverse termination
or staleness.

### Degraded

Something required is missing, stale, unavailable, conflicting, or cannot be
verified. Misty does not perform the requested action, does not claim success,
does not reuse an old `ALLOW`, and does not switch to the other robot. Stop
controls remain available. The phone reports `degraded` for the affected
request and does not report permitted, executing, or completed. That outcome
remains readable after Misty's presentation transitions to neutral. If safe,
she may provide one short fixed explanation and then transitions to neutral.
Otherwise she transitions silently.

An optional primitive may be omitted only when the remaining preapproved
composition still satisfies the same semantic action safely and truthfully.
Dropping the primitive must not silently change a dance into a different action
or turn a failure into success.

### Neutral

Neutral is the minimum safe, calm, and legible resting condition:

- no participant-requested or queued action is executing;
- no base movement, approach, following, tracking, recording, or inference is
  initiated;
- head, arms, display, sound, and base use only their adopted neutral settings,
  or remain inhibited when those settings cannot be verified;
- no prior permission, selection, or success is carried forward;
- the phone reports the real pending, terminal, failed, or interrupted state;
  and
- local safety halt and operator control remain available.

Neutral is not proof that a physical pose was reached. Until G28 observes the
platform and measured neutral settings, the receipt must distinguish
`NEUTRAL_OBSERVED` from `NEUTRAL_COMMANDED` or `NEUTRAL_UNKNOWN`.

Neutral is entered after startup only when the local safety state and adopted
neutral settings can be established; after normal completion or closure; after
the bounded degraded explanation (or silent degradation); and after failure,
timeout, withdrawal, or interruption reaches its declared locally safe
boundary. A latched safety halt enters `safety-stopped`, not neutral, even if
the robot appears still.

Neutral exits only in one of these ways:

- a valid current request moves to pending while required evidence is gathered;
- a current target-bound `ALLOW` passes the full common action gate and the
  permitted action begins; or
- a local safety halt moves the platform to `safety-stopped`.

Network restoration, a late decision, process restart, participant retry,
previous success, or activity on the other Misty does not by itself leave
neutral. Leaving neutral never resumes an old action or restores a terminal
session.

### Safety-stopped

The affected platform accepts no new or queued actuation. Its independent local
safety inhibit remains set until an authorized operator verifies conditions and
deliberately releases that platform. Network restoration, a late `ALLOW`,
process restart, participant retry, or release of the other Misty cannot clear
it. The outcome remains safety-specific; it is not rewritten as governance
`DENY`, participant withdrawal, or capability revocation.

Release is a per-platform operator action after verification; it never resumes
the interrupted request. After release, the platform enters neutral only under
the neutral-entry rule above. If neutral cannot be established, execution
remains inhibited and the outcome is recorded as unknown or failed.

## 5. Trigger and priority rules

The most protective applicable rule wins for physical execution:

1. local physical safety halt/inhibit;
2. inability to establish safe execution or safe completion;
3. withdrawal, expiry, terminal session, or operator stop;
4. missing/stale/conflicting authority, policy, decision, or target binding;
5. capability unavailable/faulted or conflicting actuation;
6. valid current target-bound `ALLOW` for the finite action.

This priority controls actuation only. It does not alter the meaning of the
underlying governance decision or fabricate authority evidence.

## 6. Non-delegating affected subjects and bystanders

A participant controls only the offered session actions. They cannot grant
authority over another person nearby. A QR scan, tip, selection, adult presence,
or apparent parent/child relationship does not make a bystander a participant
or delegator.

For the first mission:

- actions are non-contact, non-navigational, and not directed at a person based
  on appearance, identity, age, emotion, relationship, or inferred attention;
- no photography, identity processing, emotion inference, participant tracking,
  or retained bystander audio/image data is authorized;
- sound, motion, and display remain within the same finite catalog regardless of
  who is nearby;
- a participant cannot select arbitrary content or movement affecting others;
- obstruction/hazard uncertainty blocks affected movement;
- a bystander objection or operator concern can cause ordinary interaction to
  stop without being represented as that person's governance authority; and
- the independent physical safety halt remains available for immediate risk.

The model does not claim that ordinary speech, sound, display, or movement has
no effect on bystanders. It limits the action envelope and preserves a stop;
measured space, sound, reach, obstruction response, and operating-area controls
remain G28 validation and deployment work.

## 7. Failure and evidence rules

- Permission is not dispatch; dispatch is not start; start is not completion.
- Process death, network loss, or HTTP success does not prove physical stopping,
  neutral state, or completion.
- A completed receipt requires independent observation adequate for that
  primitive. Otherwise record interrupted, failed, or unknown outcome.
- Missing audit delivery may use only the adopted local durable buffer rule in
  the isolation/network requirements.
- Every result names the platform, session, semantic action, primitive or
  composition, decision, state transition, and evidence source.
- Evidence for A cannot satisfy B, and neither platform silently fails over to
  the other.

## 8. Tests required for this model

Before robot connection, fake execution surfaces must demonstrate:

1. each finite semantic action reaches only its correctly bound fake surface;
2. each common-gate failure prevents invocation and produces the correct
   pending, degraded, terminal, interrupted, failed, or unknown state;
3. optional-primitive omission never changes the semantic action silently;
4. withdrawal and expiry cancel queued work without a new permission;
5. safety stop supersedes an `ALLOW` without rewriting it as `DENY`;
6. process/network failure never produces a false completion or automatic
   resume;
7. excluded perception, arbitrary content, raw commands, navigation, and
   cross-target requests are rejected;
8. neutral receipts distinguish commanded, observed, and unknown outcomes; and
9. bystander/third-party inputs cannot create inferred identity, relationship,
   authority, or expanded action scope;
10. for every candidate physical primitive and prebounded composition in the
    versioned catalog, cover successful invocation, missing required context,
    unavailable/faulted capability, stale permission, withdrawal/expiry,
    its declared interruption category and safe boundary, optional omission
    where allowed, and every receipt state it claims to emit; and
11. a named **safety-stop release test** proves independently that each of the
    following fails to clear A's latched stop: network restoration, late
    `ALLOW`, PEP/adapter process restart, participant retry, and release of
    Misty B. Repeat symmetrically for B. The test then verifies that only the
    named per-platform operator release path can attempt the transition and
    that release does not resume the interrupted request.

The fake safety-stop input tests state priority and receipt semantics only. It
does not count as the independent physical safety halt, which D-023 prohibits
mocking and which must exist and be verified separately before connection.

These tests complement the positive and negative isolation controls in
`knowledge/research/G27_AB_ISOLATION_NETWORK_REQUIREMENTS_2026-08-20.md`.
Passing fake tests does not validate physical primitives or authorize either
Misty to be powered or connected.

## 9. Explicit nonclaims and next boundary

This model does not establish actual reach, speed, force, stopping distance,
volume, pose, sensor behavior, obstruction response, latency, primitive
availability, physical interruption, or neutral-state attainment. Those are
G28 measurement and validation matters after G27 exit.

After this model is adopted, the remaining positive-control criterion is to run
the fake-surface path from authorized mission and bounded session through
Authority Established to exactly one permitted semantic-action invocation,
with the other fake surface unchanged. That demonstration is evidence work, not
robot connection authorization.
