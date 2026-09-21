# M02 AAuth `fcf656d` Static Installation Recovery Proposal

Date: 2026-09-21
Status: PROPOSED — NO VERIFIER CREATION OR EXECUTION AUTHORIZED
Prepared at: `main @ cc78065`
Authority to create: D-094
Author/integrator: Codex
Review class: mandatory blind dual review

## Purpose

Determine whether the preserved D-093 installation is statically complete and
internally consistent without rerunning pip, importing any installed module,
executing bundled native code, deleting `xcrun_db`, or changing any preserved
byte or permission.

## Fixed preserved inputs

- wheel source:
  `/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels`;
- installation parent:
  `/private/tmp/m02-aauth-fcf656d-phase1-install-20260921`;
- installed target: `site-packages` below that parent;
- preserved scratch artifact: `tmp/xcrun_db`, observed mode `0600`, size 499,
  SHA-256
  `767b97e4e6c44f3e9a7b2496c54bcc1c3901650873f4fc67d811e051bd9f6e8b`;
- D-093 raw evidence SHA-256
  `caaacd3791b77e83668d94769c7226c7ecd65a41105cab2996b391798f9a6bb3`;
- installation controller SHA-256
  `84f4594b25a68f4560eeb575b7977cbfc7047331daddf9006ea578a2acd34b13`.

The recovery does not need to establish why macOS created `xcrun_db`. It treats
the file as a disclosed boundary artifact outside `site-packages`, preserves it
unchanged, and records its identity. Any causal classification is separate
research and is not required to verify the installed tree.

## Proposed read-only verifier

Create a standard-library-only verifier that accepts no arguments and performs
no writes. It must:

1. record its own hash and exact SOGA HEAD/tree state using the pinned minimal
   Git environment;
2. recompute the four accepted source-wheel sizes and SHA-256 values and compare
   them with D-091;
3. recompute the D-093 evidence and controller hashes;
4. inventory and hash the entire installation parent, including `xcrun_db`,
   without following symlinks;
5. reject every symlink, path traversal, unexpected `.dist-info` distribution,
   duplicate distribution, absent METADATA/RECORD, or installed name/version
   outside exactly `cryptography 50.0.1`, `cffi 2.0.0`, `pycparser 2.23`, and
   `typing-extensions 4.15.0`;
6. parse every RECORD as CSV, confine every resolved path beneath
   `site-packages`, verify every recorded SHA-256 and size, permit an unhashed
   entry only for that distribution's RECORD file, and require the union of all
   RECORD paths to equal every regular installed file;
7. verify scratch contains exactly one regular nonsymlink file named `xcrun_db`,
   mode `0600`, size 499, and SHA-256
   `767b97e4e6c44f3e9a7b2496c54bcc1c3901650873f4fc67d811e051bd9f6e8b`
   without claiming its cause;
8. confirm the source wheels and preserved D-093 evidence are unchanged after
   verification; and
9. emit its complete result to stdout only. The operator may capture stdout in
   a separately named evidence file outside the preserved installation parent;
   the verifier itself must open no output file.

The verifier must not add `site-packages` to `sys.path`, load distribution entry
points, call `importlib.metadata`, import any installed package, inspect a native
library by loading it, invoke pip, launch a subprocess other than the two bounded
read-only Git queries, access a network, or change access/modify times where the
platform permits avoiding them. Ordinary file reads may update filesystem access
metadata; no stronger claim is made.

## Execution and evidence holdpoint

The complete verifier requires blind dual static review before commit or use. A
later prospective authorization must name the exact committed verifier hash,
the stdout evidence destination outside the preserved parent, finite runtime and
output bounds, and one execution with no retry. Independent reviewers must then
recompute its result from the preserved files before the installation can be
accepted for any later import.

## Claim boundary and exclusions

A positive result would establish only static installed-tree identity,
containment and RECORD completeness for the preserved D-093 output. It would not
establish importability, Ed25519 behavior, native-code safety, vulnerability
absence or AAuth conformance.

This proposal authorizes no verifier creation or execution, pip retry, cleanup,
file modification, import, native-code execution, implementation, test,
listener, wallet/WAS work, Misty access, G28 or G29. The unrelated PI
routine-tool proposal remains excluded and untouched.
