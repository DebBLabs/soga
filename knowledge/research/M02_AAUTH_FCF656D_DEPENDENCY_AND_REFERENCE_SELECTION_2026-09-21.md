# M02 AAuth `fcf656d` Dependency and Reference Selection

Date: 2026-09-21
Status: RESEARCH DRAFT — NOT YET INDEPENDENTLY REVIEWED
Authority: D-086, documentation and package metadata retrieval only
Author/integrator: Codex

## Result

The bounded research identifies one exact dependency set and pins the normative
reference set required before Phase 1 can be proposed. No distribution artifact
was downloaded, installed, imported or executed.

### Selected provider candidate

Use `cryptography==50.0.1` through the official non-yanked CPython 3.9 ABI3
macOS 11+ arm64 wheel:

| Field | Verified value |
|---|---|
| Project | `cryptography` / Python Cryptographic Authority |
| Version | `50.0.1`, released 2026-08-25 |
| Artifact | `cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl` |
| Size | 4,035,307 bytes |
| SHA-256 | `ca83d00d9e69cd5eb63f2e69c3a5a59e0cecae5ae14c6ae0b35830fe3b37bad0` |
| Python requirement | `!=3.9.0,!=3.9.1,>=3.9`; local Python is 3.9.6 |
| Platform tag | CPython 3.9 ABI3, macOS 11.0+ arm64 |
| License | `Apache-2.0 OR BSD-3-Clause` |
| Publication | PyPI Trusted Publishing; artifact is not yanked |
| Native content | Platform-specific compiled wheel; official documentation says macOS wheels are statically linked and 50.0.1 wheels use OpenSSL 4.0.2 |

Primary metadata:

- <https://pypi.org/project/cryptography/50.0.1/>
- <https://pypi.org/pypi/cryptography/50.0.1/json>
- <https://cryptography.io/en/50.0.1/>
- <https://cryptography.io/en/50.0.1/hazmat/primitives/asymmetric/ed25519/>
- <https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst>

The versioned API documentation verifies the required minimal interface:
`Ed25519PrivateKey.generate()`, `sign(data)`, `public_key()`,
`Ed25519PublicKey.from_public_bytes()`, `public_bytes(..., Raw)`, and
`verify(signature, data)`. It also specifies `InvalidSignature` on failed
verification and `UnsupportedAlgorithm` when the bundled backend does not
support Ed25519.

This selection is for Ed25519 primitives and raw public-key bytes only. It does
not delegate JWS, JWK, JWT, HTTP structured-field, Content-Digest or HTTP Message
Signature construction to `cryptography`; SOGA must implement and test those
profile rules itself or select separately reviewed libraries later.

### Exact direct and transitive distributions

Official `cryptography 50.0.1` metadata declares two required dependencies for
CPython 3.9. The following compatible, non-yanked wheels form the proposed exact
closure:

| Package | Artifact | SHA-256 | Size | License | Role |
|---|---|---|---:|---|---|
| `cffi==2.0.0` | `cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl` | `de8dad4425a6ca6e4e5e297b27b5c824ecc7581910bf9aee86cb6835e6812aa7` | 180,509 | MIT | Required by cryptography on CPython |
| `pycparser==2.23` | `pycparser-2.23-py3-none-any.whl` | `e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934` | 118,140 | BSD-3-Clause | Required by cffi on CPython |
| `typing-extensions==4.15.0` | `typing_extensions-4.15.0-py3-none-any.whl` | `f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548` | 44,614 | PSF-2.0 | Required by cryptography below Python 3.11 |

Metadata sources:

- <https://pypi.org/pypi/cffi/2.0.0/json>
- <https://pypi.org/pypi/pycparser/2.23/json>
- <https://pypi.org/pypi/typing-extensions/4.15.0/json>

Direct metadata verification for the `pycparser` wheel was performed without a
summarizing intermediary. The version-specific PyPI JSON response was saved as
`/private/tmp/pycparser-2.23-metadata.json` on 2026-09-21 at 00:42:57 EDT. Its
SHA-256 is
`f422a7e7530f1ae09c7d2c350cbe42a6b4372aeb8b274e0948a61110c5562e3d`.
Parsing that JSON and selecting the entry whose `filename` is exactly
`pycparser-2.23-py3-none-any.whl` yields SHA-256
`e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934`,
size 118,140, and `yanked: false`. This raw-record extraction controls over any
conflicting transcription produced by a summarizing web reader.

The `ssh` extra and its `bcrypt` dependency are not selected. Source builds are
not selected. A later acquisition must use only the four exact wheels above,
must disable dependency resolution and source builds, and must verify every
SHA-256 before installation. Those controls are recommendations for a later
proposal, not authority conveyed here.

## Security and maintenance assessment

- `50.0.1` is the latest stable release shown by official project/PyPI records
  during this research; `51.0.0` is explicitly unreleased development work.
- The project documents Python 3.9+ and arm64 macOS as supported/tested.
- `50.0.1` follows the `50.0.0` security release and updates platform wheels to
  OpenSSL 4.0.2. Published historical advisories exist for earlier cryptography
  or bundled-OpenSSL versions. This research does not claim absence of unknown
  defects or general safety of unrelated APIs.
- The selected wheel contains native cryptographic code and bundled OpenSSL.
  Its exact artifact hash, platform and provenance therefore remain mandatory
  acquisition and execution checks.
- The implementation must use only the documented Ed25519 surface and preserve
  the accepted rule that private keys remain in memory and never enter logs,
  SQLite or committed fixtures.

## Pinned normative reference set

| Reference | Exact pin | Authority and use |
|---|---|---|
| AAuth | editor's-copy Git commit `fcf656de1926535f5bd6fc0538147ead6646e727`; protocol SHA-256 `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953` | Governing profile and Steps 1–3 requirement source |
| HTTP Signature Keys | `draft-hardt-httpbis-signature-key-09`, published 2026-09-13 | `Signature-Key`, schemes, algorithm determination, negotiation and `Signature-Error` grammar |
| HTTP Message Signatures | RFC 9421, February 2024 | Signature base, covered-component and parameter serialization/verification |
| Digest Fields | RFC 9530, February 2024 | `Content-Digest` construction and verification |
| Structured Field Values for HTTP | RFC 9651, September 2024 | Dictionary, List, Item, Token, String and Byte Sequence grammar used by the companion draft |

Authoritative documents:

- <https://datatracker.ietf.org/doc/html/draft-hardt-httpbis-signature-key-09>
- <https://www.rfc-editor.org/rfc/rfc9421.html>
- <https://www.rfc-editor.org/rfc/rfc9530.html>
- <https://www.rfc-editor.org/rfc/rfc9651.html>

### Why the companion pin is `-09`

The AAuth source cites the unversioned Datatracker name
`draft-hardt-httpbis-signature-key`. Revision `-09` was published on 2026-09-13;
the pinned AAuth commit was authored on 2026-09-14. Thus `-09` was the current
published revision at the AAuth checkpoint and contains the `jwt`, `jwks_uri`,
fully specified algorithm, negotiation and `Signature-Error` mechanisms the
AAuth text invokes. This is a chronology-and-content inference, stated as such;
the AAuth source does not embed an explicit revision suffix.

## Required Phase 1 matrix extension

Before Phase 1 source creation, extend the accepted normative matrix with exact
requirements from the pinned companion documents for:

1. RFC 9421 signature-base construction, strict serialization, component
   identifiers, `Signature-Input`, `Signature`, `created`, `expires`, and label
   correlation;
2. RFC 9530 `Content-Digest` construction over message content and its Structured
   Field dictionary form;
3. RFC 9651 parsing/serialization, duplicate handling, canonical forms and
   rejection behavior for all field types used; and
4. Signature Keys `-09` `jwt` and `jwks_uri` scheme parameters, selected-member
   behavior, algorithm determination, error headers/codes, label correlation,
   discovery admission and cache rules.

The extension must identify any conflict between AAuth `fcf656d` and the
companion `-09`; AAuth's explicit profile rules control only where it intentionally
specializes the underlying specification. Ambiguity or conflict is a stop
condition, not permission to invent a wire format.

## Boundary and next decision

This report identifies a proposed exact dependency closure and reference set.
It authorizes nothing. Both blind gates must verify the package metadata,
compatibility, hashes, licenses, native-code disclosure, source chronology and
reference selection.

Only after PI acceptance may a separate proposal request acquisition of the four
named wheel artifacts and create the matrix extension. No download, install,
import, implementation, compile, test, listener, wallet/WAS work, Misty access,
G28 or G29 is authorized here.
