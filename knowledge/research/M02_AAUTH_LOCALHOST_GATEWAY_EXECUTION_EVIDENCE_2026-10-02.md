# M02 AAuth Localhost Gateway Execution Evidence

Date: 2026-10-02  
Status: GATED NEGATIVE EVIDENCE — AWAITING BLIND DUAL REVIEW AND PI DISPOSITION  
Authority: D-124  
Execution HEAD: `b27f1285553d2a84aafb0a904baabbd7ac622423`

## Result

The single D-124 localhost execution completed as a gated negative. The exact
53-test suite ran to completion: 52 passed and one failed. There were no test
errors, skips, expected failures, unexpected successes, timeout, output
overflow, source/provider mutation, module-origin escape or stderr variance.

The failure was deterministic evidence from the single run:

`test_transport_input_errors_routes_and_methods_fail_closed`

Expected HTTP status `404`; observed `501` at
`tests/test_m02_aauth_fcf656d_localhost.py:361`.

No retry, diagnosis or source modification is authorized by D-124. This report
records the run without classifying whether the defect is in the test
expectation, the HTTP handler's unsupported-method behavior or another source
contract.

## Exact instrument and inputs

- Controller:
  `tools/m02_aauth_fcf656d/run_localhost_gateway_tests.py`
- Controller SHA-256:
  `e3005703baa5ea0e917f8eee48549003b91a74de4e4c041482ff9b8d7c70285e`
- Accepted durable runtime manifest SHA-256:
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`
- Durable evidence directory:
  `/Users/debb/dev/research-evidence/soga/executions/localhost-gateway`
- Evidence payload SHA-256:
  `f8c4f794fc09543868791bf7a9a4f38de3d26fa278c7671300766676b4ae54dc`
- Run record SHA-256:
  `dd7f17b890ded48edee2fcb736918ca72fd772c0ec59eba9143c7a42e4090c20`
- Empty stderr SHA-256:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Controller outcome

| Field | Observed |
|---|---|
| Result | `AAUTH_LOCALHOST_GATEWAY_EXECUTION_NEGATIVE` |
| Child result | `AAUTH_LOCALHOST_GATEWAY_TESTS_FAILED` |
| Return code | `1` |
| Duration | `10.606393098831177` seconds |
| Timeout | `false` |
| stdout | `10432` bytes, preserved, no overflow |
| stderr | `0` bytes, preserved and allowed |
| Parse error | none |
| Post-verification error | none |

## Test and socket evidence

| Field | Observed |
|---|---:|
| Expected tests | 53 |
| Tests run | 53 |
| Passed | 52 |
| Failures | 1 |
| Errors | 0 |
| Skips | 0 |
| Expected failures | 0 |
| Unexpected successes | 0 |
| Literal-loopback binds admitted by audit guard | 22 |
| Literal-loopback connects admitted by audit guard | 33 |

The socket audit guard permits only literal `127.0.0.1`, only ephemeral binds,
and no name resolution or other socket operation. The run record reports no
guard or confinement exception. Independent post-run listener inspection found
no Python, AAuth or SOGA TCP listener.

## Successful claims within the negative run

The following bounded tests passed in the same run:

- all 24 Phase 1 token/signature/profile tests;
- all 11 transport-free exchange and mission-continuity tests;
- real SOGA-supervised four-hop exchange and gateway;
- exact auth-token requirement when a person token reaches the gateway;
- SOGA deny, malformed and exception paths issuing no auth token;
- signature-failure handling;
- non-profile bind rejection;
- HTTPS identity/loopback transport separation;
- content-length and body-read failure controls;
- authority and transport-map validation; and
- all SOGA supervision-state validation tests.

These passing observations do not convert the complete run into a positive
result. The accepted claim remains gated negative until the one failing
method/route expectation is diagnosed and any corrected execution is separately
reviewed and authorized.

## Immutability and cleanup

The controller verified before and after that:

- all fourteen protected source/test files retained their accepted hashes and
  exact committed bytes;
- the controller retained its exact committed hash;
- the accepted provider manifest and all 190 provider files remained intact;
- all relevant modules loaded only from the repository or accepted provider
  root; and
- repository source/provider state did not change.

The execution evidence directory contains exactly the preserved stdout JSON,
empty stderr file and run record. No listener remained after the run. The
unrelated untracked PI routine-tool proposal remained untouched.

## Claim boundary and next decision

Established:

- the full bounded suite loads and runs using the accepted durable runtime;
- 52 named tests pass, including the SOGA-governed four-hop exchange; and
- one exact HTTP method/route expectation fails `501 != 404`.

Not established:

- a completely passing 53-test localhost gateway proof;
- the cause or correct disposition of the `501`/`404` difference;
- complete AAuth conformance;
- Mockin, wallet, WAS, QR, parent-authority or Misty integration; or
- G28/G29 readiness.

The D-124 attempt is consumed. Diagnosis, source or test modification, another
execution or retry requires separate review and prospective PI authorization.

