# Passive Adapter Specification v0.1

Status: Stable Interface  
Date: 2026-07-03  
Sprint: Sprint B — Adapter Boundary Expansion

---

## Purpose

This document defines the passive adapter boundary for SOGA.

Passive adapters allow ecosystem-specific representations to be projected into
the canonical SOGA RuntimeEnvelope without modifying the governance core.

---

## Definition

A passive adapter is a projection layer that:

1. Receives an ecosystem-specific representation.
2. Extracts governance-relevant fields.
3. Projects those fields into canonical RuntimeEnvelope structures.
4. Adds explicitly supplied governance context from an explicitly declared
   source when the source ecosystem does not carry that context.
5. Preserves source evidence.
6. Performs no governance evaluation.

---

## Adapter Boundary

A passive adapter MAY parse:

- protocol-shaped payloads
- mission-shaped payloads
- capability-shaped payloads
- workflow-shaped payloads
- representative static payloads

A passive adapter SHALL NOT:

- evaluate authority
- make ALLOW / RESTRICT / DENY decisions
- infer missing governance context
- calculate subject agency state
- calculate mission constraints
- calculate governance_reasoning_token
- modify GovernancePDP behavior
- modify RuntimeEnvelope structure
- depend on live protocol services
- require external protocol SDKs for baseline projection

---

## Static Governance Context Rule

Any governance context appended by an adapter SHALL be supplied by static
configuration or deterministic lookup at adapter initialization.

This includes:

- subject_agency_state
- mission_constraints
- governance_reasoning_token
- supervision_required
- forbidden_conditions
- execution capability labels

The adapter may place such context into the RuntimeEnvelope only when the
source of that context is explicit.

The adapter SHALL NOT dynamically infer, calculate, deduce, or synthesize
governance context from ambiguous input.

---

## Required Output

A passive adapter SHALL produce one of the following:

1. Canonical RuntimeEnvelope model object; or
2. Canonical RuntimeEnvelope-shaped dictionary accepted by existing
   normalization paths.

For Sprint B and later canonical integrations, the preferred output is the
RuntimeEnvelope model object.

---

## Provenance Preservation

A passive adapter SHALL preserve source evidence in one or more of:

- authority.raw_evidence
- authority.references
- mission.references
- mission.metadata
- envelope.metadata

The adapter should preserve enough source material to explain what was
projected without requiring the original ecosystem to remain active at
decision time.

---

## Ecosystem Neutrality

Passive adapters enforce G19 — Ecosystem Neutrality.

Each adapter absorbs ecosystem specificity at the boundary.

The governance core remains protocol-neutral and ecosystem-neutral.

Adding a new adapter SHALL NOT require changes to:

- GovernancePDP
- RuntimeEnvelope
- Canonical Decision Package
- governance dimensions
- core decision logic

If any of those changes are required, the work is no longer a passive adapter
extension and must receive explicit architectural authorization.

---

## Current Passive Adapter Examples

Existing or representative passive adapters include:

- AAuth adapter
- UCAN adapter
- ZCAP adapter
- AIIM-style adapter
- OAuth/GNAP-style adapter
- MCP-style capability adapter

Each adapter may differ in source shape.

Each adapter must project into the same canonical governance boundary.

---

## Sprint Gate Invariants

Every adapter sprint SHALL verify:

- GovernancePDP unchanged
- RuntimeEnvelope unchanged
- regression baseline passing
- adapter performs projection only
- governance context is explicitly supplied
- no protocol-specific logic enters the governance core

---

## Non-Goals

This specification does not define:

- OAuth behavior
- GNAP behavior
- AAuth behavior
- UCAN behavior
- ZCAP behavior
- MCP transport
- AIIM schema
- cryptographic validation
- token issuance
- policy evaluation
- capability execution

Those remain external ecosystem concerns.

SOGA consumes projected governance evidence.

SOGA does not replace the originating ecosystem.

