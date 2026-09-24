# M02 AAuth `fcf656d` Phase 1 Corrected Test Execution Evidence

Date: 2026-09-24  
Status: ACCEPTED GATED POSITIVE UNDER D-108

## Authority and execution

D-107 authorized exactly one execution of the blind dual-reviewed corrected
test and controller, with no automatic retry. Execution occurred at commit
`2d1748b7667a22e468b4dd8dd9490242904f5172`.

- corrected test SHA-256:
  `89b71359c6c071453fab289aa85443aa4f7156e4a2d263d8ac12f85bee4deaad`;
- controller SHA-256:
  `1d38794aa2e75e7a6889bd1465f2b24c2824e2236df77c049b1f9939bd50136a`;
- evidence directory:
  `/private/tmp/m02-aauth-fcf656d-phase1-tests-rerun-20260924`.

The single execution completed without timeout and without automatic retry.

## Accepted evidence

- `phase1-test-evidence.json`: 4,958 bytes; SHA-256
  `0b95d4f7d80607e36e00a557be707fcba71a6036a2df50ef7a0d78fd6da7bbf3`;
- `phase1-test-stderr.bin`: 0 bytes; SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `run-record.json`: 6,167 bytes; SHA-256
  `5108b8390b55f1c46632b31b022352f8d29f07d614cbc16562fc33f873a38bd8`.

Both blind request-059 reviewers independently recomputed the package and
returned PASS with no blocking findings.

## Result

The evidence records `AAUTH_PHASE1_TESTS_VERIFIED` and
`AAUTH_PHASE1_TEST_EXECUTION_POSITIVE`.

- expected tests: 24;
- tests run: 24;
- failures: 0;
- errors: 0;
- skips: 0;
- expected failures: 0;
- unexpected successes: 0.

The corrected clock-skew test establishes the pinned inclusive boundary:
`created=160`, `now=100` is accepted, while `created=161`, `now=100` is rejected
with `clock_skew`. The stale-signature and replay assertions also passed.

The controller verified exact committed source identities, pinned provider and
accepted evidence bindings, module-origin confinement and matching pre/post
state. Stderr was empty. Reviewers found no generated private key, public key,
signature, token or complete HTTP-signature material in the evidence.

## Claim boundary

This positive result establishes only that the exact committed Phase 1 package
passes its 24 encoded bounded JOSE, HTTP Message Signature, Structured Fields,
metadata and regression tests under the pinned provider. It does not establish
complete AAuth `-11` conformance, a live person/resource/auth token exchange,
`mission_s256` continuity, audience verification, supervision, resource
enforcement, wallet/WAS integration, QR admission or Misty operation.

No additional execution or other excluded activity is authorized.

