# IIW iPad-First Table R2 Execution Evidence

Date: 2026-10-29
Status: OBSERVED POSITIVE — PENDING BLIND DUAL EVIDENCE REVIEW AND PI ACCEPTANCE
Authorization: D-166
Attempt: consumed; no retry authorized

## Reviewed instruments

- presentation commit: `b7772026f54196c0b370fd70012ca0f30b0c4ef3`;
- corrected test SHA-256:
  `d190758c39c6a9f20bae35a4a5a6e1548be347beaa6ca91776d79da98c770f8d`;
- controller SHA-256:
  `f7a0758641bd77001058302f4c96266e509d519938d603d4c65b423ac8c71a3c`;
- runtime manifest SHA-256:
  `41ec44ec5b518e068a8834f952be5abd49d7a82f98e996e8d5bf29243fc96724`;
- unchanged `bridge.py` SHA-256:
  `a71bb86a1dd86b80d58e67699f1c6db9bfd9725ab209c1d6fe8d5d4daacf31d6`;
- provider manifest SHA-256:
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`.

## Pre-start holdpoints

Every reviewed pre-start holdpoint matched before controller launch:

- presentation HEAD and the exact three allowed changes since `15a855f`;
- SOGA HEAD and exactly the proposal, decision-log and current-state changes
  since `5b047d3`;
- exact corrected test, controller, manifest, bridge and provider hashes;
- `/usr/bin/python3`, its resolved Command Line Tools Python 3.9.6 executable,
  and Darwin arm64;
- byte-identical v1 evidence at all three accepted hashes;
- absent `iiw-table-foundation-v2` evidence directory; and
- no listeners on ports 4317 or 4318.

## Execution result

The exact committed controller was invoked once. It exited zero after 59.094
seconds and wrote only to:

`/Users/debb/dev/research-evidence/soga/evidence/iiw-table-foundation-v2`

Observed result:

- accepted fictional-parent baseline: 128 of 128 tests passed, return code 0;
- iPad-first presentation suite: 31 of 31 tests passed, return code 0;
- combined: 159 of expected 159 tests passed;
- before/after presentation and SOGA protected status were unchanged;
- post-run ports 4317 and 4318 had no listeners;
- all three v1 evidence hashes remained byte-identical; and
- no retry occurred.

## Durable v2 evidence identities

- `evidence.json` — 1,119 bytes — SHA-256
  `0880071a0d3b4290bca4f3160a4e1ee67063df4c12a9de6a249cbcd08ee7eaed`;
- `stdout.txt` — 18,653 bytes — SHA-256
  `60060ef0b76ccc13deb55fb3414d17c125e1ee57234cbae2c0f65cb23b1e360a`;
- `stderr.txt` — 3,695 bytes — SHA-256
  `455b0a00f3c3823a55f2b6dbd90f946032ba853c11e8c6e5e47064da24f210d7`.

## Preserved v1 evidence identities after R2

- `evidence.json` SHA-256
  `5e5a5ad498a24a6bee1917fb76bdf8853081968b814cafdfc2801c295ea4bb33`;
- `stdout.txt` SHA-256
  `7358f9848273c939efba7c596d6d5a27d1fd16cb08582facb5b953c18cb28315`;
- `stderr.txt` SHA-256
  `cf09f5c4f2f080e2ac7662a8281aa132ee05f71b9519a2446b18d0b03551acb3`.

## Claim boundary

If independently accepted, this result establishes only the bounded
synthetic-loopback behavior of the accepted iPad-first table package and
preserved fictional-parent baseline. It does not establish Beryl/iPad
operation, a live QR or device interaction, verified identity, parenthood,
parental or legal authority, legal consent, complete AAuth conformance, Project
Agent, wallet/WAS, mBot2, Misty, G28 or G29.

No additional execution, diagnosis, source change or use is authorized pending
blind dual evidence review and PI acceptance.
