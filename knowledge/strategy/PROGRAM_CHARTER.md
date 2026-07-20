# PROGRAM CHARTER
## Deb B Labs Embodied Governance Research Program

Status: DRAFT v0.1 — proposed for adoption via the G0 initialization commit
Editorial authority: Debbie Bucci (Principal Investigator)
Advisory review: Claude, CG, G (July 20, 2026 three-agent review)

---

## Governing Principle

The embodied governance program is the experimental environment in which
governance hypotheses become physically observable.

The repository exists to answer research questions.
Implementation exists to validate those answers.
Standards participation grounds those questions in real-world
interoperability and informs, but does not determine, the research
agenda.

---

## Mission

Help society understand and safely adopt increasingly autonomous
technologies through standards participation, governance research,
embodied AI, and human-centered demonstration.

SOGA, IntentGate, and the embodied laboratory are expressions of this
mission. They serve it; they do not define it.

---

## Scientific Question

Can delegated authority over autonomous agents be governed at execution
time — verifiably, across digital and physical execution surfaces —
without degrading the human experience those agents serve?

---

## Primary Hypotheses

Each hypothesis is stated falsifiably and mapped to the sprint expected
to produce its first Observed evidence.

- **H1 — Embodied governance.** The canonical pipeline (RuntimeEnvelope
  → Governance Policy Server → Canonical Decision Package → Capability
  Registry → execution) can govern physical actuation within measured
  latency budgets acceptable per capability risk class.
  *First evidence: G28. Latency budgets are Hypothesis-class until
  measured.*

- **H2 — Orchestration abstraction.** Mission-scoped authority is
  expressible in a conceptual model that crosswalks to AAuth and
  adjacent standards, and the correct model can be selected on
  evidence rather than preference.
  *First evidence: G26 architecture decision record.*

- **H3 — Heterogeneous participation.** Embodied devices of differing
  capability (Misty B, Misty A, companion devices) can participate
  under a common governed interaction layer with bounded — not zero —
  architectural adaptation.
  *First evidence: G28 (two-platform comparison); extended by the
  companion-layer concept work.*

- **H4 — Living-lab evidence.** Live human-interaction events can
  produce classifiable research evidence, not anecdote, when
  instrumented under a defined methodology.
  *First evidence: G29 methodology applied at G30.*

---

## Evidence Methodology

This program follows `docs/RESEARCH_METHODOLOGY.md` (evidence classes:
Verified, Observed, Hypothesis, Future Research).

That document is the single methodology source. This charter cites it
and does not restate it.

---

## Program Structure

Three layers, deliberately separated:

1. **Program governance** — continuous. This charter, document
   precedence, guardrails, decision authority, gate reviews.
2. **Continuous program tracks** — continuous. Standing
   responsibilities that persist across every sprint (see below).
3. **Research sprints** — time-boxed. Defined in
   `SPRINT_ROADMAP_G0_G30.md`.

Sprints answer: what research are we advancing next?
Tracks answer: what responsibilities must never be neglected while we
advance it?

---

## Continuous Program Tracks

Each track has a register section in `knowledge/strategy/TRACKS.md`,
reviewed at every sprint boundary. The Standards Track is additionally
updated event-driven (after each meeting, call, or contribution).

- **Research Track** — hypotheses, evidence, publications, peer review.
- **Implementation Track** — repository, prototypes, runtime,
  engineering hardening.
- **Standards Track** — DIF, AAuth, PIC, IETF, Kantara, NIST NCCoE,
  OIDF/AIIM: meeting outcomes, open issues, contributions, editorial
  roles, opportunities to influence specifications.
- **Funding & Partnerships Track** — SBIR, fellowships, grants,
  collaborations, and the periodic tooling/subscription governance
  review.
- **Living Laboratory & Outreach Track** — research conducted in human
  environments: music and performance venues, public demonstrations,
  healthcare and community interaction contexts — plus the
  communications activity (talks, public engagement) that surrounds
  it. Outreach is one activity within this track, not its definition.
  No public living-lab event occurs before the G29 methodology exists;
  until then this track holds planning and venue development only.

A track without a current register entry and a next action is a track
in name only. Registers are updated; prose is not duplicated across
documents.

---

## Roles and Authority

- **Principal Investigator (Debbie Bucci)** — singular editorial and
  decision authority over all program artifacts and adoptions. All
  gate activations are authorized by the PI.
- **Advisory agents (Claude, CG, G)** — advisory only. Roles as
  practiced: Claude — repository review and Gate 1 verification;
  CG — strategic synthesis; G — architectural review. Gate
  verification produces a pass/fail recommendation with findings; it
  does not itself activate a sprint.
- **External collaborators** — contribute under the repository
  guardrails (G19–G23) and this charter.

Agent-to-agent exchange (chat-mediated today; API/orchestrated in the
future) is an implementation detail. This organizational model is
stable regardless of transport. Governed agent-to-agent exchange is
itself a Future Research item of this program.

---

## Document Precedence

`knowledge/working/CURRENT_STATE.md` is the sole synchronization
contract. Strategy artifacts (this charter, the sprint roadmap, the
track registers, the decision log) are subordinate to it and are
referenced by it. No strategy artifact may state active program status
independently of CURRENT_STATE.md.

---

## Domain Relationships

- **Standards** define the interoperability surfaces the architecture
  must honor (AAuth, `act:` claim, PIC, DIF threat model).
- **Governance research** (SOGA/IntentGate) supplies the execution-time
  authority model under test.
- **Embodied systems** (Misty B as higher-capability research platform,
  Misty A as stable comparative baseline, companion devices) are the
  physical execution surfaces where hypotheses become observable.
- **The Living Laboratory** converts real-world interaction —
  including music performance environments — into classifiable
  evidence under the G29 methodology.
- **Healthcare and public-sector experience** provide evaluation
  contexts and the therapeutic-environment motivation.
- **Public outreach** presents the human experience; governance remains
  invisible to audiences and fully logged underneath.

---

## Amendment

This charter changes rarely and only by PI decision, recorded in
`DECISION_LOG.md`. Operational churn belongs in the decision log and
track registers, not here.
