# RuntimeEnvelope Specification v0.1
## Part I — Foundations

**Specification:** Canonical Runtime Representation for Execution-Time Governance  
**Status:** Accepted Draft  
**Version:** v0.1  
**Phase:** Phase 2  
**Repository Path:** `specifications/runtime-envelope/v0.1/part-1.md`

---

## 1. Introduction

Autonomous and semi-autonomous systems increasingly act under delegated authority. A human, organization, agent, workflow, or protocol may authorize an action before that action is actually performed. Existing identity and authorization systems can describe who is acting and what authority was granted. They do not, by themselves, determine whether that authority should still be exercised at the moment of execution.

Execution-time governance addresses this gap.

Execution-time governance evaluates whether an authority-bearing action remains legitimate when execution is attempted. This evaluation may depend on the mission context, delegated authority, subject condition, runtime state, policy constraints, environmental conditions, and the specific execution request.

The RuntimeEnvelope is the canonical runtime representation consumed by the SOGA Governance Server at the execution boundary.

The purpose of the RuntimeEnvelope is to provide a protocol-independent structure for governance-relevant runtime inputs. It allows evidence from different sources to be projected into a common form before governance evaluation occurs.

- A RuntimeEnvelope does not grant authority.
- A RuntimeEnvelope does not make a governance decision.
- A RuntimeEnvelope does not execute an action.
- A RuntimeEnvelope carries the canonical inputs required for execution-time governance. It acts as an out-of-band contract compilation target; it does not introduce an active network layer, runtime proxy, or transport wrapper.

The RuntimeEnvelope exists because protocol artifacts alone are insufficient as governance inputs. Protocols may carry tokens, credentials, scopes, claims, delegation chains, event tokens, or authorization context. These artifacts may be valid and still not answer the execution-time governance question: *Should this authority be exercised now?*

The RuntimeEnvelope provides the structured input required to answer that question.

---

## 2. Architectural Position

The RuntimeEnvelope sits immediately before governance evaluation and immediately after protocol-specific or system-specific projection. It is located at the SOGA execution boundary.

The execution boundary separates systems that plan, authorize, delegate, orchestrate, or request action from the SOGA Governance Server that evaluates execution-time legitimacy.

The canonical flow is:

~~~text
[ Human Intent ]
      │
      ▼
[ Mission Builder / Planning System ]
      │
      ▼
[ Mission or Task Representation ]
      │
      ▼
[ Runtime / Orchestrator ]
      │
      ▼
[ Execution Request ] ───► [ Protocol-Specific Evidence ]
      │
      ▼
[ SOGA RuntimeEnvelope ]
      │
      ▼
[ SOGA Governance Server ]
      │
      ▼
[ ALLOW / RESTRICT / DENY ]
      │
      ▼
[ Canonical Decision Package ]
      │
      ▼
[ Execution Layer ]
~~~

The RuntimeEnvelope is the input to the SOGA Governance Server. The Governance Server MUST evaluate RuntimeEnvelopes as canonical runtime inputs. The Governance Server MUST NOT depend on the original protocol-specific structure once projection into the RuntimeEnvelope has occurred.

The RuntimeEnvelope MAY be produced from AAuth, UCAN, ZCAP, OAuth, GNAP, MCP, enterprise workflow systems, human-authored artifacts, internal orchestration systems, or future delegation mechanisms. No protocol is privileged. No protocol is required. Protocol-specific systems remain outside the Governance Server.

### 2.1 Relationship to AAuth

AAuth may provide governance-relevant evidence, including agent identity, delegated authority, authorization context, resource context, execution request data, subscribe tokens, event tokens, or Agent Provider context. An AAuth adapter MAY project AAuth-specific artifacts into a RuntimeEnvelope.

The RuntimeEnvelope does not extend AAuth. The RuntimeEnvelope does not alter AAuth token semantics. The RuntimeEnvelope does not replace AAuth Events, AAuth Protocol, AAuth R3, or AAuth Bootstrap. AAuth remains a protocol source. The RuntimeEnvelope is the canonical governance input produced after projection.

AAuth Events introduces event tokens and subscribe tokens as additional AAuth artifacts. An AAuth adapter MAY project event token claims, subscription context, and `eid` correlation into RuntimeEnvelope fields. The `eid` MAY be preserved as mission correlation metadata. The event token `exp` claim MAY inform runtime condition evaluation. Because event-driven tokens carry state assertions across asynchronous boundaries, the RuntimeEnvelope processes these tokens as point-in-time cryptographic evidence of an event's occurrence, without requiring synchronous, blocking validation calls at T-execution.

### 2.2 Relationship to UCAN and ZCAP

UCAN and ZCAP artifacts may express delegated capabilities, caveats, attenuation, resource targets, authorized actions, or delegation chains. A UCAN or ZCAP adapter MAY project these artifacts into the RuntimeEnvelope authority field and related metadata.

The RuntimeEnvelope does not replace capability delegation. The RuntimeEnvelope treats capability artifacts as evidence, not as final governance decisions.

### 2.3 Relationship to OAuth and GNAP

OAuth and GNAP artifacts may provide access tokens, authorization grants, scopes, resource indicators, claims, subject identity, client identity, or proof-of-possession context. An OAuth or GNAP adapter MAY project these artifacts into RuntimeEnvelope authority, subject, execution context, policy, or metadata fields.

The RuntimeEnvelope does not redefine OAuth or GNAP authorization semantics. The Governance Server evaluates the projected runtime meaning of these artifacts as evidence.

### 2.4 Relationship to MCP

MCP may provide tool context, tool invocation requests, agent/tool boundaries, server metadata, resource descriptions, or runtime action requests. An MCP adapter MAY project MCP tool invocation context into a RuntimeEnvelope.

The RuntimeEnvelope does not define MCP transport. The RuntimeEnvelope does not define MCP authorization. The RuntimeEnvelope provides the governance-ready representation of an MCP-related execution request when SOGA is used as the execution-time governance layer.

### 2.5 Relationship to Mission Builder

Mission Builder produces mission representations or mission-related artifacts. Mission Builder does not produce governance decisions. Mission Builder does not evaluate RuntimeEnvelopes.

Mission Builder may provide mission context that is projected into the RuntimeEnvelope mission field. The Governance Server may evaluate an execution request even when no Mission Builder was involved.

### 2.6 Relationship to Execution Layer

The Execution Layer performs or refuses the action after governance evaluation. The Execution Layer does not determine runtime legitimacy.

The RuntimeEnvelope is not sent to the Execution Layer as permission to execute. The Execution Layer receives governance output, not raw governance input. The Execution Layer relies on the governance output and the Canonical Decision Package, not on the RuntimeEnvelope directly.

---

## 3. Design Principles

### 3.1 Protocol Independence

The RuntimeEnvelope MUST be protocol independent. Protocol-specific artifacts MUST be projected into canonical fields before governance evaluation. The Governance Server MUST NOT require direct knowledge of AAuth, UCAN, ZCAP, OAuth, GNAP, MCP, or any other source protocol in order to evaluate a RuntimeEnvelope.

Adapters MAY preserve original protocol artifacts as evidence references or metadata, but canonical governance evaluation MUST operate on the RuntimeEnvelope structure. Protocol independence ensures that SOGA evaluates execution-time legitimacy rather than protocol compliance.

### 3.2 Immutable Evidence

The RuntimeEnvelope represents the evidence available at the time the execution request reaches the governance boundary. Adapters MUST NOT alter the semantic meaning of source evidence. Adapters MAY normalize, map, or structure evidence into canonical form. Adapters SHOULD preserve provenance sufficient to determine where each evidence element originated.

A RuntimeEnvelope SHOULD be treated as immutable once submitted to the Governance Server. If runtime evidence changes, a new RuntimeEnvelope SHOULD be produced for a new governance evaluation. This principle supports the invariant that one execution event maps to one governance evaluation and one Canonical Decision Package.

### 3.3 Separation of Projection and Governance

Projection is the process of translating source-specific artifacts into canonical RuntimeEnvelope form. Governance is the process of evaluating the RuntimeEnvelope and producing ALLOW, RESTRICT, or DENY.

Adapters perform projection. The Governance Server performs governance. An adapter MUST NOT produce ALLOW, RESTRICT, or DENY. An adapter MUST NOT generate a Canonical Decision Package. An adapter MUST NOT evaluate Subject Agency State. An adapter MUST NOT apply governance policy. This separation prevents protocol adapters from becoming hidden policy engines.

### 3.4 Separation of Governance and Execution

Governance determines whether execution may proceed, must be restricted, or must be denied. Execution performs the action or refuses to perform it.

The RuntimeEnvelope is an input to governance, not an execution instruction. The Governance Server MUST NOT execute the requested action. The Execution Layer MUST NOT reinterpret the RuntimeEnvelope as authority to act. This separation ensures that governance remains an execution-time decision function and that execution remains the responsibility of the host environment.

### 3.5 Runtime Specificity

A RuntimeEnvelope represents one execution request. A mission may produce many execution requests. Each execution request MUST be evaluated independently.

A RuntimeEnvelope MUST NOT aggregate multiple execution events into one governance input. If a mission contains multiple authority-bearing tasks, each task execution attempt SHOULD result in its own RuntimeEnvelope. This supports the SOGA invariant: one execution event maps to one governance evaluation and one Canonical Decision Package.

### 3.6 Evidence, Not Authority

The RuntimeEnvelope carries evidence relevant to authority. It does not itself confer authority. A valid RuntimeEnvelope does not imply ALLOW. A valid delegation artifact inside a RuntimeEnvelope does not imply ALLOW. A valid authorization token inside a RuntimeEnvelope does not imply ALLOW.

The presence of a cryptographically valid permission token within the envelope is evaluated as an assertion of capability, not as a deterministic instruction to execute. The Governance Server determines whether the presented authority should be exercised now.

### 3.7 Universal Policy Semantics

The Governance Server evaluates the RuntimeEnvelope without privileging its origin. A RuntimeEnvelope produced from AAuth, UCAN, ZCAP, OAuth, GNAP, MCP, enterprise workflow, or a local orchestrator MUST be evaluated under the same canonical governance model.

The source of evidence may affect trust, weight, provenance, or policy interpretation, but the source of evidence MUST NOT replace governance evaluation.

### 3.8 Minimal Canonical Surface

The RuntimeEnvelope SHOULD contain only the canonical runtime inputs required for governance evaluation. Protocol-specific detail SHOULD remain in evidence references, metadata, or source artifacts unless required for canonical evaluation.

The RuntimeEnvelope SHOULD avoid becoming a universal protocol translation format, and it SHOULD avoid duplicating the complete internal model of any source protocol. This protects the RuntimeEnvelope from expanding into a replacement protocol.

### 3.9 Reviewability

A RuntimeEnvelope SHOULD be structured so that a human reviewer, auditor, or implementer can understand what evidence was presented to governance. This does not require the RuntimeEnvelope to contain the final decision rationale; decision rationale belongs in the Canonical Decision Package.

The RuntimeEnvelope should make clear:

- What action was requested
- Whose authority is implicated
- What mission or task context is relevant
- What authority evidence was supplied
- What runtime conditions were known
- What policy inputs were presented
- What metadata supports traceability

### 3.10 Versioned Stability

RuntimeEnvelope versions MUST be explicit. A Governance Server MUST know which RuntimeEnvelope version it is evaluating. Backward-incompatible changes MUST require a new version. Versioning supports durable review, testability, regression, and publication. RuntimeEnvelope v0.1 is the first canonical specification version.
