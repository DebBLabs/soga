# Gate 3 — Governance View Design
Status: Draft for Review  
Coding Status: No coding authorized
---
## Objective
Design the simplest possible Governance View that makes the RESTRICT lifecycle visible for the Canonical Caregiver Scenario.
The view must explain:
- what was attempted
- who was acting
- what authority was presented
- what state mattered
- why RESTRICT occurred
- what action was required
- how execution resumed
---
## Primary User
Governance Operator
Examples:
- caregiver
- reviewer
- auditor
- compliance officer
- supervisor
The Governance Operator needs to understand why execution was held and what must happen next.
---
## Scenario
Subject: Alice  
Delegate: Beth  
Mission: Birthday Gift Purchase  
Mission Step: Complete Purchase  
Subject Agency State: SUPERVISED  
Initial Decision: RESTRICT  
Execution Status: HOLDING  
Approval: Beth grants approval  
Re-Evaluation Decision: ALLOW  
Final Execution Status: EXECUTING
---
## Core View Layout
# Mission Governance Status
## Mission Summary
Mission:
Birthday Gift Purchase
Subject:
Alice
Delegate:
Beth
Current Step:
Complete Purchase
Authority Requirement:
Delegated purchasing authority
Authority Evidence:
AAuth-shaped mission evidence
Protocol Role:
Supporting evidence only
---
## Current Governance Decision
Decision:
RESTRICT
Reason:
Alice is in SUPERVISED state. Execution requires caregiver approval before proceeding.
Restrict Mode:
SUPERVISED_EXECUTION
Execution Status:
HOLDING
Required Action:
Beth approval required
---
## RESTRICT Lifecycle
1. Mission step requested
2. Authority evidence presented
3. Subject state evaluated
4. Governance issued RESTRICT
5. Execution entered HOLDING
6. Beth approved
7. Governance re-evaluated
8. Governance issued ALLOW
9. Execution resumed
---
## Re-Evaluation Result
Approval Event:
Beth approval granted
New Decision:
ALLOW
Execution Status:
EXECUTING
---
## Expandable Evidence Sections
The first view should show summary first.
Optional expandable sections:
- Mission Context
- Authority Evidence
- Subject State Snapshot
- RESTRICT CDP
- Approval Event
- ALLOW CDP
- Execution Receipts
---
## Design Principles
1. Start with governance outcome, not protocol.
2. Mission step is primary.
3. Protocol appears only as authority evidence.
4. RESTRICT is shown as its own lifecycle.
5. ALLOW and DENY are terminal outcomes.
6. The view must be understandable without reading code.
7. No mission editing.
8. No approval workflow implementation.
9. No new governance logic.
---
## Minimum Visible Fields
Required fields for Gate 3 design:
- Mission
- Subject
- Delegate
- Mission Step
- Authority Requirement
- Authority Evidence
- Subject Agency State
- Governance Decision
- Restrict Mode
- Execution Status
- Required Action
- Approval Event
- Re-Evaluation Decision
- Final Execution Status
---
## Non-Goals
This design is not:
- Mission View
- Execution View
- Mission Workbench
- Approval service
- Notification service
- Protocol explorer
- Production UI
---
## Gate 3 Success Criteria
Gate 3 design passes when a reviewer can look at the Governance View and understand:
RESTRICT
→ HOLDING
→ Approval Required
→ Approval Granted
→ Re-Evaluation
→ ALLOW
→ EXECUTING
without reading code, specifications, or terminal output.
