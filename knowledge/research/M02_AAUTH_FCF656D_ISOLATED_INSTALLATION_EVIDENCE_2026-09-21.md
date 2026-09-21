# M02 AAuth `fcf656d` Isolated Installation Evidence

Date: 2026-09-21
Status: EXECUTED ONCE — GATED NEGATIVE RESULT PENDING BLIND DUAL REVIEW
Authority: D-093
Execution HEAD: `c4bc86fe402d9b6e88ff5d55de1308e081ca1e44`
Controller SHA-256: `84f4594b25a68f4560eeb575b7977cbfc7047331daddf9006ea578a2acd34b13`

## Result

The single authorized installation attempt is consumed. The controller exited
1 and recorded `FAILED` at stop rule `pip scratch directory not empty`.
There was no retry.

pip 21.2.4 itself exited 0 and reported successful installation of exactly:

- `cryptography 50.0.1`;
- `cffi 2.0.0`;
- `pycparser 2.23`; and
- `typing-extensions 4.15.0`.

The installation target contains files, but the controller stopped before its
post-pip source re-verification, installed-distribution/RECORD verification,
scratch removal and positive result. The target therefore remains unaccepted
and must not be imported or used.

## Stop evidence

Fixed parent:
`/private/tmp/m02-aauth-fcf656d-phase1-install-20260921`

The private scratch directory contains one unexpected file:

- `tmp/xcrun_db`, mode `0600`, 499 bytes.

This is consistent with a macOS/Xcode runtime cache name, but that attribution
has not been established as an accepted cause. Its presence violates the
reviewed empty-scratch success condition regardless of cause. No file was
removed or changed after the stop.

The preserved `evidence.json` is mode `0400` with SHA-256
`caaacd3791b77e83668d94769c7226c7ecd65a41105cab2996b391798f9a6bb3`.
It records pip exit 0, empty stderr, bounded stdout naming only the four local
wheel paths and exact installed versions, the controller/repository identities,
pre-install source hashes, command/environment, and a 222-entry failure-state
inventory. Local and remote HEAD remained at the execution commit; no tracked
repository file was modified.

## Claim boundary

This is not positive installation evidence. It establishes that pip reported a
local four-wheel installation and that the controller stopped fail-closed on an
unexpected scratch artifact. It does not establish post-install source
immutability, RECORD completeness, importability, Ed25519 behavior, native-code
safety or AAuth conformance.

No provider import, native-code verification, cleanup, retry or use is
authorized. Any diagnosis, classification of `xcrun_db`, revised scratch rule,
cleanup or new attempt requires a separate reviewed proposal and prospective PI
authorization.
