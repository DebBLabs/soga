# Canonical Caregiver Scenario

Status: Draft

Purpose:

Demonstrate the RESTRICT lifecycle using a mission involving Alice and Beth.

---

## Actors

Subject:
Alice

Delegate:
Beth

Relationship:
Beth is Alice's caregiver.

Delegate Role:
Caregiver Delegate

---

## Subject State

Subject Agency State:
SUPERVISED

Meaning:

Alice can participate, but this mission step requires caregiver approval before execution.

---

## Mission

Mission:
Purchase Birthday Gift

Purpose:

Alice wants her granddaughter's birthday gift purchased and delivered on time.

Objective:

Allow Beth to complete the purchase on Alice's behalf while preserving Alice's participation and oversight.

Why Delegation Exists:

The delegation is not for general purchasing authority.

The delegation exists for a specific purpose: completing a birthday gift purchase for Alice's granddaughter.

Mission Context:

The purpose of the mission remains visible throughout governance evaluation. Authority evidence explains what may be done. Mission context explains why the authority was delegated.

---

## Governed Mission Step

Step:
Complete Purchase

Authority Requirement:

Bounded purchasing authority on behalf of Alice.

Authority Evidence:

To be supplied by existing proof output.

Authority Rationale:

The delegate is attempting to exercise limited purchasing authority for Alice.

---

## Expected Governance Flow

1. Mission is created.
2. Authority evidence is presented.
3. Alice's Subject Agency State is evaluated as SUPERVISED.
4. Governance PDP issues RESTRICT.
5. Execution enters HOLDING.
6. Beth approval is recorded.
7. Governance re-evaluates.
8. New CDP issues ALLOW.
9. Execution proceeds.

---

## Expected Output

Initial Decision:

RESTRICT

Restriction Reason:

Caregiver approval required.

Execution State:

HOLDING

Post-Approval Decision:

ALLOW

Post-Approval Execution State:

EXECUTING
