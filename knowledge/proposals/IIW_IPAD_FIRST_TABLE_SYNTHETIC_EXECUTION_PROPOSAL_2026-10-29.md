# IIW iPad-First Table Synthetic-Loopback Execution Proposal

Date: 2026-10-29
Status: PROPOSED — NOT AUTHORIZED; CONTROLLER BASIS-LOGIC CORRECTION REQUIRED
SOGA basis: `ab4d3a124e244a5991c85dd01a588db3a6796ee2`
Presentation basis: `a139376193276ac0ad780e6b61b4520d000f2e37`
Review class: mandatory blind dual review under D-064

## Purpose

Prepare one bounded synthetic-loopback verification of the D-159 seven-file
iPad-first table package. This is not the Beryl/iPad rehearsal. It may exercise
only the accepted 128-test SOGA baseline and the 31 presentation tests on
literal loopback. It may not generate or expose a live table QR, bind a LAN
address, contact a device or activate physical behavior.

## Required mechanical controller correction

The exact accepted controller at SHA-256
`81d82ea71646c4a8d20968dba24e009beca5f037efd9435717e96c5d77c3ee0e`
correctly pins the six other D-159 files, but two exact-HEAD checks now refuse:

- embedded `PRESENTATION_BASIS` is the pre-implementation commit
  `8aa6eec5d40eb671940b73238f8c08cc0c87be76`, while D-159 committed the
  reviewed package as `a139376193276ac0ad780e6b61b4520d000f2e37`; and
- embedded `SOGA_COMMIT` is accepted source basis
  `ab4d3a124e244a5991c85dd01a588db3a6796ee2`, while D-159 canonical records
  advanced SOGA HEAD to `d47be19f45e8453befbdf776f6ff81921ad8c51f`.

Exact HEAD equality is structurally unsuitable because committing a corrected
controller or a later canonical decision necessarily advances HEAD. A file
cannot embed the hash of the commit that contains it.

No execution is proposed against either mismatch. If this proposal is accepted,
create-only authority is requested to change only the controller's basis-check
logic:

1. set `PRESENTATION_BASIS` to
   `a139376193276ac0ad780e6b61b4520d000f2e37`;
2. replace both exact HEAD equalities with `git merge-base --is-ancestor`
   checks for the presentation and SOGA bases;
3. require presentation changes since its basis to be confined to the
   controller and `table-runtime-manifest.json`;
4. require SOGA changes since its source basis to be confined to this proposal,
   `knowledge/strategy/DECISION_LOG.md` and
   `knowledge/working/CURRENT_STATE.md`; and
5. retain all exact `PRESENTATION_SOURCES`, `SOGA_SOURCES` and
   `PROTECTED_TREES` checks unchanged.

No test, timeout, evidence or execution behavior may change. The corrected
controller and revised manifest require blind dual static review before commit
or execution.

## Exact currently preserved inputs

The companion `table-runtime-manifest.json` records:

- the accepted presentation commit and all seven D-159 file hashes;
- the current controller hash and its known pre-implementation embedded basis;
- SOGA commit `ab4d3a124e244a5991c85dd01a588db3a6796ee2`;
- the accepted fictional-parent baseline controller and test hashes;
- Darwin arm64, Python 3.9.6 and `/usr/bin/python3`; and
- both current refusal bases and the required ancestor/content rule;
- status `NOT_EXECUTABLE_PENDING_REVIEWED_BASIS_LOGIC_UPDATE`.

The manifest is a review and operator holdpoint, not permission to execute.

## Proposed bounded execution after correction and review

One later PI-authorized invocation may run only:

1. the accepted 128-test fictional-parent synthetic-loopback baseline through
   its exact committed controller; and
2. the 31 D-159 presentation tests through `/usr/bin/python3 -B -m unittest
   -v`.

The corrected parent controller must require exactly 159 passing tests, a
150-second parent timeout, 2,000,000-byte limit per output stream, the exact
source and protected-tree hashes, pre/post repository immutability and a new
absent durable evidence directory
`/Users/debb/dev/research-evidence/soga/evidence/iiw-table-foundation-v1`.

Only literal `127.0.0.1` ephemeral listeners used by the tests are permitted.
DNS, internet, Beryl/LAN, hostname, wildcard, public, non-reviewed private and
IPv6 binds are prohibited. No automatic retry is permitted.

## Operator pre-start and post-run records

Before invocation, the operator must record and verify the provider-manifest
hash, `/usr/bin/python3` launch path, resolved
`/Library/Developer/CommandLineTools/usr/bin/python3` executable, Python 3.9.6,
Darwin arm64 and absence of listeners on ports 4317 and 4318. After invocation,
the operator must again record listener absence. These are explicit operator
holdpoints; the current controller does not independently enforce them all.
Before invocation, the operator must also verify that the controller and
`table-runtime-manifest.json` SHA-256 values equal the exact values accepted at
holdpoint 3 and stop on either difference.

The presentation unittest child writes its normal verbose results to stderr.
The controller preserves that stream and requires child return code zero and
the exact 31-test count; evidence review must inspect the preserved stream. No
claim is made that the current controller applies a separate stderr allowlist.

## Stop rules

Stop without execution if any hash, ancestry/content, tree, provider,
interpreter, platform, clean-status, evidence-directory or listener holdpoint
differs. Any nonzero child, wrong count, failure, error, skip, timeout, overflow,
mutation, confinement escape, cleanup variance or evidence-boundary variance
is a gated negative. Preserve bounded evidence and require blind dual evidence
review before acceptance or use.

## Claim boundary and exclusions

A positive result could establish only the bounded synthetic-loopback behavior
of the accepted table package and preserved fictional-parent baseline. It would
not establish Beryl/iPad operation, a live QR, verified identity, parenthood,
parental or legal authority, legal consent, complete AAuth conformance,
Project Agent, wallet/WAS, mBot2, Misty, G28 or G29.

This proposal itself authorizes no source change, import, compilation, lint,
test, execution, listener, network access, QR generation, device contact or
physical action. The unrelated PI routine-tool proposal remains excluded and
untouched.

## Holdpoints

1. Both blind gates review this proposal and the current manifest.
2. The PI may accept them and separately authorize only the bounded
   controller basis-check correction plus corresponding manifest update.
3. Both blind gates review the corrected controller and revised manifest.
4. The PI prospectively authorizes at most one bounded execution.
5. Both blind gates review resulting evidence before acceptance or use.
