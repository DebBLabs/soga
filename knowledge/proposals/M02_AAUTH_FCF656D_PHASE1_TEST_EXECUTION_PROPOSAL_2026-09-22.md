# M02 AAuth `fcf656d` Phase 1 Test Execution Proposal

Date: 2026-09-22
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ c2c9f8c6203de94578ac68d5d53923a087720403`
Review class: mandatory blind dual review under D-064

## Purpose and single claim

Execute the complete, previously reviewed AAuth Steps 1–3 test package once and
determine whether its bounded JOSE, HTTP Message Signature, Structured Fields
and truthful interim-metadata behavior works under the pinned provider.

This proposal is batched by claim rather than by file or API. A positive result
may establish only that the committed Steps 1–3 package passes its encoded
tests. It does not establish complete AAuth conformance or an end-to-end token
exchange.

## Authority and accepted basis

- D-100 accepted the create-only Phase 1 proposal and authorized the seven-file
  package, which both blind gates reviewed before commit.
- D-102 accepted the bounded provider extension. It closes the provider
  holdpoints for `Ed25519PublicKey.from_public_bytes` and
  `Ed25519PrivateKey.generate()` and names a separately authorized Phase 1 test
  execution as the next boundary.
- Governing AAuth source: editor's-copy commit
  `fcf656de1926535f5bd6fc0538147ead6646e727`.

## Exact committed package

Execution must occur at
`c2c9f8c6203de94578ac68d5d53923a087720403` or a later commit whose seven
listed blobs are byte-identical:

- `m02_aauth_fcf656d/__init__.py` — SHA-256
  `c480bf75ecea51a368627cb00dabdd96ed9e48df784497ce9b7efee80f8f58e8`;
- `m02_aauth_fcf656d/http_signatures.py` — SHA-256
  `f6ae4f4463852b310d09608d4a60084a566733e857098bcd42f2bc1a659cab65`;
- `m02_aauth_fcf656d/jose.py` — SHA-256
  `cda9b577746116e65c34977706593475a8637a3ec6823375dda7baffa961cdd4`;
- `m02_aauth_fcf656d/metadata.py` — SHA-256
  `89d6bf45fa1183f23bb3b9af737004962c5d50298b2c7307cd99e1b83cca2653`;
- `m02_aauth_fcf656d/profile.py` — SHA-256
  `fb7b9b51ada64c7e45f61eb24991078cbe5d172cdf781887bf6843c27fb7afbf`;
- `m02_aauth_fcf656d/structured_fields.py` — SHA-256
  `9d774a03dd096577a9ce917b40f4c3693e30758319fa05f455feb3b734c78a71`;
- `tests/test_m02_aauth_fcf656d.py` — SHA-256
  `160f636b875145a11aa7e593b01aa8b1aa0420ffc58a3eadef589517856d0774`.

No other test module is in scope.

## Exact runtime and preserved inputs

- Interpreter: `/usr/bin/python3`, exact expected version `3.9.6`.
- Isolated flags: `-I -S -B`.
- Repository import root: exact committed repository root
  `/Users/debb/dev/soga-clean`, inserted explicitly by the bounded controller
  only after removing the empty entry and controller directory from `sys.path`.
- Provider import root:
  `/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/site-packages`,
  inserted ahead of the repository root.
- Accepted static installation evidence: SHA-256
  `fe66cc77cc1e4ceabcd99968fd6ab372c6b066b0f0e8c48291660e3636f792b0`.
- Accepted D-099 provider evidence: SHA-256
  `d6c7564e55e81fbc11931fb0306b9ce4c210f968fce587cc1f6919ebaba505fe`.
- Accepted D-102 provider-extension evidence: SHA-256
  `8b4676330643dea6db04c23027bf0e002ca752514a409337712f6ad416a5da8c`.
- The controller must recompute the complete preserved installation inventory,
  the four pinned wheels and the accepted evidence bindings before importing
  any Phase 1 module or provider code.

## One bounded controller

A later PI decision may authorize creation only of
`tools/m02_aauth_fcf656d/run_phase1_tests.py`. The complete controller must then
receive blind dual static review before commit or execution.

The controller must:

1. accept no arguments and require exact committed controller, package and test
   bytes;
2. fail if any protected path has a working-tree entry;
3. complete every preserved-input and provider-evidence check before candidate
   import;
4. refuse the pre-existing evidence directory
   `/private/tmp/m02-aauth-fcf656d-phase1-tests-20260922` and create it at mode
   `0700` only after all pre-import checks pass;
5. launch exactly one isolated child process with a minimal fixed environment,
   no stdin, a 60-second timeout and a 2,000,000-byte limit per output stream;
6. have the child insert only the pinned provider root and exact repository root,
   load exactly `tests/test_m02_aauth_fcf656d.py`, and run the resulting
   `unittest` suite once with verbosity sufficient to identify every test;
   capture the `unittest` report in memory rather than allowing its default
   stream to write to stderr; emit exactly one JSON document to stdout with the
   exact result `AAUTH_PHASE1_TESTS_VERIFIED`, all counts required by item 9,
   the module-origin map and the redacted captured report;
7. prohibit test discovery and prohibit loading any other test module;
8. preserve bounded raw stdout and stderr before evaluating them; stderr is
   permitted only when empty or exactly 110 bytes with SHA-256
   `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`;
   any other content or superset fails;
9. record the exact number of tests run and the counts of failures, errors,
   skips, expected failures and unexpected successes; require every non-run
   count to be zero and require the controller's independently counted test
   methods to equal the executed count;
10. require child exit zero, no timeout and a unique exact positive result;
11. verify that all loaded `cryptography`, `cffi`, `_cffi_backend`,
    `pycparser` and `typing_extensions` modules with file origins resolve below
    the pinned provider root, and that all loaded `m02_aauth_fcf656d` modules
    resolve below the exact repository package root; no other repository package
    may be imported;
12. verify after execution that the seven committed blobs, preserved
    installation inventory and accepted evidence inputs remain unchanged;
13. write a compact atomic run record containing source hashes, command,
    environment, timings, counts, stream hashes, module origins and pre/post
    checks; and
14. perform no automatic retry or cleanup and preserve all bounded evidence on
    every post-start stop.

No generated private key, public key, signature, token or complete HTTP
signature value may enter the controller's run record. Test output must not use
subtests or assertion text to expose such values. If the existing test runner
would emit sensitive generated material on failure, the controller design must
redact it without obscuring the failing test identity and exception class; that
design must be visible in static review before execution. Static review must
specifically verify redaction of the compact JWS carried by `subTest(token=...)`,
the public JWK carried by `subTest(jwk=...)`, and the signed request carried by
`subTest(changed=...)`.

## Required proof and negative cases

One execution covers the complete committed test suite as a single claim. The
evidence must distinguish at least:

- exact `fcf656d` profile and token-type pins;
- strict Ed25519 JOSE signing and verification for every encoded AAuth token
  type;
- fail-closed cross-token-type rejection at the token-verification layer,
  including rejection of a person token when the verifier expects an auth token;
- algorithm, key, JWK and tampering rejection;
- public-only deterministic JWKS behavior;
- HTTP request component, key, digest and content-type binding;
- freshness, forward-skew and replay rejection;
- Structured Fields limits, duplicate rejection and uniform signature errors;
- truthful interim metadata; and
- non-modification of the accepted Stage 2 Person Server package.

This phase does not yet assert a common `mission_s256` value across person,
resource and auth tokens, issue a resource or auth token, perform supervision,
publish an `aauth:local@domain` agent metadata document, or exercise a resource
endpoint. It does not verify an `aud` claim, and no endpoint yet requires an auth
token. Those are the separately batched October-exchange claim, not hidden
requirements of this execution.

## Stop rules

Stop before candidate import or execution if any source, provider, wheel,
accepted evidence, inventory, interpreter or fixed-path check differs; if the
evidence directory exists; if the controller cannot isolate the exact test
module; if a new dependency, listener, network access, test discovery, source
change, permission change or unreviewed algorithm is required; or if bounded
diagnostic preservation cannot avoid generated secret material.

After child start, any timeout, overflow, unexpected stderr policy, count
mismatch, import escape, source mutation, failure, error, skip or nonzero exit is
a gated negative. Preserve evidence and do not retry.

## Review and authorization sequence

1. Both blind gates review this complete proposal once: Gate 1 for `fcf656d`
   fidelity and implementation precision; Gate 2 for security boundaries,
   negative cases and test completeness.
2. After PI acceptance, create only the controller.
3. Both gates review the exact complete controller. They must identify all
   blockers in their first pass and separate optional improvements. Purely
   mechanical corrections receive a hash-pinned diff-only recheck.
4. A separate prospective PI decision names the committed controller hash and
   authorizes exactly one execution.
5. Both gates review the resulting evidence blindly before PI acceptance.

## Claim boundary and exclusions

A positive result establishes only that the exact committed Steps 1–3 package
passes its encoded bounded tests under the pinned provider. It does not establish
complete AAuth `-11` conformance, a real person/resource/auth token exchange,
mission continuity, supervision, resource enforcement, external interoperability
or a Misty demonstration.

This proposal authorizes nothing. No controller creation, import, native-code
execution, compilation, lint, test, listener, network access, dependency
operation, wallet/WAS integration, QR flow, Misty access, physical actuation,
G28 or G29 is authorized. The unrelated PI routine-tool proposal remains
excluded and untouched.
