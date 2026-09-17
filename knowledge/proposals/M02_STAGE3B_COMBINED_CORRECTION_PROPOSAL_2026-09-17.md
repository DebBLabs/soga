# M02 Stage 3B — Combined create-only correction

Date: 2026-09-17
Status: PROPOSED — IMPLEMENTATION AND EXECUTION UNAUTHORIZED
Author/integrator: Codex. Mandatory blind dual review: executable mechanics,
security controls, third-party composition and material evidence claims.
Basis: request-043 diagnosis report
`8c0aa2f2a469489aaf86ed1ab95357571988feabfe917257853c5056bc7381a7`.
This proposal does not establish the causes of the consumed D-072/D-067 runs.

## Phase 1 authority requested — create only

After both proposal reviewers PASS and prospective PI authorization, modify
only these SOGA-owned files, with no import, compile, lint, test or execution:

- m02_was_composition/adapter.py
- m02_was_composition/worker.mjs
- m02_was_composition/diagnostic_tests.py
- tests/test_m02_was_composition.py
- tests/test_m02_was_diagnostics.py

Do not modify controller.py, the old execution proposals, upstream code,
dependencies/build output or Person Server implementation. Preserve the exact
fixed WAS environment and existing retained diagnostic directory unchanged.
If an additional file/mechanism is needed, stop and seek revised scope.

## Complete correction design

1. Public ESM package loading. Remove createRequire-based root resolution.
   Preserve the temporary package-name symlink under the existing linkRoot's
   node_modules. At execution time only, create an exclusive harness-owned
   loader.mjs under linkRoot which re-exports FileSystemBackend from the bare
   'was-teaching-server' package root. Dynamically import that local loader by
   URL. This selects the upstream public import condition, never a deep backend
   import or rewritten upstream exports. Use fixed loader text and existing
   disposable-root cleanup. Install process-local guards before creating/importing
   the loader; retain the pre-import readiness/observer/release holdpoint.
   Candidate identity/export metadata remain prerequisites for later execution.

2. Binding. Limit the second-envelope request-id check to duplicate/collision.
   Store and all guard modes remain single-envelope, with no authority implied.
   Preserve mode, interpretation, identifier, data-root and second-request checks.
   Add regression assertions for every guard mode and both two-envelope modes.

3. Shared canonical bytes. Retain the existing restricted ASCII/boolean/null/
   safe-integer/list/string-keyed-object domain, size limits and secret screening.
   Change Python to ensure_ascii=False only after existing ASCII validation;
   encoded output remains UTF-8 containing ASCII bytes. JavaScript serializes
   recursively with explicit lexically sorted object keys rather than depending
   on Object.fromEntries property enumeration; use JSON.stringify for primitive
   strings/keys and validated primitives. DEL remains literal; required C0
   control characters remain escaped. Do not relax byte/hash equality. Preserve
   rejection of non-ASCII, unsafe integers, floats and unsupported types, and
   JavaScript negative-zero rejection. Include DEL and numeric-looking object
   keys in shared fixtures to check both escaping and ordering. State that the
   domain is this research contract, not a general JSON canonicalization standard.

4. Correct negative fixtures. The deliberately wrong-hash fake must report
   valid canonicalFixtures matching the shared fixtures, networkAttempts=0,
   valid response structure/version and intentionally wrong first.s256. No
   earlier acceptance predicate may be omitted. The timeout fake must keep a
   finite live timer (five seconds) after release while the adapter deadline
   stays one second; assert named timeout and temporary-root cleanup. Do not
   increase adapter deadlines or allow lingering resources. Preserve all other
   malformed/nonzero/overflow/cleanup/collision controls.

5. Fixed redacted stages. Replace message-prefix stage derivation with explicitly
   tagged local errors and a finite operation-stage state. Use allowlisted
   package_resolution/was_import categories for loading failures and fixed
   existing storage/readback/binding/guard categories where assigned. Guard events
   retain prohibited_api plus the fixed intercepted API name. Never emit upstream
   exception messages, paths, tokens, envelopes, traces or arbitrary stage strings.
   Untagged failures use a fixed non-secret category, not parsed message text.
   Update diagnostic STAGES with only the exact new fixed categories; preserve
   unknown handling for unavailable/unrecognized data and all JSON/record caps.
   Synthetic diagnostics must verify those stages without exposing raw exceptions.

## Full self-review and regression requirements

Review the complete adapter/worker/test path, not just the nine old methods.
Verify constructor/call/result shape compatibility with the unchanged WAS public
backend; loader cleanup in success and failure; all guard/second-envelope modes;
both positive round-trips, idempotency/collision, byte fixtures, negative response
predicate ordering, finite timeout liveness, bounded stage reporting, and all
existing cleanup/observation controls. Preserve the 24-invocation process budget,
ten-second worker ceiling, 180-second focused-child ceiling, stream/input/output
caps, subprocess limits, temp-root ownership and bytecode suppression. Count
potential adapter.store calls in the expanded focused suite before review;
stop if tests cannot fit the existing invocation ceiling. No new invocation
budget or command is authorized by this design.

Tests may be written and statically reviewed, never run in Phase 1. Harness
loader files/timers/symlinks are designed here but may be materialized only in
a separately authorized execution. No production data, tokens or identities.
The tests continue using synthetic result dictionaries; this milestone cannot
claim live Person Server, wallet presentation or AAuth protocol compliance.

## Evidence, reviewers and holdpoints

Record exact created-file hashes, complete diff, static self-audit, invocation
count and any unresolved runtime assumption. Source creation has no candidate
runtime side effects. Both eligible non-authoring reviewers receive separate
hash-pinned requests and independently read all complete created files. They
must not read peer reviews or claude-to-cg before posting and must state
independence/contributor position. No reviewer-run imports/tests are permitted.

Commit/push requires PI acceptance of the exact reviewed final sources. Phase 2
requires a separate finite execution proposal, two blind proposal passes and
prospective PI authorization. The previous diagnostic invocation is consumed
and may not be reused. Future execution evidence requires blind dual review
before acceptance. This proposal contains no execution command authorization.

## Stop rules and exclusions

Stop on absent/changed candidate inputs, need for upstream/dependency edits,
scope expansion, guard weakening, budget mismatch, unavailable verification,
personal data, or any new permission requirement. Label unverified runtime
behavior; do not use review as a substitute for author research/self-audit.
No execution, automatic retry, package/build operation, network, listener,
Docker, external service, Freewallet integration, Person Server change,
payment, Misty access, physical action, G28 or G29. No unrelated file changes.
The separate PI routine-tool proposal remains unread/unadopted/untouched.
Queue files and current-session permission do not adopt this unseen design.
