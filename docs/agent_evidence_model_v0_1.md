# Agent Evidence Model v0.1

Status: Sprint 7 Working Model

## Purpose

Agent Evidence is governance-relevant input contributed by an advisory agent.

Agent Evidence is NOT a governance determination.

## Required Fields

- agent_id
- evidence_type
- evidence_content
- provenance
- confidence

## Evidence Type

Evidence type identifies the governance dimension or runtime concern the evidence may inform.

Examples:
- mission
- authority
- subject_agency_state
- reachability
- execution_context
- policy

## Rules

Agent evidence MAY:
- support a governance dimension evaluation
- contradict another advisory input
- expose uncertainty
- record provenance

Agent evidence SHALL NOT:
- determine ALLOW, RESTRICT, or DENY
- produce a Canonical Decision Package
- override the Governance PDP
- act as governance authority

Agent disagreement is represented as conflicting evidence inputs, not competing governance outcomes.
