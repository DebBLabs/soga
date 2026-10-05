# M02 AAuth Approval-Pending R2 Execution Evidence

Date: 2026-10-05
Status: GATED POSITIVE — AWAITING BLIND DUAL REVIEW AND PI ACCEPTANCE
Authority: D-139
Execution commit: `7001c82510b1d80790210ca025b3791d7cfe590f`
Attempt count: one; consumed; no retry performed

## Accepted instrument

- controller:
  `tools/m02_aauth_fcf656d/run_approval_pending_tests.py`
- controller SHA-256:
  `fb76b2135042178a6915ddca03f409e85981ddf40df49937839355540aab0ee7`
- corrected test SHA-256:
  `b0936449de6a143102ac012f7783ef138a5fe743a56fae41093b53d2eda37c69`
- production lifecycle SHA-256:
  `18717f7b64007c92f6fb893498f1329b8ed049bb6636eb586a44267588bea47b`
- durable provider manifest SHA-256:
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`
- command:
  `/usr/bin/python3 -I -S -B tools/m02_aauth_fcf656d/run_approval_pending_tests.py`
- working directory: `/Users/debb/dev/soga-clean`

## Required pre-execution record

Local `HEAD` and `origin/main` both resolved to
`7001c82510b1d80790210ca025b3791d7cfe590f`.

The complete result of
`git diff --name-only ad743c73c93425cf84d7b0ad9a4fd09325e79578 HEAD`
was exactly:

```text
knowledge/proposals/M02_AAUTH_APPROVAL_PENDING_R2_EXECUTION_PROPOSAL_2026-10-05.md
knowledge/strategy/DECISION_LOG.md
knowledge/working/CURRENT_STATE.md
```

`git status --porcelain -- engines input_adapters verify advisory` was empty.
The four `HEAD` tree IDs were:

- `engines`: `edb7a6500a34f1b1184adc7d79e96fb4846e75f7`;
- `input_adapters`: `8f57ecbb39718327cb93a691d0dd56223489463a`;
- `verify`: `db72f46f5d4c2e99292d219dde18f3b73019d9ec`;
- `advisory`: `20b61d89ddca8002671a30976dc690f7a80e6653`.

The durable `approval-pending-v2` target did not exist before execution. Every
required pre-start control passed.

## Result

The controller exited `0` after `28.3631911277771` seconds. It did not time
out, exceed either output limit, mutate protected state or escape module-origin
confinement. Stderr was empty. All 81 expected tests ran and passed:

- failures: 0;
- errors: 0;
- skipped: 0;
- expected failures: 0;
- unexpected successes: 0.

The socket audit recorded 78 binds and 224 connects under the runner's
literal-`127.0.0.1` guard. The corrected exact status cases passed, including
the privacy-preserving `404` for a complete but unverifiable poll signature.

## Durable artifacts

Directory:
`/Users/debb/dev/research-evidence/soga/executions/approval-pending-v2`

- `approval-pending-evidence.json`: 13,223 bytes, SHA-256
  `21046ece1e1ea96c23a8bcb0675522680f60525666e3ca43e9b57ae841391f46`;
- `approval-pending-stderr.bin`: 0 bytes, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `run-record.json`: 3,556 bytes, SHA-256
  `55f07847bd139d50132d5906416006d2ce24d947413b41393ce07dbe49873af3`.

The run record reports `AAUTH_APPROVAL_PENDING_EXECUTION_POSITIVE`. Its
pre/post source, provider and runner verification completed without error.

## Claim boundary and next holdpoint

This evidence may support only the bounded localhost approval-pending lifecycle
and preserved 65-test AAuth/SOGA and other-party-approval baseline. It does not
establish complete AAuth conformance, verified approver identity, parental or
legal authority, consent, QR, wallet/WAS, presentation or Misty integration.

The D-139 attempt is consumed. No additional execution is authorized. Blind
dual review of this report and the durable artifacts is required before PI
acceptance or further use. All D-139 exclusions remain in force. The unrelated
PI routine-tool proposal remains excluded and untouched.
