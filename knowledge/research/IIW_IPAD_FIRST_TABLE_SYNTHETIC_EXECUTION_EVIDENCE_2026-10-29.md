# IIW iPad-First Table Synthetic Execution Evidence

Date: 2026-10-29
Status: GATED NEGATIVE — PENDING BLIND DUAL EVIDENCE REVIEW AND PI ACCEPTANCE
Authorization: D-162
Attempt: consumed; no retry authorized

## Reviewed instruments

- presentation commit: `15a855fea252e7b7ea14936326d5f4b06312b86a`;
- controller SHA-256:
  `cb7e5758d5d707d698bf4d973b8a1ac7970e9bb62e809c13918d278eabd4283b`;
- runtime manifest SHA-256:
  `ad33928a2d1e7bce6a47aecd437c92ce73d014879b16281c1ab3837b70abdd59`;
- provider manifest SHA-256:
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`.

The final execution authorization remained untracked as required.

## Pre-start holdpoints

All reviewed pre-start holdpoints matched before controller launch:

- presentation HEAD was `15a855fea252e7b7ea14936326d5f4b06312b86a`;
- presentation working-tree diff from `a139376193276ac0ad780e6b61b4520d000f2e37`
  contained only the controller and runtime manifest;
- SOGA working-tree diff from `ab4d3a124e244a5991c85dd01a588db3a6796ee2`
  contained exactly the accepted synthetic execution proposal, decision log and
  current state;
- `/usr/bin/python3` resolved to the Command Line Tools Python 3.9.6 runtime on
  Darwin arm64;
- the durable evidence directory was absent; and
- ports 4317 and 4318 had no listeners.

## Execution result

The exact committed controller was invoked once. It exited nonzero after 58.692
seconds and wrote bounded durable evidence to:

`/Users/debb/dev/research-evidence/soga/evidence/iiw-table-foundation-v1`

Observed result:

- accepted fictional-parent baseline: 128 of 128 tests passed, return code 0;
- iPad-first presentation suite: 30 of 31 tests passed, return code 1;
- combined: 158 of expected 159 tests passed;
- before/after presentation and SOGA protected status were unchanged;
- post-run ports 4317 and 4318 had no listeners; and
- no retry occurred.

The sole failure was
`test_19_proxy_forwards_raw_choice_under_lock`. The test confirmed the required
raw-body forwarding expression exists, then failed because its whole-file
negative string assertion also found `json.dumps(body).encode("utf-8")` in the
generic response helper `_send`. This report records the observation only. It
does not diagnose whether the failure is solely a test-scope defect or authorize
any source correction.

## Durable evidence identities

- `evidence.json` — 1,119 bytes — SHA-256
  `5e5a5ad498a24a6bee1917fb76bdf8853081968b814cafdfc2801c295ea4bb33`;
- `stdout.txt` — 18,653 bytes — SHA-256
  `7358f9848273c939efba7c596d6d5a27d1fd16cb08582facb5b953c18cb28315`;
- `stderr.txt` — 50,479 bytes — SHA-256
  `cf09f5c4f2f080e2ac7662a8281aa132ee05f71b9519a2446b18d0b03551acb3`.

The stderr evidence includes the failed assertion and a rendered copy of the
inspected `bridge.py` text because `unittest` rendered the assertion operands.
It contains no runtime secret or capability value identified by this run.

## Claim boundary

This is a gated negative. It preserves a positive 128-test baseline and 30
passing presentation tests, but it does not establish the accepted 159-test
table-session claim. It does not establish Beryl/iPad operation, live QR or
device interaction, verified identity, parenthood, parental or legal authority,
legal consent, complete AAuth conformance, Project Agent, wallet/WAS, mBot2,
Misty, G28 or G29.

No diagnosis, source change, retry, additional execution or use is authorized
without later PI direction after blind dual evidence review.
