# M02 Stage 3B — One corrected socket-free composition execution

Date: 2026-09-17
Status: PROPOSED — EXECUTION UNAUTHORIZED
Prepared at: e0960f4eb7047dccc8209969adb7219d2b0d2ba4
Author/integrator: Codex. Mandatory blind dual review under D-064/B-044.

## Purpose and exact inputs

D-077 accepts corrected source, not runtime success. Test whether synthetic
Person Server result evidence survives the WAS filesystem-backend round-trip
and whether the existing negative/guard/cleanup contracts hold. Do not attribute
the consumed D-067 or D-072 failures retrospectively. This is not live Person
Server integration, wallet presentation, or AAuth protocol conformance.

Exact accepted source SHA-256:

- m02_was_composition/adapter.py: 28bcbaeda80c7436353e6872e3fa2f35390e4089ae1ea7d5c64ced93afe071e7
- m02_was_composition/worker.mjs: f3f58b1d603228c057d9a5af99045cd5783ea5a92ffaa0e550fc0cc1ce2d5b60
- m02_was_composition/diagnostic_tests.py: 794a1b961d976abeaad044221e031358922016e9817c891e2403663337719403
- tests/test_m02_was_composition.py: 9855fa34dab466314462b9cf4dbe1220e05a521678481d72a5768134d912922f
- tests/test_m02_was_diagnostics.py: 2b15758936df7f95af9f40836f949bcca87ec86d24fbbff2cfadf10f45a4f903
- m02_was_composition/controller.py (unchanged): 559a9397e610a7f60cdf34db1b96874ad60509d609a069e2c0bf2e5b78727f2e

The statically reviewed counts are nine synthetic instrumentation tests, 34
focused tests, and 23 adapter.store calls against the unchanged ceiling of 24.
Four contract calls reject before spawn; the remaining 19 include one oversized
input rejection and 18 child spawns. These counts are predictions, not runtime
observations. Stop on a source/count mismatch; do not increase the budget.

Require preserved WAS at
/private/tmp/m02-stage3lib-20260910/was-teaching-server, commit
2090a606f2723e4d57ef0090db55fd1bdab9427e, tree
540d85cea6cc7ab50ee6f00b0dead2084c1d65de, clean tracked source, unchanged public
root import export, and 298-file dist manifest SHA-256
7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586.
dist/build-info.json remains absent; conditional provenance rests on accepted
restoration evidence, not a completed upstream build. Preserve dependencies,
cache and build output unchanged. Require /usr/bin/python3 Python 3.9.6 and
/opt/homebrew/Cellar/node/26.7.0/bin/node v26.7.0. No restoration/package operation.

## Prospective holdpoints and exact sequence

Both eligible blind reviewers must PASS this complete proposal before PI
authorization. Then commit/push this proposal and a prospective execution
decision; record the resulting full commit as EXECUTION_HEAD. Verify local and
origin/main equality, accepted source hashes, candidate identity/manifest,
runtime versions, and absence of worker/fake/module leftovers before use.

Execute from /Users/debb/dev/soga-clean with explicit platform approval outside
the default agent sandbox. Use only PATH=/usr/bin:/bin:/usr/sbin:/sbin, LANG=C,
LC_ALL=C, PYTHONDONTWRITEBYTECODE=1 in the outer child environment. No persistent
permission/configuration change. Guards are process-local, not OS containment;
socket observations are unprivileged user-visible inventories, not host-wide
proof. No intentional network access or listener is permitted.

1. Once only: /usr/bin/python3 -m unittest tests.test_m02_was_diagnostics.DiagnosticInstrumentationTests -v
   Select this exact class, never the deliberate-failure SyntheticCase helper
   or the whole module. No WAS import or Node execution in this synthetic check.
   Record count/status. Apply an outer 60-second process-group deadline and
   64 KiB per-stream capture caps, TERM then after one second KILL on timeout or
   overflow, and wait/drain completion. Stop on nonzero, mismatch, timeout,
   overflow, unexpected process, or incomplete cleanup; no composition run.
2. Verify the synthetic check left no new diagnostic temporary directory by
   comparing before/after scoped directory inventories. Preserve the existing
   /private/tmp/m02-stage3b-diagnostics-20260916-001 unchanged; it is not a leftover
   from this check. Require /private/tmp/m02-stage3b-diagnostics-20260917-001 absent.
   Create that new empty directory exclusively with mode 0700; never reuse,
   overwrite, or delete an occupied path.
3. Once only, replacing solely EXECUTION_HEAD with the recorded full commit:

   /usr/bin/python3 -c 'import json; from pathlib import Path; from m02_was_composition.controller import run_diagnostic_once; print(json.dumps(run_diagnostic_once(expected_soga_head="EXECUTION_HEAD", evidence_root=Path("/private/tmp/m02-stage3b-diagnostics-20260917-001")), sort_keys=True))'

   Use the unchanged diagnostic entry point, not run_once. Its child sets
   M02_STAGE3B_EXECUTE=1 and PYTHONDONTWRITEBYTECODE=1. Preserve 24 invocation,
   180-second focused-child, ten-second worker and existing input/output ceilings.
   Apply an outer 240-second process-group deadline and 64 KiB per-stream caps
   with the same termination/wait/drain discipline. The loader and package-root
   symlink may be created only inside each owned disposable module directory;
   install guards and complete pre-import observer/release checks before WAS
   import. FilesystemBackend data is exclusively synthetic temporary storage
   outside both repositories. No HTTP app or service startup is permitted.

Each attempt is consumed when its corresponding process starts. No retry after
any failure. Any outer orchestration used to enforce these limits must preserve
the exact commands and environment, be recorded in evidence, and receive both
blind reviews before execution if it introduces executable script source.
The controller's ok field, execution outcome, complete diagnostic counts and
postflight—not merely the outer exit status—determine acceptance eligibility.

## Evidence, cleanup and interpretation

Retain atomic record.json (0600, at most 24576 bytes), exact hash/size, stream
hashes, fixed test/stage records and controller execution/postflight outcomes.
Preserve 128-record and 16384-byte diagnostic-document caps. Never report raw
focused exceptions, stack traces, paths in upstream errors, envelopes, tokens,
or subtest values. Unknown remains unknown. Parameterized failures can identify
only the parent method. Printing failure after retention does not authorize a
rerun: inspect the retained artifact read-only.

Independently inspect no surviving scoped controller/test/Node worker process,
no m02-stage3b-run-*, m02-stage3b-fake-* or m02-was-composition-modules-* root,
unchanged SOGA status and WAS source/dist manifest, and unchanged user-visible
listener inventory. Stop/report on incomplete verification or leftovers; no
unapproved cleanup repair. Retain both diagnostic evidence roots unchanged
pending separate PI retention/removal authority.

Write standalone evidence with exact commands, full execution commit, source
pins, permissions, runtime counts/statuses, finite-limit observations, retained
redacted record transcription, and independent cleanup observations. Both gates
receive separate hash-pinned requests and review blindly before acceptance.
Do not open peer review directories or claude-to-cg before posting; end each
response with independence/contributor statement. PASS on evidence quality is
not composition success. Any successful result is limited to synthetic evidence
storage through this exact socket-free WAS backend profile.

## Stop rules and exclusions

Stop on absent/changed inputs, unavailable controls, unexpected permission,
scope/count mismatch, network attempt, listener, timeout/overflow, altered
dependencies, personal data, or cleanup failure. No code change, retry, build,
dependency operation, network/external service, Docker, Freewallet integration,
live Person Server changes, participant sessions, payment, Misty access,
physical actuation, R3 protocol work, G28 or G29. The unrelated PI routine-tool
proposal remains unread, unadopted and untouched. D-077 authorizes proposal
preparation/review only; this document grants no execution authority.
