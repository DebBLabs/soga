# IIW Misty-first Gateway Synthetic Execution Evidence

Date: 2026-11-03
Status: ACCEPTED GATED POSITIVE
Authority: D-196 and D-197

## Exact execution basis

- SOGA execution HEAD:
  `9ddd1e5ac4b9310e746e640175f02872f5518560`
- Accepted proposal SHA-256:
  `81d2d32848cc97b246cf112f5d0ca686e89fe19955f196e70d4fb1424c3d0b86`
- External execution request SHA-256:
  `dc4cad264b497970da8408bc6930e9b92eaa327544dc4a8a21739aa98441481d`
- Controller SHA-256:
  `a5e17e25d61dfb089ccdd8447b73337dcc60a7c7eff5c5f211a8990b2c46063e`
- Runtime manifest SHA-256:
  `27c0758984fa0653652d52cd8d47c45276fe357a6888f0f9b232c5037bd45aa6`
- External execution authority SHA-256:
  `96d20de5a29b1750e08fbb7e257612b02be8beb51e26c468bfab9eb064a73f4a`
- External preflight record SHA-256:
  `19d5a8509b4e6d62b6dc7f513d9289831c4eb8979bf5dc9537b5c81a4f532876`
- Operator clarification SHA-256:
  `a251241bb9ee2faa6971689f49dc86256fe65fc5802c32b9c187ec7665da71f7`

The one authorized invocation used `/usr/bin/python3 -B` and the exact accepted
controller. No automatic retry occurred.

## Exact evidence

Evidence directory:
`/Users/debb/dev/research-evidence/soga/evidence/iiw-misty-gateway-static-v1`

It contains exactly three files:

- `evidence.json` — SHA-256
  `865be12385e54b52434bde60eec983b20b33638985ac8c5241bca3157938395f`
- `stdout.bin` — SHA-256
  `6722a9705301502675c49c585a14d602e0b78efabc2e254fe464f3b724ff1547`
- empty `stderr.bin` — SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

AGy Gate 2 independently returned PASS with zero blockers in request 130.
Claude Gate 1 verified that the run itself was clean and identified one
preflight-recordkeeping departure. The PI accepted that named departure under
D-197 after the operator clarification was preserved; no rerun was required.

## Accepted result

- Outcome: `completed`.
- Return code: `0`.
- Tests: 34 of 34 passed.
- Failures, errors and skips: zero.
- Stderr: empty.
- Elapsed child time: 0.48381 seconds, within the 60-second limit.
- Stdout: 4,105 bytes, within the 2,000,000-byte limit.
- Controller error type: null.
- Repository HEAD, status and exact twelve-path committed diff matched before
  and after execution.
- All source, preserved, presentation and accepted-evidence hashes matched the
  manifest before and after execution.
- The complete `before` and `after` state objects were equal.
- Presentation status remained clean.
- The evidence directory contained exactly the reviewed three files.

The bounded child installed the reviewed audit hook before importing the test
module. The hook denies its enumerated network, process-creation and
filesystem-mutation operations. It is a bounded test control, not a general
Python sandbox or native-code-safety claim.

## Accepted preflight-record departure

The read-only observations were made at approximately 23:09 on 2026-11-02.
Durable placement was delayed by the required host-filesystem approval. The
critical live holdpoints were rechecked before invocation.

The external preflight JSON did not independently enumerate and recompute every
holdpoint-5 hash. It relied on completed request-129 review verification and
the pinned controller's pre-evidence-directory recomputation. The controller
captured every hash in `evidence.json.before`, recomputed them afterward, and
the complete before-and-after states matched the manifest. D-197 accepts this
package-specific recordkeeping departure without creating precedent.

## Claim boundary and remaining holds

This establishes only bounded static and synthetic gateway behavior. It does
not establish Misty contact or behavior, the real Misty `StopSpeaking`
acknowledgement response shape, completion-event transport, a runtime driver
calling `RobotInvitationCoordinator.tick()`, restart persistence, physical
speech or stillness, mBot2/CyberPi behavior, or complete AAuth conformance.

Before any physical Misty execution, the real harmless stop-only response,
completion-event driver, restart/lock behavior and exact physical execution
command remain subject to separate review and prospective PI authorization.
