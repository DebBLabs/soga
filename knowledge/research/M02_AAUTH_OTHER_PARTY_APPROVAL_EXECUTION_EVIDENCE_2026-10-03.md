# M02 AAuth Other-Party Approval Execution Evidence

Date: 2026-10-03
Status: EXECUTED ONCE — AWAITING BLIND DUAL REVIEW AND PI ACCEPTANCE
Authority: D-131
Execution commit: `4c691a24e48856f59c9fc830a2c8c815a2a121b1`

## Prospective controls and preflight

The D-131 single attempt used the D-130-accepted runner
`tools/m02_aauth_fcf656d/run_other_party_approval_tests.py` at SHA-256
`b0fa483f3ab0ea343de847b8b4acb78096afc81bd81d3f69b0206ef579a3bdc1`.
Local `HEAD` and `origin/main` both equaled the execution commit before the
run. The durable target
`/Users/debb/dev/research-evidence/soga/executions/other-party-approval-v1`
was absent.

The complete pre-execution
`git diff --name-only 1a45a431ecc184508e107f4c79ff50e740cd11f0 HEAD`
result was exactly:

```text
knowledge/proposals/M02_AAUTH_OTHER_PARTY_APPROVAL_EXECUTION_PROPOSAL_2026-10-03.md
knowledge/strategy/DECISION_LOG.md
knowledge/working/CURRENT_STATE.md
```

Pre-execution
`git status --porcelain -- engines input_adapters verify advisory` returned
empty. The execution-commit tree IDs, each equal to its corresponding tree ID
at source basis `1a45a431ecc184508e107f4c79ff50e740cd11f0`, were:

| Directory | Tree ID |
|---|---|
| `engines` | `edb7a6500a34f1b1184adc7d79e96fb4846e75f7` |
| `input_adapters` | `8f57ecbb39718327cb93a691d0dd56223489463a` |
| `verify` | `db72f46f5d4c2e99292d219dde18f3b73019d9ec` |
| `advisory` | `20b61d89ddca8002671a30976dc690f7a80e6653` |

The unrelated untracked PI routine-tool proposal was outside these directories
and remained excluded and untouched.

## Exact execution

From repository-root working directory `/Users/debb/dev/soga-clean`, the
controller executed once as:

```text
/usr/bin/python3 -I -S -B tools/m02_aauth_fcf656d/run_other_party_approval_tests.py
```

The outer process exited `0` after approximately 19.17 seconds and emitted no
terminal output. No retry occurred.

## Durable artifacts

The controller created three mode-`0400` artifacts:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `other-party-approval-evidence.json` | 11,426 | `47fc2c8fa7c063ae3bb03e42c6acc93e20d67345b96e1318437f635d2de2741d` |
| `other-party-approval-stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `run-record.json` | 3,230 | `da09d7cee3f28fe99727edffe499f5fbc7ae5b3dabd0ea2e6d618470d67a12b5` |

The run record reports:

- result `AAUTH_OTHER_PARTY_APPROVAL_EXECUTION_POSITIVE`;
- parsed child result `AAUTH_OTHER_PARTY_APPROVAL_TESTS_VERIFIED`;
- child return code `0`;
- no timeout or stream overflow;
- empty, allowed stderr;
- no parse or post-verification error;
- the accepted durable provider manifest SHA-256
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`;
- all 190 provider RECORD files verified; and
- exact accepted hashes for the runner and every protected source/test file.

The child evidence reports 65 tests run with zero failures, errors, skips,
expected failures or unexpected successes. Socket auditing recorded 46 binds
and 80 connects under the runner's literal-loopback restrictions. Loaded SOGA,
AAuth and provider module origins remained within their required repository or
durable-runtime roots.

The twelve additive tests passed for absent receipt, exact active approval,
ambient bypass, SOGA denial/failure precedence, withdrawal at the next directed
enforcement, continued cryptographic validity but policy denial of a previously
issued token, cross-participant denial, schema/type rejection, expiry and
future-observation rejection, unknown-scope denial, binding mismatches and the
single-variable receipt-state comparison.

## Result and claim boundary

The observed result is a candidate gated positive, pending blind dual evidence
review and PI acceptance. It can establish only that this bounded additive
fixture makes the next directed action depend on a separately represented,
exactly bound, explicitly `unverified-demo-input` other-party receipt while
preserving the accepted AAuth/SOGA flow and 53-test regression baseline.

It does not establish the approver's identity, parental or legal authority,
consent or assent, refusal precedence, continuous consent, cryptographic token
revocation, AAuth `requirement=approval` pending/polling conformance, complete
AAuth conformance, or a real QR, wallet, WAS, phone, presentation or Misty
integration. No further execution or excluded activity is authorized.
