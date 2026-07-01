# Governance Normalization Research Assessment v0.1

**Status:** Research Assessment
**Date:** 2026-07-01
**Sprint:** Governance Normalization Research v0.1
**Gate 1:** APPROVED (Claude)
**Gate 2:** APPROVED (Gemini)
**Repository Inspection:** COMPLETE

No architectural decisions are made by this document.
This document is a research assessment, not a specification.

---

## Research Question

Is governance normalization a distinct scientific problem, or is it
already solved by existing work in semantic normalization, ontology
alignment, evidence fusion, decision theory, or related disciplines?

---

## Related Repository Artifacts

- docs/governance_evidence_taxonomy_v0_1.md
- docs/execution_time_observation_catalog_v0_1.md
- knowledge/research/RESEARCH_OBSERVATIONS.md (RO-001)
- knowledge/research/METHODOLOGICAL_CONSTRAINTS.md

---

## WP1 — Working Definition of Governance Normalization

*Written before literature review. This definition will change.
That change is a finding.*

Governance normalization is the process by which execution-time
observations — produced by heterogeneous systems across different
domains, using different measurement methods, and carrying different
semantic meanings — are mapped to governance significance relative
to a specific delegated authority context.

Governance significance is distinct from semantic meaning. Two
observations may be semantically unrelated yet contribute equivalent
governance significance. Two observations may be semantically similar
yet contribute different governance significance depending on the
delegated authority context in which they occur.

The governance significance of an observation is not a fixed property
of the observation. It is a function of:

- the observation itself — its type, source, measurement method,
  and confidence
- the delegated authority context — who authorized what, on whose
  behalf, under what constraints
- the subject agency state — the current governance posture of the
  human subject whose authority is implicated
- the consequence severity — the potential impact of exercising or
  withholding delegated authority at this moment

Governance normalization therefore asks: given this observation, in
this delegated authority context, what governance significance does
it contribute — and toward which governance dimension?

This is distinct from:

- **Semantic normalization** — which asks whether observations mean
  the same thing
- **Evidence fusion** — which asks how observations should be
  combined into a belief state
- **Decision theory** — which asks when a rational decision should
  be made given evidence
- **Runtime safety** — which asks whether a system is safe to
  continue operating
- **Ontology alignment** — which asks whether knowledge models can
  be mapped to each other

The candidate claim is that none of these existing frameworks address
the combination of:
1. heterogeneous observations requiring normalization
2. governance significance as the normalization target
3. delegated authority context as the evaluation frame
4. execution-time assessment as the operational requirement

This working definition was tested against the literature in WP2.

---

## WP2 — Cross-Disciplinary Literature Survey

*Who already solves part of this problem?*

### Semantic Interoperability

The semantic interoperability literature addresses how systems with
different data models, vocabularies, and ontologies can exchange
information meaningfully.

Key work: Sheth and Larson (1990) federated databases; Bernstein
et al. (2011) ontology matching; W3C semantic web stack (RDF, OWL,
SPARQL).

What it solves: mapping concepts across heterogeneous systems so
that data from one system can be interpreted by another.

What it does not address: the governance significance of
observations, delegated authority context, or execution-time
assessment. Semantic interoperability asks whether two systems agree
on what a concept means. It does not ask what that concept
contributes to a governance decision.

### Ontology Alignment

Ontology alignment is a specialized form of semantic interoperability
focused on finding correspondences between formal knowledge
representations.

Key work: Euzenat and Shvaiko (2013) ontology matching; OAEI
(Ontology Alignment Evaluation Initiative); Noy and Musen (2000)
PROMPT algorithm.

What it solves: structural and semantic alignment between knowledge
models, typically at design time.

What it does not address: runtime observations, delegated authority,
or dynamic execution-time governance. Ontology alignment is a
design-time activity. Runtime observations from heterogeneous
systems do not arrive as formal ontology instances.

### Knowledge Representation and Policy Reasoning

The knowledge representation literature addresses how to formally
represent facts, rules, and constraints for automated reasoning.

Key work: Hayes (1979) situation calculus; Brachman and Levesque
(2004) knowledge representation; SWRL, OWL-DL for policy reasoning.

Policy reasoning extensions: XACML (OASIS), ODRL, Cedar (AWS).

What it solves: formal evaluation of whether a request satisfies
a stated policy, given a well-defined policy language and a
well-formed request.

What it does not address: heterogeneous runtime observations that
must be normalized before policy evaluation can occur. Policy
reasoning assumes the inputs are already in a form the policy
engine can evaluate. The normalization step precedes policy
reasoning — it is not performed by it.

### Decision Theory

Decision theory provides a formal framework for making optimal
decisions under uncertainty.

Key work: von Neumann and Morgenstern (1944) expected utility
theory; Savage (1954) subjective expected utility; Jeffrey (1965)
evidential decision theory; Pearl (1988) probabilistic reasoning.

What it solves: given outcomes, probabilities, and a utility
function, decision theory identifies the optimal action.

What it does not address: decision theory assumes the evidence has
already been interpreted. It operates on probability distributions
over outcomes, not on raw heterogeneous observations. Decision
theory also does not address delegated authority context — it
optimizes for expected utility, not for whether exercising
delegated authority remains legitimate.

### Evidence Fusion / Sensor Fusion

Evidence fusion addresses how to combine observations from multiple
heterogeneous sources into a unified belief state.

Key work: Dempster (1967) and Shafer (1976) Dempster-Shafer theory;
Dezert and Smarandanche (2004) DSmT; Kalman (1960) filter; Hall
and Llinas (1997) multisensor data fusion.

What it solves: combining conflicting or uncertain observations from
different sources into a single coherent belief about world state.

What it does not address: governance significance. Evidence fusion
produces a belief state about factual world conditions. It does not
produce a governance significance assessment. It does not evaluate
delegated authority context.

### Subjective Logic / Uncertainty Fusion (Jøsang)

Subjective Logic extends Dempster-Shafer theory by adding an
explicit representation of uncertainty as a first-class element
alongside belief and disbelief.

Key work: Jøsang (2001, 2016) Subjective Logic — A Formalism for
Reasoning Under Uncertainty; Jøsang et al. (2006) trust management
using Subjective Logic.

What it solves: Subjective Logic allows reasoning agents to hold
explicit beliefs, disbeliefs, and uncertainty values about
propositions, and to combine these across multiple sources using
defined fusion operators. Applied to trust management, reputation
systems, and multi-agent belief combination.

What it does not address: Subjective Logic operates on propositions
about world state or agent trustworthiness. It does not address
governance significance — the question of whether an observation
justifies continuing to exercise delegated authority. It does not
incorporate delegated authority context, mission constraints,
subject agency state, or consequence severity.

**Critical negative finding:** Subjective Logic is the closest
existing framework to governance normalization. It handles
heterogeneous, uncertain observations from multiple sources. It
fails to address governance normalization because it does not
incorporate delegated authority context or governance significance
as its normalization target. The gap is real and precisely
locatable.

### Resilience Engineering / Functional Resonance (Hollnagel)

Resilience Engineering addresses how systems maintain acceptable
performance under varying and unexpected conditions.

Key work: Hollnagel (2004) Barriers and Accident Prevention;
Hollnagel et al. (2006) Resilience Engineering; Hollnagel (2012)
FRAM — Functional Resonance Analysis Method.

What it solves: understanding how normal variability in system
functions combines to produce unexpected outcomes, and designing
systems resilient to that variability.

What it does not address: delegated authority governance. FRAM
analyzes functional variability in engineered systems at the design
and analysis level. It does not address execution-time governance
of delegated authority, subject agency state, or mission context.

### Runtime Safety / Safety-Critical Systems

Runtime safety literature addresses whether a system is safe to
continue operating given current conditions.

Key work: Leveson (1995) Safeware; IEC 61508 functional safety;
DO-178C aviation software; ISO 26262 automotive safety; Rushby
(1994) critical system properties.

What it solves: evaluating whether system state satisfies safety
constraints at runtime. Safety integrity levels (SIL) scale
evidence requirements to consequence severity.

What it does not address: delegated authority legitimacy. Runtime
safety asks whether it is safe to continue operating. Governance
normalization asks whether it remains legitimate to exercise
delegated authority. Safety and legitimacy are orthogonal
properties.

### Human Factors

Human factors literature produces observations — workload levels,
situation awareness states, attention measures. It does not provide
a framework for normalizing those observations into governance
significance or for evaluating them against delegated authority
context.

### Robotics and Autonomous Systems

Produces execution-time observations. Does not address governance
normalization. Covered in the Execution-Time Observation Catalog.

### AI Safety

Key work: Russell (2019) Human Compatible; Amodei et al. (2016)
Concrete Problems in AI Safety; Hadfield-Menell et al. (2016)
cooperative inverse reinforcement learning.

What it solves: alignment between AI behavior and human preferences
or values, typically at design time or through learning.

What it does not address: execution-time governance of delegated
authority. AI safety asks whether a system is aligned by design.
Governance normalization asks whether a specific execution action
remains legitimate given current conditions.

### Identity and Authorization

Authorization systems (AAuth, UCAN, ZCAP, OAuth, GNAP) establish
what authority has been delegated. They answer the authorization
question: what was permitted? They do not answer the governance
question: should that permission be exercised now?

---

## WP3 — Comparative Matrix

| Discipline | Primary Question | What is Normalized? | Input | Output | Decision Context | Missing Relative to Governance Normalization |
|---|---|---|---|---|---|---|
| Semantic normalization | Do these concepts mean the same thing? | Concept meaning | Heterogeneous vocabularies | Semantic equivalence mappings | Static / Design-time | Governance significance; delegated authority context; execution-time assessment |
| Ontology alignment | Can these knowledge models be aligned? | Knowledge model structure | Formal ontologies | Alignment correspondences | Static / Design-time | Runtime observations; delegated authority; dynamic execution-time governance |
| Policy reasoning (XACML, Cedar) | Does this request satisfy this policy? | Request structure | Well-formed policy + request | Permit / Deny | Static policy evaluation | Observation normalization precedes policy reasoning; does not address heterogeneous raw observations |
| Decision theory | When should a rational decision be made? | Expected utility | Probability distributions over outcomes | Optimal action | Assumes interpreted evidence | Does not normalize observations; assumes utility function is known; no delegated authority context |
| Evidence fusion (Dempster-Shafer) | How should multiple observations be combined? | Belief state about world | Heterogeneous sensor observations | Unified belief state | Factual world state | Governance significance not addressed; no delegated authority context; no mission constraints |
| Subjective Logic (Jøsang) | How should uncertain beliefs from multiple sources be combined? | Belief, disbelief, uncertainty | Heterogeneous agent opinions | Combined subjective opinion | Agent trustworthiness / world state belief | Governance significance not addressed; no delegated authority context; no subject agency state; no mission constraints |
| Resilience Engineering / FRAM (Hollnagel) | How does functional variability propagate through a system? | Functional performance variability | System function outputs | Resonance risk assessment | System design / safety analysis | Not execution-time; no delegated authority; no mission context |
| Runtime safety (IEC 61508, ISO 26262) | Is it safe to continue operation? | System safety state | Runtime system telemetry | Safe / Unsafe | Dynamic / execution-time — static architecture | Safety not equivalent to authority legitimacy; no delegated authority context; no subject agency state |
| AI safety / alignment | Does this system behave in accordance with human values? | Behavioral alignment | System behavior observations | Alignment assessment | Design-time or learning-time | Not execution-time governance; no delegation chain; no per-execution authority assessment |
| Identity / authorization (AAuth, UCAN) | What authority has been delegated? | Delegation claims | Credential artifacts | Permission grants | Design-time / issuance-time | Establishes what is permitted; does not evaluate whether exercising permission remains legitimate now |
| **Governance normalization (candidate)** | **What governance significance should heterogeneous observations contribute?** | **Governance significance** | **Heterogeneous runtime observations** | **Governance dimension contributions** | **Dynamic / multi-hop execution-time delegation** | **— this is the candidate construct** |

---

## WP4 — Gap Analysis

The complete governance normalization chain requires:

```
Heterogeneous runtime observations
      ↓
Governance significance mapping
      ↓
Delegated authority context evaluation
      ↓
Execution-time decision support
```

Testing each candidate framework against the complete chain:

**Subjective Logic** — handles heterogeneous observations and
uncertainty combination. Stops before governance significance.
Does not reach delegated authority context.
**Partial — fails at step 2.**

**Evidence fusion (Dempster-Shafer)** — handles heterogeneous
observations and belief combination. Produces factual belief state,
not governance significance. Does not reach delegated authority
context.
**Partial — fails at step 2.**

**Policy reasoning (XACML, Cedar)** — handles delegated authority
context and decision support. Requires well-formed inputs. Does not
perform observation normalization.
**Partial — fails at step 1.**

**Decision theory** — handles decision support given interpreted
evidence. Assumes steps 1 and 2 are already complete. Does not
address delegated authority context as a governance frame.
**Partial — fails at steps 1 and 2.**

**Runtime safety (IEC 61508)** — handles dynamic execution-time
assessment and consequence-scaled evidence requirements. Evaluates
system safety, not authority legitimacy. Does not incorporate
delegated authority context or subject agency state.
**Partial — fails at steps 2 and 3.**

**Resilience Engineering / FRAM** — handles system-level variability
and propagation. Design-time and system-level. Does not reach
execution-time governance or delegated authority.
**Partial — fails at steps 2, 3, and 4.**

**No existing framework completes the full chain.**

The gap is locatable and precise: no existing framework normalizes
heterogeneous runtime observations into governance significance
within a delegated authority context at execution time.

---

## WP5 — Research Conclusion

Applying the four permitted outcomes:

**Outcome 1 — Already solved:** No. No existing framework completes
the full chain from heterogeneous observations through governance
significance to delegated authority context evaluation at execution
time.

**Outcome 2 — Partially solved:** Yes, in components. Subjective
Logic solves heterogeneous observation combination. Policy reasoning
solves authority context evaluation. Runtime safety solves
consequence-scaled evidence requirements. Decision theory solves
action selection given interpreted evidence. No framework combines
all four steps.

**Outcome 3 — Adjacent work exists:** Yes, and it is directly
useful. The adjacent frameworks are components, not obstacles.
Subjective Logic may inform how observations are combined before
governance significance is assessed. Policy reasoning may inform
how governance decisions are reached after significance is
established. Runtime safety may inform evidence sufficiency
thresholds (RO-002).

**Outcome 4 — Distinct research area:** Yes, in the specific
combination. The integration of heterogeneous observation
normalization, governance significance mapping, delegated authority
context, and execution-time assessment has not been addressed as
a unified framework in the surveyed literature.

**Conclusion: Outcomes 3 and 4 apply simultaneously.**

Adjacent work exists and is valuable. The specific combination
required for governance normalization — particularly the delegated
authority context as the normalization frame and governance
significance as the normalization target — constitutes a distinct
research contribution not addressed by any existing framework.

This is not a claim that governance normalization is entirely novel.
It is a finding that the specific combination has not been unified,
and that unifying it requires going beyond what any single adjacent
framework provides.

---

## WP6 — Negative Findings

*What adjacent disciplines demonstrably do not address.*

**NF-001 — Semantic normalization does not determine governance
significance.**
Semantic normalization establishes whether concepts mean the same
thing across systems. Whether two observations are semantically
equivalent does not determine whether they contribute equivalent
governance significance. A high workload reading and an emergency
stop proximity alert are not semantically equivalent. Both may
contribute equivalent governance significance — RESTRICT — in a
specific delegated authority context. Semantic equivalence is
neither necessary nor sufficient for governance significance
equivalence.

**NF-002 — Ontology alignment does not evaluate delegated
authority.**
Ontology alignment operates at design time on formal knowledge
representations. Runtime observations from heterogeneous systems
do not arrive as formal ontology instances. Even where ontology
alignment could be applied, it produces structural correspondences
between knowledge models, not assessments of whether delegated
authority should be exercised given current conditions.

**NF-003 — Evidence fusion does not produce governance
significance.**
Dempster-Shafer theory and related evidence fusion frameworks
combine heterogeneous observations into a unified belief state
about factual world conditions. A belief state about world
conditions is not a governance significance assessment. The belief
that a human subject's workload is high does not itself determine
what governance action is warranted — that determination requires
the delegated authority context and the subject agency state, which
evidence fusion frameworks do not incorporate.

**NF-004 — Subjective Logic does not incorporate delegated
authority context.**
Subjective Logic is the closest existing framework to governance
normalization. It explicitly handles uncertainty, belief, and
disbelief from heterogeneous sources using formal fusion operators.
It fails to address governance normalization because its
normalization target is agent trustworthiness or world state belief,
not governance significance. It does not incorporate mission
constraints, subject agency state, consequence severity, or the
delegated authority context that determines what governance
significance an observation should contribute.

**NF-005 — Decision theory assumes evidence has already been
interpreted.**
Decision theory optimizes action selection given probability
distributions over outcomes and a utility function. It does not
perform the observation normalization step. The normalization of
heterogeneous runtime observations into governance-relevant inputs
is a precondition for decision-theoretic analysis, not a product
of it. Decision theory also does not address delegated authority
context — it optimizes for expected utility, which is not the same
as governance legitimacy.

**NF-006 — Resilience Engineering evaluates system resilience, not
authority legitimacy.**
FRAM and related resilience engineering frameworks analyze how
functional variability propagates through systems. They address
system-level safety and resilience at the design and analysis
level. They do not address execution-time governance of delegated
authority, subject agency state, or mission context. A system may
be resilient in the FRAM sense while simultaneously operating
under delegated authority that is no longer appropriate given
current subject conditions.

**NF-007 — Runtime safety evaluates system safety, not delegated
authority legitimacy.**
IEC 61508, DO-178C, and ISO 26262 address whether systems are safe
to operate given current conditions. Safety and legitimacy are
orthogonal. A system may be safe to operate — no hardware faults,
no safety constraint violations — while the delegated authority to
operate it on behalf of a specific human subject is no longer
appropriate given changes in subject agency state, mission context,
or oversight conditions. Runtime safety frameworks do not
incorporate these governance-specific inputs.

**NF-008 — Policy reasoning assumes well-formed inputs.**
XACML, Cedar, and related policy reasoning frameworks evaluate
whether requests satisfy stated policies. They require inputs in a
form the policy engine can evaluate. They do not perform observation
normalization — the transformation of heterogeneous runtime
observations into policy-evaluable inputs. This normalization step
must occur before policy reasoning can be applied. Policy reasoning
is downstream of governance normalization, not a substitute for it.

**NF-009 — AI safety alignment does not address per-execution
authority assessment.**
AI safety frameworks address behavioral alignment between AI
systems and human values, typically at design time or through
learning. They do not address the execution-time governance
question: given current runtime observations, should this specific
delegated authority be exercised now on behalf of this specific
subject? AI safety asks whether a system is aligned by design.
Governance normalization asks whether a specific execution action
remains legitimate given current conditions.

**NF-010 — Authorization systems establish permission, not
execution-time legitimacy.**
AAuth, UCAN, ZCAP, OAuth, and GNAP establish what authority has
been delegated. They answer the authorization question: what was
permitted? They do not answer the governance question: should that
permission be exercised now? This distinction is the founding
premise of SOGA and is confirmed by the negative finding that no
authorization framework addresses execution-time legitimacy
assessment.

---

## Summary

**Research question:** Is governance normalization a distinct
scientific problem?

**Answer:** Yes, as a specific combination. Adjacent work exists
and is valuable — particularly Subjective Logic, policy reasoning,
and runtime safety frameworks. No existing framework addresses the
complete chain: heterogeneous runtime observations → governance
significance → delegated authority context → execution-time
decision support.

**Research conclusion:** Outcomes 3 and 4 — adjacent work exists,
and the specific combination constitutes a distinct research
contribution.

**Ten negative findings** precisely locate what existing frameworks
do not address and why.

**Strongest adjacent framework:** Subjective Logic (Jøsang) —
closest to governance normalization; fails specifically at delegated
authority context and governance significance as normalization
target.

**Most useful components for future work:**
- Subjective Logic → observation combination under uncertainty
- Policy reasoning → authority context evaluation
- Runtime safety (IEC 61508) → consequence-scaled evidence
  thresholds (directly relevant to RO-002)
- Decision theory → action selection after normalization is complete

---

## Open Research Questions

- RO-002: Evidence Sufficiency for Governance Decisions — when is
  there sufficient evidence to safely exercise delegated authority?
  (Deferred pending classification function research.)
- Classification functions: how are observations transformed into
  governance evidence inputs?
- Ecosystem positioning: where does execution-time governance fit
  within the broader identity, delegation, and agent framework
  ecosystem? (Candidate future workstream.)

---

## Repository Inspection

Inspection confirmed this assessment extends existing repository
artifacts without conflict:

- Extends docs/governance_evidence_taxonomy_v0_1.md
- Extends docs/execution_time_observation_catalog_v0_1.md
- Confirms RO-001 in knowledge/research/RESEARCH_OBSERVATIONS.md
- Satisfies MC-001 through MC-006

No existing artifact requires modification.
Repository Curator (Deb) authorizes commit.
