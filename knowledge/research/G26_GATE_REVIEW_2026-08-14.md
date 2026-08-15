# G26 Gate Review — Caregiver Approval Flow

Date: 2026-08-14
Reviewed commit: `ab2dbba5bba9cfe62f786dea6b9ba18e85910e6e` — "Implement G26 caregiver approval flow"
Branch: main. Verified `git rev-parse HEAD` == `ab2dbba5bba9cfe62f786dea6b9ba18e85910e6e`,
`git status --short` empty (working tree clean) both before and after this review.
**Inspection only — no files were modified, staged, or committed by this review.**

Checklist source: Stage Gate request supplied directly in the chat session (not a
repository artifact).

Method: for each item, the underlying code path was read and cited by file and
line. Where a test exists, it is cited additionally as corroboration, not as
the basis of the confirmation. Per the reporting rules, no item is confirmed
on a passing test alone, and any item not exercised by the test suite is
flagged as a test-coverage gap rather than inferred as behaving correctly.

Primary AAuth source cross-referenced for wire-format items: `draft-hardt-oauth-aauth-protocol-10.txt`,
retrieved and read directly earlier in this session (see
`knowledge/research/AAUTH_PERMISSION_RESPONSE_2026-08-14.md` §1 for retrieval
provenance). Re-consulted directly again for this review (Section 12.4.4,
Section 12.6.4).

---

## Confirmations

### 1. Subject state may cause RESTRICT but does not select the RESTRICT path.

**Established.** `engines/runtime_governance_engine.py:112-114`: any dimension
(including `subject_agency_state`) equal to `"REVIEW"` triggers
`decision = "RESTRICT"`. The mode itself is a separate step delegated to
`RestrictModeSelector.select()` (line 116-122), which does not use the raw
`subject_agency_state` value to pick a mode — see item 2.

### 2. Authorized policy/mission selects HOLDING.

**Established.** `engines/restrict_mode_selector.py:30-39`: when
`dimensions["subject_agency_state"] == "REVIEW"`, the mode is
`constraint["restrict_path"]`, where `constraint` comes from
`authorized_restrict_constraint(policy, action)` (`engines/restrict_policy.py:6-13`),
which reads `policy["stage_gate"]` entries keyed by `step_id == action`. The
canonical caregiver fixture declares
`"restrict_path": "HOLDING"` at `tests/fixtures/missions/caregiver_discharge_followup.json:18`,
so for this scenario the mode is sourced from the authorized policy, not
inferred from subject state. Cross-checked by
`tests/test_g26_permission.py:82-88` (`test_supervised_without_approval_remains_pending_not_granted`),
which asserts `pending["constraint"]["restrict_path"] == "HOLDING"`.

### 3. RESTRICT with no authorized path fails closed.

**Established.** `engines/restrict_mode_selector.py:40-43`: if
`authorized_restrict_constraint` returns `None`, the mode is `"fail_closed"`.
`aauth_permission/service.py:69,91-97`: `fail_closed` is explicitly excluded
from `internally_dischargeable_modes` (`mode != "fail_closed"`) and does not
match the `HOLDING` branch, so it falls to the final `else`, producing
`{"permission": "denied", "reason": ...}`. Cross-checked by
`tests/test_g26_permission.py:155-162` (`test_restrict_without_authorized_path_fails_closed`).

### 4. Canonical caregiver flow uses AAuth `requirement=approval`, not `interaction`.

**Established.** `aauth_permission/service.py:268` (`_pending_body`) hardcodes
`"requirement": "approval"`; `aauth_permission/http_server.py:69` sends
`AAuth-Requirement: requirement=approval` on every `202`. The string
`"interaction"` does not occur anywhere in `aauth_permission/` (confirmed by
direct search) — no code path in this module can emit
`requirement=interaction`. The primary source (draft -10, Section 12.4.4,
"Approval Pending") independently describes `requirement=approval` as the
value for the case "a server is obtaining approval from another party
without requiring the agent to direct a user," which matches the
implementation's administrative-approval framing and is distinct from the
user-directed `interaction` value (Section 12.4.3).

### 5. Initial deferred response conforms to AAuth -10 approval requirements.

**Established.** `aauth_permission/http_server.py:68-73` sets, on status 202:
`AAuth-Requirement: requirement=approval`, `Location: <pending_url>`,
`Retry-After: <retry_after_seconds>`, `Cache-Control: no-store`. Draft -10,
Section 12.4.4 (line 4580): "The response MUST include Location and
Retry-After." Section 12.5.2 additionally requires `Cache-Control: no-store`
(REQUIRED) for pending responses in general. `pending_id` is generated as
`f"pending-{uuid.uuid4().hex}"` (`aauth_permission/service.py:72`), an
unguessable value, and `pending_url` is the relative path `/pending/{pending_id}`
(`service.py:73`), which resolves to the same origin as the responding
server by construction (no scheme/host is emitted), matching the draft's
"Location URL MUST be on the same origin" requirement. Wire-level
cross-check: `tests/test_g26_permission.py:229-247`
(`test_http_approval_wire_and_terminal_delivery`) asserts all four headers
over a real HTTP round trip.

### 6. Pending polling is agent-bound.

**Established.** `aauth_permission/service.py:209-212` (`poll`): raises
`PermissionError` if the caller-supplied `agent` does not equal
`pending["agent"]`, which was fixed at creation time
(`service.py:80`, taken from the original permission request). Cross-checked
by `tests/test_g26_permission.py:224-227` (`test_poll_is_agent_bound`).

### 7. Same mission, same action, and same SUPERVISED state are retained after approval.

**Established.** `aauth_permission/service.py:157-166` (`record_approval`,
approve path): `reeval_request = dict(pending["request"])` copies the
original request verbatim (only `request_id` is suffixed, line 158); this
preserves the original `"mission"` and `"subject"` (including
`subject_agency_state`) fields unchanged, and `mission = self._mission_for(...)`
resolves the same mission object by its unchanged `s256`. The action is
taken from `pending["action"]`, set once at pending creation
(`service.py:82`) and never reassigned. Cross-checked by
`tests/test_g26_permission.py:117` asserting
`pending["reevaluation"]["runtime_envelope"]["subject"]["governance_state"] == "SUPERVISED"`.

### 8. PS-retained approval evidence — not an agent-supplied assertion or subject-state mutation — causes governance re-evaluation.

**Established**, three sub-claims:
- *Not agent-supplied*: `aauth_permission/service.py:304`
  (`_execution_request`): `policy.pop("approval_evidence", None)`
  unconditionally strips any `approval_evidence` present in the caller's
  original request policy before every evaluation, including the initial
  `permission()` call. The only way `approval_evidence` reaches evaluation is
  via the `trusted_approval_evidence` parameter (`service.py:307-308`), which
  is populated exclusively by `record_approval` (`service.py:164`), a
  server-side method gated by an authentication check
  (`service.py:123-124`: raises `PermissionError` unless
  `asserted_by == self.person_server_id` and
  `person_server_authenticated_assertion` is true).
- *Not subject-state mutation*: per item 7, the subject dict passed to
  re-evaluation is the original, unmodified request subject.
- *Causes re-evaluation*: `service.py:166` calls
  `evaluate_aauth_execution_request(execution_request)` inside
  `record_approval`, i.e., approval directly triggers a fresh governance
  evaluation.

Cross-checked by `tests/test_g26_permission.py:90-107`
(`test_agent_supplied_approval_evidence_is_not_trusted`): an agent-forged
evidence object embedded in the request policy is discarded; the call still
returns `202`/pending rather than granting.

### 9. Approval evidence references both the authority artifact and the constraint it satisfies.

**Established.** `aauth_permission/models.py:92-116`
(`ProvisionalG26ApprovalEvidence`) declares both `authority_reference: str`
(field, line 103) and `constraint_reference: str` (field, line 100) as
required dataclass members, populated at construction in
`service.py:127-144` from the caller-supplied `authority_reference` and
`constraint_reference` arguments.

### 10. Mission log preserves separately: original SOGA RESTRICT, AAuth deferred projection, PS approval assertion/evidence, re-evaluated SOGA result, final AAuth projection.

**Established**, five distinct `MissionLog.append` calls across the flow:
1. `soga_decision` — `service.py:233-240` (`_log_soga_and_projection`,
   called from `permission()` at line 100-102): the original SOGA evaluation
   (e.g., `RESTRICT`).
2. `aauth_projection` — `service.py:241-247` (same call): the `202`
   deferred-approval projection.
3. `provisional_g26_approval_evidence` — `service.py:249-256`
   (`_log_approval`, called at line 174 for the approve path and line 153
   for the decline path): the PS approval assertion/evidence.
4. `soga_reevaluation_decision` — `service.py:175-187` (inline `append` call
   in `record_approval`, approve path only): the re-evaluated SOGA result.
5. `aauth_final_projection` — `service.py:258-265` (`_log_final_projection`,
   called at line 206 for approve, line 154 for decline, line 231 for
   expiry): the final AAuth projection.

Each is a separate `mission_log.append(...)` call, and `MissionLog.append`
(`models.py:128-147`) creates a new `MissionLogEntry` with a monotonically
increasing `sequence` number per call — these are five distinct records, not
one result rendered five ways (see also item 15). Cross-checked by
`tests/test_g26_permission.py:119-124`, which asserts all five `kind` values
are present after a full approve cycle.

### 11. Explicit decline terminates negatively and is not rewritten as SOGA DENY.

**Established.** `aauth_permission/service.py:146-155` (`record_approval`,
decline branch): sets `pending["terminal"] = (403, {"error": "denied", ...})`
directly, without ever calling `evaluate_aauth_execution_request` — no SOGA
decision is produced on this path at all. `pending["originating_soga_decision"]`,
set once at pending creation (`service.py:84`), is never reassigned by the
decline branch, so it remains whatever the original evaluation produced
(`RESTRICT` in this scenario). Cross-checked by
`tests/test_g26_permission.py:145-153`
(`test_explicit_decline_is_terminal_error_not_soga_deny`), which asserts the
original decision remains `"RESTRICT"` after decline.

### 12. Configured expiry terminates pending; no fixed caregiver timeout or escalation policy was invented.

**Established.** `aauth_permission/service.py:224-231` (`_expire_if_needed`)
compares elapsed time against `pending["expires_after_seconds"]`, which is
copied from `self.pending_expiry_seconds` (`service.py:79`) — a constructor
parameter (`PermissionService.__init__`, `service.py:22`,
`pending_expiry_seconds: float | None = None`) with no default numeric value
and no caregiver-specific constant anywhere in `aauth_permission/`. Callers
(tests, demo) supply the duration explicitly
(e.g., `tests/test_g26_permission.py:29`, `pending_expiry_seconds=60`). On
expiry, `_expire_if_needed` only sets a terminal `408` response
(`service.py:230`) — no retry, re-notification, or escalation logic exists
in `aauth_permission/`. The only `"escalation"` string in the reviewed code
is an unrelated `RestrictModeSelector` mode for the `policy` dimension
(`engines/restrict_mode_selector.py:52-56`), not connected to expiry.

### 13. Historical terminology was annotated rather than rewritten.

**Established.** `ab2dbba5` touches three pre-G26 documents with
purely-additive diffs (no `-` lines against existing content, confirmed by
`git show ab2dbba5 -- <path>` for each):
- `sprints/gate-3/GOVERNANCE_VIEW_DESIGN.md` (original content dated
  2026-06-17, commit `?` "Add governance view demo for RESTRICT lifecycle";
  `ab2dbba5` appends a "2026-08-14 Prospective terminology annotation"
  section only).
- `canonical_caregiver_scenario.md` (original content dated 2026-06-17/06-20;
  `ab2dbba5` appends a "2026-08-14 G26 semantic annotation" section only).
- `docs/stage_gate_architecture_v0_1.md` (original content dated 2026-07-04,
  commit `d7a922f`; `ab2dbba5` appends a "2026-08-14 Prospective terminology
  annotation" section only).

Each appended section explicitly states the original is "preserved as
historical evidence" and does not characterize the earlier combined
`HOLDING`/`SUPERVISED_EXECUTION` usage as an established mistake. No prior
line in any of the three files was deleted or edited by `ab2dbba5`
(verified directly from the diffs, which contain only added lines below the
original terminal line of each file).

### 14. StageGateEngine remains unchanged.

**Established.** `engines/stage_gate_engine.py` does not appear in
`git show --stat ab2dbba5` (only `docs/stage_gate_architecture_v0_1.md`, a
doc, was touched). `git log --oneline -- engines/stage_gate_engine.py` shows
a single commit, `933963b` ("Sprint C Phase C2 — Stage Gate Engine and
lifecycle demonstration"), predating G0; `git diff 2dd9d5c ab2dbba5 --
engines/stage_gate_engine.py` (G0-init to reviewed commit) is empty.

### 15. The five mission-log records are five distinct records, not one result rendered five ways; the PS approval is recorded as an assertion with its source, not as an established fact.

**Established.** Distinctness: see item 10 (five separate `append` calls,
each producing a `MissionLogEntry` with its own `sequence`, `kind`, and
`payload`; `models.py:128-147`). Assertion-with-source: the
`provisional_g26_approval_evidence` entry's payload is
`evidence.to_dict()` (`service.py:255`), an instance of
`ProvisionalG26ApprovalEvidence`, whose fields include `asserted_by: str`
(`models.py:104`), `person_server_authenticated_assertion: bool`
(`models.py:105`), and `provenance: str` (`models.py:110`), populated at
`service.py:143` as the literal string
`"Person Server authenticated approval assertion"`. The record therefore
carries its own source/attribution metadata rather than presenting the
approval as a bare fact. This is reinforced textually by the annotation
added to `sprints/gate-3/GOVERNANCE_VIEW_DESIGN.md` in `ab2dbba5` ("durably
represented as a Person Server assertion attributable to a holder of the
referenced authority, not merely as the statement 'Beth approved'").

### 16. Explicit decline has a recorded terminal state and a recorded projection.

**Established.** Terminal state: `service.py:148-152` sets
`pending["state"] = "terminal"` and `pending["terminal"] = (403, {...})`
directly on the in-memory pending record. Recorded projection:
`service.py:154` calls `self._log_final_projection(pending,
"approval_declined", *pending["terminal"])`, which appends an
`aauth_final_projection` mission-log entry
(`service.py:258-265`) carrying `projection="approval_declined"`. (The
decline path also logs the evidence itself via `_log_approval` at
`service.py:153`, per item 10's entry #3.)

### 17. The provisional approval-evidence schema carries the convergence obligation to the future canonical Stage Gate evidence model.

**Established.** `aauth_permission/models.py:113-116`
(`ProvisionalG26ApprovalEvidence`): field defaults
`evidence_schema: str = "provisional-g26-approval-evidence-v1"` and
`convergence_obligation: str = "future-canonical-stage-gate-clearance-evidence-schema"`
are set directly on the dataclass, present on every evidence instance
regardless of caller input (not passed as constructor arguments in
`service.py:127-144`, so every instance uses the class default).

---

## Negative Controls

### 1. No valid approval evidence → no grant.

**Established.** Before any approval, `permission()` for a `SUPERVISED`
subject with the caregiver constraint takes the `HOLDING` branch
(`service.py:71-90`), returning `202`/pending — never `granted`. Code path:
`dimensions["subject_agency_state"]` stays `"REVIEW"` in
`runtime_governance_engine.py` because `approval_satisfies_constraint`
(`restrict_policy.py:16-43`) requires a non-`None` `evidence` argument, which
is `None` (`policy.get("approval_evidence")` on the original, un-approved
request — `runtime_governance_engine.py:85`). Cross-checked by
`tests/test_g26_permission.py:82-88`.

### 2. Valid PS-asserted approval satisfying the declared constraint → re-evaluation may produce ALLOW/granted.

**Established.** `service.py:189-191`: if `reevaluation["governance_determination"]
== "ALLOW"`, terminal is `(200, {"permission": "granted"})`. This is reached
via `approval_satisfies_constraint` returning `True`
(all twelve conjuncts in `restrict_policy.py:26-43` matched), which flips
`dimensions["subject_agency_state"]` to `"PASS"`
(`runtime_governance_engine.py:100`), and — with the fixture's other
dimensions already `PASS` — the engine decides `ALLOW`
(`runtime_governance_engine.py:125-131`). Cross-checked by
`tests/test_g26_permission.py:109-128`.

### 3. Wrong authority reference does not satisfy the constraint.

**Established.** `restrict_policy.py:41`:
`evidence.get("authority_reference") == constraint.get("authority_reference")`
is one conjunct of the `all(...)` in `approval_satisfies_constraint`
(lines 26-43); a mismatch makes the function return `False`, leaving
`subject_agency_state` at `"REVIEW"`, so the decision stays `RESTRICT` and
`service.py:195-203`'s catch-all `else` branch returns `denied`.
Cross-checked by `tests/test_g26_permission.py:130-136`.

### 4. Evidence for another constraint does not satisfy this one.

**Established.** `restrict_policy.py:39`:
`evidence.get("constraint_reference") == constraint.get("gate_id")` is
likewise one conjunct of the same `all(...)`. Cross-checked by
`tests/test_g26_permission.py:138-143`.

### 5. Explicit decline does not grant.

**Established.** Per confirmation 11, the decline branch
(`service.py:146-155`) never calls `evaluate_aauth_execution_request` and
its terminal response is always `(403, {"error": "denied", ...})` —
structurally incapable of producing `{"permission": "granted"}`.
Cross-checked by `tests/test_g26_permission.py:145-151`.

### 6. Missing authorized restrict path does not grant.

**Established.** Per confirmation 3, absence of an authorized constraint
produces mode `"fail_closed"` (`restrict_mode_selector.py:40-43`), which is
explicitly excluded from the internal-discharge branch and the `HOLDING`
branch in `service.py:69,91`, falling through to the `denied` `else`.
Cross-checked by `tests/test_g26_permission.py:155-162`.

### 7. Evidence with the correct authority reference and correct constraint reference but not affirmatively satisfied → no grant.

**Established via code path; absent from the test suite as a distinct case.**
`approval_satisfies_constraint` (`restrict_policy.py:26-43`) is a single
`all(...)` over twelve conjuncts, including
`evidence.get("result") == "approve"` (line 32),
`evidence.get("person_server_authenticated_assertion") is True` (line 33),
and `evidence.get("holder_attribution_asserted") is True` (line 34), in
addition to the authority/constraint-reference checks. If authority and
constraint references match but any other conjunct fails (e.g.
`holder_attribution_asserted` is `False`), `all(...)` is `False` and the
function returns `False` regardless of the matching references — the same
`denied` path as item 3/4 is taken. However, no test in
`tests/test_g26_permission.py` constructs this exact combination (correct
authority and constraint references, one of the other conjuncts
unsatisfied); the closest tests (`test_wrong_authority_reference_...`,
`test_evidence_for_different_constraint_does_not_satisfy`) vary the
reference fields themselves, not the affirmative-result/attestation fields
while holding references correct. This is recorded as a test-coverage gap,
not inferred as passing behavior.

### 8. A different agent presenting the pending_url does not receive the result.

**Established.** Per confirmation 6, `service.py:211-212` raises
`PermissionError` when the polling `agent` does not match
`pending["agent"]`; the caller receives no `terminal` body. Cross-checked by
`tests/test_g26_permission.py:224-227`.

### 9. Valid approval where re-evaluation still returns RESTRICT → no grant emitted.

**Established via code path; absent from the test suite as a distinct case.**
`service.py:189-203` is an exhaustive three-way branch on
`reevaluation["governance_determination"]`: `ALLOW` → granted (line
189-191), `DENY` → denied (line 192-194), and a catch-all `else` for any
other value — including `RESTRICT` — that returns `denied` with a reason
(line 195-202). This `else` branch fires regardless of *why* the result is
still `RESTRICT`, so it also covers the case where the submitted evidence
does fully satisfy the declared `HOLDING` constraint but a different,
unrelated dimension (e.g. `authority` or `reachability`) is independently
`REVIEW`, keeping `"REVIEW" in dimensions.values()` true
(`runtime_governance_engine.py:112`) and the overall decision `RESTRICT`.
No test in `tests/test_g26_permission.py` constructs this specific
scenario (fully-satisfying evidence plus an independently-REVIEW second
dimension); the existing "still RESTRICT" tests
(`test_wrong_authority_reference_...`, `test_evidence_for_different_constraint_does_not_satisfy`)
reach the `else` branch via *unsatisfied* evidence, not via satisfied
evidence combined with an unrelated failing dimension. Recorded as a
test-coverage gap.

---

## Summary of test-coverage gaps identified

Two items (negative controls 7 and 9) are enforced by code — traced to
specific, unconditional branch logic — but are not exercised by a dedicated
test case in `tests/test_g26_permission.py` for their exact scenario. All
other items (confirmations 1-17, negative controls 1-6 and 8) have both a
direct code-path citation and a corroborating test.
