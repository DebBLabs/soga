# SOGA Architectural Principles
# June 2026

## Principle 1 — Authoring and Evaluation Are Separate

Mission Builder authors mission representations.
Governance Server evaluates execution-time legitimacy.
Neither performs the other's responsibility.

## Principle 2 — Artifact-Based Integration

Communication between Mission Builder and Governance Server occurs
through artifacts.

Mission Builder does not invoke Governance Server.
Governance Server does not invoke Mission Builder.
The Canonical Mission Representation is the handoff artifact.

## Principle 3 — Governance is Origin-Agnostic

Governance Server does not depend on where a mission representation
originated. A CMR may be produced by Mission Builder, AAuth-compatible
systems, enterprise workflow engines, human-authored artifacts, or other
conformant systems. Governance evaluation is independent of artifact
origin.

## Principle 4 — No Predictive Governance

Mission Builder does not perform governance evaluation.
It does not pre-flight missions against Governance Server policy.
Execution-time legitimacy is determined only at the execution boundary.

## Principle 5 — Peer Inputs

Mission context is one input to governance. Delegation evidence,
authorization context, capability context, policy inputs, Subject Agency
State, runtime conditions, and the execution request are peer inputs.
No single source is privileged.

## Principle 6 — Separation of Concerns

This architecture separates concerns, not deployment models.

Mission Builder and Governance Server may be deployed together or
independently. The reference implementation separates them because the
architectural boundaries became clearer through implementation.

No architectural requirement is implied regarding deployment topology.

## Principle 7 — Implementation Continuity

The UI separation established between Mission Planning Workbench and
Governance Decision Workbench is the target interface.

Future sprints replace mock data with real outputs.
They do not redesign the separation.

## Principle 8 — RESTRICT is First-Class

RESTRICT is not a degraded ALLOW.
RESTRICT is a governed state that preserves mission continuity while
preventing inappropriate execution.
RESTRICT has its own lifecycle:
Notification → Approval or New Evidence → Re-evaluation → Execution

## Principle 9 — The Execution Boundary is Explicit

The execution boundary is the stable interface between systems.
It is not cosmetic. It is not implied. It is the first-class architectural
concept that separates planning from governance.

## Principle 10 — Falsification Over Confirmation

Any proposed schema addition or architectural change requires
demonstrating a concrete wrong Decision Package the change would correct.
Attack the methodology. Do not defend it.

## Canonical Architecture

Human Intent
      │
      ▼
Mission Builder
(independent adjacent contribution)
(protocol-independent)
      │
      ▼
Canonical Mission Representation
(objective, actors, constraints,
authority requirements,
governance requirements)
      │
      └─────────────────────────────┐
                                    │
Authorization / Delegation /        │
Capability / Policy / Workflow      │
Systems                             │
(AAuth, OAuth, GNAP, MCP,          │
Cedar, UCAN, ZCAP)                 │
      │                             │
      ▼                             ▼
Governance-Relevant Information
(mission context, delegation evidence,
authorization context, capability context,
Subject Agency State, runtime conditions,
policy inputs, execution request)
      │
══════════════════════════════════════
EXECUTION BOUNDARY
══════════════════════════════════════
      │
      ▼
SOGA Governance Server
(independent adjacent contribution)
(protocol-independent)
      │
      ▼
ALLOW / RESTRICT / DENY
+ Canonical Decision Package
      │
      ▼
Execution Layer
(responsibility of host environment)

## Runtime Behavior

A mission may produce multiple execution requests.
Each is evaluated independently.
Each produces its own Canonical Decision Package.
Governance may never see the complete mission.

Example:
Mission
├── Task A → Execution Request → CDP → ALLOW
├── Task B → Execution Request → CDP → DENY
├── Task C → Execution Request → CDP → RESTRICT
└── Task D → Execution Request → CDP → ALLOW

## Migration Note

The original architecture used a single pipeline:
Human Intent → Mission → SOGA → Execution

Three discoveries during implementation forced the separation:

Discovery 1: Mission Builder is useful without Governance Server.
Discovery 2: Governance Server is useful without Mission Builder.
Discovery 3: Multiple systems feed governance simultaneously.

The separation is separation of concerns, not required separation of
services.

## Invariant 1 — The Decoupling Invariant

SOGA gates execution, not token creation.

Offline token minting agility is explicitly preserved. Agents may mint
capability tokens completely offline. SOGA intercepts at the execution
boundary, not at the token creation boundary. The offline token arrives
as evidence. Governance evaluates at execution time.

## Invariant 2 — The Singularity Invariant

One execution event maps to exactly one Canonical Decision Package.

One execution event → one governance evaluation → one CDP.
This is terminal. There is no partial CDP. There is no aggregate CDP
across multiple execution events. Everything else is evidence.

## Invariant 3 — The Telemetry Invariant

Structural protocol elements are consumed strictly as incoming authority
evidence.

AAuth, UCAN, ZCAP, and equivalent delegation artifacts are evidence
inputs to the governance evaluation. They are not self-contained
governance decisions. The protocol does not decide. The Governance
Server decides.
