# M02 AAuth `fcf656d` No-Execution Static Acceptance Proposal

Date: 2026-09-21
Status: PROPOSED — NO ACCEPTANCE OR EXECUTION AUTHORIZED
Prepared at: `main @ a2a6b5f94c2e5ccdbdf47f976b89b774d8105950`
Authority: PI disposition of the consumed static-verifier execution
Review class: mandatory blind dual review

## Purpose

Decide whether the preserved D-093 installed tree may be accepted for static
identity, containment and RECORD completeness based on two independent
recomputations of the preserved bytes, without repeating the consumed run. The
execution remains a gated negative; this proposal does not waive or explain its
empty-stderr control.

## Review method

Each eligible reviewer must independently, without reading the peer response:

1. verify the runner, verifier, raw stdout evidence, run record and durable
   evidence-report hashes;
2. recompute all four source-wheel sizes and hashes;
3. recompute the D-093 evidence, controller and `xcrun_db` identities;
4. inventory the preserved installation parent without following symlinks;
5. verify exactly the four expected distribution names and versions;
6. independently parse all RECORD files, confine their paths beneath
   `site-packages`, verify every available SHA-256 and size, permit an unhashed
   entry only for its own RECORD, and require their union to equal every regular
   installed file;
7. confirm no preserved input changed and no provider was imported or native
   code loaded; and
8. state separately whether the static properties pass and whether the consumed
   execution remains negative.

Reviewers may use bounded, read-only analysis code outside the repository. They
must not execute the runner or verifier, import from the installed tree, load a
native library, modify preserved state or access an external service.

## Proposed acceptance rule

If both reviewers independently return PASS for every static recomputation, the
PI may accept only this claim:

> The preserved D-093 installation has the pinned distribution identity,
> filesystem containment and RECORD completeness required to proceed to a
> separately proposed provider-behavior verification.

Acceptance would not turn the consumed execution positive, explain its stderr,
or authorize import or execution. Any provider verification must prospectively
authorize `cryptography`'s bundled native code, pin exact positive and negative
tests, and preserve bounded stderr content. Any reviewer mismatch leaves the
installation unaccepted and requires a new PI disposition. No automatic retry
or fallback applies.

## Exclusions

This proposal authorizes no acceptance, execution, retry, cleanup, file change,
provider import, native-code execution, pip operation, AAuth implementation,
test, listener, network access, wallet or WAS work, personal data, payment,
Misty access, G28 or G29. The unrelated PI routine-tool proposal remains
excluded and untouched.
