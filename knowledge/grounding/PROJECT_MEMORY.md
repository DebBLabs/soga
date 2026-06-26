# PROJECT MEMORY

**Repository:** soga-clean

**Last Updated:** 2026-06-27

---

# Purpose

This document provides a concise implementation-oriented overview of the project.

Unlike the constitutional documents, this file changes as the project evolves.

Its purpose is to allow a new implementation AI or collaborator to become productive within minutes rather than reconstructing weeks of conversation.

---

# Project Identity

SOGA (Subject-Oriented Governance Architecture)

SOGA introduces execution-time governance for delegated authority.

Authentication answers:

    Who are you?

Authorization answers:

    What are you permitted to do?

SOGA answers:

    Should this authority still be exercised now?

Execution-time governance is independent of authentication, authorization, transport protocols, and AI models.

---

# Primary Components

The implementation currently consists of four major architectural areas.

## Mission Builder

Responsible for transforming human intent into structured mission representations.

Produces execution-ready mission steps.

Does not make governance decisions.

---

## Runtime Governance

Evaluates one execution request at a time.

Produces one governance determination:

- ALLOW
- RESTRICT
- DENY

Consumes evidence from multiple protocol-independent sources.

Produces a Canonical Decision Package.

---

## Execution Layer

Executes only after governance approval.

Receives governance output.

Never determines legitimacy itself.

---

## Canonical Decision Package (CDP)

Authoritative record describing why a governance decision was made.

Evidence may originate from many protocols.

The CDP is protocol-independent.

---

# Current External Integrations

Current integrations include:

- AAuth
- Person Server
- Christian Posta AAuth demonstration
- Runtime execution-boundary interception

Additional protocol adapters remain independent of governance.

---

# Long-Term Direction

Current work supports the larger vision of governed human/autonomous teams.

Future work includes:

- Physical embodiment (Misty)
- Autonomous multi-agent collaboration
- Team presence
- Runtime supervision
- Human authority continuity
- Multi-hop delegated authority

---

# Repository Memory Principle

Conversation is temporary.

Repository knowledge is durable.

Architectural decisions belong in the repository.

Implementation status belongs in the repository.

Conversation should never become the primary source of project memory.

