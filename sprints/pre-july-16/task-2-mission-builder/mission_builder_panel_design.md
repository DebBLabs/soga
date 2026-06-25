# Mission Builder Panel Design

## Purpose

This file defines the visual design for the Notional Mission Builder panel in the Governance Workbench.

The panel is presentation only.

It does not add governance logic.

It does not add Mission Builder functionality.

It makes the architectural boundary visible.

## Reviewer Goal

A reviewer should be able to understand the following in less than two minutes:

- Human intent is authored before governance.
- Mission Builder is an independent adjacent contribution.
- Mission Builder produces a Canonical Mission Representation (CMR).
- The CMR is one peer input into Governance-Relevant Information.
- Delegation evidence and Subject Agency State also contribute.
- SOGA Governance Server evaluates at the execution boundary.
- Governance Server produces ALLOW, RESTRICT, or DENY.

## Required Label

Mission Builder - independent adjacent contribution.

Produces mission context consumed by the Governance Server alongside delegation evidence, authorization context, policy inputs, capability context, Subject Agency State, runtime conditions, and the execution request.

## Visual Model

The panel must not render Mission Builder as a straight pipeline into SOGA.

The panel must show convergence.

Conceptually the reviewer should see:

Human Intent

    |

Mission Builder

    |

Canonical Mission Representation

        +

Delegation Evidence

        +

Subject Agency State

        +

Other Governance-Relevant Inputs

        |

Governance-Relevant Information

        |

SOGA Governance Server

        |

ALLOW / RESTRICT / DENY

## Caregiver Scenario

### Human Intent

"My caregiver may coordinate my daily care while I recover from surgery."

### Notional Mission Builder Output

- Objective: Coordinate daily care during recovery
- Subject: Patient
- Delegate: Caregiver
- Allowed actions:
  - Schedule appointments
  - Coordinate transportation
  - Purchase approved items
- Prohibited actions:
  - Authorize treatment
  - Transfer assets
  - Change beneficiaries
- Governance requirement:
  - Evaluate at execution time

### Representative Governance Inputs

- Canonical Mission Representation
- Delegation Evidence
- Subject Agency State

## Multi-Hop Scenario

### Human Intent

"Alice delegates appointment coordination to Beth. Beth delegates scheduling execution to a Care Agent."

### Notional Mission Builder Output

- Objective: Schedule cardiology appointment
- Subject: Alice
- Delegates:
  - Beth
  - Care Agent
- Allowed actions:
  - Schedule appointment
- Prohibited actions:
  - Authorize treatment
  - Change medication
  - Access unrelated records
- Governance requirement:
  - Evaluate at execution time

### Representative Governance Inputs

- Canonical Mission Representation
- Delegation Evidence
- Subject Agency State

## Explicit Non-Goals

The panel must not imply:

- Mission Builder is inside SOGA.
- SOGA requires Mission Builder.
- Mission Builder calls the Governance Server.
- Mission Builder performs predictive governance.
- Mission Builder approves or denies missions.
- Governance Server manages execution.
- Any protocol is required.

## Future Evolution

The Mission Builder shown in the Governance Workbench is intentionally a static architectural illustration.

Its purpose is to show where structured mission authoring occurs before execution-time governance.

Future work may implement Mission Builder as an interactive component capable of transforming natural language, structured input, or conversational interaction into a Canonical Mission Representation (CMR).

The Governance Server architecture does not change.

Mission Builder and Governance Server remain independent contributions connected through governance-relevant artifacts rather than direct service calls.

## Implementation Rules

- Static panel only.
- No interactive input.
- No new governance logic.
- No new protocol logic.
- No changes to regression baseline.
- Existing governance flow continues unchanged below the panel.
- Panel appears only for the caregiver and multi-hop scenarios.
