# Architectural Principles — Mission Builder and Governance Server
## Pre-July-16 Track Addendum

## Canonical Mission Representation (CMR)

The Canonical Mission Representation (CMR) is the architectural handoff between intent authoring and execution-time governance.

Mission Builder produces a CMR.

The Governance Server consumes governance-relevant information, which may include a CMR together with delegation evidence, authorization context, capability context, policy inputs, Subject Agency State, runtime conditions, and the execution request.

The CMR is an artifact, not a service interface.

---

## Principle 1 — Authoring and Evaluation are Separate

Mission Builder authors mission representations.

Governance Server evaluates execution-time legitimacy.

Neither performs the other's responsibility.

---

## Principle 2 — Artifact-Based Integration

Communication between Mission Builder and Governance Server occurs through artifacts.

Mission Builder does not invoke the Governance Server.

Governance Server does not invoke the Mission Builder.

---

## Principle 3 — Governance is Origin-Agnostic

The Governance Server does not depend on where a mission representation originated.

A CMR may be produced by:

- Mission Builder
- AAuth-compatible systems
- Enterprise workflow engines
- Human-authored artifacts
- Other conformant systems

Governance evaluation is independent of artifact origin.

---

## Principle 4 — No Predictive Governance

Mission Builder does not perform governance evaluation.

It does not pre-flight missions against Governance Server policy.

Execution-time legitimacy is determined only at the execution boundary.

---

## Principle 5 — Peer Inputs

Mission context is one input to governance.

Delegation evidence, authorization context, capability context, policy inputs, Subject Agency State, runtime conditions, and the execution request are peer inputs.

No single source is privileged.

---

## Principle 6 — Separation of Concerns

This architecture separates concerns, not deployment models.

Mission Builder and Governance Server may be deployed together or independently.

The reference implementation separates them because the architectural boundaries became clearer through implementation.

No architectural requirement is implied regarding deployment topology.

---

## Implementation Guidance

The Mission Builder panel ends with the Canonical Mission Representation (CMR).

The Governance panel begins with Governance-Relevant Information.

The CMR is shown as one contributor among several, converging with delegation evidence, authorization context, policy inputs, capability context, Subject Agency State, runtime conditions, and the execution request before reaching the Governance Server.

This visual separation reinforces that Mission Builder and Governance Server are independent adjacent contributions connected through artifacts rather than direct service coupling.
