# G27 D-025 Review Evidence Summary

Date: 2026-08-30

## 1. Scope and checkpoints

D-025 authorized a loopback-only split-service acceptance stage at `90a668e`.
The reviewed implementation is committed at `a5af621`. The subsequent D-026
safety-model alignment and explicit session-count assertions are committed at
`680e444`.

The implementation provides four localhost HTTP surfaces in one Python process:
an authoritative grant/session runtime, a governance-decision relay, and
target-bound recording-only surfaces for fake Misty A and fake Misty B. It
contains no external-network, robot, discovery, query, hardware-adapter, or
actuation path.

## 2. PI-visible terminal walkthrough

The PI ran `python3 -m g27_tip_jar localhost` from the repository terminal.
Four distinct ephemeral `127.0.0.1` service addresses were displayed.

The positive path visibly established:

- a single-use grant bound to fake Misty A;
- grant consumption and a live bounded session;
- a request remaining Pending before governance delivery;
- zero fake receipts while Pending;
- a separately delivered `ALLOW` crossing the governance relay;
- one receipt at fake Misty A and zero at fake Misty B;
- distinct request, decision, dispatch, and outcome events; and
- physical and participant-visible outcome remaining `unknown`.

The walkthrough also encountered the adopted one-minute inactivity timeout: a
later request against the expired session was rejected at
`session_validation:terminal_expired`.

The safety path visibly established a fresh Pending request, a safety halt, and
a later `ALLOW` rejected at `session_validation:terminal_safety_stopped`.
Fake Misty A's receipt count remained unchanged and fake Misty B remained at
zero. The services then shut down through the terminal's `quit` command.

## 3. Claude technical gate and correction

The PI-retained Claude report reviewed the complete D-025 working tree against
`90a668e`, read all requested implementation and governing files, and ran the
full suite. It confirmed the loopback, service separation, Pending,
safety-precedence, truthful-outcome, target-isolation, and disclosure claims.

The first pass found one required correction: after a safety stop, a fresh grant
could be consumed into a new live session and the older terminal could expose a
raw state-transition exception when a request followed. No action could
execute, but session admission and terminal behavior were inconsistent.

The correction moved the safety-latch check into runtime-coordinated session
admission. A latched platform now rejects before grant consumption at
`session_admission:safety_stopped`; the grant remains issued, the stopped
session remains the only session, and no fake surface receives anything. State
transition errors are normalized at the runtime boundary and caught
defensively by the original terminal.

The recheck reproduced the original sequence and reported PASS. Its two earlier
nonblocking items were also taken: grant/session memory-only state is stated
directly, and an A-session request naming B is tested across HTTP. The later
explicit session-count assertion is included at `680e444`.

## 4. Independent AGy verification

The PI-retained AGy report independently read the governing artifacts and code
in both directions, inspected commits `90a668e`, `a5af621`, and `680e444`, and
reported PASS with no blocking findings. It confirmed that D-026 refines the
Safety-stopped rule in section 4 of the adopted safety model and that the model
and implementation agree.

The reverse review found one known implementation omission: D-023 specifies
per-action cardinality, but the prototype does not enforce those counters.
Single-use credentials and request idempotency do not implement a turn limit.
That limitation is now stated directly in `g27_tip_jar/GAPS.md` and remains open
beyond this bounded acceptance prototype.

## 5. Verification result

The unchanged full command
`python3 -m unittest discover -s tests -p "test_*.py" -v` passes 72 tests after
D-026. The suite includes the prior 63 tests and nine localhost-stage or
follow-up assertions. No external network or robot is contacted.

## 6. Remaining boundaries

The adopted gaps remain material:

- all four services are threads in one process;
- grant, session, and event state are process-local and memory-only;
- the relay delivers a supplied governance decision but does not evaluate it;
- D-023's per-action and conversation-turn cardinality is not enforced;
- there is no TLS, service identity, authentication, durable store, production
  deployment, replicated-state atomicity, or process-crash isolation;
- fake surfaces establish receipt only and never physical outcome; and
- there is no MCP implementation, Misty connection, or G28 authorization.

This summary records review evidence. It does not itself close G27 or authorize
any excluded capability.
