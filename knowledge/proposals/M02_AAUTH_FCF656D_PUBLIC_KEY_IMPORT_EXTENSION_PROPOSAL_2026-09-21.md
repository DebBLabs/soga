# M02 AAuth `fcf656d` Public-Key Import and Generation Provider Extension Proposal

Date: 2026-09-21
Revised: 2026-09-22
Status: PROPOSED — NOT AUTHORIZED FOR SOURCE CREATION OR EXECUTION
Prepared at: `main @ 2d561822c056b2870718986deb9347c3400c030b`
Review class: mandatory blind dual review under D-064

## Purpose

Close both provider-evidence holdpoints identified before AAuth Phase 1 test
execution: `Ed25519PublicKey.from_public_bytes`, recorded by D-100, and
`Ed25519PrivateKey.generate()`, identified by static review of the committed
tests. Verify their bounded behavior in the pinned `cryptography 50.0.1`
installation without recording generated private or public key material.

This is a provider-API extension only. It does not execute the AAuth Phase 1
package or establish JWT, HTTP Message Signature or AAuth conformance.

## Accepted basis

- D-097 accepts the preserved installation's identity, containment and RECORD
  completeness.
- D-099 accepts the bounded Ed25519 behavior already exercised by the RFC 8032
  Test 1 verifier.
- D-100 permits created AAuth source to reference `from_public_bytes`, but
  prohibits any execution relying on it until a separately proposed and
  reviewed extension exercises it against the pinned installation.

## Proposed create-only artifacts

A later PI decision may authorize creation only of:

- `tools/m02_aauth_fcf656d/verify_ed25519_public_key_import.py`
- `tools/m02_aauth_fcf656d/run_ed25519_public_key_import.py`

The child and runner must remain separate. Neither may import, compile, lint,
test or execute before blind dual static review.

## Exact inputs

- Interpreter: `/usr/bin/python3`, expected Python `3.9.6`.
- Installation parent:
  `/private/tmp/m02-aauth-fcf656d-phase1-install-20260921`.
- Provider root:
  `/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/site-packages`.
- Wheel root: `/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels`.
- Wheels accepted under D-091:
  - `cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl`, 4,035,307 bytes,
    SHA-256 `ca83d00d9e69cd5eb63f2e69c3a5a59e0cecae5ae14c6ae0b35830fe3b37bad0`;
  - `cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl`, 180,509 bytes,
    SHA-256 `de8dad4425a6ca6e4e5e297b27b5c824ecc7581910bf9aee86cb6835e6812aa7`;
  - `pycparser-2.23-py3-none-any.whl`, 118,140 bytes,
    SHA-256 `e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934`;
  - `typing_extensions-4.15.0-py3-none-any.whl`, 44,614 bytes,
    SHA-256 `f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548`.
- Accepted static verification evidence:
  `/private/tmp/m02-aauth-fcf656d-static-recovery-20260921/static-verification-evidence.json`,
  SHA-256 `fe66cc77cc1e4ceabcd99968fd6ab372c6b066b0f0e8c48291660e3636f792b0`.
- Authoritative D-099 raw provider evidence:
  `/private/tmp/m02-aauth-fcf656d-ed25519-provider-r2-20260921/provider-evidence.json`,
  SHA-256 `d6c7564e55e81fbc11931fb0306b9ce4c210f968fce587cc1f6919ebaba505fe`.
- Authoritative D-099 R2 run record:
  `/private/tmp/m02-aauth-fcf656d-ed25519-provider-r2-20260921/run-record.json`,
  SHA-256 `6cb4f1ab9a5f13fe99b524c8df8f051f0bca75886e449d997dd89ae3db3d2591`.
- New evidence directory:
  `/private/tmp/m02-aauth-fcf656d-provider-extension-20260922`.

## Child behavior

Under `/usr/bin/python3 -I -S -B`, bind imports only to
`/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/site-packages` and require
`cryptography 50.0.1`.

Using RFC 8032 Section 7.1 Test 1 preserved in D-099:

1. construct the public key through `Ed25519PublicKey.from_public_bytes` using
   the exact 32-byte public-key vector;
2. serialize it with `public_bytes_raw` and require byte equality with the
   input;
3. verify the exact RFC signature over the empty message;
4. reject the same signature over a wrong message;
5. reject a one-bit-altered signature; and
6. reject 31-byte and 33-byte public-key inputs, recording the observed
   exception class without prescribing one in advance.

Then exercise `Ed25519PrivateKey.generate()` as a separate behavioral section:

1. generate two in-memory private keys;
2. sign the same fixed non-secret message with each;
3. verify each signature with its corresponding public key;
4. reject each signature for a wrong message;
5. require both public keys to serialize to 32 bytes and require the two public
   values to differ; and
6. record only boolean outcomes and lengths—never generated private bytes,
   public bytes, signatures, hashes of generated material or object text.

Record the provider version, Python version, vector identifier, non-secret input
and signature hashes, boolean outcomes, observed exception class names and all
loaded provider-module origins. Every module with a file origin must resolve
beneath the accepted provider root; a built-in or extension submodule without a
file origin is recorded rather than treated as failure. Emit exactly one bounded
JSON document to stdout. Because no generated material enters the document, the
evidence schema and values remain deterministic even though generation uses
randomness. Do not write files, use temporary storage, access a network,
serialize generated private material, or log generated public material,
signatures, their hashes, object text or token-like data.

## Runner behavior

The runner must:

1. accept no arguments and verify its exact committed child and runner bytes;
2. recompute the accepted static installation evidence, full installation
   inventory and four pinned wheel identities before child start;
3. verify the D-099 provider-evidence record and its exact accepted hashes;
4. refuse a pre-existing fixed evidence directory at
   `/private/tmp/m02-aauth-fcf656d-provider-extension-20260922`;
5. launch exactly one child with the minimal reviewed environment, a 30-second
   timeout and 1,000,000-byte limit per stream;
6. preserve bounded raw stdout and stderr before evaluating either;
7. permit stderr only when empty or exactly 110 bytes with SHA-256
   `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`;
   any other content or superset fails;
8. require exit zero and the exact positive child result; and
9. write a compact atomic run record with command, environment, timings,
   repository state, source hashes, static inputs, stream hashes and the pinned
   Darwin-diagnostic match field.

No automatic retry or cleanup is permitted. Preserve all evidence on every
post-start stop.

## Review, execution and claim boundary

After a later create-only authorization, both blind gates must inspect both
complete files before commit or execution. A separate prospective PI decision
must name their committed hashes and authorize exactly one execution. Resulting
evidence requires blind dual review before acceptance.

A positive result may establish only the pinned provider's bounded
`from_public_bytes` behavior for the encoded RFC vector and negative cases, and
bounded `generate()` behavior for the stated in-memory checks. It does not
authorize or execute the AAuth Phase 1 tests and does not establish AAuth, JOSE,
JWT, HTTP Message Signature conformance or general randomness quality.

No source creation, import, native-code execution, compilation, lint, test,
network access, dependency operation, listener, wallet/WAS work, Misty access,
G28 or G29 is authorized by this proposal. The unrelated PI routine-tool
proposal remains excluded and untouched.
