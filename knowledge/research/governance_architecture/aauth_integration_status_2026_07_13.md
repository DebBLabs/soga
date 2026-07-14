# AAuth Integration Research Status
## SOGA Governance Interface Investigation
Date: 2026-07-13
Status: Research capture
This artifact records the current AAuth integration research state.
It does not define a canonical interface, authorize implementation, or modify SOGA architecture.
---
## Purpose
Separate:
- verified AAuth specification behavior
- observed implementation activity
- SOGA integration hypotheses
- unresolved implementation questions
This document exists to prevent meeting discussion, AI memory, and architectural preference from being mistaken for repository implementation state.
---
## 1. Primary Source Status
### Verified
The AAuth protocol specification was read directly during the July 2026 architecture review.
Foundational findings included:
- the Person Server is person-scoped
- the person chooses the Person Server
- one Person Server may support multiple agents and missions
- missions and Mission Logs are real protocol constructs
- mission context may include history and justification
- the Person Server federates with Access Servers
- AAuth supports deferred interaction behavior
- AAuth does not prescribe one internal Person Server implementation
### Verified
The previously used resource-scoped interpretation of the Person Server was incorrect.
That correction produced G23 — Primary Source Grounding.
### Future Research
Before implementation decisions, re-read the current AAuth draft version directly and verify that all cited behavior remains current.
---
## 2. Governance Server Placement Options
### Observed
Dick Hardt identified two possible integration models:
1. The Person Server communicates mission and authorization requests to an external Governance Server.
2. The Governance Server implements the Person Server role.
Dick presented both as legitimate possibilities for discussion.
He did not select one as the required architecture.
### Hypothesis
The SOGA team currently leans toward the external Governance Server model because it may preserve:
- protocol neutrality
- one governance core
- multiple passive adapters
- separation from identity-plane responsibilities
- reuse across AAuth, UCAN, ZCAP, and future systems
This is a team hypothesis.
It is not an AAuth requirement and was not established as agreement with Dick.
### Future Research
Evaluate both models against:
- Person Server trust
- service discovery
- mission-context access
- policy access
- interaction handling
- privacy boundaries
- deployment complexity
- protocol neutrality
- implementation burden
---
## 3. External Governance Server Consultation
### Hypothesis
A Person Server may consult an external Governance Server by supplying sufficient context for an execution-time decision.
Potential context may include:
- mission
- Mission Log
- requested action
- resource description
- justification
- authority evidence
- policy references
- interaction state
- subject state where available
No canonical request or response schema has been adopted.
### Future Research
Determine:
- how the Governance Server is identified
- how the Person Server trusts it
- what context may be disclosed
- how consent and privacy constraints apply
- whether trust patterns resemble existing Person Server–Access Server trust
- whether consultation requires an AAuth extension, companion specification, or implementation convention
- whether existing authorization APIs can be reused
---
## 4. RESTRICT Mapping
### Verified
SOGA implements three canonical outcomes:
- ALLOW
- RESTRICT
- DENY
RESTRICT is persistent and first-class.
It is not a softened DENY.
### Verified
AAuth defines deferred interaction behavior and uses pending interaction state during unresolved decisions.
### Hypothesis
A SOGA RESTRICT decision may be translated by an AAuth adapter into AAuth-compatible deferred or pending behavior.
Possible conceptual mapping:
SOGA RESTRICT
→ AAuth pending state
→ deferred interaction or waiting behavior
→ new evidence or authorization
→ full SOGA re-evaluation
This mapping has not been adopted as a canonical interface.
### Future Research
Verify against the current primary AAuth specification:
- exact response fields
- state transitions
- interaction semantics
- approval semantics
- polling or continuation behavior
- whether RESTRICT maps to one AAuth state or requires additional SOGA state
---
## 5. Christian Reference Implementation and Connector Work
### Observed
Deb confirmed that Christian's reference implementation was cloned for connector work.
This means the integration effort is not starting from zero.
### Future Research
Inspect the actual local repository and connector code before making claims about:
- exact upstream repository and branch
- current AAuth draft version
- whether the upstream implementation runs unchanged
- which AAuth flows are implemented
- where the Person Server decision point exists
- what connector code has already been added
- whether external Governance Server consultation is wired
- whether deferred interaction is operational
- whether any work is committed
- whether any work exists only outside the SOGA repository
No implementation status beyond the confirmed clone shall be inferred from conversation.
---
## 6. FIDO and CTAP2
### Observed
The interposed.ai / aauth-go implementation discussion described hardware-key interaction using CTAP2.
The distinction identified during research was:
- User Presence indicates that a live human interacted with the authenticator.
- User Verification separately indicates verification of the expected user through an authenticator-supported method.
### Hypothesis
FIDO or CTAP2 may provide evidence for an interaction or approval lifecycle associated with a RESTRICT decision.
This would address evidence capture or liveness.
It would not independently determine contextual governance legitimacy.
### Future Research
Inspect the cloned implementation and connector work to determine:
- whether CTAP2 code is present
- whether a hardware key is required
- whether User Presence is enforced
- whether User Verification is enforced
- what event or evidence is returned
- whether SOGA consumes that evidence
- whether the flow is live, simulated, or planned
Do not describe FIDO as integrated until repository and runtime inspection confirm it.
---
## 7. Enforcement and Governance
### Observed
The DIF discussion distinguished execution enforcement from contextual legitimacy.
Kernel or hardware-backed enforcement may establish that:
- an action was intercepted
- a human interaction occurred
- execution remained blocked until a condition was satisfied
SOGA evaluates a different question:
- whether the authority should be exercised in the current mission and execution context
### Hypothesis
Enforcement and contextual governance may be separate but complementary layers.
Possible lifecycle:
execution intercepted
→ governance consultation
→ ALLOW, RESTRICT, or DENY
→ interaction or evidence capture if required
→ re-evaluation
→ enforcement of the resulting decision
### Future Research
Determine where:
- the PEP resides
- the Governance Server resides
- interaction evidence is captured
- policy is accessed
- the final execution decision is enforced
---
## 8. AuthZEN Authorization API
### Hypothesis
The AuthZEN Authorization API may provide a standardized external interface for projecting SOGA decisions to a Policy Enforcement Point.
Potential symmetry:
AAuth / UCAN / ZCAP evidence
→ RuntimeEnvelope input normalization
→ SOGA decision
→ CDP
→ AuthZEN-compatible output projection
### Verified
No primary-source mapping between the Canonical Decision Package and the AuthZEN Authorization API has yet been completed.
### Future Research
Read the current AuthZEN Authorization API specification directly.
Evaluate:
- request schema
- response schema
- binary decision assumptions
- metadata and obligation support
- extension mechanisms
- representation of RESTRICT
- representation of interaction requirements
- compatibility with CDP evidence and reasoning
- whether AuthZEN is additive to or narrower than CDP
AuthZEN is a research candidate, not an adopted SOGA interface.
---
## 9. Attenuation
### Observed
Dick treated attenuation as outside AAuth's intended protocol scope during discussion with Deb.
Alan Karp identified lack of native attenuation as a serious concern for delegation to less-trusted external agents.
### Hypothesis
AAuth mission and server-mediated negotiation may address contextual authorization without replacing cryptographically attenuated delegation.
AAuth and capability protocols may therefore remain complementary rather than interchangeable.
### Future Research
Evaluate:
- external sub-agent authority
- downstream delegation
- permission narrowing
- delegation-chain verification
- mission-specific authority subsets
- interaction between AAuth and UCAN, ZCAP, or other capability systems
Do not claim that AAuth provides native attenuation unless verified in the current primary specification.
---
## 10. Current Sayable Claim
### Verified
SOGA currently demonstrates:
- execution-time governance evaluation
- ALLOW, RESTRICT, and DENY
- RESTRICT and re-evaluation lifecycle behavior
- protocol-derived fixture normalization
- governance outcome stability across AAuth, UCAN, and ZCAP fixtures
### Observed
Christian's reference implementation was cloned for connector work.
### Not Yet Verified
The repository has not yet been inspected in this sprint to establish:
- live AAuth Person Server consultation
- live external Governance Server integration
- live FIDO or CTAP2 interaction
- AuthZEN output projection
- committed connector implementation state
---
## 11. Open Questions
1. Which exact Christian repository and branch were cloned?
2. What connector code exists today?
3. Does the existing AAuth implementation run unchanged?
4. Where is the Person Server decision hook?
5. Is external Governance Server consultation already partially wired?
6. Is deferred interaction live?
7. Is CTAP2 present and runnable?
8. Does the flow require User Presence, User Verification, or both?
9. What context can the Person Server disclose to a Governance Server?
10. Can SOGA RESTRICT map cleanly to AAuth pending behavior?
11. Can CDP project to AuthZEN without losing RESTRICT?
12. Can one Governance Server interface remain invariant across AAuth, UCAN, and ZCAP?
---
## Architectural Impact
None authorized.
---
## Implementation Impact
Repository and runtime inspection are required before scheduling connector or FIDO implementation work.
---
## Conclusion
AAuth provides useful mission, Person Server, interaction, and contextual-authorization primitives.
SOGA provides protocol-neutral execution-time evaluation and a persistent RESTRICT lifecycle.
An external Governance Server integration is a credible research direction, but the interface, trust model, connector state, and FIDO status remain subject to direct repository and primary-source inspection.
This artifact records research state only.
It does not authorize architectural or implementation changes.
