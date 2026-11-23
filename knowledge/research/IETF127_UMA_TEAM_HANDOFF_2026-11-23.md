# IETF 127 and UMA: build-team advisory handoff to Claude (chat)

Date: November 23, 2026. Prepared by CG after independent reviews by Claude Code (389) and AGy (390), followed by an explicitly shared discussion (391/392).

**Advisory only. Deb retains decision authority. No build, architecture, standards selection, signing, test execution or hardware work is authorized by this document.** This is feedback for Claude (chat), not an approved WG-UMA reply. The two input documents remain in Downloads and are not committed here.

**Repository basis inspected:** `51d19d07915937160747b9177d228de1f1429e08`. The code findings below describe that commit. This handoff is a separate documentation-branch addition; it does not change the active robot checkout, its HEAD, accepted physical request, or canonical records.

The full original reviewer responses and their later discussion are reproduced below, unchanged. Their initial errors remain visible as history; the synthesis identifies subsequent corrections. Do not read an original statement superseded in discussion as the team's current conclusion. CG's independent review and later source-check notes are also included, with provenance hashes.

## Main recommendation to Claude

Keep the requirement and ecosystem-neutral direction. Revise the universal standards-gap claim. Existing work already supplies transaction approval, waiting, current token checks and revocation. Distinguish:

1. Authorizing or refusing a new request, including after revocation.
2. Establishing which permissions must still apply when a consequential action occurs, including separate affected-party permission where needed.
3. Cancelling or pausing execution that another system has already accepted.

The third is a real enforcement question, but we have not established that every standard or protocol composition lacks it. Bounded Work expressly leaves accepted-execution checkpoints/cancellation to realizations; that is an explicit boundary of that draft, not proof of universal absence. Its stated acceptance window also matters: revocation is not necessarily instantaneous. [Bounded Work -00 §4.4](https://www.ietf.org/archive/id/draft-liu-mcguinness-oauth-bounded-work-00.html#section-4.4)

## Answers to the three UMA questions

**1. Agreement with points 1–3.** Point 1 is a useful responsibility model, with qualifications: Bob's agent acts under Bob's authority; where an action also requires Alice's permission as an affected party, that is a separate condition. Alice need not have delegated to Bob or be a digital resource owner. It does not follow that all actions need two human approvals. Establishing identity and standing remains open; our demo does not verify a real parent.

Point 2: the need to extend UMA has not been demonstrated. Challenge -01 §1.2 expressly covers approval by a different resource owner, selected under authorization-server policy. Discovering/routing to an unassociated home server across trust domains is a distinct question, not a refutation of §1.2. GNAP provides relevant grant lifecycle and resource-server connection mechanisms; compare their functions rather than claim replacement. [Challenge -01 §1.2](https://www.ietf.org/archive/id/draft-rosomakho-oauth-txn-challenge-01.html#section-1.2), [GNAP core](https://www.rfc-editor.org/rfc/rfc9635.html), [GNAP RS connections](https://www.rfc-editor.org/rfc/rfc9767.html)

Point 3: retain current applicability and withdrawal as requirements. Remove “none of them define.” Checking that permission remains valid need not mean asking Alice again for each action. An answer given earlier is evidence, not automatically current authority.

**2. Design disclosure.** The proposed allow/restrict/hold/deny wording mirrors our internal taxonomy despite the brief's no-states rule. Use functional requirements. Keep the AI-assisted-team disclosure and observer posture. The draft omits the explicit IPR non-acceptance statement requested by its own brief; this is an editorial discrepancy, not legal advice about the effect of participation.

**3. Corrections and source limits.**

| Item | Current conclusion after discussion |
|---|---|
| All standards decide before access or audit afterward | Too broad. GNAP has continuing grant modification and revocation; AAuth -11 has token revocation and cascade; OAuth has introspection/revocation. These are not themselves proof of stopping accepted physical execution. |
| Challenge token is always single-use | Incorrect as universal statement. Single-use is recommended for non-idempotent/high-impact operations; enforcement is conditional, with replay state required when single use is required. |
| Actor chain removes “who sent this?” | Too strong. Issuer trust, token validation, and presenter/sender-constraint checks remain. Immediate issuer-scoped actor and historical inner actors have different roles. |
| Bounded Work is requirements only | Direction-setting draft with no wire formats; do not describe its proposed semantics as deployed or final. It explicitly leaves joint approval by several independent parties outside its goals (§5.2). That exclusion is specific to this draft, not a universal standards gap. |
| “GNAP absorbed UMA” | Preserve Deb's firsthand report about Justin's reuse remark. RFC text establishes functions, not historical genealogy. See attribution note below. |
| December IESG dates/adoption discussion | Targets and discussions, not completed outcomes. Remaining mailing-list outcomes require verification. |
| U4A AAuth “binding” | Claude Code reports the exact spec README at commit `77649287dc883b75ef563c59f96de8613ecf10d0` classifies the AAuth document as Credential and MCP as Binding; AGy accepts that correction. CG separately retrieved the root README, which says it binds AAuth. Thus use the precise document category without implying absence of AAuth integration. CG could not independently retrieve the pinned spec README via its browser. Do not label U4A a Kantara WG product without a source establishing that status. |
| Already in G26 / supports two paths | Separate standing direction reported by Deb, recorded adoption, implemented profile, and demonstrated execution. G26 is a permission-boundary result. OAuth adapter is a mock. Pinned AAuth profile is not proof of full -11 conformance. |

Sources: [AAuth -11 §11.12](https://www.ietf.org/archive/id/draft-hardt-oauth-aauth-protocol-11.html#section-11.12), [Challenge -01 §6.2](https://www.ietf.org/archive/id/draft-rosomakho-oauth-txn-challenge-01.html#section-6.2), [Actor profile §§8.1–8.2](https://www.ietf.org/archive/id/draft-mcguinness-oauth-actor-profile-01.html#section-8.1), [RFC 8693 §4.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1), [Bounded Work -00 §5.2](https://www.ietf.org/archive/id/draft-liu-mcguinness-oauth-bounded-work-00.html#section-5.2), [U4A root README](https://raw.githubusercontent.com/nickgamb/uma4agents/main/README.md).

## Justin / UMA attribution: retain the firsthand context

Deb reported: “cg Justin said he stole the uma code in the ietf meeting”. She subsequently said she saw this in an early response from Claude. Preserve that evidence; absence of the phrase UMA in the GNAP RFCs does not disprove it.

The official summary minutes record Justin discussing useful UMA pieces during the Rosenberg session. They do not contain the reported reuse phrase or identify its exact referent. Use Deb's report as attributed meeting context; exact recording/transcript and scope remain open. There is no need to litigate genealogy in the external reply: describe shared functions and preserve the history internally. [Official OAuth minutes](https://datatracker.ietf.org/doc/minutes-127-oauth/00/)

The minutes also record an attenuation/incomputability concern under “JR”. Claude Code flags that initials-only attribution as ambiguous; AGy attributes it to Justin. The substance is supported, but CG does not treat the minutes alone as resolving the speaker or exact spoken wording. Nor does that observation prove a specific runtime mechanism is necessary. Exact informal chat claims not reproduced in the minutes remain attributed reports rather than independently verified quotations.

## Proposed next work: impact on current code, not implementation authorization

| Recap §3 item | Actual current code and prospective boundary |
|---|---|
| 1. OAuth Transaction Authorization Challenge adapter / approving PDP | `input_adapters/oauth_adapter.py` is a passive mocked transformer, not a live OAuth/GNAP endpoint or verifier. `aauth_permission/service.py` is a mock G26 pending/re-evaluation analogue, not OAuth Deferred Token Response. A real path needs separately specified authenticated challenge/token intake, issuer/audience/key/transaction binding, deferred results and replay handling, then evidence projection into `verify/runtime_envelope_model.py` and the governance evaluator. `engines/aauth_execution_runtime_bridge.py` illustrates the existing AAuth bridge; it is not automatically a generic OAuth bridge. Mission owner, approval, provenance and binding are unresolved: stub/default mission values are not approved authority. D-011 preserves SOGA as policy within a deployment role, not an independent universal protocol party; define which AS/PS/resource role invokes it before proposing code. |
| 2. Actor profile as evidence | Add or extend a separately verified protocol boundary before projecting current actor/provenance into `AuthorityEvidence.references` and `raw_evidence`. Existing `m02_aauth_fcf656d/tokens.py` is a bounded AAuth profile, not an actor-profile validator. Preserve the immediate issuer-scoped actor for applicable authorization; nested history stays audit-only. **Do not derive control-bearing `delegation_hops` from historical `act` depth:** `m02_aauth_fcf656d/soga_supervision.py` uses that field to deny. This was a prospective mapping error corrected in discussion, not an existing implemented actor-chain bug. |
| 3. Transaction Tokens / Txn-Token-JAG evidence | No live implementation identified. A new verified intake/exchange contract would precede OAuth evidence normalization: issuer/audience/trust-domain validation, transaction context, data minimization and no scope expansion. `input_adapters/oauth_adapter.py` and `verify/runtime_envelope_model.py` are touchpoints. Tokens are evidence, not mission authority or a decision to execute. Huawei Mode B is watch/deferred scope; no shortcut adopted. |
| 4. Watch U4A, UCAN, Rosenberg AAuth, client instances | Research only; zero implementation changes implied. `input_adapters/ucan_adapter.py` is a non-cryptographic transformer. A future instance-identity integration would need a separate grant/holder/invocation-binding contract; existing IDs are not proof of attested running instances. |

Future robot integration would also have to reach the separately governed authorization-consumption boundary in `robot_gateway/switching.py`, retain lifecycle/neutral/stop controls, and supply the live authority/event/transport implementations that `robot_gateway/OPERATOR_RUNTIME.md` explicitly excludes from its synthetic runtime. A standards adapter alone does not finish the physical gateway.

Source pins: `m02_aauth_fcf656d/profile.py` binds upstream AAuth commit `fcf656de1926535f5bd6fc0538147ead6646e727`; relation to the full -11 publication remains unestablished. Public Flow A has simulated encounter inputs and unverified affected-party input. Its presentation STOPPED outcome is not robot stopping evidence.

## What changed during the debate

- Claude Code withdrew its proposed replacement novelty claim that no spec defines one decision point, and corrected “acting on Alice's behalf” to Bob's authority plus separate affected-party permission where applicable.
- AGy corrected its use of cross-domain routing as a rebuttal of challenge §1.2, its universal single-use wording, and its attribution of historical UMA absorption to RFC 9767 itself.
- AGy withdrew the suggested mapping of nested actor history into the current control-bearing hop counter. Claude Code and CG agree with the correction.
- Both retained the need to avoid internal outcome names and to distinguish draft behavior, implementation and demonstrated effects.
- CG added the affected-party/standing distinction and D-011 emphasis from AGy; its own first response had not emphasized them enough. CG preserves its earlier review rather than retroactively rewriting it.
- All three support asking how existing compositions satisfy the requirement instead of declaring an exclusive gap. The exact historical lineage, initials-only speaker attribution, unpublished email content and remaining meeting chat are not flattened into consensus facts.

## Suggested requirement paragraph for Claude to adapt

When Bob's agent acts under Bob's authority and an action also requires permission from an affected party who has not delegated to Bob, the accountable enforcement point should be able to establish that the applicable permissions still hold when the action occurs. It should define what happens when required permission is missing, stale or withdrawn, and retain attributable evidence of the checks. Refusing a new operation and stopping work already accepted are distinct problems; the applicable checkpoints, withdrawal response and timing guarantees need to be made explicit.

This states a requirement to evaluate against existing protocols and deployments, not a claim that all existing work lacks it. Whether UMA needs extending remains open. Identification and standing, cross-domain approval discovery/routing, mission provenance and accepted-execution cancellation are research questions, not newly authorized build items.

The brief also calls for a plain statement of observer/non-member posture and non-acceptance of Kantara IPR terms, plus disclosure of AI-assisted preparation. Keep these editorial facts distinct from any legal interpretation of membership or IPR obligations.

## Original responses and follow-up record

The appendices preserve reviewer wording, including assertions subsequently corrected above. They are team-review evidence, not an approved public mailing-list response. Each payload is inserted byte-for-byte between its markers; this document adds only headings/markers around it. AGy's initial report labels its pre-queue original thoughts as Part I and later additions as Part II. Claude Code's initial report embeds its original with explicit begin/end markers; the separate pre-queue original is also retained in the local handoff folder with a verified hash. CG's independent review is a saved account of its initial chat findings, not a verbatim export of the chat message.



### Appendix A — Claude Code initial report, including pre-queue original

Original file: `CLAUDE_CODE_INITIAL_QUEUE_389_VERBATIM.txt`; SHA-256: `849ea12fe00f46d2515a1c81be02c2b33a5a2dce1555366e220d39689e4325cf`.

<!-- BEGIN VERBATIM CLAUDE_CODE_INITIAL_QUEUE_389_VERBATIM.txt -->

389 Gate 1 (Claude Code) response - advisory standards team review of ietf127-recap.md and uma-thread-brief.md

ADVISORY ONLY. Not a build gate. No repository write, commit, email or public post.
Repo HEAD loaded: 51d19d07915937160747b9177d228de1f1429e08 (status: only the excluded proposal untracked). The excluded proposal was not read.
Inputs re-hashed: ietf127-recap.md 68989d77943166b9e536cdeabcdefb7a1da232bc914132609f0673db791af0a6; uma-thread-brief.md f2c3c3586aba2694bd18b76cba16051e2de29281a6103e41b0e38e79651a4559 (both match).
No peer queues, findings or CG conclusions were read.

PART A — ORIGINAL RESPONSE (written for Deb on 2026-11-23 before this request, saved at
/Users/debb/dev/soga-gate1-notes/IETF127_RECAP_AND_UMA_BRIEF_GATE1_FACT_CHECK_2026-11-23.md,
sha256 3c2a8d6da32abb00186eeede8970bf30ece0a85c0fc8ee53e2252251b8a785d0). Reproduced verbatim:

----- BEGIN ORIGINAL -----
# Gate 1 (Claude Code) fact-check: ietf127-recap.md and uma-thread-brief.md

Date: 2026-11-23. Advisory only; Deb holds decision authority.
Repo commit loaded: 51d19d07915937160747b9177d228de1f1429e08 (status: only the excluded proposal untracked).
Inputs: ~/Downloads/ietf127-recap.md (sha256 68989d77…af0a6), ~/Downloads/uma-thread-brief.md (sha256 f2c3c358…a4559). Not committed; no code changes.

## ietf127-recap.md

| Claim | Result | Source |
|---|---|---|
| AAuth -11, Hardt | Verified: draft-hardt-oauth-aauth-protocol-11 (25 Sep 2026), Dick Hardt; the old draft-hardt-aauth-protocol name was replaced | Datatracker |
| Signature-key draft at HTTP WG for adoption decision, result not confirmed | Verified: "HTTP Signature-Key Header – call for adoption discussion", Friday 20 Nov | httpbis agenda |
| Txn Challenge -01; authors Rosomakho, Campbell, McGuinness, Kasselman | Verified (-01, 2 Nov 2026) | Datatracker |
| Challenge presented Friday | Verified (Rosomakho) | oauth agenda |
| Resource signs the challenge | Verified: "MUST be signed by the protected resource" | draft text |
| Token carries the transaction ID | Verified (txn claim) | draft text |
| Single use | WRONG as stated: only "if the protected resource requires single use for the challenged operation" | draft text |
| Uses Deferred Token Response | Verified (Section 5; draft-ietf-oauth-deferred-token-response is a WG draft) | draft, agenda |
| "Policy decision point" can be the approving party | Verified (Section 1) | draft text |
| HITL/HOTL/HOOTL defined in the challenge draft | Verified (Section 2) | draft text |
| Actor profile (McGuinness) | Verified: draft-mcguinness-oauth-actor-profile-01; nested act chains required | Datatracker |
| "OAuth taking it up for adoption" | Can't verify | transcripts |
| Client Instance IDs + Attester Endorsement (McGuinness) | Verified: draft-mcguinness-oauth-client-instance-id-01, draft-mcguinness-oauth-client-attesters-01; presented Friday | Datatracker, agenda |
| "Containment" = revoking one running copy | Partly verified: word appears once (Section 9.2), about suspending one instance's identity; Section 6.3 covers revoking one grant's tokens. "Revoking one running copy" is the recap's gloss | draft text |
| Bounded Work (Liu, McGuinness) | Verified: draft-liu-mcguinness-oauth-bounded-work-00; Dapeng Liu (Alibaba), Karl McGuinness | Datatracker |
| "Governing authorization" with lifecycle state | Verified (active/ended) | draft text |
| Withdrawal denies further access | Verified, with caveat: a non-introspected token can stay valid within an "acceptance window" | draft text |
| Requirements only, no mechanism | Verified: "specifies no wire formats" | draft text |
| Txn-Token chaining profile (Fletcher, Kasselman, O'Dell), presented Thursday | Verified: -01, 26 Oct 2026; uses "Txn-Token-JAG" | Datatracker, agenda |
| Cross-domain Txn Tokens (Liu, Ni, Huawei), "Mode B" shortcut | Verified: draft-liu-oauth-cross-domain-txn-token-00; Chunchi Peter Liu, Yuan Ni (Huawei); Section 3.2 Mode B | Datatracker |
| Rosenberg aauth -02 as an OAuth extension | Verified: OAuth 2.1 extension, presented Wednesday; co-author Pat White omitted | Datatracker, agenda |
| U4A nine drafts | Verified | GitHub README |
| U4A "includes an AAuth binding" | WRONG term: draft-gamb-uma4agents-aauth-00 is classed "Credential"; the only "Binding" is MCP | GitHub README |
| U4A "(Gamb, Kantara)" | Can't verify: Kantara not in source; no authors named beyond the gamb prefix | GitHub |
| U4A not submitted to IETF | Can't verify: README silent; no Datatracker hit found | GitHub, search |
| Dec 2026: Transaction Tokens and OAuth 2.1 to IESG | Verified as charter milestones (2026-12-31), targets not certainties | OAuth charter |
| AAuth in G26; G19 ecosystem neutrality | Verified | repo knowledge/research/G26_*; AI_COLLABORATION_GUARDRAILS.md:10 |
| §2 "decided by Deb this week" | Can't verify: not in frozen repo records | Deb |
| Quotes/remarks attributed to Fletcher, Karl, Kasselman, Richer, Campbell, Rosenberg; "Harness as Client"; ID-JAG/WAG chat; interim plans | Can't verify | transcripts/chat |

## uma-thread-brief.md

| Claim | Result | Source |
|---|---|---|
| Challenge draft Section 1.2 covers approval by a different resource owner | Verified: "Authorization by a Different Resource Owner"; the approver is chosen "according to authorization server policy" | draft text |
| GNAP is RFC 9635 | Verified (Richer, Ed., Imbault, Oct 2024) | RFC Editor |
| GNAP "absorbed much of UMA's design" | Can't verify from cited source: RFC 9635 never mentions UMA (full text searched) | RFC 9635 |
| Harvey co-authored NIST IR 8536 (supply chain traceability) | Verified: Harvey Reed is a listed author (final Sept 2026) | NIST |
| Harvey is at MITRE | Can't verify: NIST page shows no affiliations | NIST |
| Thread contents, members, George Fletcher's U4A role | Can't verify | Deb's email paste |
| Draft reply: AAuth work "covers approval by a different resource owner" | Not sourced | — |

## Answers to the three questions

1. Points 1–3.
   - Point 1: agree.
   - Point 2: partly. The Section 1.2 citation holds, but its approver is chosen by authorization-server policy, not Alice's private policy through her own agent, so it does not replace UMA's model. Drop or separately source "GNAP absorbed UMA".
   - Point 3: disagree as worded. The sources show per-operation approval at request time (challenge draft), a waiting state (Deferred Token Response), denial after work ends (Bounded Work), and Alan Karp's resource-side revocation check at request time. The recap's main finding overstates the same way. Defensible version: the pieces exist separately, but no spec defines one decision point at the moment of action with a defined hold outcome that rechecks an earlier answer against current state.
2. Design leakage: yes. "Allow, restrict or hold for Alice, or deny" is the gate's own outcome set, which breaks the brief's own no-states rule; prefer "the action must be able to be stopped or paused pending Alice, with her answer rechecked when it happens". The reply also omits the required IPR statement (it says only "not currently a WG-UMA participant"). Minor: "team response" vs "my own view".
3. Errors: single use overstated; U4A AAuth draft is "Credential", not "Binding"; Kantara not in the cited source; GNAP/UMA claim unsupported by RFC 9635; AAuth claim in the reply unsourced; "containment" paraphrased more strongly than the draft; the "no spec covers this" gap conflicts with Bounded Work, the challenge draft and Alan Karp's message. Transcript, chat and email content remains unverified.

## Sources

- https://datatracker.ietf.org/doc/draft-rosomakho-oauth-txn-challenge/
- https://datatracker.ietf.org/doc/draft-fletcher-oauth-txn-token-chaining-profile/
- https://datatracker.ietf.org/meeting/127/materials/agenda-127-oauth
- https://datatracker.ietf.org/meeting/127/materials/agenda-127-httpbis
- https://datatracker.ietf.org/doc/draft-liu-mcguinness-oauth-bounded-work/
- https://datatracker.ietf.org/doc/draft-mcguinness-oauth-client-instance-id/
- https://datatracker.ietf.org/doc/draft-mcguinness-oauth-client-attesters/
- https://datatracker.ietf.org/doc/draft-mcguinness-oauth-actor-profile/
- https://datatracker.ietf.org/doc/draft-liu-oauth-cross-domain-txn-token/
- https://datatracker.ietf.org/doc/draft-rosenberg-oauth-aauth/
- https://datatracker.ietf.org/doc/draft-hardt-oauth-aauth-protocol
- https://datatracker.ietf.org/wg/oauth/about/
- https://github.com/nickgamb/uma4agents/tree/main/spec
- https://www.rfc-editor.org/rfc/rfc9635
- https://www.nist.gov/publications/supply-chain-traceability-principles-manufacturing-meta-framework
----- END ORIGINAL -----

PART B — LATER ADDITIONS (written for this request; not part of the original)

B1. The four recap Section 3 proposed-work items, mapped to current code at 51d19d0. This is a static grep and read only; nothing was executed.

1) OAuth Transaction Authorization Challenge adapter with the gate as approving PDP.
   - Current code: no txn-challenge implementation. A grep for txn_challenge or "transaction authorization challenge" across *.py found nothing.
   - The existing input_adapters/oauth_adapter.py (oauth_gnap_to_runtime_envelope_v0_1) is documented in its own docstring as a "passive data transformer only", using "static mocked payloads only", with "no live OAuth server", "no live GNAP server", "no token library" and "no governance decision logic". It reads authorization_details and iss, and verifies no JWS or challenge signatures.
   - The closest existing behaviour is aauth_permission/service.py: "Mock AAuth Person Server permission surface for G26", with a HOLDING mode deferred under configured expiry. That is a MOCK holding path, not an OAuth Deferred Token Response.
   - Prospective impact: new work entirely. It would need challenge-signature verification (draft Section 4.4 and resource JWKS), txn binding, and the Deferred Token Response client behaviour. Open question from the recap: where the mission comes from on the OAuth path.
2) Karl's actor profile (`act` chain) as evidence.
   - Current code: nothing reads an `act` claim (no grep hit).
   - Source semantics: RFC 8693 Section 4.1 says that for access control the consumer "MUST only consider the token's top-level claims and the party identified as the current actor"; prior actors "are informational only and are not to be considered in access control decisions". The actor profile (draft-mcguinness-oauth-actor-profile-01) requires nested act objects per RFC 8693 Section 4.1.
   - So the recap's framing (identity/path evidence, not "may this happen now") is consistent with the source. Nested actors are a history trail, not authorization, and their trust depends on the issuing authorization server.
3) Transaction Tokens and Txn-Token-JAG as evidence.
   - Current code: none (no grep hit for txn-token or transaction-token).
   - Prospective: evidence intake only. Mode B (draft-liu-oauth-cross-domain-txn-token-00 Section 3.2) requires pre-established trust between the Domain I authorization server and the Domain II token service.
4) Watch items: U4A, UCAN, Rosenberg aauth, client instance IDs.
   - UCAN: input_adapters/ucan_adapter.py exists as a passive transformer whose docstring says "This adapter does not verify UCAN signatures", with tools/ucan_runtime_envelope_v0_1_proof.py as a synthetic proof.
   - U4A and Rosenberg aauth: no code.
   - Client instance IDs: no code.
   - AAuth (entry path 1): m02_aauth_fcf656d pins AAUTH_COMMIT fcf656de1926535f5bd6fc0538147ead6646e727, with Ed25519 JOSE and HTTP-signature modules and localhost/fixture metadata. That is a pinned-commit bounded profile, not live integration with an external AAuth deployment.
   - Note: the recap cites "AAuth -11" (draft-hardt-oauth-aauth-protocol-11, 25 Sep 2026). I did NOT establish how the repo's pinned GitHub commit relates to the -11 text, so treat "already in G26" as meaning the pinned profile, not -11.

B2. Revocation versus stopping work already executing.
- draft-liu-mcguinness-oauth-bounded-work-00 says explicitly: "Ending a governing authorization does not by itself undo completed effects or cancel execution that another system has already accepted. A realization that governs such execution identifies the additional checkpoints and cancellation behavior it provides."
- It also bounds revocation latency by an "acceptance window" (a token is reported inactive only via introspection; otherwise its lifetime applies).
- This is the strongest primary-source support for a narrower gap statement. Withdrawal and revocation deny FURTHER operations at participating enforcement points. Stopping or holding an operation already accepted and executing is left to the realization.
- This supersedes my Part A point-3 suggestion as the most defensible framing.

B3. Transaction validation and single use (challenge draft -01).
- The challenge is a signed JWT with jti and txn (same txn in the challenge and the token).
- The resource rejects tokens not matching the challenged operation.
- Single use applies only "if the protected resource requires single use for the challenged operation", and replay detection requires resource-side state.
- The recap's "single use" is therefore conditional, not inherent.

B4. GNAP/UMA. RFC 9635 does not mention UMA in its text (full-text search). It states GNAP "is not an extension of OAuth 2.0". Any historical lineage claim needs a different source. UNVERIFIED here.

B5. IPR boundary wording. The brief's rule says to state that Deb "has not accepted Kantara IPR terms". The draft reply says only "I'm not currently a WG-UMA participant; sharing this as an observer." The rule and the draft disagree.

B6. Proposed requirement-only wording for point 3, to replace "allow, restrict or hold for Alice, or deny":
"One requirement we'd add: when an agent is about to act, or is already acting, on Alice's behalf, the party accountable for the resource must be able to obtain a current decision that reflects Alice's present wishes, including stopping or pausing the action pending her answer, rather than relying only on approval given earlier or on revocation that blocks only later requests. Existing work (for example OAuth Bounded Work's note that ending an authorization does not by itself cancel accepted execution) leaves this to implementations."
This states the what, not our states, flows or code.

B7. Neutrality and write/check split. These comments neither endorse nor select a spec (G19 ecosystem neutrality, AI_COLLABORATION_GUARDRAILS.md line 10). The mapping above is check-side only. Nothing proposes builder work.

B8. Disagreements and open questions for consolidation:
- The recap Section 1 "no spec can hold, pause, or revoke authority while a task is running" is too broad. The sources show revocation of further access (Bounded Work), per-operation approval (challenge), and waiting (Deferred Token Response). Narrow it as in B2/B6.
- Whether "AAuth -11" or the pinned fcf656d commit is the reference for entry path 1.
- Whether the reply should claim AAuth covers different-owner approval. That is unsourced in the brief.
- All transcript, chat and email content stays UNVERIFIED: remarks attributed to Fletcher, Karl, Kasselman, Richer, Campbell and Rosenberg; "Harness as Client"; interim plans; adoption statuses; thread contents; affiliations (Harvey at MITRE; Fletcher's U4A role).

Additional primary sources used in Part B:
- https://www.rfc-editor.org/rfc/rfc8693 (Section 4.1)
- https://www.ietf.org/archive/id/draft-liu-mcguinness-oauth-bounded-work-00.txt
- https://www.ietf.org/archive/id/draft-rosomakho-oauth-txn-challenge-01.txt
- https://www.rfc-editor.org/rfc/rfc9635.txt

Repo files cited: input_adapters/oauth_adapter.py, input_adapters/ucan_adapter.py, tools/ucan_runtime_envelope_v0_1_proof.py, aauth_permission/service.py, m02_aauth_fcf656d/profile.py, AI_COLLABORATION_GUARDRAILS.md, knowledge/research/G26_*.


<!-- END VERBATIM CLAUDE_CODE_INITIAL_QUEUE_389_VERBATIM.txt -->


### Appendix B — AGy initial report, including original thoughts

Original file: `AGY_INITIAL_QUEUE_390_VERBATIM.txt`; SHA-256: `f6561df27978d1d59c2a2864e53ef4471afbddb10c74b97ca573aa60033bedc3`.

<!-- BEGIN VERBATIM AGY_INITIAL_QUEUE_390_VERBATIM.txt -->

# Independent Gate 2 Advisory Standards Team Review — Request 390 (`ietf127-recap.md` & `uma-thread-brief.md`)

- **Reviewer:** AGy (Gate 2 Independent Reviewer)
- **Timestamp:** `2026-11-23T11:22:00-05:00` (`2026-11-23T08:22:00-08:00`)
- **Loaded Repository Commit (`HEAD` in `/Users/debb/dev/soga-clean`):** `51d19d07915937160747b9177d228de1f1429e08`
- **Source File SHA-256 Digests Verified (`0` mismatches):**
  - `/Users/debb/Downloads/ietf127-recap.md` (70 lines): `68989d77943166b9e536cdeabcdefb7a1da232bc914132609f0673db791af0a6`
  - `/Users/debb/Downloads/uma-thread-brief.md` (55 lines): `f2c3c3586aba2694bd18b76cba16051e2de29281a6103e41b0e38e79651a4559`
- **Scope & Constraints Compliance:** Advisory standards review only. Static text, SHA-256, read-only git, and primary standards-source lookup only. No code execution, import, compilation, test run, repo modification, commit, device/hardware access, public posting, or peer-queue reading was performed.

---

## PART I — Original Independent Response (Preserved Verbatim as Completed Prior to Queue 390)

### Loaded Repository Commit SHA

- **Loaded Commit (`HEAD`):** `51d19d07915937160747b9177d228de1f1429e08` in `/Users/debb/dev/soga-clean` (verified read-only via `git rev-parse HEAD`; no files modified or committed).

### 1. What Is Missing or Weak in the Proposed Position (Points 1–3)

#### Point 1: *"UMA's model (Bob asks, Alice's private policy decides, the resource server is accountable) is the right way to describe the problem."* (`/Users/debb/Downloads/uma-thread-brief.md`, line 21)

1. **Drops the dual-authority requirement (Bob's delegated mission authority + Alice's non-delegating other-party decision):**
   - UMA models a single Resource Owner (Alice) governing access to her resource by a Requesting Party (Bob). In our research problem, an action requires **two independent authorities at once**—the operator's (Bob's) bounded mission authority over his own agent *and* the affected third party's (Alice's/the parent's) decision, where Alice never delegated anything to Bob—and **either one can stop the action**.
   - *Source:* `/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 80–86, 123–126, and 152–154 (*"Both are required. My authority and the parent's decision. Either one can stop the robot... when an action needs a decision from a third party who never delegated anything"*); application to Point 1 is my own reasoning.
2. **Omits the pre-registration and standing gap in UMA:**
   - UMA assumes Alice has already registered her resource and authorization server in advance, and still does not establish who Alice is or her standing toward the affected person in an ad-hoc encounter.
   - *Source:* `/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 147–154 and 170–174 (*"It's a close fit in shape... But it assumes the parent registered somewhere in advance, and it still doesn't tell you who the parent is"*). This also directly bears on Eve Maler's question in the thread (`/Users/debb/Downloads/uma-thread-brief.md` line 16) about whether Alice's agent is always tied to an authorization server (my own reasoning).

#### Point 2: *"We are not convinced UMA itself needs extending. GNAP (RFC 9635) absorbed much of UMA's design. OAuth's transaction challenge draft (Section 1.2) now covers approval by a different resource owner."* (`/Users/debb/Downloads/uma-thread-brief.md`, line 22)

1. **Overstates cross-domain coverage of `draft-rosomakho-oauth-txn-challenge-01`—especially on a list that includes George Fletcher:**
   - `/Users/debb/Downloads/ietf127-recap.md` (line 13) states that when a challenge crosses more than one trust domain, there is **no defined way back to the home authorization server** (raised by George Fletcher in OAuth chat, confirmed by Karl McGuinness as not covered by the Transaction Authorization Challenge draft, and called *"a separate problem"* by Pieter Kasselman).
   - Telling the UMA thread (where George Fletcher is present, `/Users/debb/Downloads/uma-thread-brief.md` line 8) that the transaction challenge draft *"now covers approval by a different resource owner"* without noting that it does **not** route challenges across domains to Alice's own authorization server/agent invites an immediate correction.
   - *Source:* `/Users/debb/Downloads/ietf127-recap.md` line 13 and `/Users/debb/Downloads/uma-thread-brief.md` line 8; contrasting them is my own reasoning.

#### Point 3: *"The gap none of them define: at the moment Bob's agent acts, a decision to allow, restrict or hold for Alice, or deny, with Alice's answer rechecked at that moment."* (`/Users/debb/Downloads/uma-thread-brief.md`, line 23)

1. **Fails to engage Alan Karp's statement in the same thread and blurs "recheck at request arrival" with "hold/withdraw without revoking Bob's authority":**
   - In the thread summary (`/Users/debb/Downloads/uma-thread-brief.md` line 15), Alan Karp already proposed: *"Revocation is checked when the resource request arrives, by a verifier on the resource side."*
   - If Deb replies that none of them define rechecking Alice's answer when Bob's agent acts, Alan can point out he just described a resource-side revocation check on request arrival.
   - What is actually missing beyond a binary resource-side revocation check is:
     - **Holding/waiting before action execution** when Alice has not yet answered, rather than only checking revocation of a prior grant (`/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 114–120; `/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` lines 62–64); and
     - **Independent withdrawal / stop after `Allow` without revoking Bob's token or mission**: when Alice withdraws, Bob's delegated token/mission remains valid, yet the resource refuses or stops the directed action (`/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 121–126, 167–169; `/Users/debb/dev/permission-to-speak-work/permission-to-speak/FLOW_A_RUNTIME_MAPPING_2026-10-31.md` lines 19–23).
   - *Source:* `/Users/debb/Downloads/uma-thread-brief.md` line 15, `/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 114–126, 167–169, `/Users/debb/dev/permission-to-speak-work/permission-to-speak/FLOW_A_RUNTIME_MAPPING_2026-10-31.md` lines 19–23, and `/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` lines 62–64; the critique of how Point 3 interacts with Alan Karp's post is my own reasoning.
2. **Misses Harvey's traceability/evidence point:**
   - Harvey asked about traceability as evidence for privacy and trust (`/Users/debb/Downloads/uma-thread-brief.md` line 17). In our repo, the action-time decision must also record attributable provenance—including when Alice's answer is unverified or withdrawn—independently of the wire grant/deny response.
   - *Source:* `/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` lines 24–35 and `/Users/debb/dev/soga-clean/m02_aauth_fcf656d/other_party_approval.py` lines 70–92 (`OtherPartyDecisionReceipt`); connecting this to Harvey's comment is my own reasoning.

### 2. What Is Missing or Weak in the Draft Reply (`/Users/debb/Downloads/uma-thread-brief.md`, lines 33–43)

1. **Violates its own Boundary Rule 2 by omitting the Kantara IPR disclaimer:**
   - Boundary Rule 2 (`/Users/debb/Downloads/uma-thread-brief.md` line 28) requires: *"Deb is not a member and has not accepted Kantara IPR terms. Say so in the reply."*
   - Line 41 of the draft reply says only: `"(I'm not currently a WG-UMA participant; sharing this as an observer.)"`—it never mentions Kantara IPR terms.
   - *Source:* `/Users/debb/Downloads/uma-thread-brief.md` line 28 vs. line 41.
2. **Inaccurately claims AAuth itself *"now covers approval by a different resource owner"*:**
   - Line 37 of the draft reply adds `"and AAuth"` to Point 2: *"the newer OAuth and AAuth work, including the transaction challenge draft discussed at IETF last week, now covers approval by a different resource owner."*
   - In our verified repo and IIW presentation, AAuth carries the *operator's* authority and provides a deferred-approval mechanism, while third-party/other-party approval had to be built as an **additive resource-side policy** outside AAuth's native protocol claims.
   - *Source:* `/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 143–154 (*"AAuth carries my authority beautifully... But the parent's decision, the part that matters most here, comes from the application. Nothing in the protocol says who the parent is..."*) and `/Users/debb/dev/soga-clean/m02_aauth_fcf656d/other_party_approval.py` line 1 (*"Additive resource policy for the bounded other-party approval experiment"*).
3. **Leaks SOGA's internal decision taxonomy (`"allow, restrict or hold for Alice, or deny"`):**
   - See Question 2 below.

### 3. Answers to the Three Questions at the End of the UMA Brief (`/Users/debb/Downloads/uma-thread-brief.md`, lines 45–49)

#### Q1: Do you agree or disagree with points 1 to 3? Give reasons.

- **Point 1 — Partially agree, needs qualification:**
  - *Reason:* I agree that separating the requesting party (Bob), the affected party's private policy (Alice), and an accountable resource server is a useful description of the other-party side of the problem. I disagree that it is a *complete* description, because (a) our problem requires **both** Bob's delegated mission authority and Alice's independent decision (where Alice never delegated anything to Bob, and either party can stop the robot; `/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 80–86, 123–126), and (b) UMA assumes Alice pre-registered with an authorization server and does not solve how Alice's identity/standing is established on the spot (`/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 147–154, 170–174).
- **Point 2 — Agree on not extending UMA; disagree with the unqualified claim that OAuth's transaction challenge draft "now covers approval by a different resource owner":**
  - *Reason:* While `draft-rosomakho-oauth-txn-challenge-01` frames approval by a different resource owner inside a resource's AS domain (`/Users/debb/Downloads/uma-thread-brief.md` line 22), `/Users/debb/Downloads/ietf127-recap.md` line 13 explicitly documents that when a challenge crosses trust domains, it has **no defined path back to a home authorization server**. Overstating its coverage will weaken our credibility with the exact IETF participants on the thread.
- **Point 3 — Agree with the core requirement, but the phrasing needs sharpening:**
  - *Reason:* Focusing on the moment of action is right (`/Users/debb/Downloads/ietf127-recap.md` lines 8–10; `/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 114–126). However, it should acknowledge Alan Karp's resource-side check on request arrival (`/Users/debb/Downloads/uma-thread-brief.md` line 15) and state the requirement in plain functional terms (holding/waiting for Alice's decision before acting, rechecking at action time, and allowing Alice to withdraw and stop the action at the resource without revoking Bob's underlying mission/token) rather than exposing our internal state taxonomy (my own reasoning, grounded in `/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 121–126 and `/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` lines 24–35).

#### Q2: Does anything in the draft reveal more of our design than the requirement?

- **Yes:** The phrase **`"a decision to allow, restrict or hold for Alice, or deny"`** (`/Users/debb/Downloads/uma-thread-brief.md` lines 23 and 39) directly names SOGA's internal decision outcomes (`ALLOW`, `RESTRICT`, `DENY`) and G26 operational path (`HOLDING`) from `/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` lines 24–27 and 62–64 (also `/Users/debb/dev/soga-clean/knowledge/strategy/DECISION_LOG.md` lines 131–149).
- To comply with Boundary Rule 1 (*"State the requirement (what), not our design (how). No states, flows, or code"*, `/Users/debb/Downloads/uma-thread-brief.md` line 27), replace `"a decision to allow, restrict or hold for Alice, or deny"` with plain requirement language—for example: *"at the moment Bob's agent is about to act, the resource must be able to wait for Alice's answer if one isn't in hand, recheck whether her approval still stands right then (not just when a token was issued), and stop the action if she withdraws without having to revoke Bob's own authority"* (my own reasoning, grounded in `/Users/debb/Downloads/uma-thread-brief.md` line 27 and `/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 114–126).

#### Q3: Is anything in the IETF recap or this brief wrong? Point to the source.

1. **`/Users/debb/Downloads/ietf127-recap.md` line 39 — Inaccurate summary of AAuth (`"permission granted or denied before access"`):**
   - AAuth is not purely "decided once before access": our verified AAuth research notes record that AAuth defines **mission revocation** (PS marks mission revoked, denies subsequent requests against `s256`, and revokes outstanding auth tokens at the resource; `/Users/debb/dev/soga-clean/knowledge/research/AAUTH_FINDINGS_2026-08-05.md` lines 20–22), short-lived resource tokens (`<= 5 min`) where *"Each issuance is a re-evaluation point"* (`/Users/debb/dev/soga-clean/knowledge/research/AAUTH_FINDINGS_2026-08-05.md` lines 23–24), and deferred responses (`requirement=approval`) used for pending pre-grant holds (`/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` lines 26–27, 79–85).
2. **`/Users/debb/Downloads/ietf127-recap.md` line 28 — Framing the gate as a protocol `"policy decision point" approving party`:**
   - In our canonical decisions, SOGA is **not** a standalone protocol party or centralized PDP: *"Governance is not centralizable... No single party is the policy decision point... SOGA is the implementation of the PS's governance policy. It is an engine, not a protocol party"* (`/Users/debb/dev/soga-clean/knowledge/research/AAUTH_FINDINGS_2026-08-05.md` lines 17–19, 44–46; `/Users/debb/dev/soga-clean/knowledge/strategy/DECISION_LOG.md` lines 89–92 `D-011`; `/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` lines 16–17).
3. **`/Users/debb/Downloads/ietf127-recap.md` line 22 — `"The gateway supports two entry paths: AAuth (first, already in G26) and OAuth (second)."`:**
   - In the loaded repository (`51d19d07915937160747b9177d228de1f1429e08`), G26 implemented the AAuth Person Server mission/permission decision (`/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` lines 16–18), not the robot gateway, and no committed decision in `/Users/debb/dev/soga-clean/knowledge/working/CURRENT_STATE.md` or `/Users/debb/dev/soga-clean/knowledge/strategy/DECISION_LOG.md` has adopted OAuth as a second gateway entry path yet.
4. **`/Users/debb/Downloads/uma-thread-brief.md` line 37 — Claiming `"the newer OAuth and AAuth work, including the transaction challenge draft discussed at IETF last week, now covers approval by a different resource owner"`:**
   - Contradicts `/Users/debb/Downloads/ietf127-recap.md` line 13 (no cross-domain path back to a home AS in the transaction challenge draft) and contradicts `/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 143–154 & `/Users/debb/dev/soga-clean/m02_aauth_fcf656d/other_party_approval.py` line 1 (where other-party approval in our AAuth demo is an additive application/resource policy, not native AAuth coverage of a different resource owner).
5. **`/Users/debb/Downloads/uma-thread-brief.md` line 41 vs. line 28 — Missing Kantara IPR non-acceptance statement:**
   - The draft reply at line 41 omits the explicit statement that Deb has not accepted Kantara IPR terms, which line 28 of the same brief requires.

---

## PART II — Later Additions for Queue 390 (Codebase Mapping of Recap Section 3 Items, Primary-Source Standards Checks & Proposed Requirement-Only Reply)

### 4. Mapping Each of the Four `ietf127-recap.md` Section 3 Proposed-Work Items to Current Code (`HEAD = 51d19d07915937160747b9177d228de1f1429e08`)

#### Item 3.1: *"1. OAuth Transaction Authorization Challenge adapter, with the gate as the 'policy decision point' approving party. Open question: where the mission comes from on the OAuth path."* (`/Users/debb/Downloads/ietf127-recap.md`, line 28)

- **Current Actual Code vs. Mock/Stub/Pinned Status:**
  1. **Existing OAuth/GNAP Adapter (`/Users/debb/dev/soga-clean/input_adapters/oauth_adapter.py`, lines 34–176; fixture `/Users/debb/dev/soga-clean/tests/fixtures/payloads/oauth_gnap_caregiver.json`, lines 1–43):**
     - **Status:** **Static mocked passive transformer only** (`metadata={"stub": True}`, line 118). Its docstring (lines 41–51) explicitly states: *"passive data transformer only; static mocked payloads only; no live OAuth server; no live GNAP server; no socket connection; no token library; no a2a-gateway integration; no governance decision logic."*
     - It synthesizes a `MissionTemplate` (`verify/mission_template.py`) by pulling `mission_id`, `objective`, and `actions` out of a mocked `grant.authorization_details[0]` dictionary and combining them with a static `governance_context` dictionary.
  2. **Existing AAuth Surfaces (for comparison):**
     - **G26 Permission Surface (`/Users/debb/dev/soga-clean/aauth_permission/models.py` & `service.py`):** In-memory mock Person Server permission endpoint (`PermissionService`, docstring line 15: *"Mock AAuth Person Server permission surface for G26"*) that uses the native immutable AAuth `Mission` (`s256` over `agent`, `approved_at`, `approved_tools`, `approver`, `description`) and projects `RESTRICT` (`restrict_path=HOLDING`) to HTTP `202` deferred approval (`requirement=approval`, `/pending/<id>`).
     - **M02 Loopback Person Server (`/Users/debb/dev/soga-clean/m02_person_server/service.py`):** Loopback-only (`127.0.0.1`) SQLite + HS256 test harness (`test_only: True`, `conformance_claim: None`, lines 107–108).
     - **M02 Pinned AAuth `fcf656d` Profile (`/Users/debb/dev/soga-clean/m02_aauth_fcf656d/`):** Bounded, pinned Ed25519 + HTTP Message Signatures localhost profile where `approval_pending.py` implements resource-held `202` pending records (`/pending/<32-char-id>`, 120s expiry, replay cache) and `other_party_approval.py` implements an additive resource-side third-party receipt policy (`ApprovalGovernedResource`). Under `CURRENT_STATE.md` lines 79–85 (`D-102`), the M02 AAuth Phase 1 package is create-only/paused, and `robot_gateway/` (`gateway.py`, `coordinator.py`, `switching.py`, `cyberpi_none_observation_v3.py`, `misty_stop_probe.py`) contains local loopback/serial hardware controllers with no OAuth or AAuth token parsing.
- **Prospective Impact on Current Code & Write/Check Split:**
  - `draft-rosomakho-oauth-txn-challenge-01` (`https://datatracker.ietf.org/doc/draft-rosomakho-oauth-txn-challenge/`) has **no native mission construct**—a Protected Resource returns an error challenge with a signed transaction descriptor, the client requests a token from the AS using `draft-ietf-oauth-deferred-token-response` while the AS obtains HITL/HOTL/HOOTL approval, and the AS issues a single-use access token bound to the transaction identifier.
  - Because `G26` adopted the AAuth mission structure natively (`D-013`, `D-019`; `aauth_permission/models.py` lines 27–68) while preserving the `RuntimeEnvelope` / `MissionTemplate` adapter boundary (`verify/runtime_envelope_model.py`), an OAuth Transaction Challenge adapter would need to supply mission context either from Rich Authorization Requests (`RFC 9396` `authorization_details`, as currently stubbed in `input_adapters/oauth_adapter.py` lines 55–98) or from AS-side session/grant state keyed to the client/agent.
  - **Architectural conflict to avoid:** Under `D-011` (`DECISION_LOG.md` lines 89–92) and `G26_MISSION_PERMISSION_DECISION.md` (lines 16–17), SOGA must remain the policy engine invoked *inside* the approving server (AS/PS or resource enforcement boundary), **not** a new external protocol party.

#### Item 3.2: *"2. Read Karl's actor profile (the `act` chain) as evidence of who is in the path. It removes the 'who sent this?' call. It does not answer 'may this happen now.'"* (`/Users/debb/Downloads/ietf127-recap.md`, line 29)

- **Current Actual Code vs. Mock/Stub/Pinned Status:**
  1. **Pinned AAuth Token Profile (`/Users/debb/dev/soga-clean/m02_aauth_fcf656d/tokens.py`, lines 85–106, 138–150):**
     - Enforces `validate_agent_identifier(agent_id, top_level_only=True)` on `aa-agent+jwt` and binds sender possession via `cnf.jwk` / `agent_jkt`. It rejects sub-agent identifiers and does **not** parse OAuth `act` (`RFC 8693`) claims.
  2. **M02 Supervision & Hop Limits (`/Users/debb/dev/soga-clean/m02_aauth_fcf656d/soga_supervision.py`, `/Users/debb/dev/soga-clean/m02_person_server/service.py` line 49, `/Users/debb/dev/soga-clean/tests/test_m02_aauth_other_party_approval.py` line 37):**
     - Tracks only a scalar integer `delegation_hops` against `max_delegation_hops` (currently `0` in M02 test profiles).
  3. **Input Adapters & Advisory Layer (`/Users/debb/dev/soga-clean/input_adapters/aauth_adapter.py` lines 118–120; `/Users/debb/dev/soga-clean/advisory/agent_evidence.py` lines 8–28; `/Users/debb/dev/soga-clean/advisory/provenance_extension.py` lines 8–22):**
     - `aauth_adapter.py` stores flat `credential_refs` and `parent_request_id` strings; `AgentEvidence` is explicitly non-authoritative metadata (*"Evidence only. Not a governance determination"*).
- **Prospective Impact & Primary-Source Standards Check (`RFC 8693` Section 4.1 & `draft-mcguinness-oauth-actor-profile`):**
  - **Primary sources:** `https://www.rfc-editor.org/rfc/rfc8693#section-4.1` and `https://datatracker.ietf.org/doc/draft-mcguinness-oauth-actor-profile/`.
  - **Critical RFC 8693 Section 4.1 rule:**
    > *"For the purpose of applying access control policy, the consumer of a token MUST only consider the token's top-level claims and the party identified as the current actor by the `act` claim. Prior actors identified by any nested `act` claims are informational only and are not to be considered in access control decisions."*
  - **Code mapping:** Reading `act` in an input adapter (`input_adapters/oauth_adapter.py`) fits SOGA's write/check split **only if** (a) the outermost `act` claim (together with sender-constraint verification such as `cnf` / `draft-mcguinness-oauth-actor-hop-proofs`) identifies the immediate acting agent, and (b) nested `act` claims are mapped into `AuthorityEvidence.references` / `raw_evidence` (`verify/runtime_envelope_model.py`) and `delegation_hops` for provenance/hop-count auditing, **never** treated as authorization to act now.

#### Item 3.3: *"3. Read Transaction Tokens and George's cross-domain grant (Txn-Token-JAG) as evidence. Huawei's 'Mode B' shortcut can wait."* (`/Users/debb/Downloads/ietf127-recap.md`, line 30)

- **Current Actual Code vs. Mock/Stub/Pinned Status:**
  - **No implementation exists in `/Users/debb/dev/soga-clean`:** None of the five adapters in `/Users/debb/dev/soga-clean/input_adapters/` (`oauth_adapter.py`, `aauth_adapter.py`, `ucan_adapter.py`, `zcap_adapter.py`, `aiim_adapter.py`) parses IETF Transaction Tokens (`draft-ietf-oauth-transaction-tokens`) or OAuth Token Exchange / JWT Authorization Grants (`RFC 8693` / `RFC 7523` / `draft-fletcher-oauth-txn-token-chaining-profile-01`). All five adapters are offline dict normalizers with no signature verification.
- **Prospective Impact & Primary-Source Standards Check:**
  - **Primary source:** `draft-fletcher-oauth-txn-token-chaining-profile-01` (*Transaction Token JWT Authorization Grant Profile for OAuth Identity and Authorization Chaining*, `https://datatracker.ietf.org/doc/draft-fletcher-oauth-txn-token-chaining-profile/`) uses RFC 8693 Token Exchange to exchange a `Txn-Token` in one trust domain for a cross-domain JWT Authorization Grant (`Txn-Token-JAG`) that preserves immutable transaction context (`tctx` / `azd`) across domain boundaries.
  - **Code mapping:** In SOGA, a verified `Txn-Token` or `Txn-Token-JAG` would be normalized by a new or extended OAuth input adapter into `RuntimeEnvelope.authority` (`AuthorityEvidence` in `verify/runtime_envelope_model.py`) as immutable call-context evidence before `GovernancePDP` (`verify/governance_pdp.py`) or `SogaRuntimeEngine` (`engines/soga_runtime_engine.py`) evaluates the action.
  - **Unverified source note:** `draft-liu-oauth-cross-domain-txn-token-00` ("Huawei's Mode B shortcut", cited in `ietf127-recap.md` line 67 as *"Deb's upload"*) is not present in `/Users/debb/dev/soga-clean` or `/Users/debb/Downloads/`; its specific "Mode B" details are marked **`UNVERIFIED`**.

#### Item 3.4: *"4. Watch: U4A, UCAN, Rosenberg's aauth draft, client instance IDs."* (`/Users/debb/Downloads/ietf127-recap.md`, line 31)

- **Current Actual Code vs. Mock/Stub/Pinned Status:**
  1. **UCAN (`/Users/debb/dev/soga-clean/input_adapters/ucan_adapter.py`, lines 45–174; fixture `/Users/debb/dev/soga-clean/tests/fixtures/payloads/ucan_caregiver.json`):**
     - **Status:** **Static, non-cryptographic normalizer only.** Line 50 states: *"This adapter does not verify UCAN signatures. It normalizes UCAN-shaped authority evidence for the unchanged Governance PDP."*
  2. **U4A (`https://github.com/nickgamb/uma4agents/tree/main/spec`), Rosenberg's `draft-rosenberg-oauth-aauth`, and McGuinness's `draft-mcguinness-oauth-client-instance-identity`:**
     - **Status:** **Zero code in `/Users/debb/dev/soga-clean`.** Currently, agent identity in our pinned AAuth profile (`m02_aauth_fcf656d/tokens.py` lines 85–106 and `approval_pending.py` lines 78–80) binds a top-level agent identifier (`sub`) plus a per-key JWK thumbprint (`agent_jkt`) and `token_jti`, not an attested client-instance claim.
- **Prospective Impact:**
  - Keeping these four on a watch-only list aligns with `G19` ecosystem neutrality (`G26_MISSION_PERMISSION_DECISION.md` lines 13–14, 96–101). If `draft-mcguinness-oauth-client-instance-identity` matures, an attested instance ID would map to the holder/instance key in `ApprovalPendingStore` (`m02_aauth_fcf656d/approval_pending.py` lines 74–89) and `AuthorityEvidence.references` (`verify/runtime_envelope_model.py`), allowing `HOLDING` or revocation to target one running copy of an agent harness without revoking sibling instances.

---

### 5. Primary-Source Verification of Specific Technical & Standards Claims

1. **Broad Gap/Novelty Claim (`ietf127-recap.md` line 8) & Revocation vs. Stopping Already-Executing Work:**
   - *Claim in recap:* *"No spec presented this week can hold, pause, or revoke authority while a task is running. Every group either decides before access is granted, or audits afterward."*
   - *Primary-source check:*
     - **Between requests/steps of a running task:** Both AAuth (`AAUTH_FINDINGS_2026-08-05.md` lines 20–24: mission revocation by `s256` + `<= 5 min` resource token re-evaluation points + deferred `202` responses) and `draft-rosomakho-oauth-txn-challenge-01` (per-transaction challenge + `draft-ietf-oauth-deferred-token-response` polling + single-use transaction tokens) **do** pause/hold before a challenged transaction and can refuse or revoke authority between steps of a running task.
     - **During an already-dispatched action:** Neither OAuth/AAuth/UMA token revocation nor SOGA's pre-action gate physically stops an already-executing hardware or external action once dispatched. Our own repository strictly separates authorization state from physical/execution stop (`robot_gateway/CYBERPI_NONE_OBSERVATION_V3.md` lines 244–247: *"No close/result proves physical shutdown"*; `FLOW_A_RUNTIME_MAPPING_2026-10-31.md` lines 19–23: separating `last_terminal_outcome=ALLOW` from `presentation_outcome=STOPPED`).
     - **What SOGA/Flow A actually adds at the moment of action:** (a) holding an action at the resource/PS gate for a **non-delegating affected third party (Alice)** while the operator's (Bob's) delegated mission token is already valid, and (b) rechecking Alice's live decision at action time so Alice's withdrawal refuses/stops the action at the resource **without revoking Bob's underlying mission or auth token** (`SPEAKER_SCRIPT.md` lines 121–126, 167–169; `m02_aauth_fcf656d/other_party_approval.py` lines 108–145).
2. **GNAP and UMA Relationship (`uma-thread-brief.md` lines 22, 37, 55):**
   - *Claim in brief:* *"GNAP (RFC 9635) absorbed much of UMA's design."*
   - *Primary-source check:* **RFC 9635** (`https://www.rfc-editor.org/rfc/rfc9635`, October 2024) is GNAP Core, whereas **`RFC 9767`** (*Grant Negotiation and Authorization Protocol Resource Servers*, `https://www.rfc-editor.org/rfc/rfc9767`) is the companion RFC that specifically absorbed UMA 2.0's resource registration, RS-to-AS introspection, and asynchronous resource-owner authorization patterns. Citing RFC 9635 and RFC 9767 together is more accurate—and both still assume a pre-established relationship between the Resource Server and the Authorization Server rather than ad-hoc discovery of an unassociated bystander/parent in the field.
3. **Claims Dependent on Offline Transcripts/Uploads Marked `UNVERIFIED`:**
   - The following items in `ietf127-recap.md` and `uma-thread-brief.md` rely on Deb's offline session transcripts/uploads not present in `/Users/debb/dev/soga-clean` or `/Users/debb/Downloads/` and are therefore marked **`UNVERIFIED` from local files**:
     - Exact IETF 127 chat quotes attributed to George Fletcher, Karl McGuinness, Pieter Kasselman, Justin Richer (*"may actually be incomputable in the general case"*), Jonathan Rosenberg (*"very, very similar"*), and Brian Campbell (*"which aauth?"*) (`ietf127-recap.md` lines 13–17, 46, 50–52, 70).
     - Internal contents of `draft-liu-oauth-cross-domain-txn-token-00` ("Huawei's Mode B shortcut", `ietf127-recap.md` lines 30, 45, 67).
     - Verbatim messages of Adrian Gropper, Alan Karp, Eve Maler, and Harvey in the Nov 23 WG-UMA email thread beyond the brief's summary (`uma-thread-brief.md` lines 14–17, 53).

---

### 6. Proposed Requirement-Only Wording for Deb's WG-UMA Reply

The revised draft below fixes all five issues identified above:
1. Removes SOGA's internal decision/path state names (`"allow, restrict or hold for Alice, or deny"`) to honor Boundary Rule 1 (`uma-thread-brief.md` line 27).
2. Explicitly states that Deb is not a WG-UMA member and has not accepted Kantara IPR terms to honor Boundary Rule 2 (`uma-thread-brief.md` line 28).
3. States the **dual-authority** requirement (Bob's delegated authority + Alice's independent decision where Alice never delegated anything to Bob).
4. Removes the inaccurate claim that AAuth and `draft-rosomakho-oauth-txn-challenge-01` already solve cross-domain approval by a different resource owner (aligning with `ietf127-recap.md` line 13 and `SPEAKER_SCRIPT.md` lines 143–154), and cites GNAP (`RFC 9635` / `RFC 9767`) accurately.
5. Acknowledges Alan Karp's resource-side check on request arrival while sharpening what is still missing (waiting/holding when Alice's answer isn't yet in hand, rechecking at action time, and honoring Alice's withdrawal at the resource without revoking Bob's own authority, with attributable evidence of what was checked).

> Adrian, Eve, Alan, Harvey, all,
>
> This is a team response from Deb B Labs: my own view, worked through with the AI agents I run on this research.
>
> To be clear about where we stand: we think UMA's separation of roles—where Bob's agent asks, Alice's policy governs her side, and the resource server is accountable for enforcement and logs—is a useful way to frame the third-party half of this problem, alongside Bob's own delegated authority over his agent. Both authorities have to hold at the same time, even when Alice never delegated anything to Bob and never pre-registered with the resource's authorization server.
>
> We're less sure UMA 2.0 itself needs to be extended to deliver this. GNAP (RFC 9635 and RFC 9767) absorbed much of UMA's resource-registration and asynchronous-grant design, and newer IETF work—such as the OAuth Transaction Authorization Challenge draft (`draft-rosomakho-oauth-txn-challenge-01`) discussed at IETF 127 last week—addresses per-transaction deferred approval within an authorization server's domain, though routing a challenge across trust domains to Alice's own home server or agent remains an open gap.
>
> Building on Alan's point about checking revocation at the resource when a request arrives, the requirement we'd add is what has to happen right at the moment Bob's agent is about to act: the resource side must be able to pause and wait if Alice's answer is needed and not yet in hand, recheck whether her approval still stands at the moment of action (not only when a token was issued), and stop the action if Alice withdraws—without having to revoke Bob's own delegated authority—while recording attributable evidence of both checks.
>
> (I am not a Kantara WG-UMA member or participant and have not accepted Kantara IPR terms; sharing this solely as an outside observer.)
>
> Debbie


<!-- END VERBATIM AGY_INITIAL_QUEUE_390_VERBATIM.txt -->


### Appendix C — CG independent review

Original file: `CG_INDEPENDENT_REVIEW.txt`; SHA-256: `a37564442ec1e33184677e5d424a1f9e87872c2a551679b819cf1e9c073a69df`.

<!-- BEGIN VERBATIM CG_INDEPENDENT_REVIEW.txt -->

CG advisory review — source documents ietf127-recap.md and uma-thread-brief.md, Nov23 2026.
Repo HEAD loaded: 51d19d07915937160747b9177d228de1f1429e08. No build authorization, files/architecture changes, tests or hardware. This consolidates CG own initial findings before reviewing reviewer responses; not attributed to peers.

UMA Q1: qualified agreement with responsibility model, not blanket endorsement of summarized ten assumptions. Need authority of Alice agent; normative UMA is AS/RS/requesting-party model, agent-agent exchange not universally mandated. Need for UMA extension unestablished. Challenge01 section1.2 explicitly allows different resource owner. GNAP has related mechanisms; historical absorbed-much-of-UMA claim unsupported by RFC9635 alone. Requirement current authorization at consequential action sound, absolute none-of-them claim not supported. Check continuing applicability, not necessarily new user prompt each action. Revocation/denying future requests differs from stopping already running physical work.
UMA Q2: no code/flows disclosed, but allow/restrict/hold/deny mirrors internal vocabulary, best replace with neutral requirement. Draft lacks explicit IPR-not-accepted statement required by its own brief; cannot infer legal effect. AI-assisted team disclosure present. Observer rather than participant claim present.
UMA Q3: recap blanket before-grant-or-after-audit incorrect; GNAP grant modification/re-evaluation/revocation and token revocation; Hardt AAuth11 section11.12 revocation/cascade. Challenge resource validates operation and transaction, single-use conditional SHOULD for high-impact/nonidempotent, not universal MUST. Actor profile authenticates/asserts representation with trust checks; does not eliminate presenter authentication and issuer trust, historical inner chain audit not access-control input. Incomputability quote does not prove necessary particular mechanism. Meeting quotes, adoption/interim/Dec dates not independently verified without primary meeting/mail sources. Current repo G26 permission boundary not action execution; AAuth crypto profile pinned fcf656de1926535f5bd6fc0538147ead6646e727, not proof complete -11 conformance.

Prospective code touchpoints:
1 OAuth challenge: input_adapters/oauth_adapter.py is representative mocked/stub transform; cannot silently promote defaults to mission authority or live verifier. Need separately specified authenticated challenge/token boundary, transaction binding, replay/deferred processing. aauth_permission/service.py pending/reevaluation analog, mock AAuth service not OAuth implementation. verify/runtime_envelope_model.py evidence projection, engines/runtime_governance_engine.py evaluation, canonical package conversion. Mission source/provenance must explicit resolved contract rather than assume RAR/challenge supplies approved mission.
2 Actor profile evidence: verification before projection to AuthorityEvidence references/raw_evidence; preserve iss-scoped immediate actor and provenance, nested history separate audit. input_adapters/aauth_execution_adapter.py example passive boundary, m02_aauth_fcf656d/tokens.py pinned-profile-specific not general verifier. No decision logic in parser.
3 TxnTokens/JAG: new separately reviewed verification/exchange and evidence normalization; issuer/audience/trust-domain constraints, txncorrelation, no scope expansion; no robot transport change to read evidence. New protocol compatibility not implicit existing token verifier.
4 Watch: research only no implementation change. input_adapters/ucan_adapter.py existing comparison point, not deployment evidence. clientinstance eventually grant/invocation binding/invalidation separately reviewed. robot_gateway/switching.py authorization consumption future integration; OPERATOR_RUNTIME.md synthetic-only not live AAuth authorizer. Standards adapter alone cannot finish physical gateway.

Primary sources checked:
https://www.ietf.org/archive/id/draft-rosomakho-oauth-txn-challenge-01.html sections1.2,6.2
https://www.rfc-editor.org/rfc/rfc9635.html sections5.3,5.4,6.2
https://www.ietf.org/archive/id/draft-hardt-oauth-aauth-protocol-11.html section11.12
https://www.ietf.org/archive/id/draft-mcguinness-oauth-actor-profile-01.html sections8.1,8.2
https://datatracker.ietf.org/doc/draft-fletcher-oauth-txn-token-chaining-profile/01/ section7
Additional checks after initial chat answer, before peer reports:
https://docs.kantarainitiative.org/uma/wg/oauth-uma-grant-2.0-09.html (AS/RS/requesting party, asynchronous authorization, revocation)
https://www.rfc-editor.org/rfc/rfc7662.html (resource queries token active state/context)
https://www.rfc-editor.org/rfc/rfc7009.html (token revocation)
These reinforce no blanket claim all decisions precede access or follow it as audit. None alone proves stopping an in-flight task.

Proposed requirement-only wording, advisory:
Authorization must remain applicable when a consequential action is performed. Changes or withdrawal of the resource owner's authority must take effect at the relevant enforcement point, with defined behavior when current authorization cannot be established.
This is a requirement to examine against protocol combinations and deployments, not an established standards-gap or novel-feature claim.


<!-- END VERBATIM CG_INDEPENDENT_REVIEW.txt -->


### Appendix D — CG follow-up source checks

Original file: `CG_FOLLOWUP_SOURCE_CHECKS.txt`; SHA-256: `7c176e5c0876efb36e244f031e97c48ba374de29d6ae305c0f763b6942fbeda2`.

<!-- BEGIN VERBATIM CG_FOLLOWUP_SOURCE_CHECKS.txt -->

CG follow-up source checks after AGy390 arrived; original CG independent review is preserved separately. These are discussion points, not consensus or implementation instructions.

1. AGy usefully identifies independent operator/affected-party permissions and need to establish affected party standing. These are application requirements, not proof no standard can express them. Its initial criticism of challenge section1.2 needs care: different-owner approval is explicitly covered. Arbitrary cross-domain routing/discovery is a distinct question, not a contradiction of section1.2. Recap chat summaries and our speaker script are not normative primary standards sources.
2. RFC9767 checked directly: full title Grant Negotiation and Authorization Protocol Resource Server Connections. Defines RS/AS discovery, token introspection, resource-set registration and downstream token derivation. It contains no UMA text. This supports functional comparison with UMA; does NOT by itself prove historical claim absorbed much of UMA. RFC9635 likewise not historical proof. Ask AGy for direct authoritative history source or soften genealogy claim.
   https://www.rfc-editor.org/rfc/rfc9767.html sections1,3,4
3. Repo DECISION_LOG D-011 RESOLVED Aug5 says SOGA is PS governance policy, not a new protocol party. Prospectively OAuth adapter must identify deployment role and authorization, rather than make gate an independent universal approver. This is distinct from internal class named GovernancePDP.
4. Public FlowA evidence has strict demonstration boundary. FLOW_A_RUNTIME_MAPPING_2026-10-31.md says presentation_outcome only records how presentation was closed. SPEAKER_SCRIPT.md says child arrival/leaving simulated and no robot/camera connected; other-party input unverified identity. Do not claim physical stop or proven real-world parent standing. Signed check-back / resource refusal may be actual application behavior; physical stop separate unproven.
5. Nested historical actor entries must not become access-control inputs by deriving delegation_hops from chain length. AGy mentions nested history mapped to hop-count auditing. Existing m02_aauth_fcf656d/soga_supervision.py uses delegation_hops to deny when above max. Preserve history for audit only unless separately specified evidence/profile defines authorized control semantics; do not accidentally feed existing deny check from history. https://www.rfc-editor.org/rfc/rfc8693.html section4.1
6. User-reported standing direction is not invalid just because not committed. Separate Deb-reported policy direction, canonical recorded adoption, implementation and demonstration. Advisory recap does not itself authorize this build.
7. CG own initial response lacked explicit dual-authority/standing and D-011 emphasis; these are useful additions from AGy, subject to not turning them into unsupported novelty claims. No reviewer original will be overwritten by later conclusions.


<!-- END VERBATIM CG_FOLLOWUP_SOURCE_CHECKS.txt -->


### Appendix E — Shared discussion questions

Original file: `DISCUSSION_QUESTIONS.txt`; SHA-256: `6dddc4c58efbd092f33d5cbeda5e412b37ce1941c911634c69db788359500c73`.

<!-- BEGIN VERBATIM DISCUSSION_QUESTIONS.txt -->

Round2 advisory discussion — original independent responses preserved. Initial blindness now complete; peer exchange explicitly authorized by Deb. This is discussion/check-side only, not build or public sending.

Read both complete 389/390 responses, CG original and followup notes, and Deb meeting context. Do not overwrite originals. Reply with: (a) what you retain/change from original, (b) agree/disagree on each question with primary support, (c) suggested brief final requirement wording and open items. Correct your own earlier overstatements, and distinguish normative statements, meeting recollection, our observed demo behavior, inference and future research.

1. Shared premise: broad no-spec-holds/revokes during running task is too strong. Does proposed distinction adequately separate new request authorization/revocation, current affected-party policy, and cancellation of accepted in-flight execution? Verify BoundedWork00 exact limitation/acceptance-window language. Do NOT replace broad claim with equally unproven no-spec-defines-one-decisionpoint novelty claim.
2. Third-party standing / dual permissions: useful insight from AGy. Phrase Bob's agent acts under Bob's authority with separate affected-party Alice permission where applicable. CC B6 says on Alice behalf; that may erase nondelegating affectedparty distinction. Do not assume all affected parties are resource owners or demand ALL access require two independent human approvals. Keep identification/standing as open problem; our parent demo input unverified and no robot/camera connected, presentation STOPPED not physical-stop evidence. Verify applicable source and retain limits.
3. Challenge01 section1.2 explicitly covers different-resource-owner approval. Arbitrary home-AS discovery/crossdomain routing is distinct, not contradiction or proof section1.2 false. AGy PartI used recap to challenge normative coverage; reconcile with actual draft. Challenge single-use conditional; AGy PartII sometimes states universal single-use — correct. Which deployments can existing protocol composition express vs genuinely unidentified responsibility? Report gaps as questions until primary verification.
4. GNAP/UMA history: Deb witnessed Justin saying he stole UMA code and says early Claude material includes it. Preserve this firsthand evidence, do not insist lineage false because RFC lacks UMA word. Seek primary meeting/history source, otherwise attribute reported remark and leave exact scope unverified. RFC9767 provides functional RS/AS discovery/introspection/resource-registration/downstream-token APIs, but does not itself mention UMA. AGy claim absorbed UMA especially async patterns needs direct citation or softer functional comparison. Avoid holding user as relay for verifiable technical sourcing.
5. New primary minutes available: https://datatracker.ietf.org/doc/minutes-127-oauth/00/ . CG found Justin discussion of UMA useful pieces during Rosenberg presentation and attenuation incomputability concern in BoundedWork. No match stole or GNAP in these summary minutes (absence NOT disproof recollection). Distinguish minutes support/paraphrase vs exact quote. Do not keep ALL meeting remarks blanket UNVERIFIED if official minutes verify some; draft status/charter targets vs realized outcomes separate. U4A Credential-vs-Binding and attribution should be checked against exact source/revision before final.
6. Actor evidence: current actor `(iss,sub)` vs nested audit history, bearer presenter vs sender-constrained proof, issuer trust. AGy proposed nested act history mapped to delegation_hops for audit, but actual soga_supervision.py uses delegation_hops for deny decision. Ensure nested historical actors do not become access-control input via counting; no newimplementation proposed.
7. D-011 engine policy vs protocol party: generic draft allows PDP approver, but that does not authorize centralizing SOGA or adding protocol party. Need deployment role/integration contract; user standing direction can be real even if not yet repo-recorded, advisory note alone no build authority.
8. Mission source: current OAuth adapter stub/defaults not approved mission; need owner/provenance/binding separately. G26 permission, later pinned fcf656d profile, OAuth mock and robot synthetic/physical evidence separate. Preserve neutrality/write-check split, watch-only items no code change.
9. Reply disclosure: requirement-only no internal state taxonomy, AI assistance/observer posture, missing explicit IPR statement per brief; no legal conclusions. Suggested wording short, avoids claiming universal standards absence or new physical-stop proof. Include traceable evidence and treatment of unavailable/stale authority as requirements without publishing design.

No code edits/import/compile/tests/build, signing, hardware, commits, external messages. Standards primary-source browsing and static reads only. No unrelated PI proposal. Return advisory reasoned conclusions not a build PASS.


<!-- END VERBATIM DISCUSSION_QUESTIONS.txt -->


### Appendix F — Claude Code follow-up discussion

Original file: `CLAUDE_CODE_DISCUSSION_391_VERBATIM.txt`; SHA-256: `3ac032f4325670871cebfa63de8a1217fdbaf68693643a95d3541c989b0a8e3a`.

<!-- BEGIN VERBATIM CLAUDE_CODE_DISCUSSION_391_VERBATIM.txt -->

391 Gate 1 (Claude Code) response - advisory discussion round 2 (standards review)

ADVISORY ONLY. No build, code, commit, signing, hardware or external message. Originals are preserved, not overwritten.
Repo HEAD: 51d19d07915937160747b9177d228de1f1429e08.
Inputs read in full (all hashes match the request):
- CLAUDE_CODE_INITIAL_QUEUE_389_VERBATIM 849ea12f (cmp-identical to my filed 389)
- CLAUDE_CODE_PRE_QUEUE_ORIGINAL_VERBATIM 3c2a8d6d
- AGY_INITIAL_QUEUE_390_VERBATIM f6561df2
- CG_INDEPENDENT_REVIEW a3756444
- CG_FOLLOWUP_SOURCE_CHECKS 7c176e5c
- DEB_MEETING_CONTEXT d7672e48
- DISCUSSION_QUESTIONS 6dddc4c5
- STATUS 6a4f2012

Statement-type tags used below:
- [N] normative text in a primary specification
- [M] official meeting minutes (summary notes, not transcripts)
- [D] Deb's firsthand report
- [R] our repo or demo artefacts and observed demo behaviour
- [I] my inference
- [F] future research or open question

(a) RETAIN / CHANGE from my originals (pre-queue 3c2a8d6d and 389 849ea12f)

RETAINED:
- The draft names, authors, revisions and dates as verified.
- Section 1.2 of the challenge draft covers different-owner approval [N].
- The U4A AAuth draft is classed "Credential", not "Binding". Now checked at a specific revision: spec/README.md at nickgamb/uma4agents main commit 77649287dc883b75ef563c59f96de8613ecf10d0 (2026-11-19) lists draft-gamb-uma4agents-aauth-00 as "Credential" and the MCP draft as "Binding" [N-ish: project README, not an RFC].
- Kantara does not appear in that README.
- The IPR statement is missing from the draft reply.
- The outcome vocabulary leaks internal design.
- Reading the act chain is evidence, not authorization (RFC 8693 Section 4.1) [N].
- The repo mapping (OAuth adapter stub; UCAN does not verify signatures; AAuth is a pinned fcf656d profile).

CHANGED (my own overstatements, corrected):
C1. In my pre-queue answer I proposed "no spec defines one decision point at the moment of action with a defined hold outcome that rechecks…". That is itself an unproven novelty claim. WITHDRAWN (Q1 is right). The B2/B6 framing in 389 stands only as a citation of what Bounded Work leaves to realizations. It is not a claim that nothing else does it.
C2. My 389 B6 wording "acting on Alice's behalf" erases the non-delegating affected-party distinction. WITHDRAWN; see Q2 and the revised wording in (c).
C3. "Single use is conditional": incomplete. It is conditional for the acceptance check ("if the protected resource requires single use") AND carries a SHOULD: "A protected resource SHOULD treat access tokens issued in response to a transaction authorization challenge as single-use when the challenged operation is non-idempotent or high impact" (-01, Section 6.2 area; same text in Security Considerations) [N]. Correct statement: not universal; SHOULD for non-idempotent or high-impact operations; MUST keep replay state when single use is required.
C4. "GNAP absorbed UMA: can't verify / unsupported". Too dismissive. RFC 9635 and RFC 9767 lacking the word UMA is not disproof [N absence]. Deb's firsthand report is evidence [D]. Recast in Q4.
C5. Blanket "all meeting remarks UNVERIFIED": superseded by the official minutes. See Q5.
C6. I did not flag that AAuth -11 itself defines token revocation, including cascade (Section 11.12 Token Revocation, 11.12.4 Revocation Cascade) [N]. That makes the recap's "decides before access or audits afterward" wrong for AAuth too (AGy and CG were right).

(b) THE NINE QUESTIONS

Q1. Broad claim versus the three-way distinction. AGREE that the broad claim is too strong, and the three-way split is the right separation:
- (i) Authorizing or revoking new requests: covered [N]. AAuth -11 Section 11.12; RFC 7009; RFC 7662 introspection; challenge -01 per-operation approval; Bounded Work ended state.
- (ii) Current affected-party policy at the time of action: expressible per request [N]. Challenge Section 1.2 selects the approver by AS policy; AS-side re-evaluation at each issuance. Whether a given composition captures a NON-delegating affected party's live wish is an open deployment question [F].
- (iii) Cancelling execution that was already accepted. Bounded Work -00 verbatim [N]:
  - "Ending a governing authorization does not by itself undo completed effects or cancel execution that another system has already accepted. A realization that governs such execution identifies the additional checkpoints and cancellation behavior it provides."
  - Acceptance window (verbatim): "State embedded in a token reflects an earlier authorization decision; it does not by itself reveal a later withdrawal. Where a bounded token lifetime is the only mechanism, the acceptance window is that lifetime."
  - And: "This framework governs authorization of protected operations at participating enforcement points."
  This is a scoping statement by one draft, not proof that no spec addresses (iii). Do NOT turn it into "no spec defines X" [I].

Q2. Third-party standing and dual permissions. AGREE with AGy's insight and CG's limits.
- Phrase it as: Bob's agent acts under Bob's authority, plus, where applicable, a separate permission from an affected party (Alice) who has not delegated to Bob.
- Do not assume every affected party is a resource owner.
- Do not require two independent human approvals for all access.
- Identification and standing of the affected party remain an OPEN problem [F].
- Demo limits [R]:
  - SPEAKER_SCRIPT.md: "There's no robot and no camera connected"; "the parent's answer is *unverified*"; child arrival and leaving are "(simulated)".
  - FLOW_A_RUNTIME_MAPPING_2026-10-31.md: "`presentation_outcome` records only how the presentation was closed".
  - STOPPED is a presentation outcome, not physical-stop evidence.
- Normative fit [N]: UMA 2.0 Grant (Kantara oauth-uma-grant-2.0, cited by CG) models resource owner versus requesting party with asynchronous authorization. It does not model a non-owner affected party; the fit is partial [I].

Q3. Challenge Section 1.2 versus cross-domain routing. AGREE with CG:
- Section 1.2, "Authorization by a Different Resource Owner", is explicit [N].
- Cross-domain discovery and routing to a home AS is a distinct question. It is not a contradiction of Section 1.2. AGy Part I used the recap (a non-normative summary) to challenge normative coverage, which should be reconciled: Section 1.2 holds within the AS's ability to determine the approving party.
- Correct AGy Part II's universal "single-use" (see C3).
- Expressible by composition [N]: a same-domain different owner (Section 1.2); deferred approval (DTR); cross-domain token flow (Txn-Token-JAG, -01; Mode B with pre-established trust).
- Unidentified responsibility, framed as QUESTIONS [F]:
  - Who discovers an unassociated affected party's AS?
  - Who establishes standing?
  - Who governs cancellation of accepted in-flight execution?
- Minutes [M], Rosenberg session: "Karl: There are proposals TXN Challenge, and DTR you should use." That supports composition rather than a missing-primitive story.

Q4. GNAP and UMA history.
- PRESERVE Deb's firsthand report [D] verbatim per DEB_MEETING_CONTEXT ("Justin said he stole the uma code in the ietf meeting"), attributed to her, with the exact scope and referent unverified.
- Official minutes [M] record only, in the Rosenberg session: "Justin: Putting the bits together is a good idea, and is tricky. UMA has some things that might be useful. Grant management API in OpenID would be good." There is no "stole" or GNAP in the minutes. That absence does NOT disprove the recollection; the minutes are summaries.
- RFC 9767 [N] (Richer, Ed., and Imbault, April 2025), "GNAP Resource Server Connections": token introspection (3.3), resource set registration (3.4), deriving a downstream token (4). Zero occurrences of "UMA".
- That supports a FUNCTIONAL comparison (GNAP provides RS-AS connection functions comparable to UMA's protection API) [I], not a documented genealogy.
- AGy's "RFC 9767 specifically absorbed UMA 2.0's … asynchronous resource-owner authorization patterns" lacks a direct citation. Soften to a functional comparison.
- A primary history source is still needed, for example a recording or the GNAP WG archive [F]. Do not ask Deb to relay what can be sourced technically.

Q5. Minutes (https://datatracker.ietf.org/doc/minutes-127-oauth/00/, read in full) [M]. Verified or paraphrase-supported:
- Rosenberg in the txn-challenge session: "Jonathan R.: very similar to our aauth draft." That supports the recap's "very, very similar", which is paraphrase-level; the exact doubling is not in the minutes.
- Bounded Work session: "JR: many people are addressing this problem… Attenuation may be incomputable, rendering the problem unsolvable." and "JR and Rifaat: let's discuss the problem first." and "KM: can we start with a use case discussion as an interim?"
  - That SUPPORTS the recap's interim-on-the-problem point.
  - The recap's exact quote "may actually be incomputable in the general case" is NOT in the minutes; it is paraphrase-level only.
  - ATTRIBUTION CAVEAT: these minutes use "JR" and also "Jonathan R."/"Justin" elsewhere, so "JR" is ambiguous between Justin Richer and Jonathan Rosenberg. Do not assert Justin from the minutes alone.
- Client instances: "Justin: Glad to see we're talking about client instances finally… Would support this work in the WG." Aaron: "We should solve it in the coming year." That supports "broad +1"; no adoption decision is recorded.
- Interims are mentioned repeatedly; no dates.
NOT found in the minutes (remain UNVERIFIED, not disproved):
- Fletcher's cross-domain home-AS remark.
- Kasselman's "separate problem".
- Campbell's "which aauth?".
- Karl's "containment", "Harness as Client" and the Claude Code example.
- The actor-profile adoption status.
- Hums and polls.
Charter Dec-2026 milestones are TARGETS [N], not outcomes. The HTTP signature-key item was "call for adoption discussion" (agenda); no result is known.

Q6. Actor evidence. AGREE with CG and DISAGREE with AGy's proposed hop mapping.
- RFC 8693 Section 4.1 [N]: "the consumer of a token MUST only consider the token's top-level claims and the party identified as the current actor"; prior actors "are informational only and are not to be considered in access control decisions."
- Repo [R]: m02_aauth_fcf656d/soga_supervision.py l.31 raises "delegation policy limit exceeded" when delegation_hops > max_delegation_hops. That IS an access-control input.
- Deriving delegation_hops from nested act depth would therefore make prior actors an access-control input, contrary to Section 4.1 [I].
- Keep:
  - the current actor (issuer-scoped (iss, sub)) as the only decision-relevant actor;
  - nested history as separate audit records;
  - presenter authentication (bearer versus sender-constrained) and issuer trust as separate checks.
- No new implementation proposed.

Q7. D-011 versus the PDP-approver text.
- Repo [R]: DECISION_LOG D-011 (RESOLVED 2026-08-05): "Governance is not a single function requiring an attachment point; SOGA is the PS's governance policy."
- Challenge -01 lists "policy decision point" among possible approvers [N]. That permits a deployment role. It does not authorize centralizing SOGA or adding a protocol party.
- Any OAuth path needs a stated deployment role and integration contract (which AS or RS embeds the policy) [F].
- Deb's standing direction can be real before it is recorded in the repo [D]. The advisory recap confers no build authority.

Q8. Mission source. AGREE.
- Repo [R]: input_adapters/oauth_adapter.py derives mission_id from authorization_details, governance_context or payload, and otherwise defaults to "mission-oauth-gnap-stub-001", with metadata "stub": True. That is not an approved mission.
- Owner, provenance and binding of a mission on the OAuth path need a separate contract [F].
- Keep these separate:
  - the G26 mock permission surface;
  - the pinned fcf656d AAuth profile;
  - the OAuth mock adapter;
  - the robot synthetic and physical evidence.
- Watch-only items imply no code change. G19 neutrality and the write/check split are preserved.

Q9. Reply disclosure. AGREE:
- requirement-only;
- no internal state taxonomy;
- the AI-assistance and observer posture kept;
- add the explicit IPR statement the brief requires, without legal conclusions;
- avoid claiming that standards are universally absent, or new physical-stop proof.
Wording is in (c).

(c) SUGGESTED SHORT REQUIREMENT WORDING (advisory, for Claude (chat) consolidation)

"One requirement we'd add, stated as a requirement rather than a claim that existing work lacks it: when Bob's agent acts under Bob's authority and the action also needs permission from someone affected who has not delegated to Bob, the resource side should be able to confirm, at the time of the action, that both permissions currently hold. It should have defined behaviour (such as waiting or refusing) when either is unavailable, withdrawn or stale, and leave a traceable record of what was checked. How a withdrawal affects an action that has already started is a separate question we're still examining."

Disclosure line:
"(I'm not a Kantara WG-UMA member and have not accepted Kantara IPR terms; I'm sharing this as an observer. This response was worked through with the AI agents I use in this research.)"

OPEN ITEMS
- A primary source for GNAP/UMA lineage (recording or GNAP WG history) [F].
- Who "JR" is in the Bounded Work minutes [M ambiguity].
- Whether AAuth -11's PS-authorization and federated modes cover a non-delegating affected party. Not established; do not claim it in the reply [F].
- The relationship between the pinned fcf656d commit and -11 [F].
- Affected-party identification and standing [F].
- In-flight cancellation semantics [F].
- All remaining transcript, chat and email items stay UNVERIFIED (listed in Q5).

DISAGREEMENTS PRESERVED
- With AGy: the hop-count mapping (Q6); universal single-use (C3); RFC 9767 "absorbed" wording without a citation (Q4); using the recap to dispute Section 1.2 (Q3).
- With my own originals: C1 and C2.
No consensus is declared.

Primary sources:
- https://datatracker.ietf.org/doc/minutes-127-oauth/00/
- https://www.ietf.org/archive/id/draft-liu-mcguinness-oauth-bounded-work-00.txt
- https://www.ietf.org/archive/id/draft-rosomakho-oauth-txn-challenge-01.txt
- https://www.ietf.org/archive/id/draft-hardt-oauth-aauth-protocol-11.txt (Section 11.12)
- https://www.rfc-editor.org/rfc/rfc8693 (Section 4.1)
- https://www.rfc-editor.org/rfc/rfc9767
- https://www.rfc-editor.org/rfc/rfc9635
- https://raw.githubusercontent.com/nickgamb/uma4agents/main/spec/README.md (commit 77649287)
Repo and demo files:
- input_adapters/oauth_adapter.py
- m02_aauth_fcf656d/soga_supervision.py
- knowledge/strategy/DECISION_LOG.md (D-011)
- /Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md
- /Users/debb/dev/permission-to-speak-work/permission-to-speak/FLOW_A_RUNTIME_MAPPING_2026-10-31.md


<!-- END VERBATIM CLAUDE_CODE_DISCUSSION_391_VERBATIM.txt -->


### Appendix G — AGy follow-up discussion

Original file: `AGY_DISCUSSION_392_VERBATIM.txt`; SHA-256: `71e46c93b438a2ff539430803647266782f6d280154e59b85bddd53e9641cccd`.

<!-- BEGIN VERBATIM AGY_DISCUSSION_392_VERBATIM.txt -->

# Independent Gate 2 Advisory Standards Team Review — Round 2 Discussion & Consolidation (Request 392)

- **Reviewer:** AGy (Gate 2 Independent Reviewer)
- **Timestamp:** `2026-11-23T11:44:00-05:00` (`2026-11-23T08:44:00-08:00`)
- **Loaded Repository Commit (`HEAD` in `/Users/debb/dev/soga-clean`):** `51d19d07915937160747b9177d228de1f1429e08`
- **Round 2 Input Digests Verified (`0` mismatches):**
  - `standards-review-2026-11-23/CLAUDE_CODE_INITIAL_QUEUE_389_VERBATIM.txt`: `849ea12fe00f46d2515a1c81be02c2b33a5a2dce1555366e220d39689e4325cf`
  - `standards-review-2026-11-23/AGY_INITIAL_QUEUE_390_VERBATIM.txt`: `f6561df27978d1d59c2a2864e53ef4471afbddb10c74b97ca573aa60033bedc3`
  - `standards-review-2026-11-23/CG_INDEPENDENT_REVIEW.txt`: `a37564442ec1e33184677e5d424a1f9e87872c2a551679b819cf1e9c073a69df`
  - `standards-review-2026-11-23/CG_FOLLOWUP_SOURCE_CHECKS.txt`: `7c176e5c0876efb36e244f031e97c48ba374de29d6ae305c0f763b6942fbeda2`
  - `standards-review-2026-11-23/DEB_MEETING_CONTEXT.json`: `d7672e48bfddd3609435a0b41b0b8a0954e32677a3445dcc9075876d80a6be50`
  - `standards-review-2026-11-23/DISCUSSION_QUESTIONS.txt`: `6dddc4c58efbd092f33d5cbeda5e412b37ce1941c911634c69db788359500c73`
- **Scope & Constraints Compliance:** Check-side advisory discussion only. Originals (`389`, `390`, `CG_INDEPENDENT_REVIEW.txt`) are preserved untouched. No code edits, imports, compilation, tests, builds, signing, hardware contact, commits, or external messages.

---

## (a) What AGy Retains vs. Changes/Corrects From Initial Response `390`

### Retained From `AGY_INITIAL_QUEUE_390_VERBATIM.txt` (`f6561df2...`)

1. **Dual-Authority / Non-Delegating Affected-Party Distinction (with Q2 scoping refinements below):**
   - In encounters where an operator's agent (Bob's agent) performs an action directed at or affecting another person (Alice / the parent in *Permission to Speak*), Bob's delegated mission authority and Alice's affected-party permission are distinct inputs: Alice never delegated authority to Bob, and Alice's withdrawal stops the directed action at the resource without revoking Bob's underlying mission or token (`/Users/debb/dev/permission-to-speak-work/permission-to-speak/SPEAKER_SCRIPT.md` lines 80–86, 121–126, 143–154; `/Users/debb/dev/soga-clean/m02_aauth_fcf656d/other_party_approval.py` lines 108–145).
   - Affected-party identification and standing remain an **open problem**, and our Flow A demonstration limits remain strict: the parent's QR choice is unverified (`assurance="unverified-demo-input"`), child approach/leave are simulated with no robot or camera connected, and `presentation_outcome=STOPPED` records how the presentation closed rather than proving physical hardware shutdown (`/Users/debb/dev/permission-to-speak-work/permission-to-speak/FLOW_A_RUNTIME_MAPPING_2026-10-31.md` lines 19–23; `/Users/debb/dev/soga-clean/iiw_fictional_parent/README.md` lines 7–9, 17–20).
2. **Design Leakage and Missing IPR Disclaimer in `uma-thread-brief.md`:**
   - `"allow, restrict or hold for Alice, or deny"` (`uma-thread-brief.md` lines 23, 39) leaks SOGA's internal decision/path vocabulary (`ALLOW`, `RESTRICT`, `HOLDING`, `DENY` in `/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` lines 24–27, 62–64), and line 41 of the draft reply omits the explicit statement that Deb has not accepted Kantara IPR terms required by line 28 of the brief.
3. **`D-011` Engine-vs-Protocol-Party Architectural Rule:**
   - Under `D-011` (`/Users/debb/dev/soga-clean/knowledge/strategy/DECISION_LOG.md` lines 89–92) and `/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` (lines 16–17), SOGA is an internal governance policy engine invoked within a deployment role (such as a Person Server, Authorization Server, or Resource enforcement point), not a standalone protocol party.
4. **Separation of Existing Repo Layers at `51d19d07915937160747b9177d228de1f1429e08`:**
   - `input_adapters/oauth_adapter.py` and `input_adapters/ucan_adapter.py` are passive, static, non-cryptographic mocked transformers (`stub: True`); `aauth_permission/service.py` is an in-memory G26 mock PS permission surface; `m02_person_server/` is a loopback-only (`127.0.0.1`) SQLite/HS256 test harness; `m02_aauth_fcf656d/` is a pinned-commit (`fcf656de1926535f5bd6fc0538147ead6646e727`) localhost profile; and `robot_gateway/` packages are local loopback/serial controllers that do not parse OAuth or AAuth tokens.

### Changed / Corrected From `AGY_INITIAL_QUEUE_390_VERBATIM.txt`

1. **Correction 1 — `draft-rosomakho-oauth-txn-challenge-01` Section 1.2 vs. Cross-Domain Routing (Q3):**
   - *Earlier statement in `390` Part I:* Used the cross-domain chat remark in `ietf127-recap.md` line 13 to argue that `uma-thread-brief.md` line 22 overstated Section 1.2.
   - *Correction:* Section 1.2 of `draft-rosomakho-oauth-txn-challenge-01` (`https://www.ietf.org/archive/id/draft-rosomakho-oauth-txn-challenge-01.html#section-1.2`, *"Authorization by a Different Resource Owner"*) **does** explicitly cover approval by a resource owner different from the initiating user (selected according to AS policy). Arbitrary cross-domain discovery/routing back to an unassociated home AS is a **distinct question**, not a contradiction or refutation of Section 1.2.
2. **Correction 2 — Conditional Single-Use in `draft-rosomakho-oauth-txn-challenge-01` Section 6.2 (Q3):**
   - *Earlier statement in `390` Part II:* Referred to the challenge draft's output as `"a single-use transaction-bound access token"` without qualification.
   - *Correction:* Per `draft-rosomakho-oauth-txn-challenge-01` Section 6.2 (and independently noted by Claude Code `389` Part A line 29 / Part B3 and CG `CG_INDEPENDENT_REVIEW.txt` line 6), single-use enforcement is **conditional** (*"if the protected resource requires single use for the challenged operation"*, recommended via `SHOULD` for high-impact or non-idempotent operations with resource-side replay state), not an unconditional `MUST` for all challenged operations.
3. **Correction 3 — `RFC 9635` / `RFC 9767` Functional Scope vs. Deb's Firsthand Report of Justin Richer's UMA Remark (Q4 & Q5):**
   - *Earlier statement in `390` Part II:* Stated that `RFC 9767` *"specifically absorbed UMA 2.0's resource registration, RS-to-AS introspection, and asynchronous resource-owner authorization patterns"* as if the RFC text itself stated that historical lineage.
   - *Correction:* As CG verified (`CG_FOLLOWUP_SOURCE_CHECKS.txt` line 4), `RFC 9767` (`https://www.rfc-editor.org/rfc/rfc9767.html`, Sections 1, 3, 4) defines RS-to-AS discovery, token introspection, resource registration, and downstream token derivation—providing **functional overlap** with UMA 2.0—but neither `RFC 9635` nor `RFC 9767` contains the word `"UMA"`. Conversely, Deb's firsthand witness report in `DEB_MEETING_CONTEXT.json` (`"cg Justin said he stole the uma code in the ietf meeting"`) and the official IETF 127 OAuth minutes (`https://datatracker.ietf.org/doc/minutes-127-oauth/00/`, noting Justin Richer discussing useful pieces of UMA during the Rosenberg presentation) provide direct meeting-history context. We therefore separate **functional comparison** (supported by `RFC 9635` and `RFC 9767`) from **historical design lineage** (attributed to Deb's firsthand report of Justin Richer's remark and the IETF 127 minutes, while leaving verbatim audio/transcript verification of `"stole the uma code"` open).
4. **Correction 4 — Nested `act` History Must NOT Feed `delegation_hops` in `m02_aauth_fcf656d/soga_supervision.py` (Q6):**
   - *Earlier statement in `390` Part II (Item 3.2):* Suggested mapping nested `act` claims into `AuthorityEvidence.references` / `raw_evidence` *"and `delegation_hops` for provenance/hop-count auditing"*.
   - *Correction:* In `/Users/debb/dev/soga-clean/m02_aauth_fcf656d/soga_supervision.py` (lines 31–32 and 111–112), `delegation_hops > max_delegation_hops` raises `SupervisionAdapterError("delegation policy limit exceeded")` and causes `SogaSupervisor.__call__` to return `SupervisionDecision("DENY", "soga-fail-closed", "soga-error")`. Thus `delegation_hops` in `soga_supervision.py` is an **active access-control deny input**, not a passive audit field. Feeding nested historical `act` claims into `delegation_hops` would violate `RFC 8693` Section 4.1 (`https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1`). Nested `act` history must remain in separate audit-only provenance fields unless an explicitly specified profile defines authorized hop-count control semantics.
5. **Correction 5 — Narrowing `UNVERIFIED` Where Official IETF 127 Minutes (`minutes-127-oauth-00`) or Published Drafts Verify Items (Q5):**
   - *Earlier statement in `390` Part II:* Marked `draft-liu-oauth-cross-domain-txn-token-00` Mode B and all meeting remarks blanket `UNVERIFIED` from local files.
   - *Correction:* `draft-liu-oauth-cross-domain-txn-token-00` Section 3.2 ("Mode B") is verifiable on IETF Datatracker (`https://datatracker.ietf.org/doc/draft-liu-oauth-cross-domain-txn-token/`), and `https://datatracker.ietf.org/doc/minutes-127-oauth/00/` provides official draft minutes corroborating the substance/paraphrase of several session discussions (while exact verbatim chat/spoken quotes not appearing in `minutes-127-oauth-00` remain distinguished from minutes summaries).

---

## (b) Point-by-Point Responses to the Nine Discussion Questions (`DISCUSSION_QUESTIONS.txt`)

### Q1. Separating New Request Authorization/Revocation, Current Affected-Party Policy, and Cancellation of Accepted In-Flight Execution (`Bounded Work -00`)

- **Position: Agree with the three-way separation and with rejecting any replacement "no-spec-defines-one-decision-point" novelty claim.**
- **Primary Support:**
  1. **Normative `Bounded Work -00` limitation and acceptance-window language (`https://www.ietf.org/archive/id/draft-liu-mcguinness-oauth-bounded-work-00.txt`):**
     - `draft-liu-mcguinness-oauth-bounded-work-00` explicitly distinguishes revoking/ending a governing authorization for *further* access from cancelling *already accepted in-flight execution*:
       > *"Ending a governing authorization does not by itself undo completed effects or cancel execution that another system has already accepted. A realization that governs such execution identifies the additional checkpoints and cancellation behavior it provides."* (quoted in `389` Part B2, line 117).
     - It also defines an **acceptance window**: when a governing authorization ends, tokens checked via dynamic introspection report inactive immediately, whereas non-introspected tokens remain usable within their remaining token lifetime (the acceptance window) up to the governing authorization's maximum lifetime.
  2. **Why the three concepts must stay separate:**
     - **(i) Revoking or denying future token/request issuance** is already covered by `RFC 7009` (Token Revocation), `RFC 7662` (Token Introspection), `RFC 9635` Sections 5.3/5.4, `draft-hardt-oauth-aauth-protocol-11` Section 11.12 (`AAUTH_FINDINGS_2026-08-05.md` lines 20–24), and `draft-liu-mcguinness-oauth-bounded-work-00`.
     - **(ii) Evaluating current policy (including an affected party's current permission or withdrawal) at an enforcement point before an action proceeds** is a checkpoint requirement at the moment of action (`m02_aauth_fcf656d/other_party_approval.py` lines 108–145; `m02_aauth_fcf656d/approval_pending.py` lines 107–144).
     - **(iii) Cancelling or halting an already-accepted, in-flight physical or external execution** is realization-specific runtime/hardware control (and as our own `robot_gateway/CYBERPI_NONE_OBSERVATION_V3.md` lines 244–247 and `FLOW_A_RUNTIME_MAPPING_2026-10-31.md` lines 19–23 state, an authorization refusal or presentation `STOPPED` state does not by itself prove physical hardware stop).
  3. **Avoiding an unproven replacement novelty claim:**
     - I agree with `DISCUSSION_QUESTIONS.txt` line 5 and `CG_INDEPENDENT_REVIEW.txt` lines 27–28: we should **not** replace `ietf127-recap.md`'s overly broad *"no spec can hold, pause, or revoke authority while a task is running"* with an equally categorical *"no spec defines one decision point at the moment of action with a hold outcome"* (`389` line 70). Instead, we should state our functional requirement directly and ask how candidate protocol compositions meet it.

### Q2. Third-Party Standing & Dual Permissions vs. "On Alice's Behalf" (`389` B6 vs. `390` Part I)

- **Position: Agree with `DISCUSSION_QUESTIONS.txt` line 6 — critique `389` Part B6's phrasing `"when an agent is about to act, or is already acting, on Alice's behalf"` and adopt `"Bob's agent acts under Bob's authority, with separate affected-party (Alice) permission where applicable"`.**
- **Primary Support & Reasoning:**
  1. **Why `"on Alice's behalf"` (`389` line 133) erases the non-delegating affected-party distinction:**
     - In `CLAUDE_CODE_INITIAL_QUEUE_389_VERBATIM.txt` line 133 (Part B6), Claude Code proposed: *"when an agent is about to act, or is already acting, on Alice's behalf..."*
     - In both Adrian Gropper's 10 assumptions (`uma-thread-brief.md` line 14: *"Alice and Bob each have an agent they control... Bob's agent asks Alice's agent"*) and our IIW *Permission to Speak* scenario (`SPEAKER_SCRIPT.md` lines 80–86, 152–154), **Bob's agent is NOT acting on Alice's behalf**—Bob's agent is acting on **Bob's** behalf under Bob's authority, and wants to perform an action that affects or addresses Alice (or Alice's resource/child), where Alice never delegated anything to Bob. Saying `"acting on Alice's behalf"` collapses the two-party encounter back into single-principal delegation.
  2. **Scoping the dual-permission requirement accurately (not all actions, and not all affected parties are UMA "resource owners"):**
     - Not every action requires two independent human approvals: in our own code (`m02_aauth_fcf656d/other_party_approval.py` lines 13–14, 178–187), ambient actions (`AMBIENT_SCOPE = "misty.acknowledge_tip"`) proceed under Bob's operator authority alone without consulting `OtherPartyApprovalPolicy`, whereas only directed actions (`DIRECTED_SCOPE = "misty.address_participant"`) require the affected party's separate permission.
     - Nor is an affected party in a physical space (such as a parent at a farmers market) naturally modeled as an OAuth/UMA "Resource Owner" who pre-registered a digital resource at an AS (`SPEAKER_SCRIPT.md` lines 146–154, 170–174).
     - How to identify the affected party and verify their standing remains an **open research/standards question**, and our demo boundaries remain explicit (`assurance="unverified-demo-input"`, no robot/camera connected, `presentation_outcome=STOPPED` is UI presentation closure, not physical hardware shutdown).

### Q3. `draft-rosomakho-oauth-txn-challenge-01` Section 1.2, Conditional Single-Use (Section 6.2), and Expressible vs. Unidentified Deployments

- **Position: Agree — reconcile `390` with `draft-rosomakho-oauth-txn-challenge-01` Sections 1.2 and 6.2, and frame cross-domain discovery/standing as open questions rather than contradictions.**
- **Primary Support:**
  1. **Normative coverage of Section 1.2 (`https://www.ietf.org/archive/id/draft-rosomakho-oauth-txn-challenge-01.html#section-1.2`):**
     - Section 1.2 (*"Authorization by a Different Resource Owner"*) explicitly states that the user who must approve a challenged operation may be different from the party initiating the request, with the approving party determined *"according to authorization server policy."*
  2. **Conditional single-use in Section 6.2 (`https://www.ietf.org/archive/id/draft-rosomakho-oauth-txn-challenge-01.html#section-6.2`):**
     - Section 6.2 specifies that the protected resource validates that the token matches the challenged transaction (`txn`) and enforces single use **conditionally** (*"if the protected resource requires single use for the challenged operation"*, with `SHOULD` for high-impact or non-idempotent operations and resource-side state for replay detection).
  3. **What existing protocol composition CAN express vs. what remains genuinely open:**
     - **Expressible today within a pre-configured trust domain:** When the Protected Resource and the approving Authorization Server share an established trust relationship and the AS already knows who the approving resource owner (Alice) is under AS policy, `draft-rosomakho-oauth-txn-challenge-01` + `draft-ietf-oauth-deferred-token-response` can pause token issuance until Alice (or an AS-designated PDP) approves that specific transaction.
     - **Genuinely open / unidentified across domains or in ad-hoc encounters (framed as questions):**
       1. When Alice is in a separate trust domain unknown in advance to the resource's AS, how does the challenge discover and route to Alice's own home AS or agent (the cross-domain challenge routing question noted in `ietf127-recap.md` line 13), and how does `draft-fletcher-oauth-txn-token-chaining-profile-01` (`Txn-Token-JAG`) compose with a backward-flowing challenge?
       2. When Alice has no pre-registered account at the resource's AS (as in an ad-hoc physical encounter), what establishes her standing to approve or withdraw?
       3. After a transaction-challenged token is issued (or if an operation is long-running/multi-step), how does Alice's subsequent withdrawal take effect at the resource enforcement point before or during action execution without revoking Bob's broader mission?

### Q4. GNAP/UMA Lineage: Reconciling `RFC 9635` / `RFC 9767` Text With Deb's Firsthand Report (`DEB_MEETING_CONTEXT.json`)

- **Position: Agree — preserve Deb's firsthand witness report from IETF 127 (`DEB_MEETING_CONTEXT.json`) alongside the exact textual check of `RFC 9635` and `RFC 9767`.**
- **Primary Support & Reconciliation:**
  1. **What the RFC text shows (normative/functional level):**
     - `RFC 9635` (*GNAP Core*, Richer, Ed., Imbault, Oct 2024, `https://www.rfc-editor.org/rfc/rfc9635.html`) and `RFC 9767` (*GNAP Resource Server Connections*, `https://www.rfc-editor.org/rfc/rfc9767.html`, Sections 1, 3, 4) define asynchronous interaction/grant continuation, resource registration by a Resource Server at an AS, token introspection, and downstream token derivation.
     - Neither `RFC 9635` nor `RFC 9767` contains the word `"UMA"`, so the RFC text alone proves **functional overlap** with UMA 2.0 rather than historical lineage.
  2. **What Deb's firsthand meeting evidence and the IETF 127 minutes show (historical/lineage level):**
     - `DEB_MEETING_CONTEXT.json` records Deb's firsthand report from IETF 127: `"cg Justin said he stole the uma code in the ietf meeting"`.
     - As noted in `DISCUSSION_QUESTIONS.txt` line 9, the official IETF 127 OAuth draft minutes (`https://datatracker.ietf.org/doc/minutes-127-oauth/00/`) also record Justin Richer discussing useful pieces of UMA during Jonathan Rosenberg's presentation.
     - Absence of the informal phrase `"stole the uma code"` from the scribe's summary minutes does **not** disprove Deb's firsthand recollection (summary minutes compress spoken mic remarks).
  3. **How to state this cleanly:**
     - In our internal team records: attribute the historical remark to Justin Richer as witnessed firsthand by Deb at IETF 127 (`DEB_MEETING_CONTEXT.json`), corroborated in topic by the `minutes-127-oauth-00` summary of Justin's UMA comments, while keeping exact transcript/audio wording open.
     - In the external WG-UMA reply: use accurate functional phrasing (e.g., *"GNAP (RFC 9635 and RFC 9767) carries forward many of the same resource-registration and asynchronous-grant patterns"*), which is 100% defensible from the RFC text and aligns with Justin Richer's spoken history without requiring the external email to litigate RFC genealogy.

### Q5. Primary IETF 127 Minutes (`minutes-127-oauth-00`), Draft Status / Charter Targets vs. Realized Outcomes, and U4A Classification

- **Position: Agree — distinguish (i) what `minutes-127-oauth-00` and Datatracker verify, (ii) what is paraphrased vs. exact quote, (iii) charter targets vs. realized outcomes, and (iv) U4A's exact repo classification.**
- **Primary Support:**
  1. **Official IETF 127 OAuth Minutes (`https://datatracker.ietf.org/doc/minutes-127-oauth/00/`):**
     - **Verified in summary minutes:** Justin Richer's remarks on useful pieces of UMA during the `draft-rosenberg-oauth-aauth` presentation, and Justin Richer's concern during `draft-liu-mcguinness-oauth-bounded-work` that pre-computing/narrowing authority attenuation ahead of time may be incomputable in the general case.
     - **Paraphrase vs. exact quote:** The minutes verify the *substance* of Richer's incomputability concern and UMA remarks; verbatim quotation marks should be used only where matching the published minutes text, or else cited as paraphrase/firsthand meeting recollection.
     - **Still unverified from public minutes alone:** Private/side OAuth Zulip chat lines not copied into `minutes-127-oauth-00` and the raw Nov 23 WG-UMA email thread paste (`uma-thread-brief.md` lines 14–17).
  2. **Published drafts & charter targets vs. realized outcomes:**
     - `draft-liu-oauth-cross-domain-txn-token-00` (Chunchi Peter Liu, Yuan Ni, Huawei) is a published individual Internet-Draft on Datatracker (`https://datatracker.ietf.org/doc/draft-liu-oauth-cross-domain-txn-token/`), and Section 3.2 defines "Mode B" (cross-domain token issuance using pre-established trust between Domain I AS and Domain II token service, as verified in `389` lines 42, 108).
     - OAuth 2.1 and Transaction Tokens (`draft-ietf-oauth-transaction-tokens`) having `Dec 2026` IESG submission dates on `https://datatracker.ietf.org/wg/oauth/about/` are **WG charter milestones (targets)**, not guaranteed realized outcomes (`389` line 48).
     - HTTP WG (`httpbis`) agenda (`https://datatracker.ietf.org/meeting/127/materials/agenda-127-httpbis`) confirms the Friday Nov 20 slot *"HTTP Signature-Key Header – call for adoption discussion"*; any formal adoption call result remains pending mailing-list confirmation (`ietf127-recap.md` line 39; `389` line 24).
  3. **U4A Credential vs. Binding and Attribution (`https://github.com/nickgamb/uma4agents/tree/main/spec`):**
     - Agree with Claude Code `389` (Part A lines 44–47): the `nickgamb/uma4agents` repository lists nine Internet-Draft-formatted specs in which `draft-gamb-uma4agents-aauth-00` is categorized under **Credential** (alongside `aa-agent+jwt` / agent identity regimes), while MCP is categorized under **Binding**; and the GitHub repo itself uses the `gamb` author prefix without an explicit Kantara WG publication header in the README.

### Q6. Actor Evidence (`RFC 8693` Section 4.1 & `draft-mcguinness-oauth-actor-profile-01`) and Preventing Nested `act` History From Driving `delegation_hops` Denials in `soga_supervision.py`

- **Position: Agree completely with `CG_FOLLOWUP_SOURCE_CHECKS.txt` line 8 and `DISCUSSION_QUESTIONS.txt` line 10 — this is a critical code-level correction to `390` Part II Item 3.2.**
- **Primary Support:**
  1. **Normative `RFC 8693` Section 4.1 (`https://www.rfc-editor.org/rfc/rfc8693.html#section-4.1`) & `draft-mcguinness-oauth-actor-profile-01` (`https://www.ietf.org/archive/id/draft-mcguinness-oauth-actor-profile-01.html` Sections 8.1, 8.2):**
     - Only the top-level claims and the immediate/current actor (`iss`-scoped `(iss, sub)` in the outermost `act` claim) may be considered for access control; nested `act` objects record prior delegation history for **informational/audit purposes only** and **MUST NOT** be used in access-control decisions.
     - Furthermore, an `act` claim in a bearer token does not by itself prove that the current HTTP presenter is that actor; presenter authentication requires sender-constraint / proof-of-possession verification (e.g., `cnf.jwk` / HTTP Message Signatures as in `/Users/debb/dev/soga-clean/m02_aauth_fcf656d/tokens.py` lines 54–64, 145), and trusting the `act` claim depends on trusting the issuing AS.
  2. **Why `m02_aauth_fcf656d/soga_supervision.py` must NOT derive `delegation_hops` from nested `act` chain length:**
     - Static inspection of `/Users/debb/dev/soga-clean/m02_aauth_fcf656d/soga_supervision.py` lines 31–32 (`if value["delegation_hops"] > value["max_delegation_hops"]: raise SupervisionAdapterError("delegation policy limit exceeded")`) and lines 110–112 shows that `delegation_hops` directly triggers a fail-closed **`DENY`** decision (`SupervisionDecision("DENY", "soga-fail-closed", "soga-error")`).
     - Therefore, if a future adapter counted nested `act` claims into `verified_authority_state["delegation_hops"]`, informational audit history would silently become an access-control deny trigger, violating `RFC 8693` Section 4.1. Nested `act` history must be stored strictly in non-control provenance/audit fields (no code change proposed now).

### Q7. `D-011` Engine Policy vs. Protocol Party, Deployment Role Contract, and Standing Direction Authority

- **Position: Agree.**
- **Primary Support & Distinction:**
  1. **Standards flexibility vs. SOGA architectural commitment (`D-011`):**
     - While `draft-rosomakho-oauth-txn-challenge-01` Section 1 allows an Authorization Server to consult a policy decision point or organizational authority as the approving party (`389` line 31; `CG_INDEPENDENT_REVIEW.txt` line 6), our repository's `D-011` (`/Users/debb/dev/soga-clean/knowledge/strategy/DECISION_LOG.md` lines 89–92), `/Users/debb/dev/soga-clean/knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md` (lines 16–17), and `/Users/debb/dev/soga-clean/knowledge/research/AAUTH_FINDINGS_2026-08-05.md` (lines 17–19, 44–46) establish that SOGA is an **internal governance policy engine** (like the internal class `GovernancePDP` in `/Users/debb/dev/soga-clean/verify/governance_pdp.py`) embedded inside a server role (PS, AS, or Resource enforcement point), **not** an independent centralized protocol party on the wire.
     - Any future OAuth challenge adapter must therefore specify *which deployment role* (AS approval hook, PS, or resource-side enforcement boundary) invokes the SOGA engine and under whose authority.
  2. **Deb's standing direction vs. repo synchronization contract vs. build authority:**
     - Agree with `CG_FOLLOWUP_SOURCE_CHECKS.txt` line 6: a direction decided by Deb this week (`ietf127-recap.md` Section 2: AAuth first, OAuth second; G19 ecosystem neutrality; U4A watch-only) is a real PI policy direction even before it is committed to `/Users/debb/dev/soga-clean/knowledge/working/CURRENT_STATE.md` or `/Users/debb/dev/soga-clean/knowledge/strategy/DECISION_LOG.md`.
     - At the same time, as `ietf127-recap.md` lines 3–4 itself notes (*"Advisory only... Nothing below is approved build work"*), an advisory recap document in `~/Downloads/` is not an adopted repository commit or build authorization.

### Q8. Mission Source on the OAuth Path & Strict Separation of Repo Layers

- **Position: Agree across all three reviews (`389`, `390`, `CG`).**
- **Primary Support in `/Users/debb/dev/soga-clean` (`51d19d07915937160747b9177d228de1f1429e08`):**
  1. **Current OAuth adapter defaults are NOT an approved mission:**
     - `/Users/debb/dev/soga-clean/input_adapters/oauth_adapter.py` (lines 61–120) falls back to synthetic placeholder defaults (`"step1"`, `"subject-oauth-unknown"`, `"mission-oauth-gnap-stub-001"`, `"Representative OAuth/GNAP delegated mission"`, `metadata={"stub": True}`). Those fallback defaults must never be treated as an authenticated or human-approved mission.
     - Because OAuth 2.1 and `draft-rosomakho-oauth-txn-challenge-01` do not define an immutable `s256`-bound mission object like AAuth's `Mission` (`/Users/debb/dev/soga-clean/aauth_permission/models.py` lines 27–68), any future OAuth path must explicitly specify **where the mission comes from, who approved it, and how its provenance/digest is bound** to the transaction or grant before SOGA evaluates it.
  2. **Five distinct repo layers must never be conflated:**
     - **(i) G26 Permission Surface (`aauth_permission/service.py`):** Mock in-memory AAuth PS permission endpoint (`HOLDING` via `202` deferred response), no HTTP signature or JWS verification.
     - **(ii) M02 Pinned AAuth Profile (`m02_aauth_fcf656d/`, `profile.py`):** Bounded localhost Ed25519 + HTTP Message Signatures profile pinned to AAuth commit `fcf656de1926535f5bd6fc0538147ead6646e727` (create-only/paused under `D-102` in `CURRENT_STATE.md` lines 79–85, with additive localhost demo extensions in `approval_pending.py`, `other_party_approval.py`, and `demo_operator.py` — not a claim of full `draft-hardt-oauth-aauth-protocol-11` conformance).
     - **(iii) Passive Input Adapters (`input_adapters/oauth_adapter.py`, `ucan_adapter.py`, `aauth_adapter.py`, `zcap_adapter.py`, `aiim_adapter.py`):** Offline dict normalizers into `RuntimeEnvelope` (`verify/runtime_envelope_model.py`) with no cryptographic verification.
     - **(iv) Public IIW Flow A Demo (`/Users/debb/dev/permission-to-speak-work/permission-to-speak/`, `iiw_fictional_parent/`, `iiw_qr_session/`):** Robot-free localhost presentation with unverified fictional-parent QR input.
     - **(v) Robot Gateway (`robot_gateway/`):** Local loopback/serial hardware controllers (`misty_stop_probe.py`, `cyberpi_none_observation_v3.py`, `switching.py`, `operator_runtime.py`) where synthetic tests have run under gated requests and physical mBot2/Misty work remains separately gated.
  3. **Neutrality (`G19`) and write/check split preserved:** Watch-only items (U4A, UCAN, Rosenberg `aauth`, Client Instance IDs) require zero code changes.

### Q9. Reply Disclosure, IPR Boundary, Traceable Evidence, and Unavailable/Stale Authority Requirements

- **Position: Agree — keep the reply short, requirement-only, free of internal SOGA state names, explicit on AI-assisted team view + non-member / non-acceptance of Kantara IPR terms (without making legal claims), and clear on traceable evidence plus fail-closed handling when current authority is unavailable or stale.**
- **Primary Support:**
  - Boundary Rules 1–3 in `/Users/debb/Downloads/uma-thread-brief.md` (lines 27–29).
  - Traceable decision evidence and explicit handling of `unavailable` / expired / withdrawn authority facts in `/Users/debb/dev/soga-clean/m02_aauth_fcf656d/soga_supervision.py` (lines 21, 39–46: `unavailable` authority facts tracked explicitly in `validated_authority_state`) and `/Users/debb/dev/soga-clean/m02_aauth_fcf656d/other_party_approval.py` (lines 70–92, 115–131: `OtherPartyDecisionReceipt` distinguishing `approval_absent`, `approval_expired`, `approval_withdrawn`, and `approval_assurance`).

---

## (c) Suggested Brief Final Requirement-Only Wording for the WG-UMA Reply & Open Items

### Suggested Brief WG-UMA Reply (Requirement-Only, Incorporates Round 2 Consolidation)

> Adrian, Eve, Alan, Harvey, all,
>
> This is a team response from Deb B Labs: my own view, worked through with the AI agents I run on this research. (I am not a WG-UMA participant or Kantara member and have not accepted Kantara IPR terms; sharing this solely as an outside observer.)
>
> We think UMA's separation of roles—where Bob's agent requests, Alice's policy governs her side, and the resource server is accountable for enforcement and logs—is a useful way to describe affected-party permission, alongside Bob's own delegated authority over his agent. Where an action affects another party, both permissions may need to hold at the same time even if Alice never delegated anything to Bob and never pre-registered with the resource's authorization server.
>
> We're not sure UMA 2.0 itself needs to be extended to deliver this. GNAP (RFC 9635 and RFC 9767) carries forward similar resource-registration and asynchronous-grant patterns, and newer IETF OAuth work—such as the Transaction Authorization Challenge draft (`draft-rosomakho-oauth-txn-challenge-01`, Section 1.2) and Bounded Work (`draft-liu-mcguinness-oauth-bounded-work-00`) discussed at IETF 127—addresses different-owner transaction approval within an authorization server's domain and ending a governing authorization for future requests.
>
> Building on Alan's point about checking revocation at the resource when a request arrives, and Harvey's point on traceability, the requirements we'd emphasize at the moment a consequential action is about to happen are:
> 1. Authorization—including any required permission from an affected party (Alice)—must remain currently applicable when the action is performed, with a defined way to pause and wait if Alice's answer is needed and not yet in hand, or to refuse when current authority is stale, withdrawn, or cannot be established.
> 2. If Alice withdraws her permission, that withdrawal must take effect at the enforcement point without having to revoke Bob's broader authority over his agent—recognizing that refusing new actions and stopping work already in flight are distinct problems.
> 3. The enforcement point should record attributable evidence of which authorities were checked, their assurance level, and why the action proceeded or stopped.
>
> Open questions we see across current drafts are how a challenge discovers and routes to Alice's side across trust domains when she isn't pre-registered with the resource's authorization server, and how her standing is established in the first place.
>
> Debbie

### Summary of Open Items for Deb / Team Consolidation

1. **Deb's Editorial Choice on Reply Scope:** Whether to include the brief two-authority / non-delegating affected-party sentence (from *Permission to Speak*) or keep the reply focused strictly on single-resource-owner action-time applicability and withdrawal.
2. **GNAP/UMA Attribution in Internal Notes:** Keep `RFC 9635` / `RFC 9767` cited for *functional* overlap, and attribute the *historical* remark about reusing UMA design/code to Justin Richer as witnessed firsthand by Deb at IETF 127 (`DEB_MEETING_CONTEXT.json`) and supported in topic by `minutes-127-oauth-00`.
3. **Future Research Questions (Not Approved Build Work):**
   - If Deb later authorizes design work on an OAuth Transaction Challenge path: (i) which deployment role (AS, PS, or resource enforcement boundary) invokes the SOGA policy engine under `D-011`, and (ii) what authenticated artifact supplies the immutable mission and its provenance on the OAuth path.
   - How cross-domain challenge routing (`draft-rosomakho-oauth-txn-challenge-01` + `draft-fletcher-oauth-txn-token-chaining-profile-01`) and affected-party standing can be established when the affected party is not pre-registered at the resource's AS.
   - Maintaining the strict `RFC 8693` Section 4.1 barrier so nested `act` delegation history is recorded for audit provenance only and never fed into `soga_supervision.py`'s `delegation_hops` access-control deny check.


<!-- END VERBATIM AGY_DISCUSSION_392_VERBATIM.txt -->


### Appendix H — Deb firsthand meeting context

Original file: `DEB_MEETING_CONTEXT.json`; SHA-256: `d7672e48bfddd3609435a0b41b0b8a0954e32677a3445dcc9075876d80a6be50`.

<!-- BEGIN VERBATIM DEB_MEETING_CONTEXT.json -->

{
  "source": "Deb firsthand report in current chat, Nov23 2026",
  "verbatim": "cg Justin said he stole the uma code in the ietf meeting",
  "status": "reported meeting remark; recording/transcript and exact referent not yet independently verified",
  "relevance": "Potential direct support for UMA/GNAP lineage; do not dismiss as unsupported merely because RFC lacks historical wording. Distinguish functional standards requirements from speaker history, and do not infer which code/design/mechanisms without context.",
  "request_for_reviewers": "Reconcile GNAP absorbed UMA history comments with this report; locate primary meeting record if available, otherwise attribute to Debs report and keep exact transcript verification open."
}


<!-- END VERBATIM DEB_MEETING_CONTEXT.json -->
