# IIW Path-Specific Completion Pages Synthetic Execution Evidence

Date: 2026-10-30
Status: PENDING BLIND DUAL EVIDENCE REVIEW AND PI ACCEPTANCE
Authority: D-169
Attempt: one authorized attempt, consumed; no retry

## Exact inputs

- SOGA execution basis before the D-169 governance-only delta:
  30bce1c55d171b57f82f3e2c3fc1311bac98a698
- SOGA HEAD at execution:
  340b10dcbd8936cef3f7b6b89850eb781ef49fab
- Presentation basis:
  b7772026f54196c0b370fd70012ca0f30b0c4ef3
- Reviewed presentation commit:
  fa6ccaa2f2fe65c043219380e127cb14f454eae9
- Controller SHA-256:
  e07b168fd9728c2ce8e32040becdd51dd2a47ff01a978567cec78b664962c8e4
- Runtime manifest SHA-256:
  4228ef92300b73934c734a0568e7f22d83779e7310cf2ad04c5c3d5543388b86
- Evidence directory:
  /Users/debb/dev/research-evidence/soga/evidence/iiw-table-path-endings-v1

The evidence directory was absent before execution. Presentation status was
clean. SOGA's only working-tree entries were the untracked, uncommitted Beryl
rehearsal proposal and the separately excluded PI routine-tool proposal.

## Exact execution

The one execution invoked:

    /usr/bin/python3 -I -B run_fictional_parent_presentation_tests.py

from the presentation repository. The process exited 0. No second attempt was
made.

## Result

The controller recorded PASS after 60.2 seconds:

- accepted fictional-parent baseline: 128 of 128 tests passed;
- path-specific presentation package: 35 of 35 tests passed;
- total: 163 of 163 tests passed;
- child return codes: [0, 0];
- presentation and protected SOGA status were empty before and after;
- both previously accepted evidence sets remained byte-identical; and
- no automatic retry occurred.

The 35-test package includes the separate Permission to Speak ending, the
Project Agent preview explicitly labeled not executed, the shared research
framing, retired shared route, laptop-only ending routes, display-only outcome
enum lifecycle and secret-absence checks.

## Durable evidence hashes

- evidence.json:
  9609063de1faf0ab2f8f12be6d3936d7ef548a74864e8f32059015a851431989
- stdout.txt:
  752fb3cf069d5c9bbfc0914818d8b7c0bfeafe6c4b7411f1e867eb61adad5415
- stderr.txt:
  b7fc17d365eb1f3623c53dcc39f3126231c718aad84dee058a6ce4b6b14baa9c

stderr.txt contains the bounded verbose unittest listing and final
Ran 35 tests ... OK; it contains no failure or exception.

## Preserved accepted evidence

The controller verified these files before and after execution:

- v1 evidence:
  - evidence.json
    5e5a5ad498a24a6bee1917fb76bdf8853081968b814cafdfc2801c295ea4bb33
  - stdout.txt
    7358f9848273c939efba7c596d6d5a27d1fd16cb08582facb5b953c18cb28315
  - stderr.txt
    cf09f5c4f2f080e2ac7662a8281aa132ee05f71b9519a2446b18d0b03551acb3
- v2 evidence:
  - evidence.json
    0880071a0d3b4290bca4f3160a4e1ee67063df4c12a9de6a249cbcd08ee7eaed
  - stdout.txt
    60060ef0b76ccc13deb55fb3414d17c125e1ee57234cbae2c0f65cb23b1e360a
  - stderr.txt
    455b0a00f3c3823a55f2b6dbd90f946032ba853c11e8c6e5e47064da24f210d7

## Boundary

This candidate evidence establishes only the bounded synthetic claims encoded
by the reviewed controller and tests. It does not establish PI visual approval,
Beryl or iPad interoperability, a live QR/device interaction, public-event
readiness, Project Agent execution, complete AAuth conformance, verified
identity, parental or legal authority, legal consent, wallet/WAS, mBot2, Misty,
G28 or G29.

The evidence requires blind dual review and PI acceptance before any visual
preview or later rehearsal re-pinning.
