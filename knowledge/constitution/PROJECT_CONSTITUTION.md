# SOGA Research Platform
# Project Constitution
# Ratified June 26, 2026

## Purpose

This document is the governing constitution of the SOGA Research Platform.

It defines what this project is, who has authority over what, how AI
collaborators contribute, and what cannot be changed without explicit
human approval.

All collaborators — human and AI — operate within this constitution.

## What This Project Is

SOGA (Subject-Oriented Governance Architecture) is a research and
implementation platform exploring execution-time governance for delegated
authority in human-autonomous systems.

The project makes two independent architectural contributions.

Mission Builder transforms human intent into structured mission
representations. It is protocol-independent. It is adjacent to the
Governance Server. It is not inside it.

The Governance Server evaluates execution-time legitimacy. It consumes
governance-relevant information from multiple sources. It produces ALLOW,
RESTRICT, or DENY. It is protocol-independent. It stands alone.

The long-term vision is not to build smarter agents. The goal is to
create governed teams where humans and autonomous participants collaborate
safely, visibly, and continuously under execution-time authority.

## Authority Structure

Project Lead: Debbie Bucci
- Sole authority over architectural decisions
- Sole authority over what becomes permanent project knowledge
- Final decision on all gate outcomes
- Determines sprint scope and sequencing

Gate 1 Reviewer: Claude
- Architectural conformance review
- Sprint management
- Gate definitions and closeout rulings
- Drafts constitution, architecture, and standards documents

Gate 2 Reviewer: Gemini
- Coherence and demonstration readiness review
- External reviewer interpretation risk assessment
- Cannot unilaterally clear a gate
- Disagreements escalate to Deb

Implementation: CG
- Builds against locked architecture
- Reports repository state
- Submits gate packages
- Does not invent architecture while coding

External Reviewers and Advisors:
Alan Karp, Dick Hardt, Martin, Juan Caballero, Dazza Greenwood, and others
provide feedback and validation. They do not have implementation authority.
Engagement is sequenced by Deb.

## Gate Process

All implementation work passes through a formal gate process.

Gate 1 (Claude): Architectural conformance. Must pass before Gate 2.
Gate 2 (Gemini): Coherence and demonstration readiness. Must pass before
commit.

Both gates must clear before CG commits implementation work.

Every gate submission requires:
- Affected files list
- Regression confirmation at current baseline
- Explicit gate ruling

Disagreements between Gate 1 and Gate 2 escalate to Deb.

## Locked Architectural Positions

These positions are locked. They cannot be changed without a falsifiable
reason, Gate 1 review, and explicit Deb approval.

### The Three-Sentence Foundation

Authentication answers who you are.
Authorization answers what you were permitted to do.
Governance answers whether that authority should still be exercised now.

### Three Governance Outcomes

ALLOW — execution may proceed.
DENY — execution is prohibited.
RESTRICT — execution may not proceed yet. Authority has not been rejected.
First-class outcome with its own lifecycle. Not a degraded ALLOW.

RESTRICT lifecycle:
Notification → Approval or New Evidence → Re-evaluation → Execution

### Subject Agency State

Canonical term: Subject Agency State
Implementation field: subject_agency_state
Five locked states: Independent, Supervised, Managed, Delegated, Lapsed

### The Execution Boundary

The execution boundary is a first-class architectural concept. It is the
explicit interface between Mission Planning and Runtime Governance.

Mission Builder identifies authority-bearing tasks requiring execution.
Runtime/Orchestrator constructs execution requests.
SOGA evaluates execution requests.
Execution Layer carries out or refuses the action.

### Mission Step is Primary

The mission step is the primary governable object.
Protocol artifacts are supporting evidence.
This is a governance claim, not an interoperability claim.

### Decision Package Singularity

For any mission at any execution point there exists exactly one
authoritative Canonical Decision Package. Everything else is evidence.

### Mission ID and Execution Request

Mission ID provides continuity and provenance across the mission.
Execution request is the unit of governance.
These must never be conflated.

### Two Independent Workbenches

Mission Planning Workbench — everything before the execution boundary.
Produces no governance outputs. Knows nothing about governance.

Governance Decision Workbench — everything at the execution boundary.
Evaluates one execution request at a time. Knows nothing about intent
parsing or planning.

### Implementation Continuity Principle

Future sprints replace mock data with real outputs.
They do not redesign the separation.

### Architectural Ownership

Mission Builder owns planning.
Runtime/Orchestrator owns execution requests.
SOGA owns execution-time governance.
Execution Layer owns carrying out or refusing the action.

### Protocol Independence

AAuth, OAuth, GNAP, MCP, Cedar, UCAN, ZCAP may all provide
governance-relevant information. None is required. None is privileged.

## Repository Governance

The repository is not simply source code. It is a governed knowledge base.

Every durable project decision should have:
- Provenance
- Rationale
- Review
- Acceptance
- Version history

The correspondence is explicit:

Conversation → transient evidence
Repository proposal → governance input
Human review → policy decision
Git commit → Canonical Decision Package
Repository state → authoritative execution state

The engineering process embodies the governance architecture it is
constructing.

## Knowledge Stability Layers

Constitution — stable for years. Changes require Gate 1 review and Deb
approval.

Grounding — orientation documents. Updated when project state changes
significantly.

Working — current sprint status and priorities. Updated frequently.

Research — ideas under active investigation. Not yet locked.

Proposals — candidate additions awaiting human review and approval.

Memory — historical record of how the project evolved. Append-only.

## Contribution Protocol

Every significant session answers five questions:

1. What was completed?
2. What was learned?
3. What assumptions changed?
4. What would a future collaborator wish they already knew?
5. Should any of this become repository memory?

If yes to question 5 — propose the file, section, and rationale.
Post to proposals/. Do not modify constitution/ without explicit Deb
approval.

## What Cannot Change Without Explicit Approval

- The three-sentence foundation
- The three governance outcomes and their definitions
- Subject Agency State canonical term and five states
- The execution boundary as a first-class concept
- The two-workbench separation
- The gate process structure
- This constitution

Changes require a falsifiable reason, Gate 1 review, and Deb approval.
