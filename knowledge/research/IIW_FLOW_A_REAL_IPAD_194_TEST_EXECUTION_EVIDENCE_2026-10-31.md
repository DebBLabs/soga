# IIW Flow A Real-iPad 194-Test Execution Evidence

Date: 2026-10-31
Status: EVIDENCE CREATED — PENDING BLIND DUAL REVIEW AND PI ACCEPTANCE
Authority: D-182 at SOGA commit `c3e4e84`
Attempt: one authorized attempt; consumed; no retry

## Reviewed inputs

- corrected execution proposal SHA-256:
  `e60a104dbfd2066e72e8ac8cd397af6e04af71eb30817e7b14811cae46585dd4`
- corrected runtime manifest SHA-256:
  `647f3be5a1ecc1eaf5163962ff4f9ffd5cbe97a18595925ced78c03d335c82b3`
- committed controller SHA-256:
  `e66d8a9063ef8050cbba3259f45a6196b7d7b54f26040ccf20ecd74f25f0a3e3`
- accepted presentation commit:
  `964f12626c9220e45a634d85fa407205aa9d9f3d`
- accepted presentation `origin/main`:
  `964f12626c9220e45a634d85fa407205aa9d9f3d`
- SOGA source basis:
  `8746e0cc383ec9d48ab16c89bcea5a88c79ed4d8`

The proposal, manifest and authorization remained untracked. Immediately before
execution, the tracked SOGA diff after the pinned basis contained only
`knowledge/strategy/DECISION_LOG.md` and
`knowledge/working/CURRENT_STATE.md`. The presentation worktree was clean.

## Pre-start observations

- runtime: `Darwin arm64`; `/usr/bin/python3`; Python `3.9.6`
- target evidence path:
  `/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-real-ipad-v1`
  was absent
- literal ports `4317` and `4318` had no listener at the final pre-start check
- no process matching the reviewed controller, `bridge.py`, or the accepted
  fictional-parent child runner remained at the final pre-start check
- all reviewed proposal, manifest and controller hashes matched

An earlier pre-start inventory found the already-running visual-preview bridge
on port `4317`. It was identified by PID and working directory, stopped, and the
entire final pre-start listener/process holdpoint was repeated successfully
before the controller was invoked. This was not a controller attempt and no
evidence directory existed at that time.

## Exact execution

The exact committed controller was invoked once through:

`/usr/bin/python3 -B /Users/debb/dev/permission-to-speak-work/permission-to-speak/run_fictional_parent_presentation_tests.py`

Observed controller status: `0`.

The controller recorded:

- result: `PASS`
- component return codes: `[0, 0]`
- accepted SOGA fictional-parent baseline: `128` tests
- Flow A presentation package: `66` tests
- total: `194` tests
- elapsed controller time: `64.502` seconds
- before/after protected status: empty for both SOGA and presentation inputs
- all fifteen previously preserved evidence hashes unchanged

The baseline reported zero failures, errors, skips, expected failures,
unexpected successes or load errors. The presentation unittest output ended
with `Ran 66 tests ... OK`. Its verbose unittest progress is written to
`stderr.txt`; non-empty stderr is therefore expected and is not an error claim.

## Durable evidence

Exactly three regular files were created beneath the reviewed evidence path:

- `evidence.json` — SHA-256
  `99922ab2e0806ca39c4fd1048dfcdab3e512947e5a1665d80c7064692c43e835`
- `stdout.txt` — SHA-256
  `96bc51ef212452290ad9ab25a006df67af58feee1ebad3c2aafb9fffc565e350`
- `stderr.txt` — SHA-256
  `04eb8c99f04a8cedac9d4fa25833ae99c6e19ed327a58e1544bb8adfaf84c67a`

Byte sizes were `3218`, `18653` and `8241`, respectively.

## Post-run observations

- literal ports `4317` and `4318` had no listener
- no process matching the reviewed controller, `bridge.py`, or accepted child
  runner remained
- the evidence directory contained exactly the three files listed above
- no automatic retry occurred
- the accepted presentation repository remained clean

## Claim boundary

This evidence can establish only the bounded synthetic-loopback behavior of
the exact accepted Flow A package and its preserved 128-test SOGA baseline. It
does not establish live Beryl/iPad operation, a live QR or device interaction,
verified identity, parenthood, parental or legal authority, legal consent,
complete AAuth conformance, wallet/WAS integration, presentation rehearsal,
mBot2, CyberPi, Misty, sensors, speech, movement, G28 or G29.

No evidence or claim in this report is accepted until both blind gates review
the exact report and durable files and the PI separately accepts the result.
The unrelated PI routine-tool proposal remained excluded, unread and untouched.
