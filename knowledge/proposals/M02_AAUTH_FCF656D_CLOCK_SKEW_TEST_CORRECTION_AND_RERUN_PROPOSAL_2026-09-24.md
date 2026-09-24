# M02 AAuth `fcf656d` Clock-Skew Test Correction and Rerun Proposal

Date: 2026-09-24  
Status: PROPOSED — NOT AUTHORIZED  
Prepared at: `main @ 65db8309069add268039b6dee8f60b40bd3aaa2c`  
Review class: mandatory blind dual review under D-064

## Purpose and claim

Correct the single test-fixture defect diagnosed after the D-104 execution and,
only after static review of the exact correction, execute the already committed
focused-test controller once to determine whether all 24 bounded Phase 1 tests
pass.

This is one claim-sized recovery. It changes no implementation behavior. A
positive result would establish only that the exact Phase 1 package passes its
24 encoded tests under the pinned provider.

## Accepted basis

- D-105 accepts the D-104 run as a gated negative: 23 of 24 tests passed and
  `test_created_window_skew_and_replay` failed because no exception was raised
  for `created=106`, `now=100`.
- The source-only diagnosis at
  `knowledge/research/M02_AAUTH_FCF656D_PHASE1_CLOCK_SKEW_SOURCE_DIAGNOSIS_2026-09-24.md`,
  SHA-256
  `d4d526c234552ff5192751020486bad07404a3551d495cbf763672fae5533876`,
  finds that the six-second difference is inside the configured and specified
  60-second forward-skew window.
- AAuth commit `fcf656de1926535f5bd6fc0538147ead6646e727`
  requires `clock_skew` only when `created` is further ahead than the validity
  window and defines a 60-second default.
- `draft-hardt-httpbis-signature-key-09`, Section 5.4.14, uses the same
  further-ahead-than-the-window rule.

## Exact correction

Only `tests/test_m02_aauth_fcf656d.py` may change. In
`test_created_window_skew_and_replay`:

1. preserve the existing stale-signature and replay assertions;
2. replace the erroneous excessive-future fixture `created=106` with
   `created=161`, keeping `now=100`, and continue to require error code
   `clock_skew`; and
3. add an explicit boundary assertion that a separately signed request with
   `created=160`, verified at `now=100`, succeeds without a replay cache.

No production source, dependency, configuration, or other test may change. The
controller may change only after the corrected test hash is known, and only in
these two constants:

1. the `PACKAGE_HASHES` entry for `tests/test_m02_aauth_fcf656d.py`, replaced
   with the exact SHA-256 of the corrected test file; and
2. `EVIDENCE_DIR`, replaced with the new fixed path
   `/private/tmp/m02-aauth-fcf656d-phase1-tests-rerun-20260924`, which must not
   exist before the authorized execution.

Every other controller byte must remain unchanged. Generated keys and
signatures must not be recorded.

## Review and execution sequence

1. Both blind gates review this proposal and the source-only diagnosis.
2. After PI acceptance, create only the exact test correction above.
3. Compute the corrected test hash and create only the two permitted mechanical
   controller changes above.
4. Both blind gates review the complete corrected test file, complete corrected
   controller and their diffs, confirming specification fidelity, unchanged
   implementation sources, negative-case completeness, the `160`/`161`
   boundary, the exact new test-hash pin, the unique evidence path and byte
   identity of every other controller line. This may be a hash-pinned diff-only
   recheck rather than a full controller re-review.
5. A separate prospective PI decision may authorize commit of those exact two
   files and exactly one execution of the newly reviewed controller, naming its
   new SHA-256. Both corrected files must be committed before execution because
   the controller verifies each against `HEAD` and rejects protected working-tree
   changes.
6. The new execution must use the fixed new evidence directory above, preserve the same
   interpreter, provider, isolation, time, stream, redaction, module-origin and
   pre/post verification controls accepted under D-103 and D-104, prohibit
   automatic retry, and receive blind dual evidence review before acceptance.

The prior D-104 evidence directory remains unchanged and is not reused or
removed. The original controller SHA-256
`177b4f1231fb30ca053308a4dbfb726c05cdc5b917d6ed614a83c1c817ac4303`
identifies the base for the two permitted mechanical changes; it is not the
artifact to be executed after correction.

## Stop rules

Stop before execution if any implementation source, controller, provider input,
accepted evidence binding or unrelated test differs; if the new evidence
directory already exists; or if any new dependency, permission, listener,
network access or broader change is required. Any timeout, overflow, unexpected
stderr, import escape, source mutation, failure, error, skip or nonzero exit is
a gated negative and must not be retried automatically.

## Claim boundary and exclusions

This proposal authorizes nothing. It does not authorize the test or controller
edits, commit, execution or retry. It does not establish complete AAuth conformance, a live
person/resource/auth token exchange, `mission_s256` continuity, audience
verification, supervision, resource enforcement, wallet/WAS integration, QR
admission or Misty operation. No dependency operation, network access,
listener, personal data, payment, physical actuation, G28 or G29 is authorized.
The unrelated PI routine-tool proposal remains excluded and untouched.
