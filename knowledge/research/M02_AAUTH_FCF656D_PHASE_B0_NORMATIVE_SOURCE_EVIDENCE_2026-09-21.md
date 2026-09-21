# M02 AAuth `fcf656d` Phase B0 Normative-Source Evidence

Date: 2026-09-21
Status: EXECUTED ONCE — POSITIVE RESULT PENDING BLIND DUAL REVIEW
Authority: D-090
Execution HEAD: `6a8d2e9922df711ef401baf6dc2795c103f96ddd`
Controller SHA-256: `e47d48cfb90e8e621ed5a9e712157a06d940037b64cd68db33300d448b827034`

## Result

The single authorized Phase B0 attempt ran from 2026-09-21T05:36:03Z through
05:36:04Z and exited successfully. Each exact HTTPS request returned HTTP 200
with no redirect, stayed below the 2,097,152-byte cap, and contained every
required title, identifier/revision and publication-date marker.

| Document | Received bytes | Observed SHA-256 | Result |
|---|---:|---|---|
| RFC 9421 | 241,160 | `612655786bf4293bfc486e4177571467fbb3de6e6f0eea90cb74c346a34fdf3c` | VERIFIED_IDENTITY |
| RFC 9530 | 67,152 | `544dbb7d9afceafa8c9931d9924ca6cff2b4807274166d7ed2483342ef2cdd6a` | VERIFIED_IDENTITY |
| RFC 9651 | 74,086 | `fe27f2ec8819911afbe4bd11f6fcb947580da4c49e5423a1fff960e252ced26d` | VERIFIED_IDENTITY |
| `draft-hardt-httpbis-signature-key-09` | 183,683 | `b5e8602e217bbccd254b93419d0b54ec2b2a6cdce38351983624718029528a5d` | VERIFIED_IDENTITY |

The RFC Editor responses omitted `Content-Length`; the controller enforced the
received-byte cap as authorized. The IETF draft declared and delivered 183,683
bytes. TLS observations and peer-certificate hashes are retained in the raw
evidence.

## Preserved evidence

Target: `/private/tmp/m02-aauth-fcf656d-phase-b0-20260921/sources`

- target parent mode: `0700`;
- target mode: `0500`;
- four document modes: `0400`;
- `evidence.json` mode: `0400`, size 5,933 bytes, SHA-256
  `293431c89c2136fd2d83bcf2fb92c1f83c044d14590137789a1dc219c5d8870f`.

The evidence file's own final mode was verified by external post-run filesystem
inspection; it cannot attest its own mode from inside the record written before
the final permission transition.

The evidence records exact URLs and requested/final-by-policy hosts, HTTP
results, zero redirect counts and empty redirect chains, TLS observations,
received lengths, hashes, required/missing markers, controller identity,
timestamps, inventories and modes. All missing-marker lists are empty.

At execution, the controller's `git status --porcelain` recorded the same two
untracked paths as Phase A: `.claude/` and the excluded PI proposal. The
controller's minimal environment omits `HOME` and therefore does not read
`/Users/debb/.config/git/ignore`, which excludes
`**/.claude/settings.local.json` from an interactive status view. `.claude/`
remains present and unchanged; the difference is an environment-dependent Git
view, not a filesystem change. Local and remote HEAD remained at the execution
commit, and no tracked repository file was modified by the controller.

## Claim boundary and next holdpoint

This result establishes exact retrieval and bounded identity verification of
four normative text documents. Their observed SHA-256 values become proposed
B1 input pins only after blind dual review and PI acceptance of this evidence.
No matrix was edited, and no implementation, conformance, wheel use or package
operation occurred. Phase B1 remains unauthorized.
