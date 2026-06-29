# SOGA Process Backlog
# Last updated: June 27, 2026

## Purpose

This file tracks non-implementation work items.

Implementation backlog is in project/backlog.md.

This file tracks community, standards, funding, research,
and operational process items.

All AI collaborators should read this file at session start
alongside project/backlog.md.

This file is owned by Deb. Claude maintains it.
CG updates it when process items are discovered during
implementation sessions. Gemini flags items during gate review.

---

## Status Key

OPEN — not yet started
IN PROGRESS — actively being worked
BLOCKED — waiting on external dependency
COMPLETE — done
DEFERRED — intentionally postponed

---

## Pre-July 16 — Critical Path

P-001
Item: DIF Threat Model PR
Status: IN PROGRESS
Owner: Deb and Claude
Description: Add permission and authority glossary entries
to the DIF delegated authority report. Revise introduction
to distinguish permission from authority consistently.
Commitment: Juan Caballero invited this PR. Committed this week.
Next action: Claude drafts glossary entries and introduction
edits. Deb takes to Juan pairing session.
Reference: SESSION_BOOTSTRAP.md — Key Community Relationships

P-002
Item: July 16 Question Set
Status: IN PROGRESS
Owner: Deb and Claude
Description: Finalize four questions for Dick Hardt office hours.
Questions should show architectural depth, reference AAuth Events
published June 26, and position SOGA as complementary to AAuth.
Next action: Finalize and commit to
knowledge/working/JULY_16_PREPARATION.md
Reference: AAuth Events draft-hardt-aauth-events-latest

P-003
Item: NSF SBIR Phase I Framing
Status: BLOCKED
Owner: Deb and Claude
Blocked on: CIP application review and NSF portal login resolution
Description: Draft problem statement, research proposition,
reference monitor framing, broader impacts, commercialization path.
Core framing: Current systems determine what an agent can do.
They do not determine whether delegated authority remains
legitimate at the moment of execution.
Next action: Deb shares CIP application. Claude drafts against it.

P-004
Item: SESSION_BOOTSTRAP.md Current State Update
Status: OPEN
Owner: CG updates current state section. Claude reviews.
Description: Update the Current Repository State section
to reflect Sprint 8 completion, RuntimeEnvelope specification
commit, and AAuth integration status.
Next action: CG updates after remaining Sprint 8 files committed.

---

## Community and Standards — Active

P-005
Item: AAuth Slack — Post soga-governance-experiment
Status: COMPLETE
Description: Fork of christian-posta/aauth-full-demo created.
Community can see the integration work.
Note: Dick and Christian have both acknowledged prior posts.
Fork is visible without announcement needed.

P-006
Item: DIF Workgroup — Ongoing Updates
Status: IN PROGRESS
Owner: Deb
Description: Continue providing updates to DIF delegated
authority workgroup. Juan and team are engaged.
SOGA is influencing direction.
Next action: DIF threat model PR this week (see P-001).

P-007
Item: Alan Karp — Repository Review Follow-up
Status: IN PROGRESS
Owner: Deb
Description: Alan reviewed repository and provided substantive
feedback. Eight GitHub issues created. Delegation chain
conversation ongoing. Per-hop governance question answered
honestly with B-020 created.
Next action: Monitor for further Alan engagement.
Incorporate feedback per open GitHub issues.

P-008
Item: Martin — GitHub Issue 2 Follow-up
Status: IN PROGRESS
Owner: Deb
Description: Martin engaged on per-hop governance question.
Honest answer given. B-020 created. Martin is watching.
Next action: No immediate action. Monitor for further engagement.
B-020 is the architectural response.

P-009
Item: Juan Caballero — Pairing Session
Status: OPEN
Owner: Deb
Description: Juan offered Calendly pairing session for Git
workflow walkthrough. Use for DIF threat model PR submission.
Next action: Schedule after P-001 draft is ready.
Reference: https://calendly.com/difsupport

---

## Community and Standards — Sequenced

P-010
Item: Dazza Greenwood — External Agent Testing
Status: DEFERRED
Owner: Deb
Description: Dazza identified as external agent testing audience.
Engage after workbench is stable and demonstration is ready.
Deferred until: Post July 16. After Sprint 9 workbench is visible.

P-011
Item: Dick Hardt — Post Office Hours Follow-up
Status: OPEN
Depends on: July 16 office hours
Description: After July 16 conversation, follow up based on
Dick's feedback. May include AAuth Slack post, repository
update, or architectural response.
Next action: Define after July 16.

P-012
Item: DIF Delegated Authority Report — Introduction Revisions
Status: OPEN
Depends on: P-001 glossary PR merged
Description: After glossary entries are accepted, revise
introduction to reference the permission/authority distinction
consistently throughout the report.
Next action: After P-001 complete.

P-013
Item: AIIM Use Case Working Group — Engagement
Status: DEFERRED
Owner: Deb
Description: Deb is part of AIIM group. Moving slowly.
DIF outputs are faster and more aligned currently.
OIDF adapter is future roadmap item.
Deferred until: AIIM produces concrete deployable artifacts.

---

## Funding

P-014
Item: NSF SBIR Phase I Application
Status: BLOCKED
Depends on: P-003 framing, NSF portal login resolution
Description: Full Phase I application. Strongest current
funding opportunity. Research question is falsifiable.
Reference implementation exists. External validation from
Alan Karp, Dick Hardt engagement, DIF community.
Next action: Resolve portal login. Draft from CIP application.

P-015
Item: Anthropic Open Source Program
Status: OPEN
Description: Infrastructure credits. Eligibility improves
as repository matures and standards relevance grows.
Not cash funding but significant compute value.
Next action: Apply after repository is more publicly visible.
Timing: Post July 16.

P-016
Item: Cloud Credits — AWS and Google
Status: OPEN
Description: Low effort, medium value. More relevant once
repository is public and experimentation increases.
Next action: Apply after repository is public and prototype
is running. Post July 16.

P-017
Item: Fellowship Applications — Mozilla, Berggruen, GovAI
Status: DEFERRED
Description: Wait until one of the following exists:
preprint, stronger experimental results, or Phase I NSF pitch.
Next fellowship application will be stronger with artifacts.
Deferred until: After NSF Phase I draft exists.

---

## Research

P-018
Item: Governed Team Presence Research Direction
Status: OPEN
Owner: Deb
Description: Emerging research area from June 26 session.
How do humans collaborate with persistent autonomous teammates?
How should autonomous participants communicate?
When should an agent interrupt? When remain silent?
How is authority expressed socially?
How is runtime governance reflected in group behavior?
Misty provides physical presence for the team.
Next action: Capture in research/DESIGN_NOTES.md.
Longer term: NSF HCI framing, academic paper.

P-019
Item: Repository Governance as Research Contribution
Status: OPEN
Owner: Deb and Claude
Description: The repository governance methodology — treating
AI sessions as temporary contributors with human curatorial
authority — may be a publishable contribution independent
of SOGA. The development process mirrors SOGA's own governance
principles.
Next action: Capture in research/RESEARCH_LOG.md.
Longer term: Consider as a companion paper or blog post.

P-020
Item: Per-Hop Governance Evaluation Research
Status: DEFERRED
Reference: B-020
Description: Research question identified by Martin.
Requires formal architectural design before implementation.
Deferred until: After July 16 and Sprint 9.

---

## Operational

P-021
Item: Reachability Default Policy
Status: OPEN
Reference: Sprint 8 Task 2 Gate 1 observation
Description: The reachability default in
aauth_execution_runtime_bridge.py treats absent reachability
as Reachable for the initial ALLOW path. This is a
governance-relevant decision that should eventually move
to a policy configuration rather than bridge code.
Next action: Track in project/backlog.md as future
implementation item. No immediate action required.

P-022
Item: Protocol Projection Layer Verification
Status: OPEN
Description: Confirm Protocol Projection is a distinct layer
not implicitly embedded inside adapters.
This open verification item has been carried since early gates.
Next action: Verify during Sprint 9 architecture review.

P-023
Item: GitHub Issues — Alan Karp Review
Status: IN PROGRESS
Description: Eight GitHub issues created from Alan's review.
Labels: repository-hygiene (resolved), scenario-enhancement,
architectural.
Open items:
- Contrast human-in-loop vs agent payment protocol
- Make intent visible in caregiver scenario
- Banking use case Supervised state clarification
- Delegation chains (B-020)
- forbidden_actions enumeration
Next action: Address scenario-enhancement items in Sprint 9.

---

## Instructions for AI Collaborators

CG:
When you discover a process item during implementation —
a community commitment, a standard to review, a funding
deadline, a relationship to maintain — add it here.
Use the next available P-number.
Flag it at the end of your gate submission.

Claude:
Review this file at session start alongside
project/backlog.md and knowledge/working/CURRENT_STATE.md.
Update status fields when items complete or change.
Add new items when identified during gate review.

Gemini:
Flag process items during gate review when you identify
community, standards, or external posture implications.
Recommend addition to this file in your gate review notes.

All agents:
This file is process memory.
It is not implementation scope.
Do not add implementation items here.
Implementation items belong in project/backlog.md.

---

P-024

Item:
Program Transition Observation

Status:
IN PROGRESS

Owner:
Deb / Claude / CG

Description:

Transition repository emphasis from governance foundation development
toward purposeful application of governance in support of the Compaia
vision.

Governance research continues in parallel.

Next Action:

Complete Sprint 9 and reassess prior to July 16 Office Hours.

---

P-025

Item:
README Regression Baseline Verification

Status:
OPEN

Description:

Verify public repository regression counts accurately reflect the
current repository baseline before July 16.

Owner:
CG

