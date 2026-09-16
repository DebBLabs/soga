# M02 Stage 3B diagnostic execution evidence

Date: 2026-09-16
Status: EXECUTED NEGATIVE RESULT — PENDING BLIND DUAL REVIEW AND PI ACCEPTANCE
Authority: D-072, recorded and pushed before either test process began.
Execution HEAD: `02e703e7d865bef482fae94b5a4070ae4dea5679` (local and origin/main matched).

## Exact inputs and permission context

Controller SHA-256: `559a9397e610a7f60cdf34db1b96874ad60509d609a069e2c0bf2e5b78727f2e`.
Runner SHA-256: `26396fa08b02a1971276604bfa7f474ff055c14a88e25075286c6576e59c3b1a`.
Synthetic tests SHA-256: `e468530de98b29b8849c8ef92668c095d031b13a11a097430381ca50d6120c49`.
Execution proposal SHA-256: `caa80928e45916a2a7ce0c66e43e187fa96ee7c1a3d549a0af5fd1207780d114`.
WAS commit `2090a606f2723e4d57ef0090db55fd1bdab9427e`, tree `540d85cea6cc7ab50ee6f00b0dead2084c1d65de`; tracked source clean.
Before execution, the exact 298-file dist manifest matched `7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586`.
Python 3.9.6 and pinned Node v26.7.0 verified. No build or installation occurred.

Explicit platform approval allowed execution outside the default sandbox.
Both children received only PATH=/usr/bin:/bin:/usr/sbin:/sbin, LANG=C,
LC_ALL=C, PYTHONDONTWRITEBYTECODE=1. Reviewed process-local network guards
are not an OS-level containment guarantee.

## Commands, limits, and observed results

From /Users/debb/dev/soga-clean, a standard-library Python supervisor launched
these exact argv lists with stdin DEVNULL, separate captured streams and
start_new_session=True:

1. `/usr/bin/python3 -m unittest tests.test_m02_was_diagnostics.DiagnosticInstrumentationTests -v`
2. `/usr/bin/python3 -c 'import json; from pathlib import Path; from m02_was_composition.controller import run_diagnostic_once; print(json.dumps(run_diagnostic_once(expected_soga_head="02e703e7d865bef482fae94b5a4070ae4dea5679", evidence_root=Path("/private/tmp/m02-stage3b-diagnostics-20260916-001")), sort_keys=True))'`

Supervisor deadlines were 60 and 240 seconds respectively, with 64 KiB per-stream
caps, threaded drains, process-group TERM followed by KILL after one second,
wait/drain completion checks. Both exited zero without timeout or overflow.
Supervisor elapsed times including termination grace: 1239 ms and 2910 ms.
The controller retained its own reviewed inner limits.

Step 1: seven synthetic instrumentation tests passed (unittest reported 0.010s).
Only the specified class ran; no standalone SyntheticCase helper execution.
After that check, no m02-stage3b-diagnostics-* path existed. The designated
fresh root was created empty at mode 0700; no existing root was reused/deleted.

Step 2: controller returned ok=false, execution=focused_tests,
postflight=success. Diagnostic child status was 1; 31 tests ran,
seven failures, two errors, zero skips. Controller elapsed time was 1783 ms.
All failing/error stages were unknown. The artifact identifies test methods,
not causes or parameterised subcases. This does not establish the cause of the
historical D-067 failure or demonstrate successful WAS/Person Server composition.
The single diagnostic attempt is consumed; no retry or repair occurred.

## Artifact and independent cleanup observations

Retained primary artifact: /private/tmp/m02-stage3b-diagnostics-20260916-001/record.json.
Observed mode 0600, size 5901 bytes; SHA-256
`7cab14762d0189e7f78f82848ac512d6b3c24a2921bacba7edf6995bd3916ceb`.
The diagnostic directory is retained pending PI disposition.

Before writing this report, git status showed only the unrelated untracked PI
routine-tool proposal, which remained unread and untouched. WAS tracked source
remained clean. Controller postflight compared repository state, dist manifest,
and user-visible TCP listeners against preflight and reported success.
Independent find found no worker/fake-worker/module temporary roots.
Initial sandboxed ps inventory was denied; escalated read-only ps succeeded and
showed only the inventory shell and its rg process, no matching surviving worker
or diagnostic child. This is scoped observation, not whole-host proof.

No listener/service startup, dependency operation, repair, Freewallet integration,
Misty access, physical actuation, G28, or G29 was authorized or performed.
No raw focused traceback, secret, envelope, token, or subtest value is reproduced.

## Complete retained redacted record

The following is transcribed byte-for-byte from the retained primary artifact
(excluding the Markdown fences and surrounding newline):

```json
{"controller_stage":"none","diagnostic":{"counts":{"error":2,"failure":7,"skip":0},"exit_status":1,"records":[{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_adapter_pins_runtime_and_bounds_streaming_output"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_controller_has_observation_and_cleanup_gates"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_controller_regenerates_manifest_and_checks_identity"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_observer_is_mandatory_before_worker"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_rejects_mode_and_second_binding_before_worker"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_storage_projection_cannot_carry_governance_semantics"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_worker_failure_stage_is_preserved"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AdapterContractTests.test_worker_source_has_guards_holdpoint_and_no_listener"},{"error_class":"AssertionError","outcome":"failure","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_changed_content_collision_has_named_stage"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_cleanup_failure_is_named_and_chains_primary"},{"error_class":"AssertionError","outcome":"failure","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_dns_and_network_guards_intercept_before_system_call"},{"error_class":"CompositionError","outcome":"error","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_duplicate_is_idempotent_in_one_worker"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_malformed_nonzero_and_excess_output_have_named_stages"},{"error_class":"AssertionError","outcome":"failure","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_mismatched_hash_fails_cross_language_verification"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_oversized_worker_input_fails_before_spawn"},{"error_class":"CompositionError","outcome":"error","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_successful_write_read_and_hash"},{"error_class":"AssertionError","outcome":"failure","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_timeout_is_named_and_temp_root_is_removed"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_unsupported_interpretation_fails_at_binding"},{"error_class":"AssertionError","outcome":"failure","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_was_named_child_process_binding_is_guarded"},{"error_class":"AssertionError","outcome":"failure","stage":"unknown","test":"tests.test_m02_was_composition.AuthorizedCompositionTests.test_worker_thread_spawn_and_exec_guards"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_bool_integer_and_key_order"},{"error_class":"AssertionError","outcome":"failure","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_control_characters"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_invalid_issuer_and_correlation_fail"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_projection_is_non_secret_and_bounded"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_rejects_float_non_ascii_unsafe_integer_and_non_plain_type"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_unknown_secret_and_bad_authority_fail_closed"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.CanonicalEnvelopeTests.test_wrong_bindings_fail_at_binding"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.ControllerNegativeTests.test_controller_detects_leftover_temporary_path"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.ControllerNegativeTests.test_manifest_count_and_hash_fail_closed"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.ControllerNegativeTests.test_was_identity_runtime_and_candidate_fail_closed"},{"error_class":"none","outcome":"success","stage":"unknown","test":"tests.test_m02_was_composition.ControllerNegativeTests.test_wrong_soga_head_fails_preflight"}],"schema":1,"tests_run":31,"truncated":false},"elapsed_ms":1783,"execution":"focused_tests","expected_target":"02e703e7d865bef482fae94b5a4070ae4dea5679","postflight":"success","schema":1,"stderr_s256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_s256":"9cf870c15b41a2cfd323f303a4ca8210396043a03fcaa99f8acf2a050583586f","subprocess_status":1}
```

