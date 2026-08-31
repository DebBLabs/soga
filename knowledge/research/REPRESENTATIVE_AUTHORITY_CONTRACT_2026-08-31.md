# Representative-Authority Contract — Scenario-Derived Requirements

Date: 2026-08-31

Status: ADOPTED RESEARCH INPUT pending synchronization commit — not a gate
finding, not implementation authorization, does not enter G28, does not extend
the AAuth mission schema, and does not extend `ProvisionalG26ApprovalEvidence`.

Gate/task: Corrected artifact passed read-only Gate 1 against `2b39c89`. This
artifact uses "representative authority" and makes no claim that "Ward" or
"Warden" names the representative relationship or any component derived here.

## Scope and evidence discipline

This artifact derives what representative authority must be able to express by
walking three concrete scenarios through this repository's own pipeline, the same
method `knowledge/research/G27_SESSION_GRANT_PERSON_SERVER_CONTRACT_2026-08-18.md`
used for the session-grant contract. It does not survey the guardianship/VC
ecosystem and does not select a mechanism, format, wallet, protocol, or owner.
Gaps are recorded at the stage they arise; this document does not resolve them.

Evidence labels used below:

- **REPOSITORY EVIDENCE** — an existing committed or working-tree file, class, or
  test, cited by path and line.
- **BREAK** — the earliest stage at which the cited structure has no defined,
  validated, decision-relevant field, branch, or check capable of interpreting
  the scenario, with physical carrying capacity distinguished from governed use.
- **PROPOSED CONTRACT** — a requirement the scenarios establish, stated as what
  must be expressible, not as a schema.

All file citations were re-verified directly from the working tree at HEAD
`2b39c89e8a19e6579c5caa60d2ff939dafa7923f`; none were modified to produce
this corrected artifact.

## The seven stages

Observation → interpreted evidence → attribution → authority establishment →
governance decision → permitted semantic action → physical execution. The
walkthroughs below identify, per scenario, the first stage the current code has no
decision-relevant way to interpret — not every stage the scenario touches.

## Scenario 1 — Tip Jar: a parent authorizes a child's participation

Neither the parent nor the child is the Tip Jar mission's `approver` or its
`agent`. D-023's adopted model treats every participant as
unknown-age/unknown-identity by design
(`knowledge/strategy/G27_POLICY_DISPOSITIONS_2026-08-20.md`). This scenario asks
only whether the *repository's own* structures can evaluate the additional
relationship; it does not rely on an ecosystem-absence claim.

**REPOSITORY EVIDENCE.** The G27 lifecycle's participant-facing state objects
relevant here are `Grant` and `Session` in `g27_tip_jar/lifecycle.py:38-66`.
`Grant` carries
`grant_id, mission_s256, platform_id, notice_version, policy_version, issuer,
issued_at, expires_at, state, consumed_at, session_id`. `Session` carries
`session_id, grant_id, mission_s256, platform_id, channel_key, created_at,
hard_expires_at, idle_expires_at, state, terminal_cause, terminal_at,
action_receipts`. Neither carries a participant-identity field, by design (D-023).

**BREAK — attribution.** The grant/session model and the typed fields in the G26
permission and runtime-envelope shapes have no defined relationship for *a second
person distinct from the subject who is asserting authority over that subject*.
`subject_id` names one person. Open dictionaries do provide physical carrying
capacity: `AuthorityEvidence.references`, `AuthorityEvidence.raw_evidence`, and
`SubjectState.context` (`verify/runtime_envelope_model.py:37-38,60`) can receive
arbitrary caller-supplied values, and the AAuth adapter captures or merges those
values (`input_adapters/aauth_execution_adapter.py:184-188,204-207`). The AAuth
runtime bridge does not read those dictionaries when it builds the
decision-relevant runtime input. Representative relationship data can therefore
be accepted and then silently discarded before evaluation; there is no defined,
validated, decision-relevant path for it.

`ProvisionalG26ApprovalEvidence.human_attribution`
(`aauth_permission/models.py:107`) can hold a second human's name, but it is
optional, free-text, and — see Scenario 2 — never checked. The break is not "the
parent's authority is insufficient" or literal inability to store a value; it is
the absence of interpreted evidence binding a representative to this person and
session before sufficiency can be evaluated.

**Consequence for later stages.** Authority establishment, governance decision,
permitted semantic action, and physical execution are all downstream of a
relationship that has no defined, validated, decision-relevant representation.
The scenario cannot reach them through today's structures, not because arbitrary
data cannot be stored but because nothing upstream hands governance interpreted
relationship evidence to evaluate.

## Scenario 2 — Senior case: adult child presents asserted POA authority for a parent

**SCENARIO ASSUMPTION — not a legal conclusion.** For this walkthrough only, the
presented POA is assumed to have been conferred by the parent and to be subject to
revocation by the parent. Actual creation, scope, durability, capacity, and
revocability vary by instrument, jurisdiction, and circumstances and require
authoritative legal research outside this repository-derived contract.

This scenario has real prior art in the codebase: the canonical caregiver
constraint from D-020, exercised in
`tests/fixtures/missions/caregiver_discharge_followup.json` and
`tests/test_g26_permission.py`.

**REPOSITORY EVIDENCE — the constraint shape.**
`tests/fixtures/missions/caregiver_discharge_followup.json:10-20` is the entire
constraint object:
```
{
  "gate_id": "gate-supervision-required",
  "name": "supervision_required",
  "step_id": "schedule_appointment",
  "governance_reasoning_token": "supervision_required",
  "required_evidence": "supervisor_confirmation",
  "authority_reference": "authority-caregiver-001",
  "restrict_path": "HOLDING"
}
```
`authority_reference` and `required_evidence` are bare opaque strings. Matching
is exact-string equality against
`ProvisionalG26ApprovalEvidence.authority_reference` and
`.required_evidence`, enforced field-by-field in
`engines/restrict_policy.py:26-42` (`approval_satisfies_constraint`).

**REPOSITORY EVIDENCE — attribution reaches this far and no further.**
`aauth_permission/service.py:127-144` constructs the evidence record;
`asserted_by` must equal the fixed `person_server_id`
(`aauth_permission/service.py:123`) — the Person Server is always the recorded
asserter of record, not the caregiver. `human_attribution` can carry a name
(`tests/test_g26_permission.py:72`, value `"Beth"`) but
`engines/restrict_policy.py:26-42` never reads `human_attribution` — it is absent
from the `all(...)` tuple entirely. A caregiver's name can be written down and it
changes nothing about whether the request is granted.

**BREAK — authority establishment.** Two absences, both at this stage:

1. Nothing in the current path distinguishes *how* `authority-caregiver-001`
   came to exist — asserted as conferred voluntarily by the parent versus arising
   from another basis. The string could reference external evidence, but the
   implementation never dereferences, validates, or evaluates that evidence or
   its basis.
2. Live authority validity is structurally disconnected on this AAuth bridge
   path. `engines/aauth_execution_runtime_bridge.py:100-113` hardcodes seven
   inputs consumed by authority evaluation. Five purport to describe current
   state: `revoked: False`, `expired: False`, `delegation_hops: 0`,
   `elapsed_seconds: 0`, and `attenuated: False`. Two are policy limits:
   `max_delegation_hops: 3` and `max_elapsed_seconds: 86400`. None is read from
   the incoming AAuth authority evidence or computed from current evidence on
   this path. In particular, no live input can produce `revoked: True` or
   `expired: True`. Other repository adapters may accept such inputs; this
   finding is scoped to `AAuthExecutionRuntimeBridge`.

**PROPOSED CONTRACT implication.** The current typed and decision-relevant path
does not distinguish authority asserted to be conferred by an affected person
from authority asserted to arise from another basis. `authority_reference` could
refer to external evidence, but the current implementation never dereferences,
validates, or evaluates that evidence or its basis. The bridge then supplies
hardcoded authority state and limits rather than live validity evidence.

## Scenario 3 — Refusal: authority is validly established and the affected person declines

Take Scenario 2 as valid — the caregiver's authority checks out and the
constraint is satisfied. The parent (the `subject`) now says no.

**REPOSITORY EVIDENCE — where a "no" would have to travel.**
`SubjectState` (`verify/runtime_envelope_model.py:52-60`) carries exactly
`subject_id, governance_state, reachability, context`. `governance_state` is
`SubjectGovernanceState` (`verify/runtime_envelope_model.py:10-15`):
`INDEPENDENT | SUPERVISED | MANAGED | DELEGATED | LAPSED` — a standing-condition
enum, not a live yes/no to one pending request. `context` is an open dict
(`input_adapters/aauth_execution_adapter.py:204-207`) that nothing downstream
reads for consent/refusal — confirmed by direct search: `consent`, `assent`,
`refus*`, `declin*`, and `veto` do not appear anywhere in
`engines/runtime_governance_engine.py`, `engines/runtime_dimension_evaluator.py`,
or `verify/runtime_envelope_model.py`.

**REPOSITORY EVIDENCE — the one decline-shaped field belongs to the wrong party.**
`PermissionService.record_approval` accepts `result: "approve" | "decline"`
(`aauth_permission/service.py:121-122`), but this is the *approver's* decision —
the party named by `asserted_by == person_server_id`
(`aauth_permission/service.py:123`) — not the subject/affected person's. Nothing
in the pipeline lets the person the action is about independently veto a request
a validly-authorized representative has already approved. The two roles —
representative-approves and affected-person-declines — collapse onto one `result`
field that only the former can ever populate.

**BREAK — interpreted evidence, one stage earlier than governance decision.**
The failure is not that `RestrictModeSelector.select`
(`engines/restrict_mode_selector.py:11-63`) handles a refusal signal badly — it
never receives one. Its inputs are `dimensions["reachability" | "authority" |
"subject_agency_state" | "execution_context" | "policy"]`
(`engines/restrict_mode_selector.py:15,23,30,45,52`), none of which can carry
"the affected person was asked and said no" as distinct from their standing
governance-state enum value. There is nothing to interpret into evidence in the
first place, so there is nothing for the decision stage to act on. A refusal by
the affected person cannot currently defeat anything, because it cannot currently
be said.

## The contract: what must be expressible

Stated as requirements on what the structures must be able to hold, not as a
schema, format, or owner.

- **Who stands in for whom.** Representative, represented person, mission
  `approver`, and `agent` must be separately expressible roles and relationships
  that are not silently collapsed. The same party may occupy more than one role
  only when that fact is explicit; Scenario 1 requires different people in the
  representative and represented-person roles. The relationship is currently
  absent from decision-relevant attribution before sufficiency can be evaluated.
- **What establishes that authority, and who asserts it.** The basis for the
  authority (see the two distinctions below) and the identity of whoever is
  presenting it as valid right now must both be expressible and distinguishable
  from the identity of the Person Server or platform that merely relays the
  assertion. Scenario 2 shows the current model collapses these: the PS is always
  the recorded `asserted_by`, and the one human-naming field carries no
  governance weight.
- **Which actions it covers, and under what conditions.** Scope must bind to
  specific actions and specific conditions, not to a standing status. The current
  `stage_gate` constraint already binds to one `step_id`; what's missing is any
  conditionality beyond that single match (time bounds, situational conditions,
  bystander/other-party effects) and any way to express a *narrower* grant than
  "this whole gate."
- **Its scope relative to a mission and a specific governed action.** The
  authority must be evaluable per action-and-mission pair, not once for a whole
  relationship. G27's own per-request evaluation (`begin_request`/
  `resolve_request` in `g27_tip_jar/runtime.py:113-298`)
  already does this for governance decisions generally; representative authority
  needs the same granularity, not a standing flag on the subject.
- **When and how it ends, and who may revoke it.** Current validity must be
  derived from live, checked evidence rather than hardcoded bridge values. The
  seven hardcoded current-state and policy-limit inputs at
  `engines/aauth_execution_runtime_bridge.py:100-113` are the concrete
  counterexample on the AAuth path. Which party may revoke which form of
  authority remains unresolved and depends on the authority's established basis.
- **How it is bound to a request so it cannot be reused for another.** The
  existing `constraint_reference`/`authority_reference`/`mission_s256`/`action`
  exact-match discipline in `engines/restrict_policy.py:26-42` and the G27
  adapter's per-`request_id` idempotency and binding checks
  (`g27_tip_jar/adapter.py:59-90`) are the closest existing analogues and establish that
  this binding pattern is already familiar in this codebase; representative
  authority needs an equivalent binding of *this assertion* to *this request*,
  not just of decision to request.

## Two distinctions to carry explicitly

**Conferred versus ascribed — candidate distinction requiring authoritative
research.** The scenarios suggest that authority a person affirmatively gives
another and authority attributed by law, court order, institutional rule, or
relationship may have different sources, scopes, termination rules, and
revocation paths. This artifact does not establish those legal categories or
their consequences. It establishes only that the current implementation has no
defined, validated, decision-relevant representation of authority basis and does
not evaluate referenced external evidence that might establish one.

**Assent or refusal as its own element.** A valid representative and a valid,
satisfied constraint are not the same fact as the affected person's own current
answer. Scenario 3 shows the pipeline has no independent channel for that answer
to reach the decision at all — not that it is outweighed, but that it cannot be
transmitted. A future contract must be able to carry assent or refusal distinctly
from representative approval. Whether, when, and how that signal overrides,
restricts, or otherwise affects representative authority remains unresolved and
requires explicit policy addressing age, capacity, emergency, authority basis,
mission, action, and context rather than a precedence rule invented here.

## Explicit nonclaims

This artifact does not select a credential format, wallet, protocol, or component
owner and does not conclude that "Ward" or "Warden" names any role derived here.
It does not extend the AAuth mission object, the
`ProvisionalG26ApprovalEvidence` dataclass, or the `stage_gate` constraint shape —
it only cites their current fields to show where they run out. It does not assess
any candidate implementation. It authorizes no implementation work and does not
open or advance G28. Remaining open questions — how conferred authority is
proven, how revocation propagates in real time, how conditions are structured,
how assent is captured from a person who may be the same unknown-identity
participant G27 already declines to identify, which authority distinctions are
legally meaningful in the applicable setting, and what precedence applies among
representative authority and affected-person assent or refusal — are recorded
here as gaps, not resolved.
