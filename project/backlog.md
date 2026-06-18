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

