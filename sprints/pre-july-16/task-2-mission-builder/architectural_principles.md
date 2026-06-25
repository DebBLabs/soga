# Architectural Principles

## Mission Builder, Runtime, and Governance Server

## Pre-July-16 Track

## Principle 1 - Authoring and Evaluation are Separate

Mission Builder authors mission plans.

SOGA Governance Server evaluates execution-time legitimacy.

Neither performs the other's responsibility.

Mission Builder does not perform governance evaluation.

SOGA does not author missions.

---

## Principle 2 - Mission Builder Stops Before the Execution Boundary

Mission Builder transforms human intent into a mission plan.

The mission plan may include:

- Mission ID
- Objectives
- Actors
- Constraints
- Task list
- Capability requirements
- Authority-bearing tasks identified

Mission Builder identifies tasks that may require delegated authority.

Mission Builder does not execute those tasks.

Mission Builder does not create governance determinations.

Mission Builder does not invoke SOGA.

---

## Principle 3 - Runtime Owns the Mission Loop

The host runtime or orchestrator owns the mission loop.

The runtime may be supplied by:

- Compaia
- an enterprise application
- an agent framework
- an A2A runtime
- a workflow engine
- another host environment

The runtime decides when a planned task becomes an execution attempt.

The runtime constructs execution requests.

The runtime reaches the execution boundary.

SOGA does not own or implement orchestration.

AAuth does not own or implement orchestration.

---

## Principle 4 - Execution Requests are the Unit of Governance

SOGA evaluates execution requests.

SOGA does not evaluate complete missions.

An execution request represents one attempted action at runtime.

Representative execution request inputs include:

- Mission ID
- Task action
- Delegation evidence
- Authorization context
- Capability context
- Subject Agency State
- Runtime conditions
- Policy inputs

Mission ID may be retained for traceability.

Mission ID does not make SOGA a mission planner.

---

## Principle 5 - Governance is Origin-Agnostic

SOGA does not depend on where mission context or evidence originated.

Inputs may come from:

- Mission Builder
- AAuth-compatible systems
- UCAN
- ZCAP
- OAuth
- GNAP
- MCP
- enterprise workflow engines
- human-authored artifacts
- other conformant systems

These inputs are evidence.

They do not become SOGA.

They do not become the runtime.

They do not determine the governance result by themselves.

---

## Principle 6 - No Predictive Governance

Mission Builder does not pre-flight missions against SOGA policy.

Mission Builder does not predict governance outcomes.

Execution-time legitimacy is determined only when an execution request reaches the execution boundary.

A task that appears allowable during planning may be restricted or denied at execution time.

A task that appears blocked during planning may require a new grant before it can generate a valid execution request.

---

## Principle 7 - Peer Inputs

Mission context is one input to governance.

Delegation evidence, authorization context, capability context, policy inputs, Subject Agency State, runtime conditions, and the execution request are peer inputs.

No single source is privileged.

No single source is sufficient by itself.

---

## Principle 8 - Implementation Continuity

The Mission Planning Workbench and Governance Decision Workbench express the target architectural separation.

Future sprints should replace mock data with real outputs.

Future sprints should not redesign the separation.

Mission Planning Workbench eventually consumes real Mission Builder output.

Governance Decision Workbench eventually consumes live execution requests and generated CDPs.

The interface separation is stable.

---

## Principle 9 - Separation of Concerns

This architecture separates concerns, not deployment models.

Mission Builder, runtime, SOGA Governance Server, and execution layer may be deployed together or independently.

The reference implementation separates them because the architectural boundaries became clearer through implementation.

No architectural requirement is implied regarding deployment topology.

---

## Implementation Guidance

The Mission Planning Workbench ends before the execution boundary.

The Governance Decision Workbench begins at the execution boundary.

The workbenches are not two views of the same component.

They visualize two different architectural responsibilities.

The Mission Planning Workbench should show:

- Human Intent
- Mission ID
- Mission construction
- Task decomposition
- Capability identification
- Authority-bearing task identification

The Governance Decision Workbench should show:

- Execution request
- Mission ID for traceability
- Runtime evidence
- Subject Agency State
- Governance determination
- Canonical Decision Package
- Execution receipt

Each governance entry represents one execution-time evaluation.

Multiple entries may belong to the same mission.

They are not possible outcomes for the same request.

They are separate decisions for separate execution requests.
