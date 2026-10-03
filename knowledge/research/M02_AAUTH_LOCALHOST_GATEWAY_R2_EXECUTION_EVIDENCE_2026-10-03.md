# M02 AAuth Localhost Gateway R2 Execution Evidence

Date: 2026-10-03  
Status: EXECUTED ONCE — AWAITING BLIND DUAL EVIDENCE REVIEW  
Authority: D-127  
Execution HEAD: `0079332a24313e6156fe3a77854c84943589aecd`  
Controller SHA-256: `2a3c04506fdfa371f63680a874979421e3288ca07bb421e26e17c2af0c11b32a`

## Result

The single D-127-authorized execution completed with controller result
`AAUTH_LOCALHOST_GATEWAY_EXECUTION_POSITIVE` and child result
`AAUTH_LOCALHOST_GATEWAY_TESTS_VERIFIED`.

- tests run: 53;
- failures: 0;
- errors: 0;
- skips: 0;
- expected failures: 0;
- unexpected successes: 0;
- child return code: 0;
- timeout: false;
- stdout overflow: false;
- stderr overflow: false;
- post-verification error: none;
- socket audit: 22 loopback ephemeral binds and 34 loopback connects;
- test duration reported by unittest: 9.758 seconds;
- bounded controller duration: 10.28191089630127 seconds.

The passing scope includes the real SOGA-supervised four-hop exchange, the
gateway authorization and denial paths, and the corrected transport tests for
unsupported methods, early-rejected POST requests and the fresh-connection
`GET /unknown` route.

## Durable evidence

The controller created the previously absent directory:

`/Users/debb/dev/research-evidence/soga/executions/localhost-gateway-r2`

The files are read-only and hash as follows:

- `localhost-gateway-evidence.json`: 9,897 bytes, SHA-256
  `c4ad8317e674f2bd8570d2b82d70bce985d1c74b462e996329a5e27d6c300c31`;
- `localhost-gateway-stderr.bin`: 0 bytes, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `run-record.json`: 2,867 bytes, SHA-256
  `9035732a5a27966e7ef7a2025280f649fb19b24df99661df77eb8ae8ae54a256`.

The run record identifies the accepted durable provider manifest at SHA-256
`7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`,
verifies 190 provider RECORD files and records the expected four distribution
versions. It records the D-126-accepted localhost source and test hashes and
all other protected inputs.

## Preservation and cleanup

The execution wrote only the three bounded durable evidence files. The SOGA
working tree remained clean except for the standing excluded untracked PI
routine-tool proposal and this evidence report. The earlier D-124 evidence in
`executions/localhost-gateway` was not modified. No retry occurred.

The controller's in-process servers used literal `127.0.0.1` ephemeral
listeners and were shut down by the test fixtures. No external service,
Mockin, wallet/WAS, QR or Misty surface was accessed.

## Claim boundary

This execution establishes the bounded 53-test localhost AAuth gateway claim:
the pinned package and provider completed the tested token, HTTP-signature,
minimal exchange, SOGA-supervision, loopback transport and fail-closed
connection-handling behaviors.

It does not establish complete AAuth conformance, public-network behavior,
wallet or WAS integration, QR interaction, participant or representative
authority policy, Misty execution, G28 or G29 readiness.
