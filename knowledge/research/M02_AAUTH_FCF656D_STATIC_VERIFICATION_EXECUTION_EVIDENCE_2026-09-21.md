# M02 AAuth `fcf656d` Static Verification Execution Evidence

Date: 2026-09-21
Status: GATED NEGATIVE — SINGLE EXECUTION CONSUMED; INSTALLATION UNACCEPTED
Execution HEAD: `a2a6b5f94c2e5ccdbdf47f976b89b774d8105950`
Claim boundary: static identity, containment and RECORD completeness only

## Authorized execution

The PI authorized one execution, without retry, of runner
`tools/m02_aauth_fcf656d/run_static_installation_verifier.py` at SHA-256
`dc3d3297f66888b97711b76fd83ed257a39b642b6403df4a638cf17bebf9dc7a`,
using verifier SHA-256
`f75d8448992b08ba1040e77dd5593dc4692be76f76aa1942cd9ed69e3ea9eb71`,
a 60-second runtime bound, a 2,000,000-byte limit per stream, and writes confined
to `/private/tmp/m02-aauth-fcf656d-static-recovery-20260921`. The runner was
executed once. No retry occurred.

## Raw artifacts

| Artifact | Mode | Size | SHA-256 |
|---|---:|---:|---|
| `static-verification-evidence.json` | `0400` | 51,670 | `fe66cc77cc1e4ceabcd99968fd6ab372c6b066b0f0e8c48291660e3636f792b0` |
| `run-record.json` | `0400` | 1,241 | `3fb9479f4ae2f49302c45aa4086f3207971410ad1f5aee41a38b3ee310c0aa95` |

The run record reports duration 0.167084 seconds, child exit status zero,
stdout length 51,670, stderr length 110, and no timeout. Its stderr SHA-256 is
`2a13af67601624cb4924e88c89583b6d14c362a01c585716097d241c0a47bd61`.
The raw stderr bytes were not preserved.

## Result

The child verifier emitted `STATIC_INSTALLATION_VERIFIED`. Its evidence reports
exactly `cryptography 50.0.1`, `cffi 2.0.0`, `pycparser 2.23`, and
`typing-extensions 4.15.0`; 190 regular files accounted for by the exact union
of the four RECORD files; unchanged pinned wheel sources and D-093 evidence;
the pinned controller identity; and the pinned `xcrun_db` identity.

The runner correctly returned `FAILED` because stderr was not empty. The single
execution is therefore a consumed gated negative and must not be reclassified as
a positive run.

## Independent review

Both blind request-031 reviews passed the evidence review and independently
confirmed artifact identities, execution consumption, write confinement,
absence of input mutation and the limited claim boundary:

- Claude Gate 1 response SHA-256
  `d36647647425ec005e6569de9ed42cc334835f26cf67a89a77c0202dd876f319`;
- AGy Gate 2 response SHA-256
  `a93a91bffdc5e55fe11212ac0176e41a2e046a12020504c8840e8e1755346414`.

Claude independently recomputed thirteen static properties from the preserved
bytes and found all satisfied. AGy independently rehashed the wheel and
installation inputs and confirmed the positive stdout contents. Both kept the
execution negative because the 110 stderr bytes are unavailable for inspection.

## Disposition and gap

The static properties are corroborated; the installed tree remains unaccepted
pending a separately reviewed no-execution disposition. Every future runner
with an stderr holdpoint must preserve bounded raw stderr content before
evaluating success.

Nothing here establishes importability, Ed25519 behavior, native-code safety,
vulnerability absence or AAuth conformance. No retry, provider import,
native-code execution, pip operation, network access, wallet or WAS work, Misty
access, G28 or G29 is authorized.
