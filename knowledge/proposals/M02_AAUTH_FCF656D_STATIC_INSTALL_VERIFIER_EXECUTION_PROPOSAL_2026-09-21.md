# M02 AAuth `fcf656d` Static Installation Verifier Execution Proposal

Date: 2026-09-21
Status: PROPOSED — NO RUNNER CREATION OR EXECUTION AUTHORIZED
Prepared at: `main @ fb9e53d80a582e4372ff8de80bfc4fba150b3c19`
Authority basis: D-094 and accepted recovery proposal commit `49cbec2`
Review class: mandatory blind dual review

## Purpose

Run the independently reviewed static verifier exactly once to determine whether
the preserved D-093 installed tree has the identity, containment and RECORD
completeness required for later, separately authorized provider verification.

This phase does not import an installed package, execute bundled native code,
test Ed25519 behavior or establish AAuth conformance.

## Exact inputs

- verifier commit: `fb9e53d80a582e4372ff8de80bfc4fba150b3c19`;
- verifier path:
  `tools/m02_aauth_fcf656d/verify_preserved_installation.py`;
- verifier SHA-256:
  `f75d8448992b08ba1040e77dd5593dc4692be76f76aa1942cd9ed69e3ea9eb71`;
- preserved wheel root:
  `/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels`;
- preserved installation parent:
  `/private/tmp/m02-aauth-fcf656d-phase1-install-20260921`;
- evidence directory, outside the preserved parent:
  `/private/tmp/m02-aauth-fcf656d-static-recovery-20260921`;
- final stdout evidence:
  `/private/tmp/m02-aauth-fcf656d-static-recovery-20260921/static-verification-evidence.json`;
- runner record:
  `/private/tmp/m02-aauth-fcf656d-static-recovery-20260921/run-record.json`.

## Phase 1 — create-only runner

Create one standard-library-only SOGA runner at
`tools/m02_aauth_fcf656d/run_static_installation_verifier.py`. It accepts no
arguments and must:

1. verify, before any output directory is created, that the verifier path
   exists and is a regular nonsymlink file whose SHA-256 is
   `f75d8448992b08ba1040e77dd5593dc4692be76f76aa1942cd9ed69e3ea9eb71`, and
   that `git status --porcelain` reports no entry for either the verifier path
   or the runner path, so the file about to run is the committed and reviewed
   one; record the observed HEAD and the full porcelain status in the run record
   rather than comparing HEAD with a fixed value, because the execution HEAD is
   the commit that adds this runner and cannot be known when the runner is
   authored and reviewed;
2. verify that the wheel root and installation parent exist, are directories
   and are not symlinks;
3. refuse if the evidence directory already exists;
4. create only the evidence directory, mode `0700`, and temporary files inside
   it;
5. invoke exactly `/usr/bin/python3` and the exact verifier path, with stdin
   disconnected, a minimal fixed environment, a 60-second timeout and no shell;
6. capture stdout and stderr separately in memory, enforce a 2,000,000-byte
   bound on each, and require stderr to be empty;
7. require stdout to be exactly one JSON document with result either
   `STATIC_INSTALLATION_VERIFIED` or `FAILED`;
8. atomically write stdout bytes unchanged to
   `static-verification-evidence.json`, mode `0400`;
9. atomically write `run-record.json`, mode `0400`, recording runner and
   verifier hashes, repository state, command, fixed environment, start/end
   times, duration, exit status, timeout status, stdout/stderr lengths and
   hashes, and the parsed result, without copying the full stdout into the run
   record;
10. require result `STATIC_INSTALLATION_VERIFIED` with exit status zero for a
    positive run; any other combination is a negative result and must not be
    retried; and
11. perform no cleanup of the preserved inputs. On failure after creating the
    evidence directory, preserve every file already written for review.

The runner may write only beneath the new evidence directory. It must not write
bytecode, so its own environment and the child environment must include
`PYTHONDONTWRITEBYTECODE=1`.

## Phase 2 — single execution

After the complete runner receives blind dual static PASS and is committed, a
separate PI authorization may permit exactly one execution. The authorization
must name the committed runner and verifier hashes and repeat the 60-second and
2,000,000-byte-per-stream bounds. No automatic retry is permitted.

After execution, both reviewers must independently:

- verify cleanup is not applicable because no process or listener persists;
- recompute the verifier, evidence and run-record hashes;
- verify the evidence against the preserved wheel and installation trees; and
- confirm the claim remains limited to static identity, containment and RECORD
  completeness.

## Stop rules

Stop and preserve evidence on any HEAD or hash mismatch, missing or changed
input, pre-existing evidence directory, timeout, output overflow, nonempty
stderr, invalid or multiple JSON documents, nonzero child exit, `FAILED` result,
write failure or unexpected exception. Every stop consumes the one authorized
execution if the child verifier was started.

## Exclusions

This proposal authorizes no runner creation or execution. It authorizes no pip
retry, dependency change, provider import, native-code execution, Ed25519 test,
AAuth implementation, listener, network access, wallet or WAS work, personal
data, payment, Misty access, physical actuation, G28 or G29. The unrelated PI
routine-tool proposal remains excluded and untouched.
