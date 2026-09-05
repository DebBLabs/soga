# M01 Non-Physical Implementation Evidence

Date: 2026-09-05  
Implementer: Codex/CG  
Authority: D-029 Mission Authorization  
Base checkpoint: `72198598a84dfe178b39a783d3fa09acd34f337d`  
Status: READY FOR INDEPENDENT IMPLEMENTATION REVIEW

## Implemented boundary

The new `m01_qr` package instantiates the authorized native AAuth mission and
provides a bounded local flow:

`opaque QR grant reference → atomic grant consumption → bounded session →
AAuth PermissionService → SOGA runtime governance → canonical decision
reference → existing target-bound recording adapter`

There is no HTTP client, external URL, robot endpoint, network discovery,
physical adapter, or actuation code in `m01_qr`.

## Authorized mission

- Approver: `urn:debblabs:person-server:deb-bucci`
- Agent: `soga-m01-misty-a-qr-agent-v1`
- Approved at: `2026-09-05T18:26:42Z`
- Sole approved action: `m01.signal_light`
- Catalog: `m01-c1-v1`
- Native mission `s256`: `0D5MnDyq0C9MmCcqEy51WuN_PwLks0t7ky8XZCh928I`

The approver represents the explicitly adopted local test fixture; it is not a
claim that a production Person Server exists.

## Subject and policy representation

The local request represents the scanner as
`m01-anonymous-participant-session` with `identity_status: UNKNOWN` and
`age_status: UNKNOWN`. `subject_agency_state: INDEPENDENT` is the existing SOGA
agency-state input for this bounded session; it is not a claim that identity,
age, competence, or broader authority has been verified. D-023 §1 explicitly
permits the bounded interaction and selected low-risk action without identity
or age evidence. No identity- or age-dependent action is authorized.

The mission policy supplied to the existing SOGA bridge is intentionally empty
apart from the mission hash that `PermissionService` binds into it. The current
`m01.signal_light` request reaches `ALLOW` because all existing governance
dimensions pass and no adopted M01-specific restriction applies—not because a
new permissive rule or bypass was added. Any future catalog action requires a
new reviewed mission/policy disposition and cannot inherit this result by
analogy.

## Positive evidence

The focused test verifies that one opaque grant is consumed into one bounded
session, the authorized action is evaluated through the existing SOGA/AAuth
path, the canonical SOGA execution-receipt reference is carried into the
recording invocation, exactly one target-bound recording occurs, and physical
outcome remains `unknown`.

## Negative evidence

The focused suite verifies:

- unauthorized action rejection before grant consumption;
- invalid QR rejection without session creation or dispatch;
- QR payload exclusion of action, platform, URL, and network address;
- grant replay rejection without a second session or dispatch;
- safety latch precedence without grant consumption or dispatch; and
- deterministic native mission construction with exactly one approved action.
- explicit identity-unknown and age-unknown subject context plus the intended
  mission-hash-only policy input in the recorded SOGA envelope.

Existing G27 regression tests continue covering wrong platform, missing target,
decision-binding conflict, stale and late decisions, concurrency, expiry,
terminal non-revival, safety races, and unknown physical outcome.

## Test results

- M01 focused suite: **7/7 PASS**
- Full repository suite: **79/79 PASS**
- The full suite was rerun with permission for temporary localhost-only sockets;
  no Misty or external-network access occurred.

## Files in review scope

- `m01_qr/__init__.py`
- `m01_qr/mission.py`
- `m01_qr/flow.py`
- `tests/test_m01_qr.py`
- `knowledge/proposals/M01_MISSION_AUTHORIZATION_2026-09-05.md`
- `knowledge/proposals/M01_IMPLEMENTATION_EVIDENCE_2026-09-05.md`
- `knowledge/strategy/DECISION_LOG.md`
- `knowledge/working/CURRENT_STATE.md`

## Known limitations and nonclaims

- State is process-local and memory-only.
- The QR representation is an opaque payload string; no rendered QR image or
  participant web UI is implemented.
- The local Person Server boundary is a test fixture, not production identity,
  authentication, persistence, or wallet integration.
- The recording adapter proves receipt only and reports physical outcome
  `unknown`.
- No Misty platform identifier, address, physical condition, endpoint behavior,
  LED parameters, neutral behavior, network isolation, or operator stop has
  been verified by this implementation.
- This evidence does not authorize or establish physical connection or
  execution readiness.
