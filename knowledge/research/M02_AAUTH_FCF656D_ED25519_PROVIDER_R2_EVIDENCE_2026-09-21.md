# M02 AAuth `fcf656d` Ed25519 Provider R2 Evidence

Date: 2026-09-21
Execution commit: `8c8dea8182373c564bf2e02370553c7cd41da751`
Review: request 040, blind Gate 1 PASS and blind Gate 2 PASS

## Accepted result

The preserved `cryptography 50.0.1` installation demonstrated bounded,
deterministic Ed25519 provider behavior under `/usr/bin/python3` 3.9.6.

- RFC 8032 Section 7.1 Test 1 public-key derivation matched byte-for-byte.
- The deterministic signature matched byte-for-byte and verified.
- A wrong message and a one-bit-altered signature were rejected.
- 31-byte and 33-byte private-key inputs raised `builtins.ValueError`.
- Provider modules with file origins resolved beneath the accepted provider root.
- Two separate executions produced byte-identical provider evidence.

This establishes provider behavior only. It does not establish AAuth
conformance, JWT or HTTP Message Signature correctness, Structured Fields or
key-discovery correctness, general native-code safety, vulnerability absence,
or behavior beyond the encoded vector and negative cases.

## Exact R2 evidence

Preserved temporary directory:
`/private/tmp/m02-aauth-fcf656d-ed25519-provider-r2-20260921`

- `provider-evidence.json` — SHA-256
  `d6c7564e55e81fbc11931fb0306b9ce4c210f968fce587cc1f6919ebaba505fe`
- `provider-stderr.bin` — 110 bytes, SHA-256
  `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`
- `run-record.json` — SHA-256
  `6cb4f1ab9a5f13fe99b524c8df8f051f0bca75886e449d997dd89ae3db3d2591`

The run record states `ED25519_PROVIDER_POSITIVE`, exit status `0`, no timeout,
no error, and `pinned_darwin_stderr_matched: true`. It verified 223 installation
inventory entries and four pinned wheels before child execution. The child hash
was `9806b862a1a3969fc629081ba479303fd6847e794f739513b77fa3d3d7d9d0d5`;
the runner hash was
`4158eae860fa492048267803faa94f68d185cc8a967b369b0dde8a0aa2ce947a`.

## First execution and diagnostic boundary

The first execution at `a5e17aa` remains a consumed gated negative because its
outer runner rejected nonempty stderr. Its provider evidence was byte-identical
to R2 at SHA-256
`d6c7564e55e81fbc11931fb0306b9ce4c210f968fce587cc1f6919ebaba505fe`.
The recurring 110-byte Darwin diagnostic is admitted only as the exact pinned
value above; its precise intermittent host trigger remains unidentified and
unclaimed. Any different stderr, including a superset, remains a failure.

## Process disclosure

The R2 runner was committed and executed under D-098 before prospective blind
dual static review of that exact correction. Both gates reviewed the committed
runner and evidence retrospectively in request 040 and returned PASS. This was
a PI-authorized, package-specific deviation and is not precedent. Future
executions return to prospective blind review of the exact instrument.
