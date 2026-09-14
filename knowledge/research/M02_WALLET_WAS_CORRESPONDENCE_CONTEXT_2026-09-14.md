# M02 Wallet/WAS Correspondence and Research Context

Date: 2026-09-14
Status: RESEARCH INPUT — NON-AUTHORIZING

## Evidence classification

- **Source-reported, PI-retained:** private 2026-09-10 correspondence with Dmitry Zagidulin; not an independent source-code finding.
- **Verified document-content fact:** the PI supplied the complete 2026-05-07 *Blinding Identity Taxonomy 2.0* Group Editors' Draft, edited by Paul Knowles and John Wunderlich, and Codex read that copy. Publication status and currency were not independently verified; the copy is PI-retained.
- **Source-reported protocol-author statement:** the PI supplied the complete
  AAuth Slack thread rooted by Dick Hardt on 2026-08-30 at 1:10 PM and answered
  by him on 2026-09-14 at 9:56 AM. The permalink was supplied by the PI and was
  not independently accessed. These are author statements, not normative text.
- **Hypothesis or inference:** every architectural conclusion below; none is a compatibility, conformance, or implementation claim.

## Dmitry Zagidulin correspondence

Dmitry reported that separating Freewallet as the person-facing wallet, WAS as wallet-controlled storage, and an AAuth Person Server made sense; WAS modularity was intended although Fastify `inject()` was not specifically designed as a downstream integration pattern; Freewallet is an in-browser client-side React application without a Node backend or supported headless Node signing path; `https://github.com/interop-alliance/did-cli-typescript` may be relevant for headless VC/VP signing; and concrete workflows and reproducible breakage reports would be useful.

These reports support investigation only. They do not establish composition and authorize no acquisition, execution, or change.

## Paul Knowles and BIT 2.0

The supplied BIT 2.0 draft extends its data-field taxonomy to neural, cognitive, affective, behavioral, intentional-inference, and device-interaction data. That verified document-content fact is relevant to B-037 and B-040 because embodied interaction may create identifying or inferential data about participants and non-participants. The draft does not decide whether sensing is permitted, establish consent or representative authority, define HCI policy, or authorize collection. The PI's conversation with Paul is relationship and direction context only unless a citable artifact supports a claim.

## Dick Hardt AAuth Slack thread

The supplied thread begins with Dick's 2026-08-30 1:10 PM “Hey Debbie” message:

> 1 - There was some interesting discussion on wardens on LinkedIn a while
> ago. I don't think we have modeled this well in any of the deployed
> authorization protocols. While important, it is very much an edge case.
>
> 2 - I don't think you are talking about the AP and agent bootstrap -- but
> about the person and agent bootstrap -- correct? That happens at the person
> server. See -11 changes where we define the person token.
>
> 3 - I had considered the PS sending a clarification to the agent if it does
> not have enough context, or if it wants the agent to adjust its request.
> What are you thinking about?

The supplied transcript then shows the PI's opening at 4:08 AM and three
detailed replies at 4:33 AM, 5:43 AM, and 5:49 AM. Their calendar dates are not
displayed in the supplied transcript and are not inferred here. Their exact
concluding questions were:

1. “If representative authority does not belong in the AAuth core protocol,
   where should that evidence—and its binding to the participant, session, and
   governed action—live: a credential profile, a companion specification, or
   the Person Server?”
2. “Does -11 anticipate a participant distinct from the accountable Person
   behind the mission agent? Could the participant’s wallet or browser act as
   their agent, using a person token issued by their chosen Person Server,
   while remaining bound to this mission interaction? Or would a participant
   role and its binding to the mission need to be defined in an application
   profile?”
3. “Do you see that structured clarification living inside the deferred flow
   alongside the Markdown exchange, or as a separate artifact referenced by it?”

Dick's 2026-09-14 9:56 AM reply appears in that same thread. Supplied permalink:
`https://aauth.slack.com/archives/C0B0JGDU789/p1789394193423139?thread_ts=1788109843.696759&cid=C0B0JGDU789`.

Dick's reply reads:

> Q1 - the PS manages which entity the human interacting at the PS is acting
> for. That happens when humans act on behalf of an organization, and when a
> parent acts on behalf of a child.
>
> Q2 - the PS is saying who the action is on behalf of -- not who is acting
>
> Q3 - clarification is intended for understanding what the agent needs --
> what else is required for authorization happens at the resource or the AS

Accordingly, Dick reported that the Person Server manages which entity the
human interacting at the Person Server acts for, including an organization or
a child; that it says who the action is on behalf of, not who is acting; and
that clarification concerns what the agent needs while other
authorization requirements belong at the resource or authorization server.

This establishes reported author intent about allocation. It does not establish normative behavior or resolve validation, evidence, scope, duration, or freshness.

Per-question disposition:

- **Question 1 — partially addressed:** the response allocates on-whose-behalf
  representation to the Person Server. It does not define validating evidence,
  binding, scope, duration, or end; the QR-scanning representative who is not
  interacting at a Person Server; or independent affected-person assent or
  refusal (B-039). The credential-profile and companion-specification options
  are unanswered. The “warden” pointer is not adopted as terminology.
- **Question 2 — partially and indirectly addressed:** “not who is acting”
  clarifies what the Person Server asserts. It does not answer whether `-11`
  anticipates a distinct participant, whether that participant's wallet/browser
  and Person Server can bind a person token to this mission interaction, or
  whether an application profile is required.
- **Question 3 — addressed in direction:** clarification is for understanding
  what the agent needs, while other authorization requirements occur at the
  resource or authorization server. The deferred-flow versus referenced-
  artifact choice remains unanswered. This is narrower than the root message's
  consideration of PS clarification when context is missing or a request should
  change. Both bear on D-019's clarification boundary; their relationship is
  open research, not a harmonized conclusion or conflict.

## Canonical architectural hypothesis

The current hypothesis is layered: a wallet supplies person-facing UI, keys, credentials, and evidence; WAS supplies protected storage and atomic storage primitives; a separate AAuth Person Server supplies the AAuth person/token role; separate SOGA governance evaluates policy; separately owned participant admission controls bounded participation; and resource/adapter enforcement controls dispatch.

Inference: the correspondence supports continuing to test this hypothesis. It does not adopt a refinement or establish compatibility, deployment, or a product.

## Future research and unresolved policy

- B-038 remains open for live validity, expiry, revocation, delegation depth, attenuation, and other authority-freshness inputs beyond the bounded Stage 2 profile.
- B-039 remains open for independently affected-person consent, assent, refusal, and precedence.
- B-040 remains open for co-presence, operator role, social signaling, and what embodied presence communicates, distinct from B-037 privacy and sensing.
- The bounded participant-session lifecycle and whether a wallet can supply any Person Server functions remain open.
- A direct primary-source recheck of the exact current `-11` person-token
  definition is required before relying on the author pointer for participant admission.
- D-019 and D-020 place approval and re-evaluation in SOGA governance. Their
  relationship to PS clarification for request adjustment and to the reported
  resource/authorization-server allocation is open research, not a conflict.
