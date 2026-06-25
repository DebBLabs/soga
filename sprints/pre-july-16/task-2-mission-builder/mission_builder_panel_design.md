# Mission Builder Panel Design

## Purpose

This file defines the visual design for the Notional Mission Builder panel in the Governance Workbench.

The panel is presentation only.

It does not add governance logic.

It does not add Mission Builder functionality.

It makes the execution flow visible.

## Reviewer Goal

A reviewer should be able to understand the following in less than two minutes:

- Human intent is authored before governance.
- Mission Builder is an independent adjacent contribution.
- Mission Builder produces a mission plan with one or more tasks.
- Each task may require capabilities, delegation, governance, or none of these.
- SOGA does not evaluate the whole mission.
- SOGA evaluates delegated task execution when governance is required.
- AAuth, MCP, policy, and runtime state may provide inputs at the task boundary.
- Governance Server produces ALLOW, RESTRICT, or DENY before execution.

## Required Label

Mission Builder - independent adjacent contribution.

Produces a mission plan and task list. SOGA does not evaluate the whole mission. SOGA evaluates delegated task execution when governance is required.

## Visual Model

The panel must not render Mission Builder as a straight pipeline into SOGA.

The panel must show task routing.

Conceptually the reviewer should see:

Human Intent

    |

Mission Builder

    |

Mission Plan / Task List

    |

Task Routing

    |-- Task does not require delegated authority -> execute through host environment

    |-- Task requires capability -> select MCP/tool/API

    |-- Task requires delegated authority -> gather delegation evidence

    |-- Task requires governance -> SOGA evaluates at execution boundary

    |

Governance-Relevant Task Execution

    |

SOGA Governance Server

    |

ALLOW / RESTRICT / DENY

## Caregiver Scenario

### Human Intent

"My caregiver may coordinate my daily care while I recover from surgery."

### Notional Mission Plan

- Task: Schedule follow-up appointment
  - Capability: calendar / scheduling
  - Delegation: required
  - Governance: required

- Task: Coordinate transportation
  - Capability: transportation service
  - Delegation: required
  - Governance: required

- Task: Purchase approved items
  - Capability: shopping / payment
  - Delegation: required
  - Governance: required

- Task: Authorize treatment
  - Capability: clinical authorization
  - Delegation: not permitted
  - Governance: deny if attempted

### Representative Governance Inputs

- Task context
- Delegation Evidence
- Subject Agency State

## Multi-Hop Scenario

### Human Intent

"Alice delegates appointment coordination to Beth. Beth delegates scheduling execution to a Care Agent."

### Notional Mission Plan

- Task: Schedule cardiology appointment
  - Capability: scheduling
  - Delegation: required
  - Governance: required

- Task: Notify Alice or Beth
  - Capability: messaging
  - Delegation: may be required
  - Governance: context dependent

- Task: Authorize treatment
  - Capability: clinical authorization
  - Delegation: not permitted
  - Governance: deny if attempted

- Task: Change medication
  - Capability: medication management
  - Delegation: not permitted
  - Governance: deny if attempted

### Representative Governance Inputs

- Task context
- Delegation Evidence
- Subject Agency State

## Explicit Non-Goals

The panel must not imply:

- Mission Builder is inside SOGA.
- SOGA requires Mission Builder.
- SOGA evaluates the entire mission at mission-authoring time.
- Mission Builder calls the Governance Server.
- Mission Builder performs predictive governance.
- Mission Builder approves or denies missions.
- Governance Server manages execution.
- Any protocol is required.

## Future Evolution

The Mission Builder shown in the Governance Workbench is intentionally a static architectural illustration.

Future work may implement Mission Builder as an interactive component capable of transforming natural language, structured input, or conversational interaction into a mission plan and task list.

Future task planning may identify capabilities, MCP tools, delegation requirements, and governance-relevant execution boundaries.

The Governance Server architecture does not change.

Mission Builder and Governance Server remain independent contributions connected through task-level governance-relevant artifacts rather than direct service calls.

## Implementation Rules

- Static panel only.
- No interactive input.
- No new governance logic.
- No new protocol logic.
- No changes to regression baseline.
- Existing governance flow continues unchanged below the panel.
- Panel appears only for the caregiver and multi-hop scenarios.
