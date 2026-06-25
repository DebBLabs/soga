# SOGA Canonical Architecture

## June 2026

## Purpose

This document defines the canonical architecture for the Pre-July-16 Track.

The architecture separates two independent contributions:

- Mission Builder
- SOGA Governance Server

They can be used together or independently.

## Canonical Architecture

Human Intent
    |
    v
Mission Builder
(independent adjacent contribution)
(protocol-independent)
(not part of Governance Server)
    |
    v
Canonical Mission Representation (CMR)
(objective, actors, constraints,
authority requirements,
governance requirements)
    |
    +------------------------------+
                                   |
Authorization / Delegation /       |
Capability / Policy / Workflow     |
Systems                            |
    |                              |
    v                              v
Governance-Relevant Information
(mission context,
delegation evidence,
authorization context,
capability context,
Subject Agency State,
runtime conditions,
policy inputs,
execution request)
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
Execution
(responsibility of host environment)

## Mission Builder

Mission Builder transforms human intent into a Canonical Mission Representation.

Mission Builder structures:

- Purpose
- Objectives
- Actors
- Constraints
- Authority requirements
- Governance requirements

Mission Builder answers:

What is this mission and what does it require?

Mission Builder does not evaluate whether a mission should execute.

Mission Builder does not invoke the Governance Server.

Mission Builder is an authoring component, not an approval component.

## Canonical Mission Representation

The Canonical Mission Representation is the handoff artifact produced by Mission Builder.

The CMR may be consumed by governance systems, authorization systems, delegation systems, enterprise workflows, or other conformant systems.

The CMR is an artifact.

It is not a service interface.

## Governance Server

The SOGA Governance Server evaluates execution-time legitimacy.

The Governance Server answers:

Should this authority be exercised now?

The Governance Server consumes governance-relevant information regardless of origin.

It produces a Canonical Decision Package containing exactly one governance determination:

- ALLOW
- RESTRICT
- DENY

The Governance Server does not author missions.

The Governance Server does not manage execution.

The Governance Server does not invoke Mission Builder.

## Governance-Relevant Information

Governance evaluation uses peer inputs.

Representative inputs include:

- Canonical Mission Representation
- Delegation evidence
- Authorization context
- Capability context
- Subject Agency State
- Runtime conditions
- Policy inputs
- Execution request

No single input is privileged.

No single input is required.

## Example Input Sources

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

## Execution Boundary

The Governance Server sits at the execution boundary.

It produces a governance determination before execution occurs.

Execution is the responsibility of the consuming environment.

SOGA evaluates legitimacy.

SOGA does not execute actions.

SOGA does not orchestrate agents.

SOGA does not issue credentials.

## Three-Sentence Foundation

Authentication answers who you are.

Authorization answers what you were permitted to do.

Governance answers whether that authority should still be exercised now.

## Migration Note

The original architecture described a single pipeline:

Human Intent -> Mission -> SOGA -> Execution

That framing was useful during early development but implied that SOGA owned the full path from intent to execution.

Implementation and external review demonstrated that three concerns are distinct:

- Intent authoring
- Authority and delegation evidence
- Execution-time legitimacy evaluation

Mission Builder is useful without Governance Server.

Governance Server is useful without Mission Builder.

Multiple systems can feed governance simultaneously.

The separation is separation of concerns, not required separation of services.
