# M02 Wallet/WAS Correspondence and Research Context

Date: 2026-09-14
Status: RESEARCH INPUT — NON-AUTHORIZING

## Evidence classification

- **Source-reported, PI-retained:** private 2026-09-10 correspondence with Dmitry Zagidulin; not an independent source-code finding.
- **Verified document-content fact:** the PI supplied the complete 2026-05-07 *Blinding Identity Taxonomy 2.0* Group Editors' Draft, edited by Paul Knowles and John Wunderlich, and Codex read that copy. Publication status and currency were not independently verified; the copy is PI-retained.
- **Source-reported protocol-author statement:** Dick Hardt's 2026-09-14 public AAuth Slack response; author intent, not normative specification text.
- **Hypothesis or inference:** every architectural conclusion below; none is a compatibility, conformance, or implementation claim.

## Dmitry Zagidulin correspondence

Dmitry reported that separating Freewallet as the person-facing wallet, WAS as wallet-controlled storage, and an AAuth Person Server made sense; WAS modularity was intended although Fastify `inject()` was not specifically designed as a downstream integration pattern; Freewallet is an in-browser client-side React application without a Node backend or supported headless Node signing path; `https://github.com/interop-alliance/did-cli-typescript` may be relevant for headless VC/VP signing; and concrete workflows and reproducible breakage reports would be useful.

These reports support investigation only. They do not establish composition and authorize no acquisition, execution, or change.

## Paul Knowles and BIT 2.0

The supplied BIT 2.0 draft extends its data-field taxonomy to neural, cognitive, affective, behavioral, intentional-inference, and device-interaction data. That verified document-content fact is relevant to B-037 and B-040 because embodied interaction may create identifying or inferential data about participants and non-participants. The draft does not decide whether sensing is permitted, establish consent or representative authority, define HCI policy, or authorize collection. The PI's conversation with Paul is relationship and direction context only unless a citable artifact supports a claim.

## Dick Hardt response and the questions it addressed

The PI's three implementation questions were, in substance:

1. How should AAuth bind authority when someone authorizes an action affecting a third party who is neither the mission principal nor a delegate—for example, a guardian acting for a child?
2. Where should a pre-permission, single-use participation credential and bounded participant-session lifecycle belong?
3. Is a denial's optional Markdown `reason` intended to carry actionable remediation, or should machine-readable restrictions, obligations, and conditions for a grantable later request use the deferred flow or another artifact?

Dick reported that the Person Server manages which entity the human interacting at the Person Server acts for, including an organization or a child; that the Person Server says on whose behalf an action occurs rather than who operates the interface; and that clarification is for understanding what the agent needs, while other authorization requirements belong at the resource or authorization server.

This establishes reported author intent about allocation. It does not establish normative behavior or resolve validation, evidence, scope, duration, or freshness.

Per-question disposition:

- **Question 1 — partially addressed:** the response allocates on-whose-behalf
  representation to the Person Server; it does not address independent
  affected-person assent or refusal (B-039).
- **Question 2 — not addressed:** no reported statement places or defines the
  single-use participation credential or bounded participant session.
- **Question 3 — partially addressed:** the response distinguishes clarification
  from additional requirements at the resource or authorization server; it does
  not answer whether the denial `reason` carries remediation or define a
  machine-readable remediation artifact.

## Canonical architectural hypothesis

The current hypothesis is layered: a wallet supplies person-facing UI, keys, credentials, and evidence; WAS supplies protected storage and atomic storage primitives; a separate AAuth Person Server supplies the AAuth person/token role; separate SOGA governance evaluates policy; separately owned participant admission controls bounded participation; and resource/adapter enforcement controls dispatch.

Inference: the correspondence supports continuing to test this hypothesis. It does not adopt a refinement or establish compatibility, deployment, or a product.

## Future research and unresolved policy

- B-038 remains open for live validity, expiry, revocation, delegation depth, attenuation, and other authority-freshness inputs beyond the bounded Stage 2 profile.
- B-039 remains open for independently affected-person consent, assent, refusal, and precedence.
- B-040 remains open for co-presence, operator role, social signaling, and what embodied presence communicates, distinct from B-037 privacy and sensing.
- The bounded participant-session lifecycle and whether a wallet can supply any Person Server functions remain open.
- D-019 and D-020 place approval and re-evaluation in SOGA governance. Whether that path is consistent with the reported allocation of additional requirements to a resource or authorization server is an open research question, not a conflict established here.
