# M02 Stage 3B — Source-only diagnosis

Date: 2026-09-17
Status: RESEARCH REPORT — PENDING BLIND DUAL REVIEW AND PI ACCEPTANCE
Author/integrator: Codex; no delegated authorship.
Authority: PI “proceed” following both request-042 proposal passes; D-074.
SOGA inspection HEAD: 1444bb0086813fb875f733883ba15d2c01128ab7.
No imports, tests, code execution, repairs, network or retries occurred.

## Starting evidence and input verification

D-073 accepted the single diagnostic negative result. Its evidence hash is
`cdd474696d906a4467e7e1e0b7bf74b2f386a0fa6198660c7e3d77d8a26fa8ca`.
The retained record remains at
`/private/tmp/m02-stage3b-diagnostics-20260916-001/record.json`, hash
`7cab14762d0189e7f78f82848ac512d6b3c24a2921bacba7edf6995bd3916ceb`.
It reports seven failures and two errors among 31 tests; all nine stages unknown.
No raw exception bodies or subcase values were available or reconstructed.

WAS fixed checkout remains at commit
`2090a606f2723e4d57ef0090db55fd1bdab9427e`, tree
`540d85cea6cc7ab50ee6f00b0dead2084c1d65de`, tracked source clean.
Before inspection, SOGA had only the reviewed diagnosis proposal and excluded PI
proposal untracked. During research only D-074 and this report were written.
Candidate source/dependencies/build output and implementation/tests were not edited.

## Source-supported findings, not reproduced execution causes

### F1 — Package resolution uses the wrong export condition

worker.mjs:169-174 creates a package-name symlink, then calls
createRequire(...).resolve('was-teaching-server'), and only afterward imports the
resolved URL. WAS package.json:7-13 exports its root through types and import,
with no require or default condition. The main field also names dist/index.js,
but it does not remove this exports-condition mismatch.

The CommonJS resolution step and public import-only contract are visibly
incompatible. This is the leading explanation for the two positive-test errors,
not measured attribution: no resolver exception, code, or raw message from the
consumed run was retained. Its exact Node behavior must be confirmed by a later
authorized execution. Do not claim WAS storage was reached or failed.

### F2 — Guard modes are rejected before any guard can run

adapter.py:82-90 classifies store and all six guard modes as single-envelope
operations and supplies secondEnvelope=null. worker.mjs:145 nevertheless requires
a matching second request for every mode other than store. Thus guard_child,
guard_dns, guard_network, guard_worker, guard_spawn and guard_exec encounter
binding:second_request before installGuards at :147 and guard calls at :148-152.
The tests at :119-132 expect prohibited_api, not binding.

This is a definite static contradiction in the intended path. It explains why
these tests cannot exercise their designated guard as written; the retained
parent-method failures alone do not establish each executed subcase's stage.
Duplicate and collision genuinely require second-envelope binding; that check
must remain when any future correction is authorized.

### F3 — Byte canonicalization and the control-character oracle disagree

adapter.py:38-39 uses json.dumps(...,ensure_ascii=True). Test :27 expects literal
DEL (U+007F) in the resulting bytes; the fixtures also contain DEL (:14).
The installed Python 3.9 json/encoder.py:19,48-71 ASCII encoder escapes characters
outside space through tilde, including DEL, through a Unicode escape. The worker
uses JSON.stringify at :52-54 without a matching DEL-escape normalization.
The Python test oracle and Python encoding rule are inconsistent; a cross-language
fixture incompatibility also requires resolution before successful acceptance.

The Python source has a native _json accelerator selection (:5-8,70-71); that
native implementation and JavaScript JSON.stringify were not executed or newly
verified here. The mismatch is source-supported, not a new measured byte result.
Agree one canonical byte contract, then align both languages and the test oracle;
do not simply weaken hash verification. ASCII-only validation remains required.

### F4 — Wrong-hash fake cannot reach the wrong-hash predicate

tests :137-140 emits ok/networkAttempts/first but omits canonicalFixtures.
adapter.py:126-128 checks canonicalFixtures before cross_language_verification.
If the fake completes and its response is parsed, it is rejected as canonicalization
before the intentionally wrong hash is examined. This is a definite ordered
predicate/test-fixture contradiction. A later correction should make all earlier
response predicates valid while retaining the deliberately incorrect hash.

### F5 — Timeout fake does not establish a live timeout condition

tests :146-149 uses an unresolved top-level await after its release marker.
The fake adds no ongoing timer/I/O handle at that point. It does not independently
prove the process stays alive until the adapter's deadline. Early Node termination
on an unsettled top-level await is a runtime hypothesis, not reproduced here.
The asserted worker_timeout may instead be preempted by worker exit. A future
test must deliberately keep a bounded handle live and verify termination/cleanup;
no such change or execution is authorized by this report.

### F6 — Error-stage loss is possible, but the actual lost stages are unknown

worker.mjs:193-197 derives unguarded stages from arbitrary error.message prefixes.
adapter.py:110-113,119-122 passes any string through to CompositionError.stage;
diagnostic_tests.py:46-49 accepts only its fixed STAGES set (:14). A loader/error
prefix outside that set therefore becomes unknown. This explains a possible loss
mechanism, not the actual source value for the two recorded CompositionErrors.
F1 is a candidate trigger. No evidence supports widening the allowlist to raw
messages. Prefer fixed, non-secret worker stage categories in a later reviewed
correction, retaining unknown for genuinely unclassified failures.

## All nine recorded failing/error methods

Names below are under tests.test_m02_was_composition. These are parent methods;
the retained artifact does not identify individual parameterised cases.

| Method | Recorded outcome | Source path and present conclusion |
|---|---|---|
| AuthorizedCompositionTests.test_successful_write_read_and_hash | error | tests:105-108 -> adapter:77-131 -> worker:133-190; F1 leading hypothesis; no successful storage evidence |
| AuthorizedCompositionTests.test_duplicate_is_idempotent_in_one_worker | error | tests:109-111; same resolver before backend/second write; F1 leading hypothesis |
| AuthorizedCompositionTests.test_changed_content_collision_has_named_stage | failure | tests:112-115; resolver precedes writeAndRead:110-130 and second call:185; expected collision can be preempted; actual stage unknown |
| AuthorizedCompositionTests.test_was_named_child_process_binding_is_guarded | failure | tests:119-122; F2 binding preempts loader/quota/execFile guard |
| AuthorizedCompositionTests.test_dns_and_network_guards_intercept_before_system_call | failure | tests:123-127; F2 preempts direct guarded calls |
| AuthorizedCompositionTests.test_worker_thread_spawn_and_exec_guards | failure | tests:128-132; F2 preempts direct guarded calls |
| AuthorizedCompositionTests.test_mismatched_hash_fails_cross_language_verification | failure | tests:137-140; F4 earlier fixture predicate preempts target hash predicate |
| AuthorizedCompositionTests.test_timeout_is_named_and_temp_root_is_removed | failure | tests:146-149; F5 unresolved await/liveness hypothesis; actual exception stage unknown |
| CanonicalEnvelopeTests.test_control_characters | failure | tests:27; F3 byte-oracle contradiction; no new execution |

## Backend/API, boundary and semantic audit

Public src/index.ts:17 and dist/index.js export FileSystemBackend. Worker options
at :175-177 match filesystem.ts:278-310. writeSpace, writeCollection,
writeResource and getResource parameter shapes at filesystem.ts:909-917,
1624-1640,2181-2201,2729-2748 match the worker's calls. Binary application/json
storage matches the backend binary path at :2477-2538. Resource readback provides
stream/type/version at :2784-2794, matching worker checks :124-130. These are
source compatibility checks, not a successful write/read.

The worker's duplicate path catches PreconditionFailedError by constructor name;
WAS exports the named class in errors.ts:404 and evaluates conditional-write
preconditions before resource writing at filesystem.ts:2328-2338. Collision is
checked by comparing stored bytes after a precondition rejection (:120-129).
These paths remain unmeasured because earlier failure can preempt them.

Normal backend options do not set capacityBytes. guard_child sets it to 1;
the backend quota path can call disk-usage execFileAsync('du',...) at
filesystem.ts:355-376. Child-process guards and syncBuiltinESMExports occur
before dynamic WAS import (worker:81-97,147,174), so the intended order is sound,
but F2 prevents this guard test reaching that path. No guard is proven by a
source substring test. Upstream dependency initialization has not been exhaustively
audited and no runtime safety guarantee follows from these source checks.

dataRoot is created by the adapter under a fresh temporary root (:88-90), and
checked outside packageRoot and empty by worker:153-156. Module symlinks are
created only after release and removed in finally (:164-190); adapter removes
the whole temporary root (:135-144). No persistent upstream edit is needed to
investigate these SOGA-side issues. Controller pre/postflight and listener
observation remain intact; their earlier successful cleanup is accepted evidence,
not a fresh measurement from this research.

The focused tests fabricate result dictionaries (tests:11-17), then construct a
storage evidence envelope. Neither the focused test nor composition imports
m02_person_server. This package does not demonstrate a live Person Server call,
wallet presentation, identity verification or authorization-token issuance.
Fixing this package could establish an evidence-envelope/storage round-trip,
not full Freewallet/AAuth interoperability. That broader direction is preserved.

## Recommended next bounded step and remaining uncertainty

Prepare one create-only SOGA correction proposal covering public ESM package-root
resolution, guard-mode binding, one shared canonical byte contract, negative-test
fixtures, a live bounded timeout fixture, and fixed redacted stage categories.
Audit related paths together, not one piecemeal patch per recorded failure.
Do not alter upstream source/dependencies or discard process/network guards.
Both eligible blind reviewers must read all created executable/test files before
any later separately authorized bounded run. One later run should retain fixed
stage information and prove both positive round-trips and negative controls.

No claim is made that these corrections are sufficient or that F1/F5 were the
recorded causes. Any required Node/builtin/dependency behavior not verified from
local source remains an explicit runtime verification obligation. No unavailable
source was fetched and no execution was used to fill a knowledge gap. This report
does not attribute the historical D-067 failure or authorize any correction/run.

## Reproducible inspection record and source hashes

Read-only commands used: git rev-parse HEAD and git status --short in SOGA;
git -C <fixed WAS root> rev-parse HEAD HEAD^{tree} and status --porcelain
--untracked-files=no; nl -ba of adapter.py, worker.mjs, diagnostic_tests.py,
tests/test_m02_was_composition.py and controller.py; cat __init__.py;
cat WAS package.json; nl -ba WAS src/index.ts; sed -n '1,100p' dist/index.js;
rg for FileSystemBackend/execFile/capacityBytes/constructor/writeSpace/
writeCollection/writeResource/getResource/PreconditionFailed/export and
normalizeCapacityBytes in the relevant WAS sources; rg --files on the installed
Python json directory; nl -ba encoder.py at lines 1-80 and 185-207;
nl -ba filesystem.ts at the cited ranges and errors.ts at 1-65;
ls -ld of the retained diagnostic root; shasum -a 256 on the following files
and retained record. No denied operation occurred. Commands only inspected
local text/metadata. Source inspection has no package or runtime side effects.

SHA-256 (paths relative to SOGA unless prefixed WAS or Python):

- adapter.py: `9b1407c61303ae2c761ae3ecbd11b88256e779338de65d4083789bf232db15ad`
- worker.mjs: `ab3dda127a499452503ebff30bd93d13233dac27a49d10f2b9fc4f1dc177c9ec`
- controller.py: `559a9397e610a7f60cdf34db1b96874ad60509d609a069e2c0bf2e5b78727f2e`
- diagnostic_tests.py: `26396fa08b02a1971276604bfa7f474ff055c14a88e25075286c6576e59c3b1a`
- __init__.py: `62e10c1f9bee9b3f27d1f0acb17f71a34ea89fcf30e39f93b83bb620de3d5f97`
- tests/test_m02_was_composition.py: `8c03c698294c082e07d41a4317bf3b38066b95618090ca65e1f2023ad2001539`
- WAS package.json: `b6411c4ad70842c1bbdeda5bf4c71bc9fc743fb91fe7a62bc8f3f0bffc40b44a`
- WAS src/index.ts: `edf48731962605a3394d5dd8e496f863208a1ca377e599ac1ed2692cdd4f502b`
- WAS dist/index.js: `5971f94b09cb7784f5ced803a642a92a419fdb5c3967179837ae721025dac905`
- WAS src/backends/filesystem.ts: `a2bece3bde8d652d57b4eeb8cbd6675c59ee776c9ae3520e54872d16f805b1f5`
- WAS src/errors.ts: `0a922416fa1e7a5e5e802081732b087a8ffcc9923ff76e81204961e16ac30b9c`
- Python /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/encoder.py: `cdb1eb54c453f672c56caf00c02ace80c97fb48121c4af734b7c4123ceb1fb3d`

The first five basenames in this hash list live under m02_was_composition/.
The unrelated PI routine-tool proposal remains unread and untouched. No report
adoption, canonical milestone change, commit/push, repair or new execution has
been authorized. D-074 is an uncommitted direct-authorization record.
