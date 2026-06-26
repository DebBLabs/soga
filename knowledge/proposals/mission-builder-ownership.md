# Mission Builder Ownership

Date: 2026-06-27

Status: Proposed

Author: Claude / Deb / CG

---

## Problem

The repository currently treats Mission Packages as input to SOGA, while also containing mission generation, mission intake, and Mission Builder components.

As the architecture matures, the ownership boundary between Compaia, Mission Builder, and SOGA needs to be explicit.

If this is not resolved, future implementation may accidentally collapse human intent capture, mission construction, and runtime governance into one layer.

---

## Architectural Question

Who owns mission creation?

Questions to resolve:

- Does SOGA own only the Mission Package schema and contract?
- Does Compaia own the Mission Builder and user-facing mission construction?
- Is Mission Builder a reusable component that other applications could use to generate SOGA-compatible Mission Packages?

---

## Proposed Working Assumption

Compaia owns:

- human intent capture
- user-facing mission construction
- planning experience
- orchestration experience
- Team Presence interaction model

SOGA owns:

- Mission Package specification
- Mission Package validation requirements
- runtime governance evaluation
- Canonical Decision Package generation
- ALLOW / RESTRICT / DENY determinations

Mission Builder may be reusable:

- Compaia uses it as its native mission construction layer
- other applications may use it to generate SOGA-compatible Mission Packages
- SOGA should not depend on Compaia to evaluate a Mission Package

---

## Boundary Statement

Mission Builder creates or helps create a Mission Package.

SOGA evaluates execution-time legitimacy using the Mission Package and runtime evidence.

Mission Builder does not make governance decisions.

SOGA does not own the user-facing intent capture experience.

Execution adapters do not own either mission creation or governance.

---

## Why This Matters Now

The repository already contains:

- missions/
- generated/missions/
- builders/mission_builder.py
- builders/reference_mission_builder.py
- docs/mission_working_representation_v0_1.md
- docs/mission_working_representation_v0_1.md
- intake/
- Mission Planning Workbench work

Mission Packages are becoming first-class architectural artifacts.

The ownership boundary should be decided before expanding the workbench or mission generation components further.

---

## Review Required

This is an architectural clarification, not a code change.

Required review:

- Deb approval
- Claude Gate 1 architectural review
- Gemini coherence / external interpretation review if needed

---

## Possible Outcomes

Outcome A:

SOGA owns Mission Package schema only.

Outcome B:

SOGA owns Mission Builder as a reusable pre-governance component.

Outcome C:

Compaia owns Mission Builder; SOGA owns only the Mission Package contract and runtime governance.

Outcome D:

Mission Builder becomes an independent reusable package used by Compaia and other SOGA-compatible applications.

---

## Current Recommendation

Adopt Outcome D as the likely target:

Mission Builder should be reusable and protocol-independent.

Compaia should use Mission Builder as its user-facing mission construction layer.

SOGA should define and validate the Mission Package contract and evaluate runtime governance.

