# Methodological Constraints

These constraints guide future research sprints.

They describe how research should be conducted, not how SOGA should be
implemented.

---

## MC-001 — Demonstrate Novelty

Novelty must be demonstrated through literature review and comparison,
not asserted.

---

## MC-002 — Explicit Mapping Method

Classification functions shall specify:

- input observations
- governance targets
- mapping logic
- confidence model
- failure conditions

---

## MC-003 — Bounded LLM Usage

If LLMs contribute to classification:

- their role shall be explicit;
- they shall be evaluated against non-LLM baselines;
- reproducibility shall be measured.

---

## MC-004 — Define Success Before Building

Research shall define measurable success criteria before implementation.

Examples include:

- accuracy
- consistency
- explainability
- auditability
- latency
- human effort

---

## MC-005 — Falsifiable Research Questions

Each sprint investigates a bounded research question that can be evaluated
using evidence.

---

## MC-006 — Baselines Required

Every claimed improvement shall identify:

- the comparison baseline;
- the evaluation method;
- the measured improvement.

