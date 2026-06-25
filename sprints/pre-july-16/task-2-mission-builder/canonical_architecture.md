# SOGA Canonical Architecture

## June 2026

## Purpose

This document defines the canonical architecture for the Pre-July-16 Track.

The architecture separates three responsibilities:

- Mission Builder
- Host Runtime / Orchestrator
- SOGA Governance Server

The execution boundary is a first-class architectural concept.

They may be deployed together or independently.

---

## Canonical Architecture

Human Intent
    |
    v
Host Application
(Compaia, enterprise application,
agent runtime, workflow engine,
or other host environment)
    |
    v
Mission Builder
(independent adjacent contribution)
(protocol-independent)
(not part of Governance Server)
    |
    v
Mission Plan
(mission_id, objectives, actors,
constraints, task list,
capability requirements,
authority-bearing tasks identified)
    |
    v
Runtime / Orchestrator
(mission loop supplied by host environment)
    |
    v
Execution Request
(one attempted action plus runtime evidence)
    |
    v
══════════════════════════════════════════════
              EXECUTION BOUNDARY
══════════════════════════════════════════════
    |
    v
SOGA Governance Server
(independent adjacent contribution)
(protocol-independent)
(not part of Mission Builder)
    |
    v
Canonical Decision Package (CDP)
(governance determination:
ALLOW, RESTRICT, or DENY)
    |
    v
Host Application / Execution Layer
(carries out or refuses the action)

---

## Mission Builder

Mission Builder transforms human intent into a mission plan.

Mission Builder structures:

- Purpose
- Objectives
- Actors
- Constraints
- Task list
- Capability requirements
- Authority-bearing tasks

Mission Builder answers:

What is this mission and what does it require?

Mission Builder does not evaluate whether a task should execute.

Mission Builder does not invoke the Governance Server.

Mission Builder does not own the mission loop.

Mission Builder stops before the execution boundary.

---

## Runtime / Orchestrator

The host runtime or orchestrator owns the mission loop.

The runtime decides when a planned task becomes an execution attempt.

The runtime may be supplied by:

- Compaia
- an enterprise application
- an agent framework
- an A2A runtime
- a workflow engine
- another host environment

The runtime constructs execution requests.

The runtime reaches the execution boundary.

SOGA does not own or implement orchestration.

AAuth does not own or implement orchestration.

---

## Execution Request

An execution request is the unit of work presented for execution-time governance.

It represents one attempted action at runtime.

Representative inputs include:

- Mission ID
- Task action
- Delegation evidence
- Authorization context
- Capability context
- Subject Agency State
- Runtime conditions
- Policy inputs

Mission ID is retained for traceability.

Mission ID does not make SOGA a mission planner.

---

## Execution Boundary

The execution boundary is the architectural point at which a planned task becomes an attempted action.

It is the final opportunity to evaluate whether delegated authority should be exercised before execution occurs.

SOGA evaluates execution requests at this boundary.

SOGA evaluates legitimacy.

SOGA does not execute actions.

SOGA does not orchestrate agents.

SOGA does not issue credentials.

---

## SOGA Governance Server

The SOGA Governance Server evaluates execution-time legitimacy.

The Governance Server answers:

Should this delegated authority be exercised now?

The Governance Server consumes governance-relevant information regardless of origin.

It produces a Canonical Decision Package containing exactly one governance determination:

- ALLOW
- RESTRICT
- DENY

The Governance Server does not author missions.

The Governance Server does not manage execution.

The Governance Server does not invoke Mission Builder.

The Governance Server does not require the complete mission.

---

## Canonical Decision Package

Each governance evaluation produces one Canonical Decision Package.

A CDP records the decision for one execution request at one point in time.

A CDP is not the result of a complete mission.

One mission may produce multiple CDPs.

---

## Runtime Behavior

One mission may produce multiple independent execution requests.

Mission

├── Task A → Execution Request → CDP → ALLOW
├── Task B → Execution Request → CDP → DENY
├── Task C → Execution Request → CDP → RESTRICT
└── Task D → Execution Request → CDP → ALLOW

Each execution request is evaluated independently.

Governance may never see the complete mission.

Mission ID may be retained solely for traceability.

---

## Architectural Ownership

Mission Builder

- Owns planning
- Produces the mission plan
- Identifies authority-bearing tasks

Runtime / Orchestrator

- Owns the mission loop
- Issues execution requests
- Reaches the execution boundary

SOGA Governance Server

- Owns execution-time governance
- Produces Canonical Decision Packages

Execution Layer

- Owns carrying out or refusing the action
- Implements ALLOW, RESTRICT, or DENY

For RESTRICT, the host environment may hold, narrow, delay, supervise, escalate, or refuse according to the restriction mode.

---

## Governance-Relevant Information

Governance evaluation uses peer inputs.

Representative inputs include:

- Mission ID
- Task action
- Delegation evidence
- Authorization context
- Capability context
- Subject Agency State
- Runtime conditions
- Policy inputs

No single input is privileged.

No single input is required.

Delegation systems such as AAuth, UCAN, ZCAP, OAuth, or GNAP may provide evidence to the execution request.

They do not become the runtime.

They do not become SOGA.

---

## Protocol Independence

The architecture is protocol-independent.

Example ecosystems include:

Authorization:

- OAuth
- GNAP

Delegation:

- AAuth
- UCAN
- ZCAP

Capability:

- MCP

Policy:

- Cedar

Workflow:

- Enterprise workflow systems

These are examples only.

None is required.

None is privileged.

---

## Three-Sentence Foundation

Authentication answers who you are.

Authorization answers what you were permitted to do.

Governance answers whether delegated authority should still be exercised now.

---

## Migration Note

The original architecture described a single pipeline:

Human Intent -> Mission -> SOGA -> Execution

That framing was useful during early development but implied that SOGA owned the full path from intent to execution.

Implementation and external review demonstrated that four concerns are distinct:

- Intent authoring
- Mission loop / orchestration
- Authority and delegation evidence
- Execution-time legitimacy evaluation

Mission Builder is useful without Governance Server.

Governance Server is useful without Mission Builder.

The runtime/orchestrator may be supplied by any host environment.

Multiple systems can feed governance simultaneously.

The separation is separation of concerns, not required separation of services.
