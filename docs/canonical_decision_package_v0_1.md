# SOGA Canonical Decision Package Specification
Version: 0.1
Status: Editor's Draft

---

# 1. Purpose

This document defines the SOGA Canonical Decision Package, the normative execution-time governance artifact produced by a conformant SOGA implementation.

The purpose of this specification is to enable independent implementations to produce semantically equivalent governance determinations when presented with equivalent runtime inputs, regardless of internal architecture, programming language, or deployment environment.

This specification does not define authentication mechanisms, authorization protocols, transport protocols, user interfaces, or implementation-specific algorithms. Those components MAY differ between implementations.

Instead, this specification defines the canonical governance artifact that SHALL result from execution-time evaluation.

The Canonical Decision Package records whether delegated authority remained legitimate at the moment of execution and the governance basis for that determination.

The intent of this specification is interoperability through common governance semantics rather than implementation uniformity. Independent implementations that conform to this specification SHOULD produce semantically equivalent Canonical Decision Packages when operating over equivalent runtime conditions.

This document is an Editor's Draft and reflects the current state of the SOGA architecture as demonstrated through implementation and evaluation. It is expected to evolve as additional architectural discoveries are validated through implementation and independent review.

---

# 2. Scope

This specification defines the normative content and governance meaning of the SOGA Canonical Decision Package.

The Canonical Decision Package SHALL represent the outcome of execution-time governance evaluation for a delegated action and SHALL provide sufficient information for independent interpretation of that governance determination.

This specification defines the governance artifact produced by a conformant SOGA implementation. It does not prescribe the internal architecture, evaluation algorithms, data structures, programming language, storage model, transport mechanism, or deployment environment used to produce that artifact.

Conforming implementations MAY employ different internal evaluation mechanisms, provided that equivalent runtime inputs produce semantically equivalent Canonical Decision Packages.

This specification does not define authentication protocols, authorization protocols, delegation protocols, credential formats, policy languages, serialization formats, user interfaces, audit systems, or visualization systems, except where necessary to define the governance meaning of the Canonical Decision Package.

Nothing in this specification SHALL be interpreted as requiring a particular protocol or implementation technology. The scope of this document is limited to the Canonical Decision Package as the normative execution-time governance artifact of SOGA.

---

# 3. Conformance Language

The key words "SHALL", "SHALL NOT", "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this specification are to be interpreted as normative requirements for conformance.

"SHALL" and "MUST" identify mandatory requirements for a conformant implementation.

"SHALL NOT" and "MUST NOT" identify prohibited behavior for a conformant implementation.

"SHOULD" and "SHOULD NOT" identify recommended practices that may be departed from only when the implications are fully understood and the resulting implementation remains consistent with the governance semantics defined by this specification.

"MAY" identifies behavior that is optional and left to the discretion of the implementer, provided such behavior does not alter the normative meaning of the Canonical Decision Package.

Unless explicitly stated otherwise, all normative requirements in this specification apply to the Canonical Decision Package produced by a conformant implementation rather than to any particular internal implementation mechanism.

---

# 4. Background

Authentication establishes identity by answering the question: **Who are you?**

Authorization establishes delegated permissions by answering the question: **What were you allowed to do?**

In delegated systems, those determinations alone are insufficient to establish that a requested action remains legitimate at the moment of execution. Time, context, changes in the subject's condition, and other runtime factors may alter whether previously delegated authority should still be exercised.

SOGA addresses this execution-time governance problem by evaluating delegated authority against the runtime conditions that exist when execution is requested.

The Canonical Decision Package is the normative artifact that records the outcome of that execution-time governance evaluation. It provides a protocol-independent representation of the governance determination while remaining independent of the internal mechanisms used to produce it.

---

# 5. Problem Statement

Authentication establishes identity and authorization establishes delegated permissions. Together, these mechanisms determine who is acting and what authority has been delegated.

However, neither mechanism determines whether that delegated authority remains appropriate at the moment execution is requested.

Delegated authority exists within a changing runtime environment. Elapsed time, changes in the subject's condition, mission progression, execution context, reachability, and other governance-relevant factors may alter whether a previously authorized action should still be exercised.

Consequently, possession of valid credentials or delegated permissions alone SHALL NOT be interpreted as sufficient evidence that execution remains legitimate.

Existing authentication and authorization mechanisms intentionally answer different questions than execution-time governance. They establish identity and delegated permissions but do not define the governance determination required when execution occurs under changing runtime conditions.

SOGA addresses this gap by producing a Canonical Decision Package that represents the execution-time governance determination for the requested action. The Canonical Decision Package provides a protocol-independent artifact that may be independently interpreted, audited, exchanged, and consumed by conformant implementations while preserving implementation independence.

The problem addressed by this specification is therefore not the authentication of identity or the authorization of delegated permissions, but the production of a canonical execution-time governance artifact that records whether delegated authority remained legitimate under the runtime conditions that existed at the point of execution.

---

# 6. Relationship to Existing Identity Architecture

SOGA is complementary to existing identity, authorization, and delegation architectures. It does not replace, supersede, or redefine their responsibilities.

Authentication mechanisms establish identity by determining who is acting.

Authorization mechanisms establish delegated permissions by determining what authority has been granted.

Delegation mechanisms communicate or represent that delegated authority between participants and systems.

Those mechanisms collectively establish the identity of the actor and the delegated authority available for potential execution. They do not, by themselves, define the execution-time governance determination regarding whether that authority remains appropriate under the runtime conditions that exist when execution is requested.

Accordingly, this specification SHALL NOT be interpreted as modifying the semantics of any authentication protocol, authorization protocol, delegation protocol, credential format, or policy language. Those mechanisms remain responsible for their respective functions within the broader identity architecture.

The SOGA Canonical Decision Package operates at the execution-time governance boundary. It consumes the governance-relevant runtime information available at the moment of execution and records the resulting governance determination in a protocol-independent form.

Because the Canonical Decision Package is independent of the mechanisms used to establish identity or delegated permissions, conformant implementations MAY operate with different authentication protocols, authorization protocols, delegation protocols, or policy representations while producing semantically equivalent Canonical Decision Packages for equivalent runtime conditions.

This specification therefore defines an execution-time governance artifact that complements existing identity architectures rather than replacing them. It identifies the governance determination that occurs after identity and delegated permissions have been established and before delegated authority is exercised.

---

# 7. SOGA Runtime Model

The SOGA Runtime Model defines the conceptual governance process that produces a Canonical Decision Package. It describes the governance model rather than any particular implementation architecture.

A conformant implementation SHALL evaluate a requested delegated action using governance-relevant runtime information available at the point of execution. The result of that evaluation SHALL be represented by a single Canonical Decision Package.

The Runtime Model is conceptually independent of authentication mechanisms, authorization mechanisms, delegation protocols, policy languages, and implementation technologies. Those mechanisms MAY provide information that contributes to governance evaluation, but they do not define the governance model itself.

The Runtime Model operates on a normalized Runtime Envelope. The Runtime Envelope is the conceptual input to governance evaluation. The Canonical Decision Package is the normative output of that evaluation.

Governance evaluation is performed across six orthogonal governance dimensions:

- Mission
- Authority
- Subject Governance State
- Reachability
- Execution Context
- Policy

Each governance dimension contributes meaning that is independent of the others. A conformant implementation MAY evaluate these dimensions using different internal mechanisms, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

For any requested execution event, the Runtime Model produces a single governance determination. That determination is subsequently represented by the Canonical Decision Package defined by this specification.

This section defines the conceptual governance model that produces the Canonical Decision Package. The Runtime Envelope and the Canonical Decision Package are defined in the sections that follow.

---

# 7a. Runtime Envelope

The Runtime Envelope is the conceptual input to SOGA governance evaluation. It represents the governance-relevant state that exists at the point of execution and upon which the governance determination is based.

The Runtime Envelope is a conceptual construct rather than a prescribed data structure, serialization format, or implementation mechanism. This specification defines its governance meaning, not its representation.

A conformant implementation SHALL evaluate the requested execution using a Runtime Envelope that contains the governance-relevant information necessary to evaluate the six orthogonal governance dimensions defined by the SOGA Runtime Model.

The Runtime Envelope conceptually carries information relevant to:

- Mission
- Authority
- Subject Governance State
- Reachability
- Execution Context
- Policy

This specification does not prescribe how such information is obtained, represented, transported, normalized, or stored. Conformant implementations MAY derive Runtime Envelope information from different protocols, systems, policies, or implementation architectures, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

The Runtime Envelope SHALL be interpreted as the conceptual input to governance evaluation. It is not itself a governance determination, a delegation artifact, an authorization grant, an authentication credential, or the Canonical Decision Package.

The Runtime Envelope provides the governance context from which a single execution-time governance determination is produced. That determination is subsequently represented by the Canonical Decision Package defined by this specification.

---

# 8. Canonical Decision Package

The Canonical Decision Package is the normative execution-time governance artifact defined by this specification. It represents the governance determination produced by the SOGA Runtime Model for a requested execution event.

A conformant implementation SHALL produce exactly one Canonical Decision Package for each governance determination associated with a requested execution event.

The Canonical Decision Package is the normative output of governance evaluation. It is produced from the Runtime Envelope but is not itself the Runtime Envelope, an authentication credential, an authorization grant, a delegation artifact, or an execution receipt.

The Canonical Decision Package records the governance determination reached at the point of execution together with the governance meaning necessary for independent interpretation of that determination.

The Canonical Decision Package is independent of any particular authentication mechanism, authorization mechanism, delegation protocol, policy language, serialization format, transport mechanism, or implementation architecture. Conformant implementations MAY differ in their internal operation while producing semantically equivalent Canonical Decision Packages for equivalent runtime conditions.

The Canonical Decision Package SHALL be interpreted as the authoritative execution-time governance artifact for the requested execution event. Downstream systems, including execution systems, visualization systems, audit systems, and other consumers, consume the Canonical Decision Package rather than constructing independent governance interpretations from the Runtime Envelope or underlying implementation state.

This specification defines the governance meaning of the Canonical Decision Package as a whole. The conceptual principle governing its uniqueness is defined in Section 8a, and the semantics of its constituent elements are defined in Section 9.

---

# 8a. Decision Package Singularity Principle

For any requested execution event, there SHALL exist exactly one authoritative Canonical Decision Package representing the execution-time governance determination produced by a conformant SOGA implementation.

This principle follows from the governance model defined by this specification. Governance evaluation produces a single determination for a requested execution event, and that determination is represented by a single Canonical Decision Package.

Multiple actors, systems, policies, protocols, or advisory processes MAY contribute information to the Runtime Envelope or otherwise inform governance evaluation. Such contributions constitute governance-relevant inputs rather than independent governance determinations.

Accordingly, conformant implementations SHALL NOT produce multiple authoritative Canonical Decision Packages for the same requested execution event. The existence of multiple sources of evidence or multiple advisory evaluations does not alter the requirement that governance evaluation produces a single authoritative execution-time governance artifact.

This principle distinguishes governance evaluation from arbitration among competing decisions. The Runtime Envelope MAY contain conflicting or incomplete information requiring governance evaluation, but such conditions remain inputs to a single governance determination rather than alternative authoritative outcomes.

The Decision Package Singularity Principle ensures that downstream consumers, including execution systems, visualization systems, audit systems, and other conformant implementations, operate upon a single authoritative governance artifact rather than constructing or selecting among competing governance interpretations.

---

# 9. Canonical Schema and Field Semantics

This section defines the governance semantics of the elements that comprise the Canonical Decision Package. It defines what each element means and why it exists. It does not prescribe a serialization format, encoding, or implementation-specific representation.

A field SHALL be included in the Canonical Decision Package only if it contributes governance meaning necessary for independent interpretation of the execution-time governance determination.

A field SHALL NOT be included solely to support visualization, storage optimization, implementation convenience, or other concerns that do not contribute governance meaning.

The omission of a field SHALL NOT alter the governance meaning of any remaining field. Likewise, the addition of implementation-specific fields SHALL NOT alter the normative meaning of the Canonical Decision Package defined by this specification.

---

## 9.1 Governance Determination

The Governance Determination records the execution-time governance outcome produced by evaluation of the Runtime Envelope.

A conformant Canonical Decision Package SHALL contain exactly one Governance Determination.

The Governance Determination SHALL be one of the following values:

- ALLOW
- RESTRICT
- DENY

### ALLOW

ALLOW indicates that governance evaluation determined that the requested execution remained legitimate under the evaluated runtime conditions and may proceed in accordance with the governance determination represented by the Canonical Decision Package.

### RESTRICT

RESTRICT indicates that governance evaluation determined that execution may proceed only under explicitly constrained governance conditions. RESTRICT is a governance determination distinct from both ALLOW and DENY and SHALL NOT be interpreted as a softened DENY.

When the Governance Determination is RESTRICT, the Canonical Decision Package SHALL identify the associated RESTRICT mode defined by the governing implementation profile.

### DENY

DENY indicates that governance evaluation determined that the requested execution shall not proceed under the evaluated runtime conditions.

The Governance Determination records the governance outcome itself. It does not prescribe the internal reasoning process by which that outcome was produced, nor does it define the execution behavior of downstream consumers beyond the governance meaning represented by the Canonical Decision Package.

---

## 9.2 Governance Dimension Evaluations

The Canonical Decision Package SHALL record the governance evaluations that collectively produced the Governance Determination.

Each recorded governance dimension represents an independent governance evaluation. A dimension SHALL convey its own governance meaning and SHALL NOT derive its meaning from the evaluation result of another dimension.

A conformant Canonical Decision Package SHALL contain evaluations for the following six governance dimensions:

- Mission
- Authority
- Subject Governance State
- Reachability
- Execution Context
- Policy

For each governance dimension, the Canonical Decision Package SHALL record the evaluation outcome determined by the conformant implementation.

The evaluation outcome for each governance dimension SHALL be one of the following values:

- PASS
- REVIEW
- FAIL

### PASS

PASS indicates that the evaluated governance dimension did not identify a condition requiring governance restriction or governance denial under the evaluated runtime conditions.

### REVIEW

REVIEW indicates that the evaluated governance dimension identified a condition requiring constrained governance evaluation. REVIEW is distinct from both PASS and FAIL and SHALL NOT be interpreted as either implicit approval or implicit denial.

A REVIEW outcome contributes governance meaning to the overall Governance Determination but does not itself determine the final Governance Determination.

### FAIL

FAIL indicates that the evaluated governance dimension identified a condition that does not satisfy the governance requirements applicable under the evaluated runtime conditions.

The Canonical Decision Package SHALL preserve the individual governance dimension evaluations that contributed to the Governance Determination. The Governance Determination is derived from those evaluations but SHALL NOT replace or obscure them.

This specification defines the governance meaning of PASS, REVIEW, and FAIL. It does not prescribe the internal evaluation algorithms, weighting mechanisms, precedence rules, or implementation-specific reasoning used to produce those outcomes, provided that conformant implementations produce semantically equivalent Canonical Decision Packages for equivalent runtime conditions.

---

## 9.3 Authority Computation Inputs

The Authority dimension evaluates whether delegated authority remains legitimate at the point of execution. The Canonical Decision Package SHALL preserve the governance meaning of the Authority evaluation and the Authority computation inputs upon which that evaluation was based.

This specification defines the governance meaning of Authority computation inputs. It does not prescribe the algorithms, thresholds, attenuation models, or implementation-specific reasoning used to evaluate those inputs.

A conformant Canonical Decision Package SHALL preserve the Authority computation inputs necessary for independent interpretation of the Authority dimension evaluation.

The Authority computation inputs MAY include, but are not limited to:

- Elapsed Time
- Delegation Chain State
- Delegation Attenuation
- Revocation Status
- Other governance-relevant Authority inputs

### Elapsed Time

Elapsed Time represents the governance-relevant temporal relationship between delegation and the requested execution event. It provides governance meaning regarding the persistence of delegated authority and SHALL be interpreted as an input to Authority evaluation rather than as a governance determination.

### Delegation Chain State

Delegation Chain State represents the governance-relevant characteristics of the delegation relationship existing at the point of execution, including information such as delegation depth or chain composition where relevant to governance evaluation.

### Delegation Attenuation

Delegation Attenuation represents governance-relevant reduction, limitation, or qualification of delegated authority arising from the delegation relationship or other runtime conditions. It is an Authority computation input rather than a governance determination.

### Revocation Status

Revocation Status represents governance-relevant information indicating whether delegated authority has been withdrawn, terminated, or otherwise affected by a revocation event relevant to Authority evaluation.

Authority computation inputs SHALL contribute governance meaning to the Authority dimension evaluation but SHALL NOT themselves constitute the Authority evaluation, the Governance Determination, or the Canonical Decision Package.

This specification intentionally does not prescribe how Authority computation inputs are combined, weighted, prioritized, or otherwise evaluated. Conformant implementations MAY employ different Authority evaluation mechanisms, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

---

## 9.4 Subject Governance State

The Subject Governance State represents the governance-relevant capacity of the subject at the point of execution. It is a governance input to evaluation and SHALL NOT be interpreted as a medical diagnosis, legal determination, or clinical assessment.

A conformant Canonical Decision Package SHALL preserve the Subject Governance State that contributed to the governance evaluation.

This specification defines the governance meaning of Subject Governance State. It does not prescribe the mechanisms by which that state is determined or the evidence from which it is derived. Conformant implementations MAY employ different assessment mechanisms, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

The Subject Governance State SHALL be represented by one of the following values:

- Independent
- Supervised
- Managed
- Delegated
- Lapsed

### Independent

Independent indicates that the subject retains governance capacity sufficient to exercise authority without governance intervention beyond that required by the applicable mission and policy.

### Supervised

Supervised indicates that the subject retains governance capacity but that execution is expected to occur under governance oversight, monitoring, or assistance appropriate to the runtime conditions.

### Managed

Managed indicates that governance evaluation recognizes that authority is exercised through an established management or support relationship that contributes governance meaning to the execution-time determination.

### Delegated

Delegated indicates that governance evaluation recognizes that execution is occurring through delegated authority exercised on behalf of the subject within the applicable governance relationship.

### Lapsed

Lapsed indicates that the governance relationship no longer supports the requested exercise of delegated authority under the evaluated runtime conditions. Lapsed is a governance state and SHALL NOT be interpreted solely as a revocation event or as a permanent condition of the subject.

Subject Governance State contributes governance meaning to the overall evaluation but SHALL NOT by itself constitute the Governance Determination. The Governance Determination results from evaluation of the Runtime Envelope as a whole.

---

## 9.5 Reachability

Reachability represents the governance-relevant ability of the subject to be contacted or to participate in governance at the point of execution. It is a runtime condition and SHALL NOT be interpreted as a Subject Governance State, an Execution Context, or a Governance Determination.

A conformant Canonical Decision Package SHALL preserve the Reachability condition that contributed to the governance evaluation.

This specification defines the governance meaning of Reachability. It does not prescribe the mechanisms by which Reachability is determined or the evidence from which it is derived. Conformant implementations MAY employ different mechanisms for determining Reachability, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

The Reachability condition SHALL be represented by one of the following values:

- Reachable
- Unreachable
- Unknown

### Reachable

Reachable indicates that the subject is governance-relevantly available for communication, participation, confirmation, or other interaction that may contribute to execution-time governance evaluation under the evaluated runtime conditions.

### Unreachable

Unreachable indicates that the subject is governance-relevantly unavailable for communication or participation under the evaluated runtime conditions. Unreachable is a runtime condition and SHALL NOT be interpreted as a Subject Governance State or as evidence that delegated authority is automatically denied.

### Unknown

Unknown indicates that the Reachability condition cannot be determined with sufficient governance confidence under the evaluated runtime conditions. Unknown is a governance-relevant runtime condition and SHALL NOT be interpreted as equivalent to either Reachable or Unreachable.

Reachability contributes governance meaning to the overall evaluation but SHALL NOT by itself constitute the Governance Determination. The Governance Determination results from evaluation of the Runtime Envelope as a whole.

---

## 9.6 Execution Context

Execution Context represents the governance-relevant circumstances under which the requested execution is evaluated at the point of execution. It is a runtime condition and SHALL NOT be interpreted as a Subject Governance State, a Reachability condition, an Authority computation input, or a Governance Determination.

A conformant Canonical Decision Package SHALL preserve the Execution Context that contributed to the governance evaluation.

This specification defines the governance meaning of Execution Context. It does not prescribe the mechanisms by which Execution Context is determined, represented, or derived. Conformant implementations MAY employ different mechanisms for determining Execution Context, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

Execution Context encompasses the governance-relevant circumstances surrounding the requested execution event. Such circumstances MAY include, but are not limited to:

- Operational conditions
- Environmental conditions
- Mission progression
- Temporal circumstances
- Other governance-relevant execution conditions

The foregoing categories define classes of governance-relevant information rather than prescribed fields or implementation requirements.

Execution Context contributes governance meaning to the overall evaluation but SHALL NOT by itself constitute the Governance Determination. The Governance Determination results from evaluation of the Runtime Envelope as a whole.

Execution Context provides governance meaning regarding the circumstances of execution. It does not itself authorize, prohibit, or determine execution, nor does it replace the independent governance meaning contributed by Mission, Authority, Subject Governance State, Reachability, or Policy.

---

## 9.7 Policy

Policy represents governance-relevant constraints, obligations, permissions, or prohibitions applicable to the requested execution event at the point of execution. It is an independent governance dimension and SHALL NOT be interpreted as a Mission, an Authority computation input, a Subject Governance State, a Reachability condition, an Execution Context, or a Governance Determination.

A conformant Canonical Decision Package SHALL preserve the Policy evaluation that contributed to the governance determination.

This specification defines the governance meaning of the Policy dimension. It does not prescribe the policy language, policy engine, rule representation, decision algorithm, or implementation architecture by which Policy is evaluated. Conformant implementations MAY employ different policy representations and evaluation mechanisms, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

Policy evaluation encompasses governance-relevant rules applicable to the requested execution event. Such rules MAY originate from legal, organizational, contractual, mission-specific, operational, or other governance authorities relevant to execution.

The origin, representation, or implementation of Policy SHALL NOT alter its governance meaning within the Canonical Decision Package. This specification defines the governance meaning of the Policy dimension rather than the mechanism by which Policy is expressed or evaluated.

Policy contributes governance meaning to the overall evaluation but SHALL NOT by itself constitute the Governance Determination. The Governance Determination results from evaluation of the Runtime Envelope as a whole.

Policy provides governance meaning regarding applicable constraints on execution. It does not itself authorize, prohibit, or determine execution, nor does it replace the independent governance meaning contributed by Mission, Authority, Subject Governance State, Reachability, or Execution Context.

---

## 9.8 Mission

The Mission dimension represents the governance meaning of the delegated intent associated with the requested execution event. It defines the objective against which execution-time governance evaluation is performed and SHALL NOT be interpreted as an Authority computation input, a Subject Governance State, a Reachability condition, an Execution Context, a Policy determination, or a Governance Determination.

A conformant Canonical Decision Package SHALL preserve the Mission evaluation that contributed to the Governance Determination.

This specification defines the governance meaning of the Mission dimension. It does not prescribe the representation, serialization, authoring process, natural language expression, semantic model, or implementation architecture by which a Mission is created or interpreted. Conformant implementations MAY employ different Mission representations, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

The Mission dimension represents the delegated objective that governance evaluation seeks to preserve. It provides the semantic basis for determining whether a requested execution remains consistent with the delegated intent established for that Mission.

Mission progression, however, is distinct from the Mission dimension itself. Mission progression represents a governance-relevant circumstance describing where execution resides within the lifecycle of the delegated objective and therefore contributes governance meaning through the Execution Context dimension rather than through the Mission dimension.

Accordingly, the Mission dimension defines what delegated objective is being governed, while Execution Context may describe where execution occurs within that objective. These concepts are complementary and SHALL NOT be interpreted as equivalent or interchangeable.

Mission contributes governance meaning to the overall evaluation but SHALL NOT by itself constitute the Governance Determination. The Governance Determination results from evaluation of the Runtime Envelope as a whole.

Mission provides governance meaning regarding delegated intent. It does not itself authorize, prohibit, or determine execution, nor does it replace the independent governance meaning contributed by Authority, Subject Governance State, Reachability, Execution Context, or Policy.

---

## 9.9 Execution Receipt, Provenance, and Timestamp

The Canonical Decision Package SHALL preserve sufficient governance information to enable an independent consumer to determine what governance determination was produced, the provenance of that determination, and when the determination was made.

### Execution Receipt

The Execution Receipt records the governance outcome associated with the requested execution event. It represents the execution-time governance receipt corresponding to the Canonical Decision Package and SHALL NOT be interpreted as an authentication credential, an authorization grant, a delegation artifact, or the Governance Determination itself.

A conformant Canonical Decision Package SHALL contain an Execution Receipt.

The Execution Receipt provides governance meaning regarding the recorded execution event. It does not itself authorize, prohibit, or determine execution, nor does it replace the independent governance meaning contributed by the Governance Determination or the six governance dimensions.

### Provenance

Provenance records the governance origin of the Canonical Decision Package sufficient for independent interpretation and audit.

A conformant Canonical Decision Package SHALL contain Provenance information sufficient to identify the governance source responsible for producing the Canonical Decision Package.

This specification defines the governance meaning of Provenance. It does not prescribe identifiers, trust frameworks, cryptographic mechanisms, serialization formats, or implementation architectures used to represent Provenance. Conformant implementations MAY employ different provenance mechanisms, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

Provenance contributes governance meaning regarding the origin of the Canonical Decision Package but SHALL NOT by itself constitute the Governance Determination.

### Timestamp

Timestamp records the governance-relevant point in time at which the Canonical Decision Package was produced.

A conformant Canonical Decision Package SHALL contain a Timestamp associated with the governance determination.

This specification defines the governance meaning of Timestamp. It does not prescribe time representations, clock synchronization mechanisms, precision, or implementation architecture. Conformant implementations MAY employ different temporal representations, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

Timestamp contributes governance meaning regarding when the governance determination occurred but SHALL NOT by itself constitute the Governance Determination.

Execution Receipt, Provenance, and Timestamp collectively provide the governance context necessary for independent interpretation, audit, and interoperability of the Canonical Decision Package. They record what governance determination was produced, where it originated, and when it occurred without altering the governance meaning established by the Runtime Envelope and the Governance Determination.

---

*Sections 10 through 15 pending authoring.*

---

## Consolidation Edit Pass Notes
*(For author — not part of specification)*

1. Section 1 — Minor: Consider whether three positioning sentences (Authentication/Authorization/SOGA progression) belong in Section 4 rather than Section 1. Author's decision.
2. Section 8 — Minor: Align "governance meaning necessary for independent interpretation" with Section 2 phrasing "sufficient information for independent interpretation." Recommend "sufficient governance meaning for independent interpretation."
3. Sections 9.4 through 9.9 — Six stray URL references removed during reconstruction. No content affected.
4. Section 9.3 — "where relevant" in Delegation Chain State definition flagged for elaboration in future implementation profile.
5. Section 9.4 — Managed state may benefit from clarifying example in Section 13.
6. Section 9.9 — "implementation profile" introduced in Section 9.1 without definition. Flag for Section 15 Future Work.

Yes.

10. Conformance Requirements

A conformant implementation SHALL produce a Canonical Decision Package that satisfies the normative requirements defined by this specification.

Conformance to this specification is determined by the governance meaning of the Canonical Decision Package produced by an implementation, not by the internal architecture, programming language, evaluation algorithm, storage mechanism, policy engine, protocol stack, or deployment environment used to produce it.

A conformant implementation SHALL produce exactly one authoritative Canonical Decision Package for each requested execution event evaluated under the SOGA Runtime Model.

A conformant Canonical Decision Package SHALL include:

* exactly one Governance Determination;
* governance dimension evaluations for Mission, Authority, Subject Governance State, Reachability, Execution Context, and Policy;
* Authority computation inputs sufficient for independent interpretation of the Authority dimension evaluation;
* the Subject Governance State that contributed to governance evaluation;
* the Reachability condition that contributed to governance evaluation;
* the Execution Context that contributed to governance evaluation;
* the Mission evaluation that contributed to the Governance Determination;
* the Policy evaluation that contributed to the Governance Determination;
* an Execution Receipt;
* Provenance information sufficient to identify the governance source responsible for producing the Canonical Decision Package; and
* a Timestamp associated with the governance determination.

A conformant implementation SHALL preserve the distinction between the Runtime Envelope as the conceptual input to governance evaluation and the Canonical Decision Package as the normative output of governance evaluation.

A conformant implementation SHALL preserve the orthogonality of the six governance dimensions. No governance dimension SHALL derive its meaning from another governance dimension or replace the governance meaning contributed by another dimension.

A conformant implementation SHALL preserve the distinction between Governance Determination values and governance dimension evaluation values. ALLOW, RESTRICT, and DENY are Governance Determination values. PASS, REVIEW, and FAIL are governance dimension evaluation values.

A conformant implementation SHALL preserve RESTRICT as a first-class Governance Determination distinct from both ALLOW and DENY. RESTRICT SHALL NOT be interpreted as a softened DENY.

A conformant implementation SHALL preserve REVIEW as a first-class governance dimension evaluation value distinct from both PASS and FAIL. REVIEW SHALL NOT be interpreted as implicit approval or implicit denial.

A conformant implementation SHALL NOT interpret possession of valid credentials, delegated permissions, authorization grants, or delegation artifacts as sufficient evidence that execution remains legitimate.

A conformant implementation SHALL NOT require any particular authentication protocol, authorization protocol, delegation protocol, credential format, policy language, serialization format, transport mechanism, user interface, audit system, or visualization system.

A conformant implementation MAY use any internal evaluation mechanism, implementation architecture, policy engine, protocol stack, or data representation, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

A conformant implementation SHALL ensure that downstream consumers consume the Canonical Decision Package rather than constructing independent governance interpretations from the Runtime Envelope or underlying implementation state.

A conformant implementation SHALL NOT produce multiple authoritative Canonical Decision Packages for the same requested execution event.

A conformant implementation MAY include implementation-specific extensions, provided that such extensions do not alter, obscure, replace, or contradict the normative governance meaning of the Canonical Decision Package defined by this specification.

Conformance to this specification SHALL be evaluated against the semantic equivalence of the Canonical Decision Package, not against byte-level equivalence, field ordering, serialization form, user interface presentation, or implementation-specific processing behavior.

Excellent. Claude’s review confirms Section 10 without findings, so we can proceed.

11. Interoperability Considerations

The primary objective of this specification is semantic interoperability of execution-time governance determinations rather than implementation uniformity.

Independent conformant implementations MAY differ in programming language, internal architecture, evaluation algorithms, policy engines, serialization formats, deployment environments, storage mechanisms, transport protocols, and implementation technologies, provided that equivalent runtime conditions produce semantically equivalent Canonical Decision Packages.

Accordingly, interoperability under this specification SHALL be determined by the governance meaning represented by the Canonical Decision Package rather than by internal implementation behavior.

A conformant implementation SHALL preserve the governance semantics defined by this specification irrespective of how governance information is acquired, normalized, evaluated, represented, transmitted, or stored.

The Canonical Decision Package serves as the normative execution-time governance artifact exchanged between independent consumers. Such consumers MAY include, but are not limited to:

* execution systems;
* visualization systems;
* audit systems;
* compliance systems;
* governance review systems; and
* other conformant implementations.

Each consumer SHALL interpret the Canonical Decision Package according to the governance semantics defined by this specification and SHALL NOT construct independent governance determinations from implementation-specific internal state.

Two independent implementations operating under equivalent runtime conditions SHOULD produce semantically equivalent Canonical Decision Packages even if their internal evaluation mechanisms, policy representations, runtime architectures, or implementation technologies differ.

Semantic equivalence does not require identical serialization formats, field ordering, identifiers, timestamps, byte sequences, or implementation-specific metadata. It requires preservation of the governance meaning represented by the Canonical Decision Package.

Nothing in this specification requires interoperability at the protocol, transport, credential, policy language, or implementation framework level. Those concerns remain independent of the governance semantics defined by this specification.

The Canonical Decision Package therefore provides a protocol-independent execution-time governance artifact capable of supporting interoperability across heterogeneous identity, authorization, delegation, and policy ecosystems while preserving a common governance interpretation.

This specification intentionally defines governance semantics rather than implementation architecture. Interoperability is achieved through shared governance meaning expressed by the Canonical Decision Package, not through identical internal implementations.

12. Security and Governance Considerations

This specification defines the governance semantics of the Canonical Decision Package. It does not prescribe cryptographic mechanisms, trust frameworks, authentication protocols, authorization protocols, transport security, or implementation-specific security architectures. Those concerns remain the responsibility of the conformant implementation and its operating environment.

The security objective of this specification is preservation of the integrity, provenance, and governance meaning of the Canonical Decision Package throughout its lifecycle.

A conformant implementation SHALL preserve the integrity of the Canonical Decision Package such that its governance meaning cannot be altered without producing a different governance artifact.

A conformant implementation SHALL preserve Provenance information sufficient for an independent consumer to identify the governance source responsible for producing the Canonical Decision Package.

Consumers of the Canonical Decision Package SHALL interpret the artifact according to the governance semantics defined by this specification and SHALL NOT construct alternative governance determinations from implementation-specific internal state, partial representations, or external assumptions.

The Runtime Envelope and the Canonical Decision Package represent distinct governance artifacts. A conformant implementation SHALL preserve this distinction throughout evaluation, storage, transmission, and consumption. The Runtime Envelope is the conceptual input to governance evaluation. The Canonical Decision Package is the normative output.

Because execution-time governance may depend upon changing runtime conditions, possession of valid credentials, delegated permissions, authorization grants, delegation artifacts, or previously issued Canonical Decision Packages SHALL NOT by itself be interpreted as sufficient evidence that a requested execution remains legitimate.

A conformant implementation SHALL preserve the Decision Package Singularity Principle by ensuring that no more than one authoritative Canonical Decision Package exists for a given requested execution event. Multiple sources of evidence, advisory processes, or evaluation mechanisms MAY contribute to governance evaluation, but they SHALL NOT produce multiple authoritative governance artifacts for the same execution event.

This specification intentionally separates governance semantics from cryptographic implementation. Integrity protection, authentication of provenance, secure transport, and related security mechanisms MAY be implemented using any appropriate technology, provided that such mechanisms preserve the governance meaning represented by the Canonical Decision Package.

The greatest governance risk addressed by this specification is consumer drift: the reinterpretation, reconstruction, or replacement of the governance determination by downstream systems. Accordingly, downstream consumers SHALL consume the Canonical Decision Package as the authoritative execution-time governance artifact and SHALL NOT derive independent governance determinations from partial information or implementation-specific state.

Security under this specification is therefore achieved through preservation of governance meaning, integrity of the Canonical Decision Package, maintenance of provenance, and faithful interpretation by conformant consumers rather than through any prescribed implementation technology or cryptographic mechanism.

Certainly. This is the complete proposed Section 13 for Claude’s Gate 1 review.

13. Examples

The examples in this section are informative rather than normative. They illustrate the governance semantics defined by this specification and do not prescribe implementation architecture, evaluation algorithms, serialization formats, or implementation-specific behavior.

The SOGA architecture has been developed and refined through evaluation against a set of ten frozen regression scenarios spanning multiple domains of delegated authority. Those scenarios constitute the architectural regression corpus for the reference implementation and are intended to ensure that subsequent architectural evolution preserves previously established governance semantics.

The purpose of the examples presented here is not to reproduce the complete regression corpus, but to illustrate representative applications of the Canonical Decision Package across diverse execution-time governance situations. The complete regression corpus serves as an implementation and conformance asset rather than a normative component of this specification.

The examples that follow demonstrate that the Canonical Decision Package provides a protocol-independent execution-time governance artifact capable of representing governance determinations across heterogeneous domains while preserving common governance semantics.

⸻

Example 1 — Healthcare Proxy

A subject has previously delegated authority permitting a healthcare proxy to authorize emergency treatment when the subject cannot participate in decision-making.

At the point of execution, the Runtime Envelope indicates that the subject is currently unreachable and that the delegated Mission remains consistent with the requested action. Governance evaluation produces a single Canonical Decision Package representing the execution-time determination.

The Governance Determination may be ALLOW, RESTRICT, or DENY, depending upon the evaluated Runtime Envelope. The example illustrates that the governance determination results from execution-time evaluation rather than from the existence of the delegation alone.

⸻

Example 2 — Financial Delegation

A subject has delegated limited authority to an agent to manage financial transactions within a defined Mission.

At the point of execution, the Runtime Envelope indicates that the requested transaction exceeds the delegated Mission or requires additional governance conditions. Governance evaluation produces a single Canonical Decision Package recording the resulting determination.

The Canonical Decision Package records the execution-time governance determination together with the governance semantics that contributed to that determination. It does not merely restate the original delegation or authorization.

⸻

Example 3 — Multi-Agent Advisory Environment

Multiple advisory agents independently analyze the same requested execution event and provide differing recommendations.

Those recommendations contribute governance-relevant information to the Runtime Envelope but do not themselves constitute governance determinations.

The conformant implementation evaluates the Runtime Envelope and produces exactly one authoritative Canonical Decision Package for the requested execution event.

This example illustrates the Decision Package Singularity Principle. Multiple sources of evidence may contribute to governance evaluation, but downstream consumers receive a single authoritative execution-time governance artifact rather than multiple competing governance determinations.

⸻

These examples are illustrative rather than normative. They demonstrate governance semantics rather than implementation behavior and SHALL NOT be interpreted as prescribing evaluation algorithms, policy rules, implementation architectures, or serialization formats.

The normative requirements of this specification are defined by the preceding sections. The examples serve only to illustrate how those requirements may be expressed through representative execution-time governance scenarios.

14. Non-Goals

This specification intentionally defines the governance semantics of the Canonical Decision Package. It does not attempt to define the entirety of identity, authorization, delegation, policy, or execution architecture.

Accordingly, the following are explicit non-goals of this specification:

1. Authentication Protocols
    This specification does not define or modify authentication protocols, identity proofing mechanisms, credential issuance, or methods for establishing the identity of an actor.
2. Authorization Protocols
    This specification does not define or replace authorization protocols, permission models, access control systems, or mechanisms for granting delegated authority.
3. Delegation Mechanisms
    This specification does not define delegation protocols, token formats, delegation chains, credential structures, or methods by which delegated authority is communicated between parties.
4. Policy Languages and Policy Engines
    This specification does not define policy languages, rule syntaxes, policy evaluation engines, or implementation frameworks. It defines only the governance meaning represented by the resulting Canonical Decision Package.
5. Evaluation Algorithms
    This specification does not prescribe the algorithms, weighting mechanisms, precedence rules, scoring models, inference techniques, or decision logic used to evaluate the Runtime Envelope. Independent implementations MAY employ different evaluation mechanisms while remaining conformant.
6. Serialization and Transport
    This specification does not define serialization formats, message schemas, APIs, transport protocols, storage models, or communication mechanisms for the Canonical Decision Package.
7. User Interfaces and Visualization
    This specification does not define dashboards, visualizations, user interfaces, reporting systems, or presentation formats. Such systems consume the Canonical Decision Package but SHALL NOT redefine or reinterpret its governance meaning.
8. Execution Behavior
    This specification does not prescribe how downstream systems execute, reject, defer, supervise, escalate, or otherwise operationalize a Governance Determination. It defines the governance artifact representing the determination, not the implementation-specific behavior that follows.

The exclusion of these topics is intentional rather than accidental. By limiting its scope to the governance semantics of the Canonical Decision Package, this specification enables independent implementations to interoperate through common execution-time governance meaning while preserving freedom of implementation.

Before we send this to Claude, I think Section 15 should be deliberately conservative. Future Work should record areas intentionally deferred, not promise features. That is consistent with the discipline we’ve maintained throughout the specification.

15. Future Work

This specification defines the governance semantics of the Canonical Decision Package as established through the current SOGA architecture and implementation experience. It intentionally leaves certain topics for future standardization, implementation profiles, and independent evaluation.

Future work may include, but is not limited to, the following areas:

1. Implementation Profiles
    This specification defines the governance semantics of the Canonical Decision Package but does not define implementation profiles that may standardize RESTRICT modes, implementation-specific extensions, or other deployment-specific behaviors. Future work may define such profiles while preserving the normative semantics established by this specification.
2. Mission Semantic Types
    The Mission dimension defines the governance meaning of delegated intent but does not define standardized semantic classifications for Mission expression. Future work may establish interoperable Mission semantic types while preserving implementation independence.
3. Dimension-to-Determination Evaluation Models
    This specification intentionally does not prescribe the algorithms, weighting mechanisms, precedence rules, or reasoning processes by which governance dimension evaluations contribute to the Governance Determination. Future work may define evaluation profiles or reference models without altering the normative governance semantics defined herein.
4. Conformance Testing
    The architecture supporting this specification has been exercised against a frozen regression corpus of representative delegated authority scenarios. Future work may establish formal conformance test suites and interoperability testing procedures derived from that corpus.
5. Additional Governance Profiles
    This specification is protocol-independent and domain-independent. Future work may define governance profiles applicable to particular domains, including healthcare, finance, legal delegation, autonomous systems, and other execution-time governance environments, provided such profiles remain consistent with the normative semantics of the Canonical Decision Package.
6. Runtime Envelope Extensions
    This specification defines the Runtime Envelope as the conceptual input to governance evaluation but intentionally does not prescribe its representation or sources. Future work may standardize additional Runtime Envelope profiles, evidence models, or advisory input models while preserving the Decision Package Singularity Principle.

The topics identified in this section are intentionally deferred rather than omitted. Their exclusion from the current specification reflects the architectural objective of defining stable execution-time governance semantics before standardizing implementation-specific profiles or interoperability mechanisms.

Nothing in this section SHALL be interpreted as modifying the normative requirements defined elsewhere in this specification. Future work is expected to build upon, rather than redefine, the governance semantics established by this Editor’s Draft.