# Mission Builder Panel Design
## Purpose
This file defines the visual design for the Notional Mission Builder panel in the Governance Workbench.
The panel is presentation only.
It does not add governance logic.
It does not add Mission Builder functionality.
It makes the architectural boundary visible.
## Reviewer Goal
A reviewer should be able to see the following in under two minutes:
- Human intent is authored before governance.
- Mission Builder is an independent adjacent contribution.
- Mission Builder produces a Canonical Mission Representation.
- The CMR is one peer input into Governance-Relevant Information.
- Delegation evidence and Subject Agency State also contribute.
- SOGA Governance Server evaluates at the execution boundary.
- Governance Server produces ALLOW, RESTRICT, or DENY.
## Required Label
The panel must include this label:
Mission Builder - independent adjacent contribution. Produces mission context consumed by the Governance Server alongside delegation evidence, authorization context, policy inputs, capability context, Subject Agency State, runtime conditions, and the execution request.
## Visual Model
The panel must not render Mission Builder as a straight pipeline into SOGA.
The panel must show convergence.
Required conceptual layout:
Human Intent
    |
    v
Mission Builder
    |
    v
Canonical Mission Representation
Canonical Mission Representation
Delegation Evidence
Subject Agency State
Other Governance-Relevant Inputs
    |
    v
Governance-Relevant Information
    |
    v
SOGA Governance Server
    |
    v
ALLOW / RESTRICT / DENY
## Caregiver Scenario Content
Human Intent:
My caregiver may coordinate my daily care while I recover from surgery.
Notional Mission Builder output:
- Objective: coordinate daily care during recovery
- Subject: Subject
- Delegate: caregiver
- Allowed actions: schedule appointment, purchase gift
- Forbidden actions: authorize treatment, transfer assets, change beneficiary
- Governance requirement: evaluate at execution time
Representative peer inputs:
- CMR: bounded caregiver support
- Delegation Evidence: caregiver authority for daily care coordination
- Subject Agency State: current runtime state
## Multi-Hop Scenario Content
Human Intent:
Alice delegates appointment coordination to Beth, and Beth delegates scheduling execution to a care agent.
Notional Mission Builder output:
- Objective: schedule cardiology appointment for Alice
- Subject: Alice
- Delegates: Beth, care agent
- Allowed action: schedule appointment
- Forbidden actions: authorize treatment, change medication, access unrelated records
- Governance requirement: evaluate at execution time
Representative peer inputs:
- CMR: schedule cardiology appointment
- Delegation Evidence: Alice to Beth, Beth to care agent
- Subject Agency State: current runtime state
## Explicit Non-Goals
The panel must not imply:
- Mission Builder is inside SOGA.
- SOGA requires Mission Builder.
- Mission Builder calls Governance Server.
- Mission Builder performs predictive governance.
- Mission Builder approves or denies missions.
- Governance Server manages execution.
- Any protocol is required.
## Implementation Rules
- Static panel only.
- No interactive input.
- No new governance logic.
- No new protocol logic.
- No changes to regression baseline.
- Existing governance flow must continue unchanged below the panel.
- Panel appears only for caregiver and multi_hop scenarios.
