# G27 Review Evidence Summary

Date: 2026-08-30
Status: CANONICAL REVIEW SUMMARY — input to the final G27 exit gate; not an
exit decision or an authorization
Current checkpoint verified: `886c5d4ca6714422ced1a019c86951e9b9935ee0`
Branch: `main`

## 1. Purpose and provenance

This artifact makes the evidence supporting a possible G27 exit readable from
the repository. It records what was reviewed, the relevant repository
checkpoint or resulting commit, the reported result, the material corrections
made before PASS, and the limitations that remain.

The Claude and AGy findings below summarize reports retained by the PI outside
the repository. The full transcripts are not repository artifacts, so this
summary does not claim that a future reader can reproduce their wording or
reviewer identity from Git alone. Commit identity, file contents, tests, and the
current working-tree state are repository-verifiable evidence. The PI terminal
walkthrough is a witnessed acceptance activity, not an automated test.

## 2. Review record

### 2.1 Session-grant research package

- Scope: `G27_TIP_JAR_SCENARIO_DECOMPOSITION.md`,
  `G27_SESSION_GRANT_PERSON_SERVER_CONTRACT_2026-08-18.md`, and
  `G27_SESSION_GRANT_CANDIDATE_CONFORMANCE_2026-08-18.md`.
- Canonical result: committed at `dc50ea2` after advisory review reported PASS.
- Material corrections before PASS: source searches and clone SHAs were placed
  with the claims they support; incidental governance/decision/projection
  matches were distinguished from relevant evidence; the persistent-mission
  plus separate-session allocation received a recorded rationale; and the
  contract received a cross-reference to that rationale.
- Result established: an implementation-neutral bounded participant-session
  contract and source-backed candidate assessment. Neither candidate was
  credited with action-governance authority it did not implement.
- Remaining at that point: PI policy dispositions and build/reuse/hybrid
  ownership. D-023 subsequently resolved the six policy dispositions without
  claiming that a candidate supplies the whole contract.

### 2.2 A/B isolation and network requirements

- Scope: `G27_AB_ISOLATION_NETWORK_REQUIREMENTS_2026-08-20.md`.
- Canonical result: committed at `a52b7e8` after advisory review reported PASS.
- Material corrections before PASS: adapter-process crash received an explicit
  failure-mode row, and the existing hardcoded fallback in
  `verify/verify_server.py` was named as a silent-fallback pattern that must not
  carry forward.
- Result established: target isolation, failure behavior, and network-placement
  requirements were specified before any robot connection.
- Remaining: requirements only; no network, robot address, or physical
  connection was authorized or implemented.

### 2.3 Capability safety model

- Scope: `G27_CAPABILITY_SAFETY_MODEL_2026-08-20.md`.
- Canonical result: committed at `a434db1` after advisory review reported PASS.
- Material corrections before PASS: Pending received complete exit conditions
  and precedence; Neutral received explicit entry and exit rules; a safety halt
  was made race-precedent over a late ALLOW; automatic safety-stop release
  received a dedicated negative-control requirement; and Degraded received a
  participant-visible status that remains readable after neutral presentation.
- Result established: conceptual safety, degraded, neutral, and safety-stopped
  behavior, including the distinction between an apparently still robot and a
  latched safety stop.
- Remaining: the versioned physical primitive catalog, interruption classes,
  safe boundaries, and verified release mechanisms are not instantiated.

### 2.4 Bounded acceptance implementation and terminal flow

- Authorization: D-024 at `6d687b3`, clarified for the single-process terminal
  acceptance surface at `bce388f`.
- Implementation: bounded prototype at `4a7acac`; interactive two-stage flow
  and corrections at `d95db19`.
- Reviewed scope: `g27_tip_jar/`, `tests/test_g27_tip_jar.py`,
  `tests/test_g27_demo.py`, D-024, and `g27_tip_jar/GAPS.md`.
- External review record: PI-retained Claude and AGy reports each recorded a
  final PASS after fresh read-only inspection. The reports stated that no files
  were modified by the reviewers.
- Material corrections before final PASS: the repository recorded D-024
  prospectively rather than backdating chat authorization; concurrent different
  grants racing for one session slot received a barrier test; rejected
  governance clears Pending while preserving event history; the CLI clears its
  displayed Pending request after rejection; process-local/unbounded event-log
  limitations were added to `GAPS.md`; and dedicated tests were added for
  identical Pending retry, resolved-request reentry, DENY ordering, and a second
  CLI request while Pending.
- Result established: Pending is observably occupied; governance arrives as a
  separate event; request, decision, dispatch, and outcome are separate records;
  target-bound recording occurs once; physical outcome remains `unknown`; and a
  safety halt defeats a late ALLOW.
- Boundary established by inspection and tests: fake recording surfaces only;
  no robot, external network, HTTP transport for G27, actuation, or
  physical-success path in the active runtime or adapter. The lower-level state
  machine can represent `completed` when passed `observed=True`, as the adopted
  model anticipates, but the prototype has no observation source and its
  runtime always passes `False`; `GAPS.md` records that dormant branch.

### 2.5 PI visible terminal walkthrough

The PI ran `python3 -m g27_tip_jar interactive` and directly observed:

1. issuance and single consumption of a Misty-A-bound grant;
2. a live session with an observably Pending `greet_participant` request;
3. zero fake receipts before governance;
4. a separately delivered ALLOW producing ordered decision, dispatch, and
   unknown-outcome events, with one receipt on A and none on B; and
5. a second Pending request entering safety-stopped, followed by a late ALLOW
   rejected at `session_validation:terminal_safety_stopped`.

This walkthrough demonstrates the terminal acceptance surface. It does not
demonstrate transport, a participant application, robot availability, physical
execution, interruption, or neutral-state verification.

### 2.6 Embodied-execution and Misty landscape

- Scope: `EMBODIED_EXECUTION_AND_MISTY_COMMUNITY_LANDSCAPE_2026-08-20.md`.
- Canonical result: adopted at `c400b2d`; formatting-only normalization at
  `ec955cf`.
- External review record: PI-retained Claude and AGy reports recorded initial
  FAIL findings and later PASS results after the artifact was rebuilt.
- Material corrections before PASS: unsupported or incorrect ROS, hardware,
  processor, MCP, latency, laboratory, and SOGA-safety claims were removed or
  bounded; actual Misty hardware tiers and named community repositories were
  used; the AAuth mission remained immutable and step-free; local physical
  safety remained separate from mission governance; and the bounded MCP absence
  search terms were recorded without claiming universal absence.
- Result established: grounded research context for later implementation
  planning. It authorizes no hardware use or public demonstration.

## 3. Current reproducible verification

At checkpoint `886c5d4`, the command below was run on 2026-08-30:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Result: `Ran 63 tests in 0.530s — OK` (19 G26 permission tests, 8 G27 demo
tests, and 36 G27 Tip Jar tests). The first attempt in a restricted runner
executed all tests but could not bind the existing G26 localhost test server;
the unchanged suite passed when localhost binding was permitted. No external
network or robot was contacted.

## 4. Unresolved limitations carried into exit consideration

The following remain explicit and are not converted into completed capability
by a G27 PASS:

- atomicity and the one-live-session rule are process-local only;
- grant integrity, QR encoding, authentication, durable storage, and service
  ownership are uninstantiated;
- event history is memory-only and unbounded;
- fake surfaces prove receipt only and never physical outcome;
- the state machine's dormant `observed=True` completion representation has no
  independent observation source or evidence binding and is not usable as
  completion verification;
- no durable audit service or participant application exists;
- no primitive catalog, hardware adapter, robot addressing, discovery,
  transport, actuation, or physical safety verification exists; and
- D-025 was authorized separately and prospectively at `90a668e`, after this
  reviewed stage-one package. G28 entry, Misty power or connection, physical
  execution, and public demonstration remain unauthorized.

## 5. Exit-gate interpretation

This record makes the reviewed scope, checkpoints, results, corrections, and
remaining limits available in the canonical repository. It is evidence for the
stage-one portion of a final G27 gate. It does not itself declare that gate PASS
or close G27. It did not authorize D-025; that later authorization is recorded
separately at `90a668e`. It does not authorize G28 or contact with either Misty
robot.
