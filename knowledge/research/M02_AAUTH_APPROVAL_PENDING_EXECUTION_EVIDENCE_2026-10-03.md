# M02 AAuth Approval-Pending Lifecycle Execution Evidence

Date: 2026-10-03
Status: GATED NEGATIVE — AWAITING BLIND DUAL REVIEW AND PI DISPOSITION
Authority: D-135
Execution commit: `619516450033b5d5f7b2334bf1def57923a37441`
Attempt count: one; consumed; no retry performed

## Accepted instrument

- controller:
  `tools/m02_aauth_fcf656d/run_approval_pending_tests.py`
- controller SHA-256:
  `2d639991ef4c5aa918e9ee6328056450f56dcbfd6fdf9db2aaff63641b9cd4bc`
- durable provider manifest SHA-256:
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`
- command:
  `/usr/bin/python3 -I -S -B tools/m02_aauth_fcf656d/run_approval_pending_tests.py`
- working directory: `/Users/debb/dev/soga-clean`

## Required pre-execution record

Local `HEAD` and `origin/main` both resolved to
`619516450033b5d5f7b2334bf1def57923a37441`.

The complete result of
`git diff --name-only 27f8fdb1a84bb5aad8bc2b6534636c369991143b HEAD`
was exactly:

```text
knowledge/proposals/M02_AAUTH_APPROVAL_PENDING_EXECUTION_PROPOSAL_2026-10-03.md
knowledge/strategy/DECISION_LOG.md
knowledge/working/CURRENT_STATE.md
```

`git status --porcelain -- engines input_adapters verify advisory` was empty.
The four `HEAD` tree IDs were:

- `engines`: `edb7a6500a34f1b1184adc7d79e96fb4846e75f7`;
- `input_adapters`: `8f57ecbb39718327cb93a691d0dd56223489463a`;
- `verify`: `db72f46f5d4c2e99292d219dde18f3b73019d9ec`;
- `advisory`: `20b61d89ddca8002671a30976dc690f7a80e6653`.

The durable evidence target did not exist before execution. Every required
pre-start control passed.

## Result

The controller exited `1` after `28.314936876296997` seconds. It did not time
out, exceed either output limit, mutate protected state or escape module-origin
confinement. Stderr was empty. All 81 expected tests ran:

- passed: 80;
- failed: 1;
- errors: 0;
- skipped: 0;
- expected failures: 0;
- unexpected successes: 0.

The sole failure was
`test_10_signature_failures_and_fresh_later_poll` for the malformed-header
subcase. The live response was HTTP `404`; the test allowed only `400` or
`401`:

```text
AssertionError: 404 not found in {400, 401}
```

No diagnosis or claim about whether the implementation or assertion is wrong
is made by this evidence record.

## Durable artifacts

Directory:
`/Users/debb/dev/research-evidence/soga/executions/approval-pending-v1`

- `approval-pending-evidence.json`: 13,855 bytes, SHA-256
  `a84a6aecbde89c982e60962e2e306be0f7be9872a6e49ecd08cb96ed6f49314f`;
- `approval-pending-stderr.bin`: 0 bytes, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `run-record.json`: 3,556 bytes, SHA-256
  `3f83b7c54a3ac00b072bfe9e8ad23ee73a59b0ee2516cc6588d0e1230a84d35e`.

The run record reports `AAUTH_APPROVAL_PENDING_EXECUTION_NEGATIVE`. Its
pre/post source, provider and runner verification completed without error.

## Boundary and next holdpoint

The D-135 attempt is consumed. No retry, code change, test change, additional
listener or execution is authorized. This result does not establish the
approval-pending lifecycle claim. Blind dual review of this report and the
durable artifacts is required before PI disposition. Any diagnosis or
correction requires separate prospective authority. All D-135 exclusions
remain in force. The unrelated PI routine-tool proposal remains excluded and
untouched.
