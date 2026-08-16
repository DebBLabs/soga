# backlog.md

Status: Living Backlog

Purpose: Capture discoveries, future work, technical debt, architectural questions, and enhancement ideas without disrupting the current stage gate.

---

## Current Stage Gate

Active Gate: Stage Gate 2 — Canonical Caregiver Scenario

Current Objective:

Demonstrate:

Mission
→ RESTRICT
→ Approval Required
→ Re-Evaluation
→ ALLOW
→ Execution

using existing code and proof outputs.

---

## Architectural Questions

### B-001 Protocol Projection

Status: Open

Question:

Is Protocol Projection:

- a first-class architectural layer

or

- a translation mechanism implemented inside adapters

Priority: High

---

## Mission Package Architecture

### B-002 Mission Package as Durable Governance Object

Status: Open

Observation:

SOGA may be converging on the Mission Package as the primary durable governance object.

Potential contents:

- Mission Definition
- Mission Steps
- Subject
- Delegates
- Authority Evidence
- Subject State Snapshots
- Governance Decisions
- CDPs
- Approval Events
- Execution Events
- Audit Trail

Priority: Medium

---

### B-003 Mission Package Identifier Strategy

Status: Open

Questions:

- Mission Package ID model
- Mission Step IDs
- Governance Decision IDs
- CDP IDs

Priority: Medium

---

### B-004 Mission Lifecycle Persistence

Status: Open

Questions:

- How are long-lived missions resumed?
- How are RESTRICT states persisted?
- How are approval waits represented?

Priority: Medium

---

## Subject State Management

### B-005 Step-Triggered State Evaluation

Status: Open

Observation:

Subject Agency State should be evaluated only when a governed mission step requires current-state evidence.

Avoid:

- continuous polling
- broad liveness broadcasts

Investigate:

- step-triggered evaluation model
- state-on-demand model

Priority: Medium

---

### B-006 State Snapshot Model

Status: Open

Question:

Should governance decisions store:

- Subject Agency State
- Evaluation timestamp
- Evidence used

for audit and replay?

Priority: Medium

---

## Canonical Demonstration Framework

### B-007 Canonical Actor Registry

Status: Open

Proposed Actors:

- Alice — Subject
- Beth — Caregiver Delegate
- Carol — Financial Delegate
- David — Healthcare Delegate
- Evelyn — Governance Reviewer

Goal:

Reuse actors across all scenarios.

Priority: High

---

### B-008 Canonical State Registry

Status: Open

Proposed States:

- ACTIVE
- SUPERVISED
- IMPAIRED
- UNREACHABLE
- EMERGENCY

Goal:

Provide consistency across demonstrations.

Priority: High

---

### B-009 Authority Rationale Section

Status: Open

Observation:

Each scenario should document:

- Authority Requirement
- Authority Evidence
- Why This Evidence Is Appropriate

Goal:

Teach protocol purpose through mission context.

Priority: Medium

---

## Governance View

### B-010 Governance View

Status: Future

Goal:

Display:

- Mission
- Current Step
- Authority Presented
- Subject Agency State
- Governance Result
- Restriction
- Execution Status

Primary Objective:

Make RESTRICT visible.

Priority: High

---

### B-011 Mission View

Status: Future

Goal:

Mission-centric navigation and tracking.

Priority: Medium

---

### B-012 Execution View

Status: Future

Goal:

Execution lifecycle visibility.

Priority: Medium

---

## Protocol Ecosystem

### B-013 Additional Authority Evidence Sources

Status: Future

Examples:

- GNAP
- OAuth-derived systems
- MCP-related delegation patterns
- Future OIDF work

Goal:

Evaluate how additional authority evidence sources project into SOGA.

Priority: Low

---

## Technical Debt

### B-014 Documentation Synchronization

Status: Open

Verify consistency across:

- Bootstrap document
- Repository inventory
- Governance Overview
- North Star Diagram
- Specifications

Priority: Medium

---

## Parking Lot

Ideas worth preserving but not currently actionable:

- Mission package event model
- Governance event streams
- Approval notification architecture
- Mission replay capability
- Cross-mission analytics
- Governance telemetry
- Governance dashboards
- Mission archival strategy

---

## Knowledge Sharing

### B-015 Website / Blog Series

Status: Parking Lot

Purpose:

Capture the architectural discoveries that led to SOGA in a public-facing format.

Working Theme:

From Authorization to Governance

Potential Audience:

- Identity community
- AI governance community
- Healthcare governance
- Enterprise architects
- Developers

Potential Topics:

1. The Question Nobody Was Asking

   Authentication answers:
   Who are you?

   Authorization answers:
   What are you allowed to do?

   Governance answers:
   Should that authority still be exercised now?

2. Why ALLOW and DENY Are Not Enough

   Introduction of RESTRICT as a first-class governance outcome.

3. The Mission Is the Unit of Governance

   Shift from protocol-centric to mission-centric governance.

4. Protocols as Authority Evidence

   How AAuth, UCAN, ZCAP, and future mechanisms become supporting evidence rather than primary architecture.

5. Canonical Caregiver Scenario

   Demonstrating execution-time governance using family, legal, and business delegates.

6. RESTRICT as a Lifecycle

   RESTRICT
   → Notification
   → Approval or New Evidence
   → Re-Evaluation
   → Execution

Notes:

- Not part of current stage gate.
- Revisit after Governance View and Mission Workbench mature.
- Potential source material for debblabs.ai.

Priority: Low


---

## Gate 2 Review Observations

### B-016 Concrete Mission Step Language

Status: Open

Observation:

"Complete Purchase" is architecturally valid, but reviewers may need a more concrete step description.

Example:

Purchase birthday gift under $100 and ship to approved address.

Priority: Medium

---

### B-017 Mission-First Authority Evidence Labels

Status: Open

Observation:

Authority evidence should be labeled mission-first and protocol-second.

Preferred framing:

Delegated purchasing authority represented as AAuth-shaped mission evidence.

Priority: Medium

---

### B-018 Multi-Mission Actor Continuity

Status: Open

Observation:

Alice and Beth should be reusable across multiple missions so reviewers can see governance invariants across scenarios.

Priority: Medium


---

## Gate 2 Review Observations

### B-016 Concrete Mission Step Language

Status: Open

Observation:

"Complete Purchase" is architecturally valid, but reviewers may need a more concrete step description.

Example:

Purchase birthday gift under $100 and ship to approved address.

Priority: Medium

---

### B-017 Mission-First Authority Evidence Labels

Status: Open

Observation:

Authority evidence should be labeled mission-first and protocol-second.

Preferred framing:

Delegated purchasing authority represented as AAuth-shaped mission evidence.

Priority: Medium

---

### B-018 Multi-Mission Actor Continuity

Status: Open

Observation:

Alice and Beth should be reusable across multiple missions so reviewers can see governance invariants across scenarios.


Priority: Medium


---

### B-019 Restrict Mode Exposure Review

Status: Open

Observation:

SUPERVISED_EXECUTION originates from the current implementation path.

Determine whether restrict_mode is:

- internal implementation evidence
- governance-visible concept
- future profile-specific extension

Do not elevate restrict_mode to a primary Governance View field until reviewed.

Priority: Medium


---

## Sprint 5 — Governance Workbench

Status: Approved in Principle

Authorization: Deferred pending Alan review

Purpose:

Expose the existing mission set through a common Governance View so reviewers can explore the same governance lifecycle across multiple mission types.

---

### Trigger

Sprint 5 may begin only after Alan review has been received or explicitly deferred.

---

### Objective

Create a mission exploration layer using existing outputs only.

The reviewer should be able to select an existing mission and see the same Governance View structure applied consistently.

---

### Initial Scope

- Mission selector
- Existing missions only
- Existing governance outputs only
- Same Governance View structure
- Same actors where appropriate
- No new governance logic
- No new protocols
- No approval service
- No notification service
- No production UI

---

### Current Pattern Verified Missions

- Birthday Gift Purchase
- Medication Refill
- Travel Displacement

Pattern verification result:

RESTRICT
→ HOLDING
→ Approval Required
→ Approval Granted
→ Re-Evaluation
→ ALLOW
→ EXECUTING

The Governance View generalized across all three without modification to the view structure.

---

### Candidate Mission Set

Existing use cases available for future selector:

- banking
- caregiver
- emergency
- enterprise
- guardianship
- insurance
- medical_appointments
- research
- shopping
- travel

Existing generated missions available for future selector:

- mission-birthday-gift-purchase
- mission-medication-refill
- mission-travel-displacement
- mission-medical-appointment-scheduling
- mission-caregiver-absence-response
- mission-bounded-investment-rebalancing
- mission-cross-border-payment-under-fiduciary
- mission-incident-response-investigation
- mission-advance-directive-enforcement
- mission-software-deployment-under-approval

---

### Success Criteria

A reviewer can explore the existing mission set through a single Governance View and understand:

- what mission is being attempted
- which mission step is governed
- what authority evidence is present
- what Subject Agency State applies
- why RESTRICT occurs
- what action is required
- how re-evaluation resumes execution

without reading code or raw JSON.

---

### Non-Goals

Sprint 5 does not include:

- new governance logic
- new protocols
- new use cases
- production workbench
- persistence
- approval service
- notification service
- UI framework commitment
- architectural revision

---

### Notes

Sprint 5 should not begin before Alan review because his feedback may affect:

- which missions are foregrounded
- how the selector is labeled
- how the Governance View is presented
- whether any reviewer-facing terms need clarification


---

## Internal Review Observations

Status: Backlog

### Governance vs forbidden_actions Semantics

Question:

Should `forbidden_actions` be treated as a governance construct, a permission-system construct, or both?

Observation:

Permission systems typically assume anything not explicitly allowed is forbidden.

Governance systems may prohibit specific actions while remaining agnostic about the complete permission model of the underlying resource.

Future work should clarify the intended boundary.

Status: Backlog

---

### Subject Agency State Semantics in Banking Scenarios

Question:

What operational behavior does Subject Agency State = Supervised imply in financial delegation scenarios?

Examples:

- Approval required for every transaction?
- Approval required only for exceptional transactions?
- Approval required above defined thresholds?
- Approval required only when governance determines RESTRICT?

Future work should clarify expected behavior and reviewer-facing explanations.

Status: Backlog



B-020 — Delegation Hop Governance Evaluation

Status: Future Architecture

Origin:
External architectural review (June 2026)

Problem:
Current SOGA implementation evaluates delegation chains as authority evidence within a single Runtime Envelope and produces a single Canonical Decision Package per execution event. The Governance PDP does not currently perform independent governance evaluation of each delegation hop.

Architectural Question:
Should delegation legitimacy be evaluated solely through accumulated authority evidence, or should each delegation hop receive an independent governance evaluation and governance receipt?

Future Scope:

* Parent principal identification
* Delegated principal identification
* Hop-specific authority scope
* Hop-specific expiry evaluation
* Hop-specific revocation evaluation
* Typed admission/denial reason per hop
* Governance receipt generation per hop
* Delegation chain auditability independent of source protocol

Current State:
Delegation chain, attenuation, expiry, and revocation information may be carried as authority evidence and diagnostic inputs. They are not currently evaluated as independent governance events.

Acceptance Criteria:
A multi-hop delegation chain can be evaluated hop-by-hop, producing a governance determination and receipt for each delegation boundary prior to execution authorization.

Notes:
This item is not part of Sprint 5. Sprint 5 demonstrates multi-hop delegation evidence transport through Mission Intake, Protocol Projection, Runtime Envelope normalization, and runtime governance evaluation. Per-hop governance evaluation is a future architectural enhancement.


## Backlog item: Reconcile Subject Agency State vocabulary across SOGA and DIF Threat Model

**Status:** Not urgent. Documented so it isn't mistaken for drift and re-investigated cold.

**Observation:**
SOGA's locked `subject_agency_state` field uses five domain-neutral states: Independent, Supervised, Managed, Delegated, Lapsed.

The DIF Threat Model for Delegated Authority in AI-Mediated Systems (authored by our team, identity.foundation/delegated-authority-threat-model/) defines five states in healthcare-specific language: Normal, Temporarily Unavailable, Impaired, Unresponsive, Permanently Incapacitated.

**Why this is not a bug:** the DIF paper's states are scoped to its illustrative healthcare use case (Alice/Beth) on purpose — a threat model needs concrete, legible scenarios. SOGA's states were deliberately kept domain-neutral so the same architecture governs any mission type without the vocabulary implying "this is a medical system." Two documents, two audiences, one underlying concept — not forced into one vocabulary by design.

**Open question for later reconciliation:** are these actually the same axis expressed two ways (capacity-to-act, described differently for standards vs. implementation audiences), or two different axes that happen to share a five-state shape — subject capacity (DIF) vs. delegation relationship state (SOGA)? A person could plausibly be full-capacity ("Normal") but still "Delegated" by choice — worth checking whether SOGA's states and DIF's states compose rather than map 1:1 before any future document tries to unify them.

**Action when picked up:** do not silently rename either vocabulary to match the other. Investigate whether they're one dimension or two before proposing any change, per standing research discipline (investigate first, hypothesize second, propose last).

---

# Post-DIF Research Backlog
## Captured 2026-07-13

The following items arose from the DIF Trusted AI Agents Working Group discussion and subsequent AAuth integration analysis.

These are research items only. They do not authorize architectural or implementation changes.

---

## B-021 — Authorization Terminology Normalization

**Status:** Future Research

**Observed:**

The DIF discussion exposed ambiguity among:

- governance
- policy creation
- policy access
- policy evaluation
- enforcement
- validator
- verifier
- PAP
- PDP
- PEP

Participants interpreted the current `GovernancePDP` and Capability Registry boundaries differently.

**Hypothesis:**

SOGA may implement a richer contextual execution-time decision function than a conventional PDP, while still relying on conventional policy and enforcement concepts.

**Action:**

Map current SOGA components against conventional PAP, PDP, PEP, validator, verifier, and governance terminology before proposing any rename or component-boundary change.

**Priority:** High

---

## B-022 — Authorization Propagation Versus Identity Chaining

**Status:** Future Research

**Observed:**

The DIF discussion distinguished authorization propagation from identity chaining.

Identity may remain useful for attribution, accountability, audit, revocation, policy lookup, and dispute resolution.

The operative mechanism for delegated execution may instead be the propagation of bounded authority through an execution lineage.

**Hypothesis:**

Identity is carried as reference evidence, while authorization and execution context determine whether authority may continue.

**Action:**

Test this framing against:

- AAuth
- UCAN
- ZCAP
- capability-system literature
- conventional OAuth delegation
- multi-hop delegation scenarios

**Priority:** High

---

## B-023 — Capability Registry Architectural Boundary

**Status:** Future Research

**Observed:**

DIF participants questioned whether the Capability Registry belongs outside the current decision boundary.

**Open Questions:**

Is the Capability Registry:

- descriptive input to the decision service
- a PAP-like source
- part of the PDP boundary
- part of a broader execution-control envelope
- correctly placed, with only the diagram requiring clarification

**Action:**

Inspect implementation behavior and stable interface documents before proposing any movement or relabeling.

**Priority:** High

---

## B-024 — RESTRICT Semantic Classification

**Status:** Future Research

**Verified:**

SOGA implements RESTRICT as a first-class outcome.

The caregiver scenario demonstrates:

RESTRICT
→ HOLDING
→ new event or approval
→ full re-evaluation
→ ALLOW

**Open Question:**

Should RESTRICT be modeled as:

- a PDP decision
- an execution interruption state
- a request for additional evidence
- a transition into authorization
- a transition into governance
- a composite lifecycle state

**Priority:** High

---

## B-025 — Person Server and Powerbox Comparison

**Status:** Future Research

**Observed:**

Alan Karp compared the AAuth Person Server to a powerbox from capability-system literature.

**Hypothesis:**

The analogy may clarify the distinction among:

- person-scoped authority availability
- mission-scoped authority use
- agent-scoped delegated subsets

**Action:**

Review primary capability-system literature before treating the analogy as exact.

**Priority:** Medium

---

## B-026 — Wallet Contribution to Person Server Implementation

**Status:** Future Research

**Observed:**

A conventional wallet may provide keys, credentials, signatures, and holder-controlled identity material.

AAuth Person Server behavior may additionally require mission state, history, justification, policy access, interaction, negotiation, and authorization processing.

**Open Question:**

Can an existing wallet implement the full Person Server role, or only supply components to a broader Person Server service?

**Priority:** Medium

---

## B-027 — KYAOS / CHAOS Primary-Source Review

**Status:** Future Research

**Observed:**

Alan Karp stated that the project referred to in the meeting as KYAOS or CHAOS belongs near UCAN and ZCAP in the protocol landscape.

**Unverified:**

The preferred spelling, repository, specification, and precise architecture have not yet been confirmed.

**Action:**

Locate and read the project's primary materials before adding it to public documentation or protocol fixtures.

**Priority:** Medium

---

## B-028 — AuthZEN Authorization API Projection

**Status:** Future Research

**Hypothesis:**

The AuthZEN Authorization API may provide an output-normalization path from the Canonical Decision Package to an external Policy Enforcement Point.

Potential symmetry:

Protocol evidence
→ RuntimeEnvelope normalization
→ SOGA decision
→ CDP
→ AuthZEN-compatible projection

**Action:**

Read the primary AuthZEN Authorization API specification and evaluate:

- request and response schemas
- binary decision assumptions
- obligations or metadata
- extension mechanisms
- RESTRICT representation
- interaction requirements
- compatibility with CDP reasoning and evidence

**Priority:** Medium

---

## B-029 — Enforcement and Contextual Governance Separation

**Status:** Future Research

**Observed:**

Kernel, hardware, or PEP enforcement can intercept an action and prevent execution until conditions are met.

SOGA evaluates whether authority remains legitimate in the current mission and execution context.

**Hypothesis:**

Enforcement and contextual governance are separate but complementary architectural layers.

**Action:**

Map:

- interception
- governance consultation
- interaction evidence
- re-evaluation
- final enforcement

against the existing SOGA execution pipeline.

**Priority:** Medium

---

## B-030 — Christian Connector Integration-State Inspection

**Status:** Future Research

**Observed:**

Christian's AAuth reference implementation was cloned for connector work.

**Unverified:**

The current repository record does not yet establish:

- exact upstream repository and branch
- current AAuth draft version
- connector implementation state
- Person Server decision hook
- external Governance Server consultation
- deferred interaction status
- live FIDO or CTAP2 behavior

**Action:**

Inspect the cloned repository and connector code directly before scheduling or describing further integration work.

**Priority:** High

---

## B-031 — Multi-Principal Governance

**Status:** Future Research

**Observation:**

Some missions may be subject to multiple governance sources, including personal, enterprise, fiduciary, or regulatory governance.

A simple tenant or policy-source switch may be insufficient where those sources are simultaneously active or potentially adversarial.

**Action:**

Research composition, precedence, conflict resolution, disclosure, and accountability before proposing architecture.

**Priority:** Medium

---

# Post-DIF Research Backlog
## Captured 2026-07-13

The following items arose from the DIF Trusted AI Agents Working Group discussion and subsequent AAuth integration analysis.

These are research items only. They do not authorize architectural or implementation changes.

---

## B-021 — Authorization Terminology Normalization

**Status:** Future Research

**Observed:**

The DIF discussion exposed ambiguity among:

- governance
- policy creation
- policy access
- policy evaluation
- enforcement
- validator
- verifier
- PAP
- PDP
- PEP

Participants interpreted the current `GovernancePDP` and Capability Registry boundaries differently.

**Hypothesis:**

SOGA may implement a richer contextual execution-time decision function than a conventional PDP, while still relying on conventional policy and enforcement concepts.

**Action:**

Map current SOGA components against conventional PAP, PDP, PEP, validator, verifier, and governance terminology before proposing any rename or component-boundary change.

**Priority:** High

---

## B-022 — Authorization Propagation Versus Identity Chaining

**Status:** Future Research

**Observed:**

The DIF discussion distinguished authorization propagation from identity chaining.

Identity may remain useful for attribution, accountability, audit, revocation, policy lookup, and dispute resolution.

The operative mechanism for delegated execution may instead be the propagation of bounded authority through an execution lineage.

**Hypothesis:**

Identity is carried as reference evidence, while authorization and execution context determine whether authority may continue.

**Action:**

Test this framing against:

- AAuth
- UCAN
- ZCAP
- capability-system literature
- conventional OAuth delegation
- multi-hop delegation scenarios

**Priority:** High

---

## B-023 — Capability Registry Architectural Boundary

**Status:** Future Research

**Observed:**

DIF participants questioned whether the Capability Registry belongs outside the current decision boundary.

**Open Questions:**

Is the Capability Registry:

- descriptive input to the decision service
- a PAP-like source
- part of the PDP boundary
- part of a broader execution-control envelope
- correctly placed, with only the diagram requiring clarification

**Action:**

Inspect implementation behavior and stable interface documents before proposing any movement or relabeling.

**Priority:** High

---

## B-024 — RESTRICT Semantic Classification

**Status:** Future Research

**Verified:**

SOGA implements RESTRICT as a first-class outcome.

The caregiver scenario demonstrates:

RESTRICT
→ HOLDING
→ new event or approval
→ full re-evaluation
→ ALLOW

**Open Question:**

Should RESTRICT be modeled as:

- a PDP decision
- an execution interruption state
- a request for additional evidence
- a transition into authorization
- a transition into governance
- a composite lifecycle state

**Priority:** High

---

## B-025 — Person Server and Powerbox Comparison

**Status:** Future Research

**Observed:**

Alan Karp compared the AAuth Person Server to a powerbox from capability-system literature.

**Hypothesis:**

The analogy may clarify the distinction among:

- person-scoped authority availability
- mission-scoped authority use
- agent-scoped delegated subsets

**Action:**

Review primary capability-system literature before treating the analogy as exact.

**Priority:** Medium

---

## B-026 — Wallet Contribution to Person Server Implementation

**Status:** Future Research

**Observed:**

A conventional wallet may provide keys, credentials, signatures, and holder-controlled identity material.

AAuth Person Server behavior may additionally require mission state, history, justification, policy access, interaction, negotiation, and authorization processing.

**Open Question:**

Can an existing wallet implement the full Person Server role, or only supply components to a broader Person Server service?

**Priority:** Medium

---

## B-027 — KYAOS / CHAOS Primary-Source Review

**Status:** Future Research

**Observed:**

Alan Karp stated that the project referred to in the meeting as KYAOS or CHAOS belongs near UCAN and ZCAP in the protocol landscape.

**Unverified:**

The preferred spelling, repository, specification, and precise architecture have not yet been confirmed.

**Action:**

Locate and read the project's primary materials before adding it to public documentation or protocol fixtures.

**Priority:** Medium

---

## B-028 — AuthZEN Authorization API Projection

**Status:** Future Research

**Hypothesis:**

The AuthZEN Authorization API may provide an output-normalization path from the Canonical Decision Package to an external Policy Enforcement Point.

Potential symmetry:

Protocol evidence
→ RuntimeEnvelope normalization
→ SOGA decision
→ CDP
→ AuthZEN-compatible projection

**Action:**

Read the primary AuthZEN Authorization API specification and evaluate:

- request and response schemas
- binary decision assumptions
- obligations or metadata
- extension mechanisms
- RESTRICT representation
- interaction requirements
- compatibility with CDP reasoning and evidence

**Priority:** Medium

---

## B-029 — Enforcement and Contextual Governance Separation

**Status:** Future Research

**Observed:**

Kernel, hardware, or PEP enforcement can intercept an action and prevent execution until conditions are met.

SOGA evaluates whether authority remains legitimate in the current mission and execution context.

**Hypothesis:**

Enforcement and contextual governance are separate but complementary architectural layers.

**Action:**

Map:

- interception
- governance consultation
- interaction evidence
- re-evaluation
- final enforcement

against the existing SOGA execution pipeline.

**Priority:** Medium

---

## B-030 — Christian Connector Integration-State Inspection

**Status:** Future Research

**Observed:**

Christian's AAuth reference implementation was cloned for connector work.

**Unverified:**

The current repository record does not yet establish:

- exact upstream repository and branch
- current AAuth draft version
- connector implementation state
- Person Server decision hook
- external Governance Server consultation
- deferred interaction status
- live FIDO or CTAP2 behavior

**Action:**

Inspect the cloned repository and connector code directly before scheduling or describing further integration work.

**Priority:** High

---

## B-031 — Multi-Principal Governance

**Status:** Future Research

**Observation:**

Some missions may be subject to multiple governance sources, including personal, enterprise, fiduciary, or regulatory governance.

A simple tenant or policy-source switch may be insufficient where those sources are simultaneously active or potentially adversarial.

**Action:**

Research composition, precedence, conflict resolution, disclosure, and accountability before proposing architecture.

**Priority:** Medium

---

## B-032 — G26 Approval Negative-Control Regression Coverage

**Status:** Complete — regression coverage added; no implementation defect found

**Evidence:** `knowledge/research/G26_GATE_REVIEW_2026-08-14.md`, negative
controls 7 and 9; finalized checklist at
`knowledge/strategy/G26_STAGE_GATE_CHECKLIST.md`.

**Established implementation paths lacking exact regression cases:**

1. Correct authority reference + correct constraint reference + approval not
   affirmatively satisfied → no grant.
2. Valid approval evidence + governance re-evaluation still `RESTRICT` → no
   grant.

The Stage Gate review established both code paths. This item records missing
regression protection only and must not be reported as a runtime defect.

**External presentation condition:** Dedicated coverage for Control 7 is
required before the canonical caregiver approval path is presented externally
to Dick Hardt.

**Completion evidence:** `tests/test_g26_permission.py` now includes
`test_correct_references_without_affirmative_satisfaction_do_not_grant` and
`test_valid_approval_does_not_grant_when_reevaluation_remains_restrict`. Both
exercise the real approval and governance paths. The focused G26 suite,
regression baseline, and compile/diff checks passed on 2026-08-14.

**External presentation condition:** Satisfied. Control 7 now has dedicated
coverage before external caregiver-path presentation to Dick Hardt.

---

## B-033 — Gate 1a Canonical-Pipeline Synchronization Contradiction

**Status:** Complete — synchronization disposition recorded in CURRENT_STATE

**Established by Gate 1a:**

The working G26/AAuth integration reaches:

AAuth adapter → RuntimeEnvelope → RuntimeGovernanceEngine/SOGA → Canonical
Decision Package → PermissionService.

It does not reach Mission Builder, StageGateEngine, GovernedExecutionLoop, or
capability registry. `knowledge/working/CURRENT_STATE.md` separately describes
an unchanged canonical execution pipeline containing those components and says
that no architecture changed.

**Synchronization disposition:**

`knowledge/working/CURRENT_STATE.md` now identifies the pipeline as
target/designed architecture rather than a claim of complete current traversal.
It preserves the deliberate adoption in commit `2dd9d5c`, does not characterize
the prior statement as historically erroneous, and records both the limit of
current reachability evidence and the scope boundaries of G26.

**Boundary:** Documentation/architecture-description synchronization only. No
runtime remediation or Gate 1b functional subtraction is authorized by this
item.

---

## B-034 — Gate 1a Stale Implementation Status and Dangling Lineage References

**Status:** Open — documentation defect

**Established inconsistencies in `knowledge/working/IMPLEMENTATION_STATUS.md`:**

- Person Server and Person Server Integration are described as working although
  the G26 implementation explicitly provides a mock Person Server boundary.
- Christian Posta Demo is described as working although its implementation and
  history are not reachable in this repository.
- Runtime Restrict is described as planned although G26 demonstrably executes
  RESTRICT/HOLDING.

These are documentation defects, not Gate 1a evidence defects.

**Dangling-reference disposition evidence:**

- `tools/sanity_check.sh` actively expects external A2A gateway verification and
  GNAP container names whose implementations are not present in reachable
  repository history. Whether the script should be updated or explicitly scoped
  to external infrastructure requires a decision; repository evidence does not
  make the correct disposition unambiguous.
- `knowledge/memory/milestones/first-aauth-execution-boundary.md` names
  `agentgateway/run-aauth-extauth.sh` as a modified file in an external
  `christian-posta/aauth-full-demo` branch. The milestone should be explicitly
  marked as an external reference; the referenced implementation is not present
  or reachable in this repository. The milestone claim itself is not rewritten
  by this item.

**External-claim boundary:**

Current G26 demonstrates a governance decision at the permission boundary with
evidence-driven re-evaluation, mock Person Server authentication, and
process-local state. Governed execution of the requested external action itself
is not demonstrated. Permission enforcement must not be reported as action
execution.

---

## B-035 — StageGateEngine and G26 Clearance/Evidence Path Relationship

**Status:** Complete — PI accepted advisory determination; recorded in D-021

**Established question:**

The relationship between StageGateEngine clearance/evidence handling and the
G26 constraint/evidence/re-evaluation path is unresolved.

**Required disposition:**

Determine that relationship through a separate architectural decision. This
item does not pre-decide whether StageGateEngine converges into, is replaced by,
or permanently coexists with the G26 path.

**Boundary:**

No runtime change, schema convergence, replacement, coexistence commitment, or
other implementation authorization is created by this backlog item.

**Approved disposition:**

B-035 resolves as a schema-level convergence obligation with no mechanism-level
relationship required or established between StageGateEngine and G26. The
mechanisms operate on different units of work:

- StageGateEngine operates on a mission-execution step in the older step-bearing
  model.
- G26 operates on a permission request/action under the native immutable,
  step-free AAuth mission adopted by D-013.

The repository binds G26 to a future canonical Stage Gate clearance-evidence
schema, not to StageGateEngine itself. Future schema convergence must preserve
the assurance and binding properties established by G26 and must not weaken
D-019, D-020, or the recorded G26 trust boundary.

Mechanism-level convergence, replacement, or coexistence is neither required
nor established. The future disposition of StageGateEngine is deferred to Gate
1b, where the continuing role of the older step-bearing governed-mission model
will be evaluated.

---

## B-036 — StageGateEngine Clearance Validation Ignores Affirmative Satisfaction

**Status:** Open — repair not authorized

**Source:** Reproduced under B-035 verification at
`main @ 7337f7ee3bbf1f41a18533d8f1f86a7b18ffc158`. This defect was not required
for B-035 closure.

**Defect:**

At `engines/stage_gate_engine.py:121`, when a gate declares
`required_evidence`, `_has_clearance()` returns
`clearance_evidence.get("type") == required_evidence` and never inspects
affirmative satisfaction. `satisfied`, `supervisor_confirmed`, `source`,
`authority`, and `provenance` are ignored.

**Inverted strictness:**

When `required_evidence` is `None`, the function checks `satisfied`; when it is
configured — the stricter configuration — it stops checking satisfaction.

**Reproduction:**

```json
{"type": "supervisor_confirmation", "satisfied": false}
```

yields `_has_clearance: True` and `RESUBMIT_FOR_GOVERNANCE`.

**Blast radius:**

- `GovernedExecutionLoop` uses StageGateEngine routing and would observe false
  clearance as `RESUBMIT_FOR_GOVERNANCE`.
- No repository test exercises StageGateEngine or `_has_clearance()`.
- `tools/stage_gate_demo.py` succeeds with matching evidence type, but that
  success does not establish that affirmative clearance was validated.
- `tools/governed_execution_demo.py` and `tools/mission_builder_demo.py` provide
  a flat evidence shape not recognized by `_has_clearance()`; their subsequent
  ALLOW results follow a subject-state change and do not establish actual
  clearance.
- The three demos — `tools/stage_gate_demo.py`,
  `tools/governed_execution_demo.py`, and `tools/mission_builder_demo.py` — are
  in the repair blast radius and will break when `_has_clearance()` is repaired;
  their current success does not establish actual clearance.
- The deferred `knowledge/working/deferred/live_governance_workbench.py` uses
  the same flat evidence pattern and has the same limitation.

**Future scope:**

- establish one canonical clearance-evidence shape;
- require affirmative satisfaction in addition to matching evidence type;
- update callers and add direct StageGateEngine / `_has_clearance()` tests.

Any future canonical clearance-evidence schema must rise to G26's assurance
level, not reduce G26 to the current StageGate evidence shape. A future repair
must not weaken D-019, D-020, or the recorded G26 trust boundary.
