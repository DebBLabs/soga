# M02 AAuth `fcf656d` Ed25519 Provider-Behavior Proposal

Date: 2026-09-21
Status: PROPOSED — NO SOURCE CREATION, IMPORT OR EXECUTION AUTHORIZED
Prepared at: `main @ 0800e450386a7315e6048cea45165d7cbd72aca0`
Prerequisite: D-097 static installation acceptance
Review class: mandatory blind dual review

## Purpose

Establish whether the exact preserved `cryptography 50.0.1` installation can
perform the deterministic Ed25519 operations required by the AAuth `-11` token
path. This is provider verification only, not JWT, HTTP Message Signature or
AAuth conformance testing.

This phase will explicitly execute bundled native code from:

- `site-packages/cryptography/hazmat/bindings/_rust.abi3.so`; and
- `site-packages/_cffi_backend.cpython-39-darwin.so`, if the selected import
  loads it.

No import or native-code execution is authorized by this proposal.

## Exact preserved input

- installation parent:
  `/private/tmp/m02-aauth-fcf656d-phase1-install-20260921`;
- provider root: `site-packages` beneath that parent;
- accepted distributions: `cryptography 50.0.1`, `cffi 2.0.0`,
  `pycparser 2.23`, and `typing-extensions 4.15.0`;
- static acceptance decision: D-097, recorded in the decision log and pending
  commit; the material it accepts is committed at
  `0800e450386a7315e6048cea45165d7cbd72aca0`;
- interpreter: `/usr/bin/python3`, expected `Python 3.9.6`.

The provider root is read-only input. No file beneath the installation parent
may be changed, created, removed or permission-modified.

## Authoritative deterministic vector

Use RFC 8032, Section 7.1, Ed25519 Test 1. This RFC is not locally pinned:
unlike the four Phase B0 normative sources, RFC 8032 has not been acquired under
a bounded controller and its provenance cannot be recomputed offline from this
repository. The values below rely on the cited published RFC Editor document at
<https://www.rfc-editor.org/rfc/rfc8032.html>:

- 32-byte secret seed:
  `9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60`;
- expected public key:
  `d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a`;
- message: empty byte string;
- expected signature:
  `e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155`
  `5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b`.

## Phase 1 — create-only sources

Create two standard-library SOGA sources under `tools/m02_aauth_fcf656d/`:

1. `verify_ed25519_provider.py`, the provider-behavior child; and
2. `run_ed25519_provider_verification.py`, the bounded outer runner.

Neither source may be imported, compiled, linted, tested or executed before
both receive blind dual static PASS.

### Provider-behavior child

The child must:

1. accept no arguments and set `sys.dont_write_bytecode = True` before adding
   the exact provider root to `sys.path`;
2. run under `/usr/bin/python3 -I -S`, retain the interpreter's standard-library
   paths, remove the script directory and empty-string path, and insert only the
   exact provider root as the sole non-standard-library import root;
3. import only the required `cryptography` version, `InvalidSignature`,
   `serialization`, and Ed25519 key classes from the accepted tree;
4. verify `cryptography.__version__ == "50.0.1"` and require every loaded module
   whose name begins `cryptography`, `cffi`, `_cffi_backend`, `pycparser`, or
   `typing_extensions` to resolve beneath the exact provider root;
5. construct the private key from the RFC seed, derive the raw public key, sign
   the empty message, compare the public key and signature byte-for-byte with
   RFC 8032 Test 1, and verify the expected signature;
6. require `InvalidSignature` for the expected signature over message `b"x"`;
7. flip one bit of the expected signature and require `InvalidSignature` for
   the empty message;
8. require construction from 31-byte and 33-byte inputs to fail, recording the
   exact exception type raised for each rather than requiring a specific type in
   advance, since that type originates in compiled code and cannot be confirmed
   by static review;
9. emit exactly one bounded JSON document to stdout containing only provider
   version, interpreter version, vector identifier, boolean test results,
   expected public-key/signature hashes, loaded provider-module paths, and a
   final result; and
10. write nothing to stderr or to the filesystem and have its own operations
    access no network, listener, subprocess, clock-dependent input, random input
    or external service.

The seed and signature are public RFC test material, not production keys or
credentials. The child must not generate or persist any key.

### Outer runner

The runner must follow the accepted static runner's fail-closed pattern and its
lessons learned. It must:

1. accept no arguments, verify exact committed child and runner hashes and
   require no working-tree entry for either path before creating output;
2. confirm the provider root and installation parent are nonsymlink directories
   and recompute the accepted static identities before child start;
3. refuse a pre-existing evidence directory at
   `/private/tmp/m02-aauth-fcf656d-ed25519-provider-20260921`;
4. create only that directory at mode `0700` and write only beneath it;
5. invoke exactly `/usr/bin/python3 -I -S -B` and the exact child path once, with
   disconnected stdin, `shell=False`, a fixed minimal environment,
   `PYTHONDONTWRITEBYTECODE=1`, a 30-second timeout and no retry;
6. capture stdout and stderr separately with 1,000,000-byte bounds;
7. preserve bounded stdout bytes unchanged as `provider-evidence.json` and
   bounded stderr bytes unchanged as `provider-stderr.bin` before evaluating
   either stream; an empty stderr artifact is still required and preserved;
8. require child exit zero, empty stderr, exactly one JSON stdout document and
   final result `ED25519_PROVIDER_VERIFIED` for a positive run;
9. atomically write a compact `run-record.json` containing hashes, lengths,
   timings, command, environment, repository state and only the parsed result
   string, never a duplicate of either stream; and
10. preserve all created evidence on every stop, with no cleanup or retry.

The runner itself may not import the provider or load native code. The child is
the sole process authorized in a later phase to do so.

## Phase 2 — prospective execution holdpoint

After both complete sources receive blind dual PASS and are committed, a
separate PI authorization must name their committed hashes and explicitly
authorize one child import and execution of the bundled native provider code.
That authorization must repeat the 30-second, 1,000,000-byte-per-stream, fixed
evidence-directory and no-retry controls.

Both gates must independently review all raw evidence before the provider may be
used by AAuth implementation. A positive result establishes only deterministic
Ed25519 provider behavior for the pinned environment. It does not establish
general native-code safety, vulnerability absence, JWT correctness, HTTP
Message Signature correctness or AAuth conformance.

## Stop rules

Stop before child start on any source, commit, static-input, working-tree or
evidence-directory mismatch. After child start, preserve bounded stdout and
stderr and stop on timeout, overflow, nonzero exit, nonempty stderr, malformed
or multiple JSON documents, any failed positive or negative test, unexpected
module origin, write failure or unexpected exception. Any start consumes the
single later-authorized execution.

## Exclusions

This proposal authorizes no source creation, import, native-code execution,
test, runner/verifier execution, pip or dependency operation, AAuth
implementation, JWT or HTTP-signature work, listener, network access, wallet or
WAS work, personal data, payment, Misty access, physical actuation, G28 or G29.
The unrelated PI routine-tool proposal remains excluded and untouched.
