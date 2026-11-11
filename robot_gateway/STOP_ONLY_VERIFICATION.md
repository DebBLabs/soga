# Misty B Stop-Only Verification Instrument

This package is a diagnostic instrument for one bounded idle
`POST /api/tts/stop` request to the PI-selected Misty B. It is separate from
the public Flow A demonstration and the accepted invitation gateway.

The physical runner has no synthetic mode. The synthetic controller has no
physical mode. Neither public mode nor participant input can invoke either.

The instrument can establish only the exact HTTP response observed under the
recorded local conditions. It does not establish physical stillness, Misty
safety, speech behavior, completion-event transport, runtime tick driving,
restart persistence, invitation behavior, mBot2 behavior or complete AAuth
conformance.

Physical use requires a separately reviewed external request, prospective PI
authority, a fresh manual preflight and Deb physically beside Misty with access
to the base power switch. No retry is automatic.

## External records

Despite the `.md` suffixes retained by the reviewed paths, the request and
authority records are strict JSON objects. Duplicate keys, unknown keys and
wrong JSON types are refused. Times are RFC 3339 strings with an explicit UTC
offset.

The physical execution request pins: `schema`, exact `soga_head` and
`presentation_head`, the six-entry `package_sha256` object, `manifest_sha256`,
the exact four external paths (`physical_request_path`,
`physical_authority_path`, `physical_preflight_path`,
`physical_evidence_directory`), `physical_preflight_schema`,
`physical_preflight_max_age_seconds`, accepted synthetic evidence hashes, and
the exact argument-free command array.
Its schema value is `iiw-misty-stop-only-physical-request-v1` and its
`accepted_synthetic_evidence_sha256` object contains exactly the absolute
`evidence.json`, `stdout.bin`, and `stderr.bin` paths beneath the accepted
synthetic evidence directory.

The prospective authority contains exactly: `schema`, `request_sha256`,
`authorized_by`, `authorized_at`, `automatic_retry` (false), and
`physical_capability` (`stop_only`).
Its schema is `iiw-misty-stop-only-physical-authority-v1`; `authorized_by` is
`Deb`, `automatic_retry` is JSON `false`, and `authorized_at` is a non-future
RFC 3339 timestamp with an explicit offset.

The preflight contains exactly: `schema`, individually labelled and timestamped
observations, `confirmed_by` (`Deb`), `platform_id`, `serial`, `config`,
`misty_mac`, `misty_ip`, `laptop_interface`, `laptop_ip`,
`associated_client_count`, `beryl_exact_clients`, and strict booleans for the
reviewed idle, power-switch, placement, router, local-permission and competing-
controller holdpoints. Every observation must be no more than five minutes old
and none may be in the future.

The preflight schema is `iiw-misty-stop-only-physical-preflight-v1`. Its exact
non-time keys are `confirmed_by`, `platform_id`, `serial`, `config`,
`misty_mac`, `misty_ip`, `laptop_interface`, `laptop_ip`,
`associated_client_count`, `beryl_exact_clients`, `sole_powered_misty`,
`misty_idle`, `misty_not_speaking`, `misty_not_visibly_moving`,
`power_switch_touched_and_reachable`, `stable_on_dock_or_foam_block`,
`remote_admin_disabled`, `port_forwarding_disabled`,
`local_network_permission_confirmed`, `public_demo_closed`, `rehearsal_closed`,
`misty_studio_closed`, and `other_robot_controller_closed`. The
`observation_times` object contains exactly `serial_config_identity`,
`complete_beryl_inventory`, `misty_idle_state`, `power_switch_access`,
`stable_placement`, `router_controls`, `local_network_permission`, and
`competing_controllers_closed`.

Any later operator attestation is a separate strict JSON record. It may record
only the observed physical outcome, observer, UTC time, and the accepted
physical-evidence SHA-256. HTTP acknowledgement alone never establishes
physical stillness or successful robot behavior.

The synthetic evidence and its acceptance report remain external under
`/Users/debb/dev/research-evidence/soga/` through the physical stop-only stage.
No synthetic report is added beneath `knowledge/` during that interval. The
six package paths plus `knowledge/strategy/DECISION_LOG.md` and
`knowledge/working/CURRENT_STATE.md` are permitted from the package basis
through physical execution. The only additional paths permitted are:

- `knowledge/proposals/IIW_MBOT2_CYBERPI_PROTOCOL_VERIFICATION_PROPOSAL_2026-11-05.md`
- `robot_gateway/cyberpi_f3f4_protocol.py`
- `robot_gateway/CYBERPI_PROTOCOL_VERIFICATION.md`
- `tests/test_robot_gateway_cyberpi_protocol.py`
- `tools/robot_gateway/run_cyberpi_protocol_tests.py`
- `tools/robot_gateway/cyberpi-protocol-runtime-manifest.json`
- `knowledge/proposals/MBOT2_FIRST_PROTOCOL_OBSERVATION_R2_2026-11-09.md`
- `knowledge/proposals/TWO_ROBOT_SWITCHING_RUNTIME_R2_2026-11-09.md`
- `robot_gateway/CYBERPI_NONE_OBSERVATION.md`
- `robot_gateway/OPERATOR_RUNTIME.md`
- `robot_gateway/SWITCHING_REVIEW.md`
- `robot_gateway/cyberpi_none_observation.py`
- `robot_gateway/operator_runtime.py`
- `robot_gateway/owned_gateway.py`
- `robot_gateway/switching.py`
- `tests/test_robot_gateway_cyberpi_none_observation.py`
- `tests/test_robot_gateway_operator_runtime.py`
- `tests/test_switching.py`
- `tools/robot_gateway/cyberpi-none-runtime-manifest.json`
- `tools/robot_gateway/operator-runtime-manifest.json`
- `tools/robot_gateway/run_cyberpi_none_physical.py`
- `tools/robot_gateway/run_cyberpi_none_synthetic.py`
- `tools/robot_gateway/run_operator_runtime_synthetic.py`

Each additional path must appear as an addition in the cumulative diff
relative to the pinned basis. Both controllers disable rename detection.
The exact status, protected hashes, and physical request HEAD checks still
apply. The presentation repository remains frozen at its pinned basis.

Representative shapes (placeholder hashes/times are not authority):

```json
{"schema":"iiw-misty-stop-only-physical-authority-v1","request_sha256":"<64 hex>","authorized_by":"Deb","authorized_at":"2026-11-03T12:00:00-05:00","automatic_retry":false,"physical_capability":"stop_only"}
```

```json
{"schema":"iiw-misty-stop-only-physical-preflight-v1","observation_times":{"serial_config_identity":"<RFC3339>","complete_beryl_inventory":"<RFC3339>","misty_idle_state":"<RFC3339>","power_switch_access":"<RFC3339>","stable_placement":"<RFC3339>","router_controls":"<RFC3339>","local_network_permission":"<RFC3339>","competing_controllers_closed":"<RFC3339>"},"confirmed_by":"Deb","platform_id":"urn:debblabs:misty-b:20193802932","serial":"20193802932","config":"010-000002","misty_mac":"00:D0:CA:00:96:C3","misty_ip":"192.168.8.219","laptop_interface":"en0","laptop_ip":"192.168.8.247","associated_client_count":2,"beryl_exact_clients":["00:D0:CA:00:96:C3","laptop"],"sole_powered_misty":true,"misty_idle":true,"misty_not_speaking":true,"misty_not_visibly_moving":true,"power_switch_touched_and_reachable":true,"stable_on_dock_or_foam_block":true,"remote_admin_disabled":true,"port_forwarding_disabled":true,"local_network_permission_confirmed":true,"public_demo_closed":true,"rehearsal_closed":true,"misty_studio_closed":true,"other_robot_controller_closed":true}
```

## Verification traceability

The synthetic controller expects 56 tests.

- Tests 01–18 and 22–34 cover request identity, socket binding, delivery,
  deadlines, HTTP framing, acknowledgement classification and bounded failures.
- Tests 19–21, 42–43 cover mode separation, distinct evidence locations and the
  absence of public-demo invocation.
- Tests 35–36 cover direct on-link and forbidden gateway route fixtures.
- Tests 37, 40, 48 and 51 cover the synthetic audit policy, bounded controller
  success and failure evidence.
- Tests 41, 44–47 cover readiness, strict time/record validation, consumed
  physical evidence, and preservation of the original probe result when a
  postcondition fails.
- Test 45 also covers stale and future preflight times and refusals for
  mismatched authority, package, runner, command, and synthetic evidence.
- Tests 49–50 cover repository-basis/status and complete protected-hash maps,
  including accepted CyberPi additions and rejected unrelated paths, deletions,
  status changes and HEAD mismatches.
- Tests 52–55 cover mocked interface and listener refusals, readiness rechecks
  and existing evidence refusal before directory creation, invocation and
  environment refusal before record reads, and synthetic immutability failure
  with evidence retained.

The narrow parser deliberately validates HTTP version, header names, framing,
chunk termination and bounds more strictly than the frozen accepted transport.
The accepted transport remains byte-identical in this stage; its parser finding
must be resolved before any Speak execution.
