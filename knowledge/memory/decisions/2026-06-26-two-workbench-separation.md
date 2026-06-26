# Decision: Two-Workbench Architectural Separation
# Date: June 26, 2026
# Status: Locked

## Decision

The SOGA demonstration consists of two independent workbenches separated
by an explicit execution boundary.

Mission Planning Workbench — everything before the execution boundary.
Governance Decision Workbench — everything at the execution boundary.

These are not different views of the same process. They are
visualizations of two separate architectural components.

## Rationale

The original Governance Workbench mixed mission planning information with
runtime governance decisions. This obscured the architecture and implied
SOGA owned the planning layer.

Separation makes two things visible that were previously implicit:

1. SOGA governs execution requests, not missions. A mission may produce
   multiple execution requests. Each is evaluated independently.

2. Mission Builder's responsibility ends when it identifies an
   authority-bearing task requiring execution. The handoff is the
   execution request crossing the execution boundary.

## Implications

Future implementation replaces mock data independently on each side
without changing the architecture or demonstrations.

Mission Planning Workbench eventually consumes real Mission Builder output.
Governance Decision Workbench eventually consumes live runtime execution
requests and generated CDPs.

## Approved by

Debbie Bucci — June 26, 2026
