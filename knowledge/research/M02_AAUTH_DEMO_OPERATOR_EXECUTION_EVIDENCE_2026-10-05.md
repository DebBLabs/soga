# M02 AAuth Demo Operator Adapter Execution Evidence

Date: 2026-10-05
Status: OBSERVED POSITIVE — UNACCEPTED PENDING BLIND DUAL REVIEW
Authority: D-143
Execution commit: `7df222cd3b96409bc84a4e99ab55ae51f2228b51`
Source basis: `19294b449471ff898c4e88a1f9b68c2266ae518c`

## Authorized execution

Exactly one bounded execution was performed from
`/Users/debb/dev/soga-clean`:

`/usr/bin/python3 -I -S -B tools/m02_aauth_fcf656d/run_demo_operator_tests.py`

The execution began at `2026-10-05 13:12:55 -0400`. No retry occurred.

## Pre-start controls

The execution commit was
`7df222cd3b96409bc84a4e99ab55ae51f2228b51`.

The complete diff from the D-142 source basis contained exactly:

- `knowledge/proposals/M02_AAUTH_DEMO_OPERATOR_EXECUTION_PROPOSAL_2026-10-05.md`;
- `knowledge/strategy/DECISION_LOG.md`; and
- `knowledge/working/CURRENT_STATE.md`.

`git status --porcelain -- engines input_adapters verify advisory` was empty.
The four `HEAD` tree identities were:

- `engines`: `edb7a6500a34f1b1184adc7d79e96fb4846e75f7`;
- `input_adapters`: `8f57ecbb39718327cb93a691d0dd56223489463a`;
- `verify`: `db72f46f5d4c2e99292d219dde18f3b73019d9ec`;
- `advisory`: `20b61d89ddca8002671a30976dc690f7a80e6653`.

The durable target
`/Users/debb/dev/research-evidence/soga/executions/demo-operator-v1` was absent
before execution. The unrelated untracked PI routine-tool proposal was outside
the protected execution inputs and remained untouched.

## Exact inputs

The runner verified these accepted D-142 inputs before loading them:

- `m02_aauth_fcf656d/demo_operator.py`:
  `b65160deffccf80220a0f466384a98ad1c3d21101dc44a1ee3b5d8099bf238a3`;
- `tests/test_m02_aauth_demo_operator.py`:
  `25abd4b5af7f8eaeaf1585d641bb8e08d024b2cabd09c685c0a319cad5b50f67`;
- `tools/m02_aauth_fcf656d/run_demo_operator_tests.py`:
  `37bc90282e1cf99226c8ce8086b82644a5c429cb7048f6ff9048778bbd95e112`.

The accepted durable provider manifest was verified at SHA-256
`7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`,
including all 190 installed files.

## Result

The controller exited `0` after `34.72146677970886` seconds and recorded
`AAUTH_DEMO_OPERATOR_EXECUTION_POSITIVE`.

- expected tests: 93;
- tests run: 93;
- failures: 0;
- errors: 0;
- skips: 0;
- expected failures: 0;
- unexpected successes: 0;
- load error: none;
- timeout: false;
- stdout overflow: false;
- stderr overflow: false;
- post-verification error: none;
- socket guard counts: 102 binds and 269 connects, all confined by the
  inherited literal-`127.0.0.1` guard;
- protected source, provider and runner state: unchanged.

The result covers the accepted 81-test baseline plus the twelve demo-operator
tests. It proves the bounded standing-policy and held-request seams, signed
poll mismatch handling, sanitized events and errors, finite 120-second receipt
window, bounded duplicate tracking, concurrent operator-write serialization
and D-140 source preservation under the encoded tests.

## Durable artifacts

All artifacts are beneath the single durable directory
`/Users/debb/dev/research-evidence/soga/executions/demo-operator-v1`:

- `demo-operator-evidence.json`: SHA-256
  `36bf2a4f2f7b0e5abef76ceb14b3b793f79690b7a39ce1b74fffda4a0f7dc2ea`,
  14,535 bytes;
- `demo-operator-stderr.bin`: SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`,
  0 bytes;
- `run-record.json`: SHA-256
  `0e6298283bba4465aa00cbaa4778b1a25bd97cda7780365e5d8633e546380fea`.

## Claim boundary

This observed result may establish only that a local operator can feed
synthetic, explicitly unverified other-party state into the accepted standing
resource policy and resource-held pending lifecycle through the two accepted
in-process seams, with the exact behavior covered by the 93-test package.

It does not establish verified identity, parental or legal authority, consent
or assent, presentation correctness, complete AAuth conformance, external
service behavior, wallet/WAS, QR, phone, Misty or physical-resource
integration. It is not accepted until both blind gates review this report and
the durable artifacts and the PI accepts their findings. No additional
execution is authorized.
