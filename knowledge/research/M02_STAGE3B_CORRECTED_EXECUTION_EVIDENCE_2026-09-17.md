# M02 Stage 3B — Corrected bounded execution evidence

Date: 2026-09-17
Status: EXECUTED POSITIVE RESULT — BLIND DUAL EVIDENCE REVIEW AND PI ACCEPTANCE PENDING
Author/integrator: Codex
Execution authority: D-079, committed prospectively at
742ed046af7f50052423862dba187998b18546a6 (local main = origin/main).
Both request-047 proposal and request-048 complete runner/addendum reviewers
returned blind independent PASS before execution. No retrospective script review.

## Claim and outcome

Nine synthetic instrumentation tests passed once. The conditional diagnostic
controller then ran once and retained 34 focused test successes, zero failure,
error or skip, no truncation, successful execution and postflight. Both outer
steps completed within bounds with status0, reaped=true and drained=true.
No automatic retry, code repair or additional test invocation occurred.

The positive claim is synthetic Person Server result evidence storage/readback
through this exact socket-free WAS filesystem backend, including tested
idempotency, collision, byte agreement and negative/guard contracts.
No live Person Server process or token flow, Freewallet interaction, wallet
presentation, payment, participant session or AAuth conformance was demonstrated.
The consumed prior negative runs remain negative; no cause is retroactively proven.

## Exact source and candidate prerequisites

Seven executed source SHA-256 pins, verified before and after:
- runner: c8ab204f84c7c976a117eb28b2ef70cb806d3719199aae3b57c0f68a6171ae3a
- adapter.py: 28bcbaeda80c7436353e6872e3fa2f35390e4089ae1ea7d5c64ced93afe071e7
- worker.mjs: f3f58b1d603228c057d9a5af99045cd5783ea5a92ffaa0e550fc0cc1ce2d5b60
- diagnostic_tests.py: 794a1b961d976abeaad044221e031358922016e9817c891e2403663337719403
- controller.py: 559a9397e610a7f60cdf34db1b96874ad60509d609a069e2c0bf2e5b78727f2e
- tests/test_m02_was_composition.py: 9855fa34dab466314462b9cf4dbe1220e05a521678481d72a5768134d912922f
- tests/test_m02_was_diagnostics.py: 2b15758936df7f95af9f40836f949bcca87ec86d24fbbff2cfadf10f45a4f903

Preserved WAS path: /private/tmp/m02-stage3lib-20260910/was-teaching-server
Commit2090a606f2723e4d57ef0090db55fd1bdab9427e;
tree540d85cea6cc7ab50ee6f00b0dead2084c1d65de; tracked source clean.
298-file dist manifest matched before and after:
7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586.
dist/build-info.json absent. Conditional provenance rests on accepted restoration
evidence, not completed upstream build. No dependency/build operation occurred.
Runtime observations: /usr/bin/python3 Python3.9.6;
pinned /opt/homebrew/Cellar/node/26.7.0/bin/node v26.7.0.

## Commands and permission context

cwd: /Users/debb/dev/soga-clean.
Both steps executed outside the default agent sandbox with explicit platform
approval; no persistent configuration/permission change.

Exact launcher argv (shown as shell notation):
```
/usr/bin/env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin LANG=C LC_ALL=C PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 tools/m02_was_composition_execution.py --step synthetic --head 742ed046af7f50052423862dba187998b18546a6
/usr/bin/env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin LANG=C LC_ALL=C PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 tools/m02_was_composition_execution.py --step diagnostic --head 742ed046af7f50052423862dba187998b18546a6
```

Exact child argv:
```
['/usr/bin/python3', '-m', 'unittest', 'tests.test_m02_was_diagnostics.DiagnosticInstrumentationTests', '-v']
['/usr/bin/python3', '-c', "import json; from pathlib import Path; from m02_was_composition.controller import run_diagnostic_once; print(json.dumps(run_diagnostic_once(expected_soga_head='742ed046af7f50052423862dba187998b18546a6', evidence_root=Path('/private/tmp/m02-stage3b-diagnostics-20260917-001')), sort_keys=True))"]
```

Child environment contained only PATH, LANG, LC_ALL and
PYTHONDONTWRITEBYTECODE=1 as shown above. Diagnostic focused child additionally
sets M02_STAGE3B_EXECUTE=1 in the unchanged controller.

Pre-use commands: shasum -a 256 on the seven files; git rev-parse HEAD origin/main;
git status --short; git -C WAS rev-parse HEAD HEAD^{tree}; git -C WAS status
--porcelain --untracked-files=no; both exact runtime --version commands.
A local Python stdlib pathlib/hashlib script regenerated the same sorted
manifest rows as controller._manifest, enumerated diagnostic/worker roots and
checked absent new evidence/marker roots. No candidate import in that inspection.
Unprivileged lsof -nP -a -u debb -iTCP -sTCP:LISTEN captured baseline.
Initial /bin/ps inventory was sandbox-denied; the same read-only inventory was
then approved outside sandbox. It found only its own inventory shell/rg matches,
not a controller/test/worker. No attempt was begun on that denial.

After synthetic success, the scoped diagnostic-root inventory matched the sole
retained old root exactly. A local pathlib script used mkdir(mode=0o700) on the
absent new evidence path without exist_ok, then observed0700. The runner reserved
synthetic.attempt and diagnostic.attempt exclusively; both retained0600 under0700
marker root. No path was reused or overwritten.

## Outer and inner observations

Synthetic outer summary:
```json
{"drained":true,"elapsed_ms":1239,"ok":true,"outer":"completed","reaped":true,"status":0,"stderr_bytes":1207,"stderr_s256":"061540694216c14aeb54484cdcdbbeb86b6a39c1a32e222b923e7ef05cdc0369","stdout_bytes":0,"stdout_s256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","step":"synthetic","tests_run":9}
```

Diagnostic outer summary:
```json
{"controller_ok":true,"drained":true,"elapsed_ms":5528,"ok":true,"outer":"completed","reaped":true,"status":0,"stderr_bytes":0,"stderr_s256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_bytes":145,"stdout_s256":"a7b6074249e22adffb3a2556e286d57b343d14cb78960fedda90f8c0939388ac","step":"diagnostic"}
```

Reviewed outer60/240-second deadlines, 65536-byte per-stream caps and finite
TERM/KILL/wait/drain grace remained unchanged; no timeout, overflow or read error
was reported. Timings include shutdown grace, not just child execution.
Controller focused ceiling180seconds, worker ceiling10seconds and invocation
ceiling24 were unchanged. Static prediction23 adapter.store calls/18 spawns is
NOT an independently measured runtime count: no counter telemetry is retained.
Passing guard tests deliberately exercise intercepted prohibited API attempts;
this is not a claim that no interception attempt occurred. No permitted
application external-network access or HTTP service/listener startup occurred.
Guards are process-local, not OS containment or an exhaustive dependency audit.

The success records carry stage unknown because success has no error stage;
this is not the earlier failure-stage loss. identifier/holdpoint error categories
were not deliberately induced, as specified before execution.

## Primary artifact and independent cleanup

Retained /private/tmp/m02-stage3b-diagnostics-20260917-001/record.json:
6337bytes,0600, SHA-256
a85b1e3d676e3fd72c882e5773df6057c44e993a0da8362d60ba2f0a08ff13a6.
Evidence root0700. The complete redacted record is transcribed below for durability.

Independent post-run inspections, separate from controller self-report:
- local stdlib pathlib/hashlib inspection: no worker/fake/module temporary roots,
  no __pycache__ beneath composition/tests/tools, unchanged 298-file manifest;
- git status --short unchanged (only excluded PI proposal), WAS tracked-clean;
- user-visible lsof listener inventory identical to baseline;
- approved /bin/ps -axo pid,ppid,command filtered for composition/worker/fake
  names: only inspection shell/rg, no surviving scoped processes.

Baseline and post-run listeners: rapportd408 port52889 IPv4/IPv6;
ControlCe478 ports7000/5000 IPv4/IPv6; agy4040 loopback51897/51898;
Dropbox56872 loopback17600/17603; DropboxFi56884 port17500.
This is scoped user-visible evidence, not host-wide network absence proof.
Focused child has a separate session; outer reaped alone was not treated as
descendant cleanup proof. No cleanup repair or additional cross-group signals.

Old diagnostics record SHA-256 remained
7cab14762d0189e7f78f82848ac512d6b3c24a2921bacba7edf6995bd3916ceb.
Retain old/new diagnostics and marker roots unchanged pending PI disposition.
Temporary storage is non-durable; this report carries the record.
No Misty access, physical action, Freewallet, live Person Server execution,
personal data, payment, G28 or G29.

## Complete retained redacted record
```json
{"controller_stage":"none","diagnostic":{"counts":{"error":0,"failure":0,"skip":0},"exit_status":0,"records":[{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_adapter_pins_runtime_and_bounds_streaming_output"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_controller_has_observation_and_cleanup_gates"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_controller_regenerates_manifest_and_checks_identity"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_observer_is_mandatory_before_worker"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_public_loader_identity_and_redacted_stages_are_explicit"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_rejects_mode_and_second_binding_before_worker"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_storage_projection_cannot_carry_governance_semantics"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_worker_failure_stage_is_preserved"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_worker_source_has_guards_holdpoint_and_no_listener"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_changed_content_collision_has_named_stage"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_cleanup_failure_is_named_and_chains_primary"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_dns_and_network_guards_intercept_before_system_call"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_duplicate_is_idempotent_in_one_worker"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_fixed_loading_failure_stages_survive_adapter"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_malformed_nonzero_and_excess_output_have_named_stages"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_mismatched_hash_fails_cross_language_verification"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_oversized_worker_input_fails_before_spawn"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_successful_write_read_and_hash"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_timeout_is_named_and_temp_root_is_removed"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_unsupported_interpretation_fails_at_binding"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_was_named_child_process_binding_is_guarded"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_worker_thread_spawn_and_exec_guards"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_bool_integer_and_key_order"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_control_characters"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_invalid_issuer_and_correlation_fail"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_numeric_looking_keys_are_lexically_sorted"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_projection_is_non_secret_and_bounded"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_rejects_float_non_ascii_unsafe_integer_and_non_plain_type"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_unknown_secret_and_bad_authority_fail_closed"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_wrong_bindings_fail_at_binding"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.ControllerNegativeTests.test_controller_detects_leftover_temporary_path"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.ControllerNegativeTests.test_manifest_count_and_hash_fail_closed"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.ControllerNegativeTests.test_was_identity_runtime_and_candidate_fail_closed"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.ControllerNegativeTests.test_wrong_soga_head_fails_preflight"}],"schema":1,"tests_run":34,"truncated":false},"elapsed_ms":4428,"execution":"success","expected_target":"742ed046af7f50052423862dba187998b18546a6","postflight":"success","schema":1,"stderr_s256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_s256":"fe27e7073da6c590ebab4a454fc7f7f0f8bdf612065b364b3046d07601680387","subprocess_status":0}
```

## Next holdpoint

The D-079 attempts are consumed. Both blind gates must verify this evidence and
exact post-run artifacts before PI acceptance. No rerun, source change or next
integration stage is authorized. The unrelated PI proposal stays untouched.
