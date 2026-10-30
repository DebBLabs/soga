# IIW iPad-First Table Test 19 Correction and R2 Proposal

Date: 2026-10-29
Status: PROPOSED — NOT AUTHORIZED
SOGA basis: `5b047d334ffb01b962f53105b95fc7ea703f8977`
Presentation basis: `15a855fea252e7b7ea14936326d5f4b06312b86a`
Review class: mandatory blind dual review under D-064

## Purpose

Correct only the over-broad Test 19 assertion diagnosed and accepted under
D-164, update the bounded controller and runtime manifest mechanically, and
prepare one later R2 synthetic-loopback execution. Production `bridge.py` and
all other accepted presentation and SOGA sources remain unchanged.

## Accepted finding

The D-162 run preserved a positive 128-test baseline and 30 of 31 presentation
tests. Test 19 failed because it searched all of `bridge.py` for
`json.dumps(body).encode("utf-8")` and matched the unrelated outbound response
serializer. The fictional-parent choice branch itself reads `raw_body` once,
holds `bridge.lock` while validating lease and pending state, and returns
`self._proxy("POST", self.path, raw_body)` before the later JSON parse branch.

## Proposed create-only correction

If this proposal is accepted, create-only authority is requested for exactly
three presentation files:

1. `test_fictional_parent_presentation.py`: change only Test 19 so its negative
   assertion is confined to the `/fictional-parent-choice` branch. Preserve
   positive assertions that the branch reads the request once into `raw_body`,
   holds `bridge.lock` through lease and pending-state validation, and forwards
   `raw_body` directly to `_proxy` without parsing or reserialization.
2. `run_fictional_parent_presentation_tests.py`: update only the corrected test
   hash; set presentation basis to
   `15a855fea252e7b7ea14936326d5f4b06312b86a`; permit presentation differences
   since that basis only for the test, controller and runtime manifest; set
   SOGA basis to `5b047d334ffb01b962f53105b95fc7ea703f8977`; permit SOGA differences since
   that basis only for this proposal, `knowledge/strategy/DECISION_LOG.md` and
   `knowledge/working/CURRENT_STATE.md`; and select the absent durable evidence
   directory
   `/Users/debb/dev/research-evidence/soga/evidence/iiw-table-foundation-v2`.
   Preserve all test commands, the expected count of 159, timeout, stream limit,
   source/tree checks, immutability checks and result rules.
3. `table-runtime-manifest.json`: pin the corrected test and controller hashes,
   the two new bases and allow-lists, and the v2 evidence path. Preserve all
   other identities, platform requirements, counts, exclusions and controls.
   The v2 evidence path is a new explicit manifest field.

`bridge.py` must remain byte-identical at SHA-256
`a71bb86a1dd86b80d58e67699f1c6db9bfd9725ab209c1d6fe8d5d4daacf31d6`.
Every complete corrected file requires blind dual static review before commit
or execution.

## Required preservation

The accepted v1 evidence must remain byte-identical:

- `evidence.json` SHA-256
  `5e5a5ad498a24a6bee1917fb76bdf8853081968b814cafdfc2801c295ea4bb33`;
- `stdout.txt` SHA-256
  `7358f9848273c939efba7c596d6d5a27d1fd16cb08582facb5b953c18cb28315`;
- `stderr.txt` SHA-256
  `cf09f5c4f2f080e2ac7662a8281aa132ee05f71b9519a2446b18d0b03551acb3`.

The R2 controller must refuse if the v2 evidence path already exists. It may
not modify, replace or reuse the v1 directory.

## Later R2 execution boundary

After blind dual static review, commit of the exact three-file correction and a
separate prospective PI authorization, one invocation may run the exact
controller. It may exercise only the preserved 128-test baseline and the 31
presentation tests, requiring exactly 159 passes.

The reviewed 150-second timeout, 2,000,000-byte per-stream limit, literal
`127.0.0.1` ephemeral-test listeners, no-DNS/no-LAN boundary, pre/post
immutability checks, listener holdpoints and no-retry rule remain mandatory.
The exact provider manifest, interpreter, platform, source hashes, tree hashes,
bases, allowed diffs and absent v2 path must be recorded and verified before
controller launch. The controller and `table-runtime-manifest.json` SHA-256
values must equal the exact values accepted at holdpoint 3. The three v1
evidence files must equal the pinned hashes above before launch and must be
recomputed and recorded unchanged after the run. Stop before launch on any
difference.

Any nonzero child, wrong count, failure, error, skip, timeout, overflow,
mutation, confinement escape, cleanup variance, v1 preservation variance or
evidence-boundary variance is a gated negative. A started R2 attempt is
consumed. Resulting evidence requires blind dual review before acceptance.

## Claim boundary and exclusions

A positive R2 result could establish only the bounded synthetic-loopback
behavior of the accepted iPad-first table package and preserved
fictional-parent baseline. It would not establish Beryl/iPad operation, live QR
or device interaction, verified identity, parenthood, parental or legal
authority, legal consent, complete AAuth conformance, Project Agent,
wallet/WAS, mBot2, Misty, G28 or G29.

This proposal itself authorizes no source change, import, compilation, lint,
test, execution, listener, network access, QR generation, device contact or
physical action. The unrelated PI routine-tool proposal remains excluded and
untouched.

## Holdpoints

1. Both blind gates review this exact proposal.
2. The PI may authorize create-only implementation of the three exact files.
3. Both blind gates review all three complete files.
4. The PI may authorize their commit and one bounded R2 execution.
5. Both blind gates review resulting evidence before acceptance or use.
