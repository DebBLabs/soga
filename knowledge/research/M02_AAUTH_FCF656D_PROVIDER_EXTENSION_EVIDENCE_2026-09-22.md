# M02 AAuth `fcf656d` Provider Extension Evidence

Date: 2026-09-22
Execution commit: `b1103b03b4a67f99faf06d17fbc424f4d8ffb13a`
Review: request 050, blind Gate 1 PASS and blind Gate 2 PASS

## Accepted result

The pinned `cryptography 50.0.1` installation under `/usr/bin/python3` 3.9.6
demonstrated the bounded provider behavior needed by the created AAuth Phase 1
package:

- `Ed25519PublicKey.from_public_bytes` imported and round-tripped the exact
  RFC 8032 Section 7.1 Test 1 public key.
- The published signature verified over the empty message.
- A wrong message and a one-bit-altered signature were rejected.
- 31-byte and 33-byte public-key inputs raised `builtins.ValueError`.
- Two in-memory keys created by `Ed25519PrivateKey.generate()` had distinct
  32-byte public keys, produced signatures that verified, and rejected wrong
  messages.
- Every provider module with a file origin resolved beneath the pinned provider
  root.
- No generated private key, public key, signature, object text, or hash of
  generated material entered the evidence.

This establishes only the encoded provider behavior. It does not establish
AAuth, JOSE, JWT, HTTP Message Signature or Structured Fields conformance,
general native-code safety, vulnerability absence, or randomness quality.

## Exact evidence

Preserved temporary directory:
`/private/tmp/m02-aauth-fcf656d-provider-extension-20260922`

- `provider-extension-evidence.json` — 2,526 bytes, SHA-256
  `8b4676330643dea6db04c23027bf0e002ca752514a409337712f6ad416a5da8c`
- `provider-extension-stderr.bin` — 110 bytes, SHA-256
  `2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`
- `run-record.json` — 1,586 bytes, SHA-256
  `c83fbe9b632f32445f17720fe2aa77131068bb926fd4f1ec72bd5b3b2525714b`

The run record states `ED25519_PROVIDER_EXTENSION_POSITIVE`, exit status `0`,
no timeout and no error. It binds the exact committed child at SHA-256
`f63d3019052e272fec8fe1254510ccd16f1782b4b34ebba0a473ec0d9a025d1d`
and runner at SHA-256
`76722f9c970348cd9fec77715198d4fb42dd64a46bea518e53de6a2b43d9218f`.
Before child execution, the runner recomputed 223 preserved installation
entries, four pinned wheels, the accepted static evidence and both D-099
artifacts.

The raw stderr is the exact pinned macOS `confstr()` diagnostic accepted by the
reviewed proposal. Any different content or superset would have failed.

## Repository-status observation

The run record includes `.claude/settings.local.json` in `status_porcelain`
because the runner's HOME-free Git environment did not load the user's global
ignore rule. The file predates the run and lies outside the protected source and
provider roots. Both blind reviewers concluded that this observation does not
affect the evidence claim.

## Review boundary

Both request-050 reviewers independently recomputed the evidence hashes,
source identities, stream bindings, RFC input hashes, module origins and
encoded outcomes without executing the candidate, importing the provider,
loading native code, reading peer material or modifying the repository. Both
returned PASS with no blocking findings.
