# KNOWLEDGE

## Purpose

The `knowledge/` directory is the durable institutional memory of the SOGA project.

Conversation history is temporary working memory.

The repository is the permanent source of truth.

Every AI collaborator should initialize here before making architectural or implementation decisions.

This repository intentionally governs itself using the same principles that SOGA applies to execution-time governance.

---

## Directory Layout

    knowledge/
    ├── README.md
    ├── constitution/
    ├── grounding/
    ├── working/
    ├── research/
    ├── proposals/
    └── memory/
        ├── decisions/
        ├── discoveries/
        ├── milestones/
        └── retrospectives/

---

## Directory Responsibilities

constitution/

    Long-lived architectural truth.

    Contains:

    • Project Constitution
    • Architecture Principles

    Changes require explicit approval from Deb.

---

grounding/

    Orientation for every new collaborator.

    Contains:

    • Session Bootstrap
    • Project Memory
    • High-level project overview

    A new AI session should read this directory first.

---

working/

    Operational status.

    Frequently updated.

    Contains:

    • Current implementation state
    • Current sprint
    • Immediate priorities
    • Active engineering work

---

research/

    Engineering notebook.

    Contains:

    • discoveries
    • experiments
    • design notes
    • implementation observations

Ideas remain here until accepted or rejected.

---

proposals/

    Candidate architectural or implementation changes.

    AI collaborators should propose significant changes here before implementation whenever appropriate.

---

memory/

    Permanent project history.

    Subdirectories:

    decisions/
        Accepted architectural decisions.

    discoveries/
        Significant technical discoveries.

    milestones/
        Major accomplishments.

    retrospectives/
        Sprint and project reflections.

Memory entries should be append-only whenever practical.

---

## Ownership

Deb

    Project Lead

    Final architectural authority.

    Final approval for permanent repository knowledge.

Claude

    Gate 1

    Architecture

    Constitution

    Repository governance

    Memory curation

Gemini

    Gate 2

    External coherence

    Demonstration readiness

    Reviewer perspective

ChatGPT (CG)

    Implementation

    Engineering

    Repository maintenance

    Working state

    Research documentation

---

## Repository Governance

Repository governance is an intentional application of SOGA principles.

Research Process

    Conversation

↓

    Repository Proposal

↓

    Human Review

↓

    Git Commit

↓

    Repository State

Equivalent SOGA Concepts

    Evidence

↓

    Governance Input

↓

    Policy Decision

↓

    Canonical Decision Package

↓

    Authoritative State

The engineering process intentionally mirrors the runtime governance architecture.

---

## Information Flow

Conversation produces ideas.

Research captures observations.

Proposals capture candidate changes.

Human review determines acceptance.

Implementation follows approved direction.

Memory records the result.

Git preserves the historical record.

---

## Stability Levels

Constitution

    Rarely changes.

Grounding

    Updated when project understanding changes.

Working

    Updated frequently.

Research

    Updated continuously.

Proposals

    Temporary until resolved.

Memory

    Permanent historical record.

---

## Operating Rule

No important architectural decision should exist only inside a conversation.

At the end of meaningful work every collaborator should ask:

    "Where should this live in the repository?"

If the answer is nowhere, the conversation may end.

If the answer is somewhere, create or update the appropriate repository document before considering the work complete.

---

## Guiding Principle

Conversation accelerates development.

The repository preserves knowledge.

Git preserves history.

The repository—not conversation—is the authoritative memory of the project.

