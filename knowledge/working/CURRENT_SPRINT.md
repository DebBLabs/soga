# SOGA Research Platform
# Current Sprint: Pre-July 16 Track
# Last updated: June 26, 2026

## Track Objective

Prepare the repository, architecture narrative, and funding pitch for
July 16 Dick Hardt office hours and NSF SBIR submission.

This is positioning work, not governance architecture expansion.
Governance logic is frozen.

## July 16 Readiness Test

Applied to every deliverable:
- Would Dick understand this in under two minutes?
- Does it make the two-contribution architecture visible without
  explanation?
- Does it complement AAuth rather than compete with it?

## Task Status

Task 1 — Repository State Confirmation
Status: COMPLETE
Baseline confirmed: 11 use cases, 42 CDPs

Task 3 — Christian Posta Fork Target
Status: COMPLETE
Target: christian-posta/aauth-full-demo

Fork — soga-governance-experiment
Status: COMPLETE
Branch live. Stub integrated. ALLOW returned for all requests.
Intentional. Proves execution boundary exists.

Tasks A-D — Canonical Documentation Updates
Status: IN PROGRESS
Files: canonical_architecture.md, architectural_principles.md
Add: explicit execution boundary, runtime behavior example,
architectural ownership, Implementation Continuity Principle

Task 2 — Mission Planning Workbench
Status: PENDING
Depends on: Tasks A-D complete
Implement as architectural component not UI panel.
Ends at execution boundary. Produces no governance outputs.

Task 4 — Governance Decision Workbench
Status: PENDING
Depends on: Task 2 complete
Begins at execution boundary.
Evaluates one execution request at a time.
Displays Mission ID for traceability only.

Task 5 — Repository Architecture Visibility
Status: PENDING
Depends on: Task 4 complete
Full pipeline visible: Human Intent → Mission Planning →
Execution Boundary → Governance Decision → Execution Layer

Task 6 — DIF Threat Model PR
Status: PENDING
Owner: Deb and Claude
Permission vs Authority glossary entries.
Introduction revisions for DIF delegated authority report.
Juan pairing session this week.

Task 7 — July 16 Preparation
Status: PENDING
Owner: Deb and Claude
One focused question for Dick.
Two-minute SOGA positioning relative to AAuth.

Task 8 — NSF SBIR Framing
Status: PENDING
Owner: Deb and Claude
Depends on: CIP application shared
Problem statement, research proposition, reference monitor framing,
broader impacts, commercialization path.

## Sequencing

Tasks 1 and 3: COMPLETE
Fork: COMPLETE
Repository memory bootstrap: IN PROGRESS (current)
Tasks A-D: NEXT for CG
Task 2: After A-D
Task 4: After Task 2
Task 5: After Task 4
Tasks 6-8: Deb and Claude, parallel throughout
July 16: Target
Sprint 8: Opens after July 16

## Constraints

No new governance logic.
No new protocols.
No new governance dimensions.
No Sprint 8 work until July 16 has passed.
Gate process applies to all CG commits.
Affected files list required at every submission.
Regression must pass at 11 use cases, 42 CDPs.
