# M02 AAuth `fcf656d` Phase A Wheel-Acquisition Evidence

Date: 2026-09-21
Status: EXECUTED ONCE — POSITIVE RESULT PENDING BLIND DUAL REVIEW
Authority: D-090
Execution HEAD: `6a8d2e9922df711ef401baf6dc2795c103f96ddd`
Controller SHA-256: `4105596b13aca01b467e7a8cb42dd79c118713d7fb152840f0c7c4e78ca8f427`

## Result

The single authorized Phase A attempt ran from 2026-09-21T05:35:53Z through
05:35:54Z and exited successfully. All four exact HTTPS requests returned HTTP
200 with no redirect. Declared and received sizes matched the pinned sizes, and
all computed SHA-256 values matched the D-087/D-089 manifest.

| Artifact | Received bytes | Observed SHA-256 | Result |
|---|---:|---|---|
| `cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl` | 4,035,307 | `ca83d00d9e69cd5eb63f2e69c3a5a59e0cecae5ae14c6ae0b35830fe3b37bad0` | VERIFIED |
| `cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl` | 180,509 | `de8dad4425a6ca6e4e5e297b27b5c824ecc7581910bf9aee86cb6835e6812aa7` | VERIFIED |
| `pycparser-2.23-py3-none-any.whl` | 118,140 | `e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934` | VERIFIED |
| `typing_extensions-4.15.0-py3-none-any.whl` | 44,614 | `f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548` | VERIFIED |

The client reported TLS 1.2 with cipher
`ECDHE-RSA-CHACHA20-POLY1305` and peer-certificate SHA-256
`fad0ad5bf0f0353bf1d3778e310f2efbdd0fe2b8a6886903fc4cce1f12d831f1`
for all four requests.

## Preserved evidence

Target: `/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels`

- target parent mode: `0700`;
- target mode: `0500`;
- four wheel modes: `0400`;
- `evidence.json` mode: `0400`, size 5,819 bytes, SHA-256
  `0208d27acbaf12110eb580ca0b08aea98327479745217d42aabb32688c5854ed`.

The evidence file's own final mode was verified by external post-run filesystem
inspection; it cannot attest its own mode from inside the record written before
the final permission transition.

The evidence records the exact URLs, HTTP results, zero redirect counts and
empty redirect chains, TLS observations, expected/observed lengths and hashes,
controller identity, timestamps, inventories and modes.

At execution, the controller's `git status --porcelain` recorded two untracked
paths: `.claude/` and the excluded
`knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md`.
The controller runs Git with a minimal environment that omits `HOME`, so it does
not read the user-level exclude file. `/Users/debb/.config/git/ignore` excludes
`**/.claude/settings.local.json`, which is why an interactive `git status` does
not list that path. `.claude/` remains present and unchanged; the difference is
an artifact of the controller's deliberate minimal environment, not a
filesystem change. Local and remote HEAD remained at the execution commit, and
no tracked repository file was modified by the controller.

## Claim boundary

This result establishes acquisition of four exact distribution bytes matching
the accepted manifest. No wheel was installed, extracted, imported or executed.
It does not establish installability, runtime correctness, vulnerability
absence, or AAuth conformance. The artifacts are not authorized for further use
until this evidence receives blind dual review and PI acceptance.
