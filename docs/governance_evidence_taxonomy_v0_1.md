# Governance Evidence Taxonomy v0.1

Status: Research artifact

Date: 2026-06-30

---

## Purpose

This taxonomy identifies execution-time evidence types that may be
relevant to SOGA governance evaluation.

It extends existing repository evidence artifacts. It does not replace
them.

---

## Relationship to Existing Artifacts

- `docs/agent_evidence_model_v0_1.md` defines how evidence is contributed.
- `specifications/runtime-envelope/v0.1/` defines where evidence is carried.
- `docs/stable_interfaces_v0_1.md` defines stable evidence interfaces.
- This taxonomy defines candidate evidence types and controlled values.

---

## Scope

This is literature synthesis.

It is not architecture.
It is not implementation.
It does not modify RuntimeEnvelope.
It does not modify SOGA governance logic.

---

## Mission Evidence

- mission_phase: planning | active | critical | completing | complete
- plan_deviation: none | minor | significant | abandoned
- criticality: routine | elevated | critical
- deadline_proximity: nominal | approaching | imminent

---

## Authority Evidence

- trust_calibration: undertrust | calibrated | overtrust
- runtime_loa: controlled scale or vocabulary
- delegation_depth: integer hop count
- delegation_attenuation: none | partial | significant

---

## Subject Evidence

- agency_state: Independent | Supervised | Managed | Delegated | Lapsed
- subject_posture: monitoring | overriding | collaborating | disconnected
- workload_level: low | moderate | high | overloaded
- situation_awareness: level_1 | level_2 | level_3 | degraded

---

## Reachability Evidence

- availability_state: available | occupied | unreachable | unknown
- attention_lock: focused_on_agent | distracted | unknown
- interruption_cost: low | moderate | high
- breakpoint_proximity: at_breakpoint | approaching | mid_task

---

## Execution Context Evidence

- privacy_sensitivity: private | semi_private | public
- environmental_hazard: none | caution | critical
- spatial_hazard_index: nominal | caution_proximity | emergency_stop_imminent
- system_fault_vector: none | degraded | fault_active
- operational_status: nominal | degraded_performance | hard_fault_imminent
- safety_margin: clear | warning_proximity | breach_imminent

---

## Policy Evidence

- procedure_compliance: compliant | minor_deviation | violation
- safety_constraint: satisfied | approaching_limit | violated
- ethical_constraint: none | flagged | violated
- escalation_trigger: none | condition_met

---

## Interaction Evidence Gap

Interaction evidence remains a named taxonomy gap.

Candidate evidence types:

- interaction_id: unique identifier
- turn_holder: human | system | unassigned | transitioning
- boundary_state: quiescent | pending_entry | inside_boundary | exiting
- handoff_phase: stable_control | request_transfer | synchronized | execution_shifted
- interaction_topology: direct | supervised | multi_agent_cascade

---

## Open Questions

- Should interaction evidence remain separate or map into existing dimensions?
- Is handoff_phase an interaction property or cross-dimensional governance event?
- What classification functions map raw observations into this vocabulary?
- What metrics evaluate classification accuracy, consistency, and auditability?

---

## G9 Preservation

This taxonomy is research evidence only.

It does not promote any field into architecture.

