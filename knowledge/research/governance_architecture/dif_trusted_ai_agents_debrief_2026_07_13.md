# DIF Trusted AI Agents WG Debrief
## Execution-Time Governance Reference Implementation

Date: 2026-07-13

Status: Research capture

Source basis: Meeting transcript supplied by Deb following the DIF Trusted AI Agents Working Group session.

This artifact records what was presented, what participants stated, what the discussion revealed, and what remains unresolved.

It does not modify canonical SOGA architecture.

---

## Purpose

Capture the substantive findings from the DIF Trusted AI Agents Working Group discussion following the SOGA briefing and demonstration.

The session began as a five-minute briefing and expanded into an extended architectural discussion covering:

- governance terminology
- PDP, PAP, and PEP boundaries
- execution context
- authorization propagation
- identity
- delegation and attenuation
- mission structure
- Person Server design
- wallets
- capability systems
- related DIF work

---

## Presentation Summary

### Verified

Deb presented the existing SOGA execution path:

Mission Builder
→ Stage Gate
→ Governance evaluation
→ Capability Registry
→ Execution

The presentation included:

- the canonical caregiver scenario
- protocol-independence behavior
- AAuth integration questions
- the broader standards landscape
- an invitation for the Working Group to identify adjacent DIF work

The caregiver demonstration showed:

RESTRICT
→ HOLDING
→ approval event
→ re-evaluation
→ ALLOW
→ EXECUTING

The protocol-independence demonstration showed the same mission, subject state, and ALLOW decision across AAuth, UCAN, and ZCAP fixtures.

---

## 1. Governance Terminology

### Observed

Alan Karp stated that conventional authorization architecture treats governance as a higher-level function concerned with creating or changing policy.

He described the conventional execution path as:

Request
→ Policy Enforcement Point
→ Policy Decision Point
→ policy obtained through a Policy Administration or Policy Access function

Under that conventional model:

- governance creates or changes policy
- the PDP evaluates requests against policy
- the PEP intercepts and enforces decisions
- the PAP provides or administers policy

Alan stated that the current SOGA component labeled `GovernancePDP` appears closer to what he calls a validator or verifier.

He also stated that placing the Capability Registry outside the `GovernancePDP` contributed to his interpretation that the diagram mixed governance and execution responsibilities.

Juan Caballero observed that the AAuth specification itself uses the term runtime governance for contextual decisions that cannot be reduced to predefined machine-evaluable rules.

### Hypothesis

SOGA may occupy a boundary between conventional policy evaluation and a richer execution-time contextual decision function.

The current `GovernancePDP` label may be insufficiently precise because the component can:

- evaluate policy
- evaluate mission context
- evaluate runtime evidence
- return RESTRICT
- initiate or require interaction
- trigger re-evaluation after new evidence arrives

### Future Research

Determine whether the canonical component should remain:

- GovernancePDP

or be described as:

- verifier
- validator
- contextual decision service
- execution-time decision service
- composite governance and policy-evaluation service

No renaming is authorized by this debrief.

---

## 2. Capability Registry Boundary

### Observed

Participants questioned whether the Capability Registry belongs outside the current decision boundary.

The Capability Registry was interpreted as participating in the policy or permission evaluation required to determine whether execution may proceed.

### Hypothesis

The Capability Registry may be:

- descriptive input to the decision service
- part of the policy-access boundary
- part of a broader execution-control envelope
- separate from execution while still participating in evaluation

### Future Research

Clarify whether the Capability Registry is:

1. an external descriptive source
2. a PAP-like input
3. part of the PDP boundary
4. part of an execution-control component
5. unchanged, with only the diagram requiring clarification

No component movement is authorized by this debrief.

---

## 3. Execution Context as the Operative Dimension

### Observed

Nicola Gallo argued that identity alone does not determine whether authority is valid for a particular action.

He described two permissions associated with the same person:

- permission to read all documents for backup
- permission to read one document for summarization and sharing

The identity reference is the same in both cases.

The validity of the authority depends on the execution in which the action occurs.

Nicola described the missing dimension as temporal and execution-specific.

### Verified

SOGA already evaluates mission and runtime context independently from identity.

The repository demonstrates that the same authority evidence may produce a different result when Subject Agency State or execution conditions change.

### Hypothesis

Execution context determines whether previously delegated authority may continue to be exercised.

Identity may be carried for attribution, accountability, audit, revocation, policy lookup, or dispute resolution, but identity alone is not the authorization mechanism.

### Research Position

The operative chain is authorization propagation, with identity carried as reference evidence rather than treated as the mechanism that makes a delegated action valid.

This position is not yet canonical architecture.

### Future Research

Test this position against:

- AAuth
- UCAN
- ZCAP
- KYAOS / CHAOS naming and architecture
- conventional OAuth delegation models
- capability-based authorization literature
- multi-hop delegation scenarios

---

## 4. Authorization Propagation and Attenuation

### Observed

Nicola described authority as flowing through an execution lineage in which each continuation is bounded and non-expansive.

Alan emphasized that external agents require attenuated authority.

His example was that an agent with query and update permission must be able to delegate query-only permission to a less-trusted external agent.

Alan stated that lack of native attenuation is a serious concern in AAuth.

Deb stated that AAuth currently treats attenuation as out of scope based on her discussion with Dick Hardt.

### Hypothesis

AAuth may rely more heavily on server-mediated negotiation, mission context, and Person Server judgment, while UCAN, ZCAP, and related capability systems represent attenuation more directly in delegated artifacts.

These approaches may solve different parts of the problem.

### Future Research

Evaluate:

- how AAuth handles downstream external agents
- whether AAuth negotiation can substitute for portable attenuation
- where attenuation must be enforced
- whether SOGA should evaluate each delegation hop independently
- whether RESTRICT should be available at delegation boundaries as well as execution boundaries

This remains related to backlog item B-020.

---

## 5. Mission as a Governed Execution Object

### Observed

Deb stated that a mission must not only be created but also managed while it runs.

She described a mission as potentially containing:

- intent
- stage gates
- constraints
- expected behavior
- checks
- escalation conditions
- conditions requiring renewed authority

Alan stated that a mission is bounded by permissions.

A mission does not create authority.

The person or system begins with a larger permission set, and a mission receives a subset appropriate to that mission.

### Verified

The current SOGA Mission Builder represents mission intent and governance constraints.

The StageGateEngine determines when evaluation is required during mission execution.

### Hypothesis

The Mission Builder and StageGateEngine together may provide the structure needed to detect and manage mission drift during autonomous execution.

A mission may become the durable object linking:

- intent
- authority subset
- stage progression
- runtime context
- decisions
- approvals
- re-evaluations
- execution records

### Future Research

Clarify:

- which constraints belong in the mission
- which constraints belong in policy
- which constraints belong in delegated authority
- how new permissions are requested
- how mission continuation is re-evaluated
- how nested or multi-agent missions are represented

---

## 6. Person Server as a Powerbox

### Observed

Alan compared the AAuth Person Server to a powerbox from capability-system literature.

He described the powerbox as the user's embodiment in the system, with access to the user's permissions.

Under this interpretation:

- the Person Server is person-scoped
- multiple missions may use one Person Server
- each mission receives a subset of available permissions
- different missions may receive different subsets

Juan described the Person Server as similar to a cloud user agent acting on behalf of the person.

### Verified

The AAuth specification defines the Person Server as chosen by the person.

The previously used resource-scoped model was incorrect.

### Hypothesis

The powerbox analogy may be a useful bridge between AAuth and capability-system terminology.

It may clarify the distinction between:

- person-scoped authority availability
- mission-scoped authority use
- agent-scoped delegated subsets

### Future Research

Review primary capability-system literature on:

- powerboxes
- user agents
- capability selection
- mission-specific permission subsets
- delegated attenuation

Do not treat the analogy as exact until reviewed against primary sources.

---

## 7. Wallet as Person Server

### Observed

Deb asked whether a holder-controlled wallet could serve as an AAuth Person Server.

Alan stated that wallets are generally associated with controlling signing keys and that this would represent only part of Person Server functionality.

Juan stated that the justification and negotiation functions described by AAuth appear more active than ordinary wallet behavior.

### Hypothesis

A wallet may supply components of a Person Server implementation, including:

- keys
- credentials
- signatures
- user-controlled identity material

A complete Person Server may additionally require:

- mission state
- mission history
- justification
- policy access
- interaction
- negotiation
- authorization requests
- contextual decision support

### Future Research

Investigate whether existing holder-controlled wallet projects provide sufficient active-service capabilities to implement Person Server endpoints.

The wallet-as-Person-Server concept remains a fit hypothesis, not a verified implementation pattern.

---

## 8. RESTRICT and Reauthorization

### Observed

Deb described the SOGA decision function as capable of determining that existing authority is insufficient for the current context and that new authorization or interaction is required.

Alan agreed that a Person Server may determine that an agent requires additional permission and apply rules or policy before granting or requesting it.

### Verified

SOGA implements RESTRICT as a first-class execution outcome.

The canonical caregiver scenario demonstrates:

RESTRICT
→ HOLDING
→ new event or approval
→ full re-evaluation
→ ALLOW

### Hypothesis

RESTRICT may represent a transition between:

- policy evaluation
- governance interaction
- authorization renewal
- evidence acquisition
- mission continuation

It may therefore be richer than a conventional binary PDP response.

### Future Research

Determine whether RESTRICT is best modeled as:

- a PDP decision
- an execution interruption state
- a request for additional evidence
- a transition into authorization
- a transition into governance
- a composite lifecycle state

---

## 9. Governance and Enforcement

### Observed

The group distinguished:

- policy creation
- policy access
- policy evaluation
- enforcement
- runtime contextual interpretation

Participants noted that conventional terminology may not fully describe LLM-supported contextual evaluation.

### Hypothesis

SOGA may contain or coordinate two distinct concerns:

1. deterministic policy evaluation and enforcement support
2. contextual governance interpretation for decisions that cannot be completely predefined

These concerns may require separate components or explicit boundaries.

### Future Research

Map the current architecture against:

- PAP
- PDP
- PEP
- verifier
- validator
- governance service
- authorization service
- interaction service

Do not force the architecture into conventional terminology before determining whether the behavior is actually equivalent.

---

## 10. Related DIF and Capability Work

### Observed

Alan stated that KYAOS or CHAOS belongs in the protocol landscape near UCAN and ZCAP.

The exact project spelling and preferred naming were not verified during this session.

The discussion also referenced:

- certificate-based capability systems
- macaroons
- biscuits
- cookie-based confinement
- DIDComm cloud-agent patterns
- powerbox literature
- AuthZEN
- delegated-authority work

### Future Research

Verify the preferred project name directly from its primary repository or specification before adding it to public documentation.

Research:

- KYAOS / CHAOS
- certificate-based capability systems
- macaroons
- biscuits
- DIDComm cloud-agent architecture
- powerbox patterns
- AuthZEN Authorization API

No additional protocol is considered implemented or verified by this debrief.

---

## 11. AAuth Status After the Discussion

### Observed

The Working Group did not reach consensus on AAuth.

Views included:

- AAuth is limited by lack of native attenuation
- AAuth may rely on Person Server negotiation and contextual mission evaluation
- identity chaining does not solve distributed authorization propagation
- the Person Server may represent a powerful user-controlled cloud agent
- AAuth's mission and justification model remains technically interesting even where participants questioned its assumptions

### Hypothesis

AAuth may provide useful mission, interaction, and Person Server primitives while remaining incomplete for portable attenuated delegation.

SOGA may interoperate with AAuth without depending on AAuth as the sole delegation model.

### Future Research

Continue evaluating AAuth alongside UCAN, ZCAP, and capability-based approaches.

Do not represent the Working Group discussion as approval or rejection of AAuth by the group.

---

## 12. Architectural Impact

### Verified

No repository architecture was changed during the meeting.

### Hypothesis

The meeting may require future clarification of:

- GovernancePDP naming
- PAP, PDP, and PEP boundaries
- Capability Registry placement
- RESTRICT semantics
- mission and permission relationships
- Person Server and powerbox relationships
- attenuation and external agents
- authorization propagation terminology

### Future Research

Conduct a terminology and architecture-normalization research sprint before changing canonical component names or boundaries.

---

## 13. Implementation Impact

### Verified

The existing caregiver and protocol-independence demonstrations remain valid.

### Future Research

Inspect the repository before making claims about:

- Christian's connector integration state
- live AAuth services
- live FIDO or CTAP2 integration
- external Governance Server consultation
- AuthZEN projection
- additional protocol adapters

---

## 14. Terminology Normalization

The canonical spelling in repository narrative shall be:

- AAuth, not AOTH
- AuthZEN
- OAuth
- GNAP
- UCAN
- ZCAP

KYAOS / CHAOS remains unverified pending direct inspection of the project's own materials.

Transcript errors may be preserved only inside verbatim quotations.

---

## 15. Open Questions

1. Is SOGA's execution-time evaluator a conventional PDP, a verifier, or a richer contextual decision service?
2. Where do PAP, PDP, PEP, Capability Registry, and governance-policy creation belong?
3. Is RESTRICT a decision, interruption state, interaction request, or lifecycle transition?
4. Is authorization propagation the correct primary framing for delegated execution chains?
5. What role should identity play beyond accountability and reference?
6. How does mission-scoped authority relate to person-scoped powerbox authority?
7. How should attenuation work across external agents?
8. Can a wallet provide part of a Person Server implementation?
9. What does KYAOS / CHAOS contribute relative to UCAN and ZCAP?
10. Which parts of AAuth can be reused without adopting its full identity architecture?

---

## Conclusion

The DIF session validated the execution-context problem while challenging SOGA's terminology and component boundaries.

The group did not identify the problem as already solved.

The principal outcome was a more precise research agenda:

- distinguish governance from policy evaluation and enforcement
- model authorization propagation independently from identity
- clarify mission-scoped authority
- study Person Server and powerbox relationships
- address attenuation for external agents
- normalize terminology before changing architecture

This artifact captures research state only.

It does not authorize architectural modification.
