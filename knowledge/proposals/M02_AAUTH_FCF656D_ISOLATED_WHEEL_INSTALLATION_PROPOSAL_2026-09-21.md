# M02 AAuth `fcf656d` Isolated Wheel Installation and Verification Proposal

Date: 2026-09-21
Status: PROPOSED — NO INSTALLATION OR EXECUTION AUTHORIZED
Prepared at: `main @ e8d35f7`
Authority to create: D-091
Author/integrator: Codex
Review class: mandatory blind dual review

## Purpose

Install only the four D-091-accepted wheels into a disposable isolated target
and verify the installed distribution identities and minimal Ed25519 provider
surface required for Phase 1. No system or user Python environment is modified.

## Fixed inputs and target

Source directory:
`/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels`

Target directory (must not exist):
`/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/site-packages`

Private pip scratch directory (must not exist):
`/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/tmp`

The four source filenames, sizes and SHA-256 values are exactly those accepted
under D-091. Recompute all four before installation; any mismatch stops without
creating the target.

## Proposed bounded controller

Create and independently review a controller that:

1. pins `/usr/bin/python3`, verifies Python 3.9.6 and the execution SOGA HEAD,
   self-hash, clean tracked state and fixed input hashes;
2. invokes pip through the pinned interpreter with a minimal environment:
   `PIP_CONFIG_FILE=/dev/null`, `PIP_NO_INDEX=1`,
   `PIP_DISABLE_PIP_VERSION_CHECK=1`, `PYTHONNOUSERSITE=1`, deterministic locale,
   no proxy/index variables, and `TMPDIR` pinned to the private scratch directory;
3. uses only the four absolute local wheel paths with `--no-index`, `--no-deps`,
   `--only-binary=:all:`, `--target <fixed-target>`, no cache and finite timeout;
4. refuses any pre-existing install parent, target or scratch directory,
   unexpected subprocess, network observation, source build, resolver action,
   additional distribution, or modification outside the fixed install parent;
   creates the parent and scratch directory owner-only, inventories scratch
   before and after pip, and requires scratch to be empty after successful pip
   cleanup before removing it;
5. records exact command, environment allowlist, stdout/stderr, exit status,
   before/after inventories and hashes, installed `.dist-info` identities and
   RECORD verification; and
6. stops after installation evidence unless a separately reviewed verification
   step is explicitly authorized.

## Proposed verification step

After installation evidence passes its holdpoint, a separately authorized
standard-library harness may run with an isolated environment and the fixed
target as its only added import path. It may verify only:

- installed versions of `cryptography`, `cffi`, `pycparser` and
  `typing-extensions`;
- Ed25519 private-key generation, signing, public-key verification, altered-data
  rejection and raw public-key serialization through the selected documented
  API; and
- absence of writes, listeners, subprocesses and network activity.

No private key, signature input or secret may enter logs or durable evidence;
evidence records only public-key bytes/hash, message/signature lengths and
pass/fail outcomes. The verification harness requires complete blind dual review
before execution.

## Holdpoints and exclusions

The installation controller must be reviewed before commit or execution.
Installation evidence must be reviewed and accepted before provider import or
verification. Verification evidence must be reviewed before the environment is
an implementation input.

This proposal authorizes nothing by itself. It authorizes no installation,
import, compilation, test, package download, registry/index/network access,
system/user environment change, AAuth implementation, listener, wallet/WAS work,
Misty access, G28 or G29. The unrelated PI routine-tool proposal remains
excluded and untouched.
