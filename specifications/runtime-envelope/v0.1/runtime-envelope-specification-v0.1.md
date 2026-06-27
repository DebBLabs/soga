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
# RuntimeEnvelope Specification v0.1
## Part II — Canonical RuntimeEnvelope and Field Semantics

**Specification:** Canonical Runtime Representation for Execution-Time Governance  
**Status:** Draft for Review  
**Version:** v0.1  
**Phase:** Phase 2  
**Repository Path:** `specifications/runtime-envelope/v0.1/part-2.md`

---

## 4. Canonical RuntimeEnvelope

A RuntimeEnvelope is the canonical runtime input object submitted to the SOGA Governance Server for one execution-time governance evaluation.

A RuntimeEnvelope represents one execution request at the execution boundary.

A RuntimeEnvelope MUST contain the canonical fields required for governance evaluation.

A RuntimeEnvelope MUST NOT contain a governance decision.

A RuntimeEnvelope MUST NOT contain a Canonical Decision Package.

A RuntimeEnvelope MUST NOT instruct the Execution Layer to execute.

A RuntimeEnvelope MUST be produced before governance evaluation.

A RuntimeEnvelope SHOULD be treated as immutable once submitted to the Governance Server.

If governance-relevant evidence changes after a RuntimeEnvelope has been submitted, a new RuntimeEnvelope SHOULD be produced for a new governance evaluation.

### 4.1 Overall Object

The RuntimeEnvelope v0.1 object has the following top-level structure:

~~~json
{
  "runtime_envelope_version": "0.1",
  "mission": {},
  "authority": {},
  "subject": {},
  "execution_context": {},
  "policy": {},
  "metadata": {}
}
~~~

The required top-level fields are:

- `runtime_envelope_version`
- `mission`
- `authority`
- `subject`
- `execution_context`
- `policy`
- `metadata`

Each top-level field is a canonical projection of governance-relevant runtime input.

Protocol-specific structures MUST be projected into these canonical fields before governance evaluation.

The Governance Server MAY consider source provenance, trust level, and evidence origin when evaluating a RuntimeEnvelope, but it MUST NOT require direct parsing of the original source protocol in order to perform the governance evaluation.

### 4.2 Top-Level Fields

#### `runtime_envelope_version`

The `runtime_envelope_version` field identifies the RuntimeEnvelope specification version used by the object.

For this specification, the value MUST be:

~~~json
"0.1"
~~~

The Governance Server MUST reject or explicitly downgrade any RuntimeEnvelope version it does not support.

#### `mission`

The `mission` field contains the mission, task, or objective context relevant to the execution request.

The mission context provides continuity and traceability.

The mission context does not itself authorize execution.

#### `authority`

The `authority` field contains the projected authority evidence relevant to the requested execution.

Authority evidence may originate from protocols, credentials, delegation artifacts, workflow systems, human approvals, or internal runtime systems.

Authority evidence is evaluated as evidence, not as an automatic instruction to execute.

#### `subject`

The `subject` field identifies the human, legal person, organization, entity, or principal whose authority, interest, agency, or delegated role is implicated by the execution request.

When Subject Agency State is available, it belongs in this field.

#### `execution_context`

The `execution_context` field describes the requested action and the runtime conditions under which the action is being attempted.

This field identifies what is about to happen.

It is the primary field that binds the RuntimeEnvelope to one execution event.

#### `policy`

The `policy` field contains policy inputs, constraints, rule references, or evaluation context made available to the Governance Server.

The `policy` field does not contain the governance decision.

#### `metadata`

The `metadata` field contains traceability, provenance, source references, timestamps, adapter information, correlation identifiers, and other non-decision information needed for review, audit, debugging, and implementation interoperability.

Source references belong in `metadata`.

Source references are pointers to the evidence presented at T-execution.

Source references MUST NOT be treated as equivalent to the source artifacts themselves.

Source references SHOULD preserve enough provenance to allow a reviewer, auditor, or implementer to identify what evidence was available to governance when the RuntimeEnvelope was created.

### 4.3 Canonical Projection Model

RuntimeEnvelope v0.1 uses a canonical projection model.

In this model:

1. A source system produces protocol-specific, workflow-specific, or runtime-specific artifacts.
2. An adapter projects those artifacts into canonical RuntimeEnvelope fields.
3. The RuntimeEnvelope preserves canonical governance inputs.
4. The RuntimeEnvelope preserves source references for reviewability.
5. The Governance Server evaluates the canonical fields.
6. The Governance Server produces ALLOW, RESTRICT, or DENY.
7. The Canonical Decision Package records the decision and rationale.

The adapter is responsible for projection.

The Governance Server is responsible for evaluation.

The Canonical Decision Package is responsible for decision recordkeeping.

The RuntimeEnvelope is the canonical input boundary between projection and governance.

### 4.4 Canonical Fields and Source References

RuntimeEnvelope v0.1 uses Option B: canonical fields plus source references.

Canonical fields contain the governance-relevant projection.

Source references preserve provenance.

Canonical fields answer:

- What was projected into the governance model?
- What action is being evaluated?
- Whose authority is implicated?
- What runtime conditions are known?
- What policy inputs are available?

Source references answer:

- Where did this evidence come from?
- What source artifact, token, claim, event, credential, request, or system record was used?
- What correlation identifier connects this RuntimeEnvelope to the original source context?
- What was available at T-execution for later audit?

A source reference is not the source artifact.

A source reference is a pointer, identifier, hash, URI, token identifier, event identifier, credential identifier, log reference, or other traceable reference sufficient to support reviewability without duplicating the complete internal model of the source protocol.

This satisfies the Minimal Canonical Surface principle while preserving Reviewability.

### 4.5 Source Reference Examples

AAuth Events may provide:

- `eid` as an event correlation identifier
- event token identifier
- subscribe token identifier
- Agent Provider issuer reference
- resource issuer reference
- event token expiration reference
- event payload reference

UCAN may provide:

- capability token identifier
- delegation chain reference
- caveat reference
- resource/action reference
- token hash

ZCAP may provide:

- capability identifier
- invocation target reference
- caveat reference
- delegation proof reference

OAuth or GNAP may provide:

- access token hash
- grant identifier
- scope reference
- resource indicator
- proof-of-possession key reference
- authorization server issuer reference

MCP may provide:

- tool invocation identifier
- server identifier
- tool name
- resource URI
- call trace identifier

These source references MAY be stored under `metadata.source_references`.

---

## 5. Field Semantics

This section defines the semantics of the RuntimeEnvelope v0.1 fields.

The field definitions are normative unless explicitly marked non-normative.

### 5.1 `mission`

The `mission` field contains mission, task, or objective context relevant to the execution request.

The `mission` field provides continuity and traceability.

The `mission` field MUST NOT be treated as the unit of governance.

The unit of governance is the execution request represented in `execution_context`.

A mission may produce multiple execution requests.

Each execution request requires its own RuntimeEnvelope.

#### 5.1.1 Recommended Structure

~~~json
{
  "mission_id": "mission-123",
  "mission_version": "0.1",
  "mission_source": "mission_builder",
  "objective": "Schedule an earlier medical appointment if one becomes available.",
  "task_id": "task-appointment-waitlist-001",
  "task_description": "Accept an earlier appointment slot if permitted under delegated authority.",
  "constraints": [
    {
      "type": "time_window",
      "value": "Only accept appointments before 2026-07-16T17:00:00Z."
    }
  ]
}
~~~

#### 5.1.2 Field Semantics

`mission_id`

A stable identifier for the mission or mission-like context.

`mission_id` provides traceability.

`mission_id` MUST NOT be used as a substitute for the execution request identifier.

`mission_version`

The version of the mission representation, if available.

`mission_source`

The system or process that produced the mission context.

Examples include:

- `mission_builder`
- `human_authored`
- `workflow_engine`
- `aauth_event`
- `enterprise_orchestrator`
- `unknown`

`objective`

A human-readable statement of the mission objective.

`objective` is contextual evidence.

`objective` MUST NOT be treated as a policy rule.

`task_id`

The identifier for the task or mission step associated with this execution request.

`task_id` MAY be used for traceability across planning and execution systems.

`task_description`

A human-readable description of the task being attempted.

`constraints`

Mission-level constraints that may be relevant to governance evaluation.

Mission constraints may inform governance.

Mission constraints do not replace policy evaluation.

### 5.2 `authority`

The `authority` field contains the projected authority evidence relevant to the execution request.

Authority evidence may originate from protocol tokens, credentials, delegation chains, capability artifacts, prior approvals, workflow rules, or human-authorized records.

The `authority` field carries evidence of permission, delegation, authorization, or capability.

The `authority` field does not determine execution legitimacy by itself.

A valid authority field does not imply ALLOW.

#### 5.2.1 Recommended Structure

~~~json
{
  "authority_type": "delegated",
  "authority_state": "active",
  "grantor": {
    "id": "person-123",
    "type": "human"
  },
  "grantee": {
    "id": "agent-456",
    "type": "agent"
  },
  "scope": [
    "appointments.read",
    "appointments.schedule"
  ],
  "resource": {
    "id": "appointment-system",
    "type": "healthcare_resource"
  },
  "permitted_actions": [
    "accept_earlier_slot"
  ],
  "attenuations": [
    {
      "type": "time_limit",
      "value": "2026-07-16T17:00:00Z"
    }
  ],
  "evidence": [
    {
      "evidence_type": "aauth_event_token",
      "source_reference_id": "src-aauth-event-001"
    }
  ]
}
~~~

#### 5.2.2 Field Semantics

`authority_type`

The kind of authority being presented.

Recommended values include:

- `direct`
- `delegated`
- `capability`
- `workflow`
- `organizational`
- `emergency`
- `unknown`

`authority_state`

The projected state of the authority at T-execution.

Recommended values include:

- `active`
- `expired`
- `revoked`
- `suspended`
- `unknown`

`grantor`

The party that granted, delegated, issued, or originated the authority.

`grantee`

The party attempting to exercise the authority or act under it.

`scope`

The projected scope of the authority.

Scopes SHOULD be expressed in canonical form.

Protocol-specific scope strings MAY be preserved in source references.

`resource`

The resource, service, domain, object, or environment against which the authority is being exercised.

`permitted_actions`

The actions that the projected authority appears to permit.

The presence of an action in `permitted_actions` does not imply ALLOW.

It means the adapter projected the source evidence as asserting that the action is within the presented permission or capability.

`attenuations`

Constraints, caveats, limits, conditions, or reductions attached to the authority evidence.

Examples include:

- time limits
- purpose limits
- resource limits
- supervision requirements
- maximum use counts
- delegation depth limits
- geographic limits
- risk thresholds

`evidence`

A list of canonical evidence summaries associated with the projected authority.

Each evidence entry SHOULD reference a corresponding source reference in `metadata.source_references`.

### 5.3 `subject`

The `subject` field identifies the subject whose agency, authority, interest, or delegated role is implicated by the execution request.

The subject may be a human, legal person, organization, patient, customer, employee, principal, dependent, or other authority-bearing entity.

The `subject` field is also the canonical location for Subject Agency State when available.

#### 5.3.1 Recommended Structure

~~~json
{
  "subject_id": "person-123",
  "subject_type": "human",
  "subject_role": "principal",
  "subject_agency_state": "Supervised",
  "agency_state_source": {
    "source_reference_id": "src-agency-state-001"
  },
  "relevant_conditions": [
    {
      "condition_type": "requires_supervision",
      "value": true
    }
  ]
}
~~~

#### 5.3.2 Field Semantics

`subject_id`

A stable identifier for the subject.

The identifier SHOULD be stable within the governance context.

The identifier does not need to be globally public.

`subject_type`

The kind of subject.

Recommended values include:

- `human`
- `organization`
- `legal_person`
- `agent`
- `group`
- `unknown`

`subject_role`

The subject's role in the execution request.

Recommended values include:

- `principal`
- `grantor`
- `patient`
- `customer`
- `employee`
- `dependent`
- `guardian`
- `delegate`
- `beneficiary`
- `unknown`

`subject_agency_state`

The Subject Agency State known at T-execution.

Allowed values are:

- `Independent`
- `Supervised`
- `Managed`
- `Delegated`
- `Lapsed`

The canonical term is Subject Agency State.

The implementation field is `subject_agency_state`.

`agency_state_source`

A source reference pointer to the evidence supporting the Subject Agency State.

`relevant_conditions`

Additional subject-related runtime conditions relevant to governance evaluation.

These conditions may inform governance but do not themselves produce a governance decision.

### 5.4 `execution_context`

The `execution_context` field describes the specific execution request being evaluated.

This is the primary field binding the RuntimeEnvelope to one execution event.

The `execution_context` field MUST identify what action is being attempted.

The `execution_context` field SHOULD identify the actor, target, requested operation, runtime timestamp, and execution environment.

#### 5.4.1 Recommended Structure

~~~json
{
  "execution_request_id": "exec-789",
  "requested_action": "accept_earlier_slot",
  "actor": {
    "id": "agent-456",
    "type": "agent"
  },
  "target": {
    "id": "appointment-slot-abc",
    "type": "appointment_slot"
  },
  "runtime_timestamp": "2026-06-27T21:45:00Z",
  "execution_environment": {
    "environment_type": "aauth_agent_runtime",
    "system_id": "aauth-demo",
    "host": "agent-provider.example"
  },
  "runtime_conditions": [
    {
      "condition_type": "event_token_expiration",
      "value": "2026-06-27T21:50:00Z"
    }
  ]
}
~~~

#### 5.4.2 Field Semantics

`execution_request_id`

A unique identifier for the execution request.

The execution request is the unit of governance.

`execution_request_id` SHOULD be unique within the producing runtime or orchestrator.

`requested_action`

The action the actor is attempting to perform.

`requested_action` SHOULD be canonicalized by the adapter.

Protocol-specific action names MAY be preserved in source references.

`actor`

The entity attempting to perform the requested action.

The actor may be an agent, workload, human, service, tool, robot, workflow, or other execution-capable entity.

`target`

The object, resource, service, endpoint, tool, environment, or external system against which the requested action is directed.

`runtime_timestamp`

The timestamp at which the RuntimeEnvelope was created or the execution request reached the governance boundary.

`execution_environment`

Information about the environment where execution is being attempted.

`runtime_conditions`

Known runtime conditions relevant to governance.

Examples include:

- event expiration windows
- environmental state
- device state
- network state
- availability window
- risk signal
- supervision state
- emergency state
- current location context
- active session context

Runtime conditions are evidence.

Runtime conditions do not replace governance evaluation.

### 5.5 `policy`

The `policy` field contains policy inputs, rule references, constraints, and evaluation context made available to the Governance Server.

The `policy` field does not contain the governance decision.

The `policy` field does not contain a Canonical Decision Package.

The `policy` field MAY contain policy identifiers, policy version references, jurisdictional context, organizational constraints, or governance dimensions required by the implementation.

#### 5.5.1 Recommended Structure

~~~json
{
  "policy_context_id": "policy-context-001",
  "policy_set": [
    {
      "policy_id": "soga-default-runtime-policy",
      "policy_version": "0.1"
    }
  ],
  "governance_requirements": [
    "evaluate_subject_agency_state",
    "evaluate_authority_state",
    "evaluate_runtime_conditions"
  ],
  "jurisdiction": {
    "type": "organizational",
    "value": "demo"
  }
}
~~~

#### 5.5.2 Field Semantics

`policy_context_id`

An identifier for the policy context presented to governance.

`policy_set`

A list of policy identifiers or policy references available to the Governance Server.

The RuntimeEnvelope MAY reference policy.

The RuntimeEnvelope SHOULD NOT embed a complete policy engine.

`governance_requirements`

Canonical requirements or evaluation dimensions that should be considered by governance.

`jurisdiction`

Jurisdictional, organizational, contractual, or domain context relevant to policy interpretation.

### 5.6 `metadata`

The `metadata` field contains traceability and provenance information.

The `metadata` field SHOULD preserve adapter information, source references, correlation identifiers, creation timestamps, and audit-supporting details.

The `metadata` field MUST NOT contain a governance decision.

The `metadata` field MUST NOT be required for basic semantic interpretation of the canonical fields, but it SHOULD be sufficient to support reviewability and audit.

#### 5.6.1 Recommended Structure

~~~json
{
  "runtime_envelope_id": "re-001",
  "created_at": "2026-06-27T21:45:00Z",
  "created_by": {
    "adapter": "aauth_execution_adapter",
    "adapter_version": "0.1"
  },
  "correlation": {
    "mission_id": "mission-123",
    "execution_request_id": "exec-789",
    "external_correlation_ids": [
      {
        "type": "aauth_eid",
        "value": "evt_8f3k2n9p"
      }
    ]
  },
  "source_references": [
    {
      "source_reference_id": "src-aauth-event-001",
      "source_type": "aauth_event_token",
      "source_protocol": "AAuth Events",
      "issuer": "https://resource.example",
      "subject": "aauth:k7q3p9n2@ap.example",
      "correlation_id": "evt_8f3k2n9p",
      "artifact_reference": {
        "reference_type": "token_hash",
        "value": "sha256:example"
      },
      "observed_at": "2026-06-27T21:45:00Z"
    }
  ]
}
~~~

#### 5.6.2 Field Semantics

`runtime_envelope_id`

A unique identifier for the RuntimeEnvelope.

`created_at`

The timestamp when the RuntimeEnvelope was created.

`created_by`

Information about the adapter, system, or process that created the RuntimeEnvelope.

`correlation`

Identifiers that connect the RuntimeEnvelope to related mission, execution, source, or audit contexts.

`source_references`

A list of source references identifying the evidence projected into the RuntimeEnvelope.

Source references SHOULD be sufficient to identify the evidence available at T-execution.

Source references MAY include:

- token hash
- credential identifier
- event identifier
- event token identifier
- subscribe token identifier
- delegation chain reference
- issuer reference
- resource reference
- agent identifier
- request identifier
- log reference
- trace identifier
- artifact URI
- repository reference
- signed receipt reference

Source references SHOULD NOT duplicate the complete source protocol artifact unless required by the implementation.

Source references are provenance pointers.

Source references support reviewability.

Source references do not replace canonical governance fields.

### 5.7 Source References and Audit Semantics

Source references are part of the RuntimeEnvelope metadata.

They preserve the provenance of evidence without expanding the RuntimeEnvelope into a protocol-specific artifact store.

A source reference SHOULD identify:

- the source protocol or system,
- the type of source artifact,
- the issuer or originator when known,
- the subject or affected entity when known,
- the relevant correlation identifier,
- the artifact reference or hash when available,
- the observation timestamp,
- and the adapter that projected the artifact.

For AAuth Events, the `eid` MAY be used as a source correlation identifier.

For AAuth event tokens, the token expiration claim MAY be projected into `execution_context.runtime_conditions` while the event token reference is preserved in `metadata.source_references`.

For capability systems, the capability identifier or token hash MAY be preserved in `metadata.source_references` while the projected capability semantics appear in `authority`.

For OAuth or GNAP, token hash, grant identifier, scope reference, issuer, and resource indicator MAY be preserved in `metadata.source_references` while the projected authority appears in `authority`.

This model allows governance evaluation to operate over canonical fields while preserving sufficient evidence provenance for later review.

### 5.8 Field Relationship Summary

The RuntimeEnvelope v0.1 field relationship is:

- `mission` provides continuity and task context.
- `authority` provides projected permission, delegation, authorization, or capability evidence.
- `subject` identifies whose agency, authority, or interest is implicated.
- `execution_context` identifies the specific execution request.
- `policy` provides policy inputs and governance constraints.
- `metadata` preserves traceability, provenance, adapter information, and source references.

The Governance Server evaluates the RuntimeEnvelope as a whole.

No single field determines the governance outcome.

No single protocol artifact determines the governance outcome.

The RuntimeEnvelope is the canonical input to governance.

The Canonical Decision Package is the canonical output of governance.
