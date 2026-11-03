# IIW Misty-first Gateway Synthetic Execution Proposal

Date: 2026-11-02  
Status: PROPOSED — NO EXECUTION AUTHORITY

## Purpose

Run the accepted D-195 synthetic test controller exactly once, without network
access or physical robot contact, to determine whether the reviewed ten-file
Misty-first gateway package passes its 34 static and synthetic tests.

This proposal does not authorize Misty B access, a stop request, Speak, a
completion-event listener, Beryl access, mBot2 access or any physical action.

## Exact source basis

- Repository: `/Users/debb/dev/soga-clean`
- Accepted package commit:
  `8e8a0f41760762a416ac50e4f92a47b30e149fc9`
- Controller:
  `tools/robot_gateway/run_static_and_synthetic_tests.py`
- Controller SHA-256:
  `a5e17e25d61dfb089ccdd8447b73337dcc60a7c7eff5c5f211a8990b2c46063e`
- Runtime manifest:
  `tools/robot_gateway/misty-phase-runtime-manifest.json`
- Runtime-manifest SHA-256:
  `27c0758984fa0653652d52cd8d47c45276fe357a6888f0f9b232c5037bd45aa6`
- Expected tests: exactly 34
- Interpreter: `/usr/bin/python3`

## Exact invocation

If separately authorized after blind dual review, invoke exactly:

```text
/usr/bin/python3 -B /Users/debb/dev/soga-clean/tools/robot_gateway/run_static_and_synthetic_tests.py
```

No wrapper, alternate interpreter, environment activation, retry or additional
argument is permitted.

## Acceptance-to-execution sequence

This proposal must not be present in the SOGA working tree at execution.

If accepted, its exact reviewed bytes and SHA-256 must first be copied to the
durable external path
`/Users/debb/dev/research-evidence/soga/proposals/IIW_MISTY_GATEWAY_SYNTHETIC_EXECUTION_PROPOSAL_2026-11-02.md`.
The untracked repository copy must then be removed without changing the durable
copy. Only the prospective acceptance decision and synchronized canonical state
may be committed on top of package commit `8e8a0f4`.

After that commit, a separate execution request must be created outside the
repository. It must pin the exact resulting HEAD, the durable proposal hash,
the controller and manifest hashes, and the pre-invocation observation-record
location. Both gates must review that completed request before the PI may
authorize execution. The proposal itself may be committed only after execution
and blind evidence review, when it can no longer affect controller preflight.

## Required pre-start holdpoints

Immediately before invocation, independently record outside both repositories
and outside the absent evidence directory, and require:

1. repository HEAD equals the exact post-acceptance decision/state commit pinned
   in the separately reviewed execution request; package commit `8e8a0f4` is its
   ancestor, and the complete diff from the D-194 source basis contains exactly
   the ten accepted package paths plus `DECISION_LOG.md` and
   `CURRENT_STATE.md`;
2. SOGA status is empty except the exact excluded untracked PI routine-tool
   proposal;
3. presentation HEAD equals
   `c943e594270045daa64694f44c33e3602a8181e6` and its status is empty;
4. controller and manifest hashes equal the values above;
5. all source, preserved, presentation and accepted-evidence hashes in the
   accepted manifest match;
6. evidence directory
   `/Users/debb/dev/research-evidence/soga/evidence/iiw-misty-gateway-static-v1`
   is absent;
7. no public-demo, rehearsal, Beryl, Misty or mBot process is started for this
   execution.

Any failed holdpoint stops without invoking the controller.

## Controller-enforced boundary

The accepted controller must enforce:

- a 60-second total child runtime;
- 2,000,000 bytes maximum for each output stream;
- `/usr/bin/python3 -I -B` for its isolated child;
- exactly 34 tests;
- an audit hook denying the enumerated child network, process-creation and
  filesystem-mutation operations;
- before-and-after source, preservation, presentation and evidence hashes;
- no automatic retry;
- intended evidence outputs only to the initially absent evidence directory;
- exactly three evidence files: `stdout.bin`, `stderr.bin` and
  `evidence.json`, including on child failure after evidence creation.

The audit hook is a bounded test control, not a general Python sandbox or a
native-code safety claim.

## Acceptance boundary

A zero exit from the controller is only candidate synthetic evidence. The
result requires blind dual evidence review and a new PI acceptance decision
before use.

A controller or holdpoint refusal before creation of the evidence directory
consumes no execution attempt. Once the evidence directory is created, that
attempt is final for this path regardless of outcome.

The execution cannot establish:

- contact with or behavior of Misty B;
- the real Misty `StopSpeaking` acknowledgement response shape;
- TextToSpeechComplete event transport;
- a runtime scheduler or driver calling `RobotInvitationCoordinator.tick()`
  to enforce the ten-second completion deadline, five-second response window
  or any timed stop outside synthetic injected-clock tests;
- physical speech, stop, stillness or neutral posture;
- persistence of lock or consumed-decision state across restart;
- complete AAuth conformance;
- mBot2/CyberPi behavior;
- public or participant access to the robot gateway.

## Exclusions

No test execution is authorized by this proposal itself. No listener, Beryl
access, network request, Misty or mBot2 contact, HTTP request, speech, light,
sensor read, movement, package operation, wallet/WAS work, G28 or G29 is
authorized. The unrelated PI routine-tool proposal remains excluded, unread
and untouched.
