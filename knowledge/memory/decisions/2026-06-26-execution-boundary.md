# Decision: Execution Boundary as First-Class Architectural Concept
# Date: June 26, 2026
# Status: Locked

## Decision

The execution boundary is a first-class architectural concept.

It is the explicit interface between Mission Planning and Runtime
Governance. It defines exactly what crosses between systems: the
authority-bearing execution request.

## What Crosses the Boundary

From Mission Planning to Governance:
- Mission ID (traceability and provenance only)
- Execution request (the unit of governance)
- Runtime context

The execution request is the unit of governance.
The Mission ID is not the unit of governance.
These must never be conflated.

## Architectural Ownership at the Boundary

Mission Builder owns planning.
Runtime/Orchestrator owns execution requests.
SOGA owns execution-time governance.
Execution Layer owns carrying out or refusing the action.

## Validation

The AAuth integration confirmed this boundary exists as a natural seam
in the christian-posta/aauth-full-demo repository. The runtime naturally
constructs an execution request immediately before agent invocation,
matching the architecture locked today.

## Approved by

Debbie Bucci — June 26, 2026
