# Stage Gate 2 — Canonical Caregiver Scenario

Status: Active

Gate 1 Status: Complete

Purpose:

Demonstrate the RESTRICT lifecycle using existing SOGA capabilities and proof outputs.

No new governance functionality.

No new protocols.

No new use cases.

---

## Objective

Demonstrate:

Mission
→ RESTRICT
→ Approval Required
→ Re-Evaluation
→ ALLOW
→ Execution

using the Canonical Caregiver Scenario.

---

## Scenario

Subject:
Alice

Delegate:
Beth

Subject Agency State:
SUPERVISED

Mission:
Purchase Birthday Gift

Mission Step:
Complete Purchase

Authority Requirement:
Bounded purchasing authority on behalf of Alice.

Authority Evidence:
TBD by implementation proof.

Authority Rationale:
The delegate is attempting to perform a purchase on behalf of the subject.

Governance must determine whether the delegated authority should be exercised under current conditions.

---

## Required Demonstration Flow

### Step 1

Mission Created

Output:

- Mission ID
- Subject
- Delegate
- Mission
- Current Step

---

### Step 2

Authority Evidence Presented

Output:

- Authority Requirement
- Authority Evidence
- Supporting Context

---

### Step 3

Subject State Evaluated

Output:

Subject Agency State = SUPERVISED

---

### Step 4

Governance Evaluation

Expected Result:

RESTRICT

Reason:

Caregiver approval required.

Output:

Canonical Decision Package (RESTRICT)

---

### Step 5

Execution Hold

Expected Result:

HOLDING

Output:

Execution Status

Reason:

Awaiting caregiver approval.

---

### Step 6

Approval Event

Expected Result:

Beth grants approval.

Output:

Approval recorded.

---

### Step 7

Re-Evaluation

Expected Result:

ALLOW

Output:

Canonical Decision Package (ALLOW)

---

### Step 8

Execution

Expected Result:

EXECUTING

Output:

Execution Status

Mission Step proceeds.

---

## Success Criteria

A reviewer unfamiliar with SOGA can understand:

- what was being attempted
- why authority existed
- why execution was restricted
- what additional action was required
- why execution resumed

without reading code or specifications.

---

## Submission Package

Required Deliverables:

- Canonical Caregiver Scenario output
- RESTRICT CDP
- HOLDING execution status
- Approval event output
- ALLOW CDP
- EXECUTING status
- Affected files list
- Regression suite confirmation

---

## Non-Goals

This gate does NOT include:

- Governance View
- Mission Workbench
- New governance functionality
- New protocols
- New use cases
- Architectural revisions

---

## Exit Criteria

Gate 2 passes when:

RESTRICT
→ Approval
→ Re-Evaluation
→ ALLOW
→ Execution

is visible end-to-end using existing repository capabilities.

