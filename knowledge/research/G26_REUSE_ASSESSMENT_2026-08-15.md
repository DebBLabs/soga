# G26 Bounded Reuse Assessment — Publicly Available Components and Artifacts

Date: 2026-08-15
Checkpoint: main @ a9e5d9d4c3962a26c4b36b831c32f55d4aa903ab (verified via
`git rev-parse HEAD`). At canonicalization review, `git status --short` listed
this file as untracked and no other change. **No implementation performed. No
SOGA architecture or G26 scope change proposed.** This is a bounded survey of
the named and locally available candidates examined, not an exhaustive survey
of the available ecosystem. It may inform a future, separately authorized
decision.

This artifact is research input to Gate 1a — Implementation Lineage and Current
Architecture. It is not itself a Stage Gate finding or authorization.

Scope requested: assess existing open-source components that could replace
G26's mocked Person Server, identity/authority, approval-evidence, or AAuth
infrastructure — prioritizing Dmitri Zagidulin's wallet work, current DIF
Trusted AI Agents WG / KYA-OS work, and Dick Hardt's current AAuth/Person
Server implementations.

G26's current mock surface (for reference, all in this repo):
`aauth_permission/service.py` (in-memory `PermissionService`, `MissionLog`),
`aauth_permission/models.py` (`Mission`, `ProvisionalG26ApprovalEvidence`),
`aauth_permission/http_server.py` (`http.server`-based wire layer, no real
HTTP Message Signature verification, HTTP/1.0). Governance decisions
themselves (`RuntimeGovernanceEngine`, `RestrictModeSelector`,
`restrict_policy.py`) were outside the requested replacement assessment.

This assessment intentionally does not determine which functions remain
uniquely SOGA, irreplaceable, or “ours.” Exclusion of governance functions from
candidate replacement analysis is a scope boundary, not evidence of
irreplaceability. Those conclusions belong to the later Gate 1b
functional-subtraction review, where implemented versus designed status must
be established.

Claim labels used below follow RM-02:

- **Verified fact** — established from inspected source, repository history,
  executable behavior, or canonical repository evidence.
- **Source-reported claim** — stated by the candidate source but not
  independently executed during this assessment.
- **Functional comparison** — comparison between inspected candidate behavior
  and a G26 mock boundary; it is not a finding of substitutability.
- **Inference** — likely integration consequence that was not implemented or
  validated here.
- **Recommendation** — possible follow-up for separate review and
  authorization; it does not change architecture.

---

## Candidate 1 — `aauth-person-server` (Christian Posta repository; AAuth ecosystem)

- **Repository**: `https://github.com/christian-posta/aauth-person-server`
  (already cloned locally at `external-repos/aauth-person-server`, remote
  `origin`, last local commit 2026-05-20 "added mission / permissions
  tests/demo").
- **Verified licensing finding**: **No license found in the inspected
  checkout.** No `LICENSE` file in the repo tree; no `license` field in
  `pyproject.toml`. This assessment did not establish reuse or redistribution
  rights.
- **Verified implemented capability** (read directly from source, not the
  README's claims alone):
  - A real Person Server HTTP app (`ps/http/app.py`) plus an Agent Server
    and a unified portal, with persistence via SQLAlchemy/Alembic
    (`persistence/`, `alembic/`, `DATABASE.md`) — not in-memory only.
  - Real HTTP Message Signature handling: `ps/service/signing.py`,
    `ps/service/http_sig_auth.py` (and agent-side equivalents), referencing
    `draft-hardt-httpbis-signature-key-04` (`SIG-KEY.md`). G26's mock has no
    signature verification at all — the permission request body is trusted
    JSON.
  - Mission storage and mission log (`ps/impl/mission_state.py`,
    `ps/impl/mission_guards.py`, `MissionLogKind` enum in `ps/models.py`).
  - A permission-endpoint implementation (`ps/impl/ps_governance.py`,
    `PsGovernance.post_permission`), read in full: if the action is in the
    mission's `approved_tools`, it grants and logs; otherwise it creates a
    pending record and sets `requirement=INTERACTION` — i.e., it always
    escalates to a **user-directed** interaction, never to an
    **administrative** `requirement=APPROVAL` deferral. `RequirementLevel.APPROVAL`
    exists in the enum (`ps/models.py:42`) but is not exercised by
    `post_permission` anywhere in the file. For the RM-01 absence check, the
    permission implementation was searched using its vocabulary and the G26
    comparison terms `approval`, `evidence`, `constraint`, `restrict`,
    `holding`, and `supervised`; no RESTRICT-mode, policy-selected
    HOLDING/SUPERVISED distinction, or evidence-satisfies-constraint mechanism
    was found in that implementation. The observed decision mechanism is the
    `approved_tools` membership check.
  - A consent UI (`portal/ui/consent.html`) and well-known metadata
    endpoints (`.well-known/aauth-person.json`, `jwks.json`).
- **Interface**: HTTP, matching the draft's `/permission`, `/audit`,
  `/interaction`, `/pending/{id}` shape; Python package installable via
  `pip install -e`.
- **Functional comparison to the G26 mock boundary**: the inspected component
  has functionality corresponding to the **transport, persistence,
  mission-storage, and signing** concerns currently mocked by
  `aauth_permission/http_server.py` and the in-memory stores in
  `aauth_permission/service.py`. No drop-in or complete replacement was
  established. Its inspected governance behavior is not functionally
  equivalent to G26's `RuntimeGovernanceEngine` path.
- **Inferred integration work**:
  1. Licensing terms would need to be established before reuse or
     redistribution is assumed. Contacting an author is one possible way to
     investigate this, not a required action established by this assessment.
  2. `PsGovernance.post_permission` would likely need non-trivial changes to (a)
     call SOGA's governance bridge instead of the `approved_tools` check,
     and (b) add the `requirement=APPROVAL` deferred path that G26's
     caregiver flow (commit `ab2dbba5`) already implements and this repo
     does not.
  3. Signature verification would add a mechanism the G26 mock does not
     contain, but it is new integration surface — the
     agent side must actually sign requests, which neither G26 nor this
     repo's demo currently connects to a live agent doing so end-to-end.
  4. Moving from an `http.server` mock to a SQLAlchemy-backed FastAPI/portal
     app would add dependencies, migrations, and deployment concerns. This
     assessment did not evaluate whether that cost is proportionate to a
     future objective.

## Candidate 2 — `aauth-dev/packages-js` (AAuth ecosystem, agent/client side)

- **Repository**: `https://github.com/aauth-dev/packages-js`.
- **Verified licensing finding**: MIT (confirmed via GitHub API metadata; the earlier
  page-level fetch also reported MIT — cross-checked).
- **Verified implemented capability**: TypeScript packages —
  `@aauth/protocol` (wire format/constants), `@aauth/agent` (agent-side
  signing, tokens, challenge handling), `@aauth/resource` (server-side token
  verification), `@aauth/local-keys` / `@aauth/hardware-keys` (signing key
  management, including YubiKey PIV / Secure Enclave), `@aauth/bootstrap`,
  `@aauth/fetch`, MCP-facing proxies. **No `@aauth/person-server` package
  exists in the inspected package inventory** — the inspected packages supply
  agent- and resource-side functions, not a Person Server package. GitHub API
  metadata reported 123 commits and `pushed_at` 2026-08-14.
- **Interface**: npm packages; TypeScript, not Python (SOGA/G26 is Python).
- **Functional comparison to the G26 mock boundary**: these packages implement
  the **agent-side signing** concern that G26 currently omits (permission
  requests arrive as plain JSON, unsigned). Replacement of a G26 component was
  not established because no corresponding agent-side component exists in the
  G26 mock.
- **Inferred integration work**: Language mismatch (TypeScript vs. Python)
  means this cannot be imported directly into `aauth_permission/`; it could inform a
  Python re-implementation of signing/verification, or require a
  cross-language demo harness (a TypeScript agent calling G26's Python
  Person Server). Meaningful effort for a capability G26's current exit
  criteria do not require (HTTP Message Signatures are explicitly deferred
  per `knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md`'s Boundaries
  section).

## Candidate 3 — `aauth-full-demo`, including the dormant `soga-governance-experiment` branch (Posta upstream plus local experimental lineage)

- **Repository**: `https://github.com/christian-posta/aauth-full-demo`,
  forked to `https://github.com/DebBLabs/aauth-full-demo` (already cloned
  locally at `external-repos/aauth-full-demo`, currently checked out on
  branch `soga-governance-experiment`, with two files locally modified but
  uncommitted — `backend/app/api/optimization.py`,
  `backend/app/services/a2a_service.py` — noted here, not touched).
- **Verified licensing finding**: **No license found in the inspected
  checkout** (no `LICENSE` file in the tree). This assessment did not establish
  reuse or redistribution rights.
- **Verified source capability**: A multi-agent AAuth demo containing a
  FastAPI backend, `agentgateway`, a supply-chain agent, a
  market-analysis agent, a supply-chain UI — exercising AAuth across
  identity-only, resource-managed, PS-asserted, and federated modes
  (`AAUTH_GUIDE.md`, `SPEC.md`). Source and retained test evidence were
  inspected; this assessment did not independently execute the full demo.
- **Verified lineage evidence**: the local `soga-governance-experiment`
  branch (four commits, authored by Deb Bucci, 2026-06-25 to 2026-06-26,
  predating G26) already wires SOGA's own
  `engines.aauth_execution_runtime_bridge.evaluate_aauth_execution_request`
  — the exact bridge function G26's `PermissionService.permission()` calls
  today — into this demo's `A2AService` execution path via a thin
  `backend/app/services/soga_governance_stub.py` module (read in full;
  reproduced logic: build an `execution_request` dict, call
  `evaluate_execution_request`, and if the result is not `ALLOW`, return an
  error to the caller). Repository history establishes that these are Deb
  Bucci-authored experiment commits above Christian Posta's upstream `main`;
  they are lineage evidence, not evidence of Posta's implementation or intent.
  Inspection shows the experiment is **strictly less capable than G26's current
  implementation**: it treats every non-`ALLOW` result as a flat error —
  there is no RESTRICT/HOLDING handling, no deferred-response/polling, and
  no approval-evidence re-evaluation. It predates and does not reflect
  commit `ab2dbba5`'s caregiver approval flow.
- **Interface**: Python FastAPI backend; the SOGA hook is a plain Python
  function call, already same-language and already using G26's own bridge
  module.
- **Functional comparison to the G26 mock boundary**: this does not correspond
  to the Person Server mock directly. It is an inspected **execution
  environment** with a coarse SOGA execution-boundary hook, not an established
  replacement for G26's permission endpoint or its HOLDING/approval behavior.
  No claim is made that it is the nearest such component in the wider
  ecosystem.
- **Inferred integration work**: Licensing terms would first need to be
  established. Bringing the
  branch current would mean extending `soga_governance_stub.py` to handle
  `RESTRICT`/deferred responses the way `aauth_permission/service.py` now
  does — nontrivial, and it would need to talk to a real Person Server
  (Candidate 1, itself unlicensed) or absorb the deferred-response/polling
  logic into the demo backend directly. Relative implementation cost was not
  validated in this assessment.

## Candidate 4 — `extauth-aauth-resource` (Posta repository; AAuth resource side)

- **Repository**: `https://github.com/christian-posta/extauth-aauth-resource`
  (cloned locally at `external-repos/extauth-aauth-resource`).
- **Verified licensing finding**: **No license found in the inspected
  checkout** (no `LICENSE` file). This assessment did not establish reuse or
  redistribution rights.
- **Verified implemented capability**: A Go-based Envoy/agentgateway
  `ext_authz` filter implementing AAuth resource-managed and federated
  modes (`internal/extauthz/aauth.go`, `aauth_mode2.go`), i.e., the
  **resource** side of AAuth, not the Person Server.
- **Functional comparison to the G26 mock boundary**: none of the four boundaries
  named in this task (Person Server, identity/authority, approval-evidence,
  general AAuth infra as a Person-Server stand-in). G26 does not currently
  act as, or call, an AAuth resource — this component would become relevant
  only if a future sprint extends SOGA to sit behind a real
  resource-managed AAuth flow, which is explicitly out of G26's scope
  (`G26_MISSION_PERMISSION_DECISION.md`'s Boundaries section excludes
  resource participation).
- **Inference**: no G26-scoped integration path was identified. Noted for
  completeness only.

## Candidate 5 — `decentralized-identity/kya-os-mcp` (DIF Trusted AI Agents WG / KYA-OS)

- **Repository**: `https://github.com/decentralized-identity/kya-os-mcp`.
- **Verified licensing finding**: MIT (confirmed via GitHub API). Repository
  metadata reported a push on 2026-08-15, 22 stars, 6 open issues, and
  345 commits on `main`.
- **Source-inspected and source-reported capability** (repository source and
  description inspected; behavior was not independently executed): DID-based agent
  identity (`did:key`/`did:web`, optional
  `did:cheqd`); delegation represented as W3C Verifiable Credentials
  forming a scoped, revocable chain rooted at a named "Responsible Party";
  detached JWS proofs over canonicalized request/response hashes composing
  into a tamper-evident audit trail; a consent flow in which an
  unauthorized tool call returns `needs_authorization` with a consent URL,
  a human approves, a credential is issued, and the agent retries with
  authorization now attached. Ships as an npm SDK (`@kya-os/mcp`) with
  functions `withKyaOs()`, `card()`, `requireProof()`, `withKyaOsCard()`,
  plus HTTP surfaces (`/.well-known/did.json`, `/card.json`,
  `/status-list`).
- **Interface**: MCP (Model Context Protocol) tool-call wrapping, not
  HTTP-native AAuth; TypeScript/npm.
- **Functional comparison to the G26 mock boundary**: its mechanisms overlap
  the **identity/authority** and **approval-evidence** concerns. Its
  `needs_authorization`
  → consent → credential-issuance → retry pattern is structurally close to
  G26's HOLDING → `requirement=approval` → PS-authenticated assertion →
  re-evaluation pattern, though built for MCP tool calls rather than an
  AAuth `/permission` endpoint. This assessment did not establish that its
  evidence schema satisfies G26 requirements or can replace a G26 component.
  KYA-OS is a different protocol family, not an AAuth Person Server.
- **Inferred integration work**: Protocol mismatch (MCP-shaped vs. AAuth-shaped) and
  language mismatch (TypeScript vs. Python) preclude direct import into the
  current Python AAuth path. Whether its
  VC/JWS model should inform any future canonical evidence schema is an open
  comparison question, not a recommendation or architectural conclusion here.

## Candidate 6 — DIF TAAWG Delegated Authority reports (Dmitri Zagidulin co-chairs the WG producing these)

- **Repositories**:
  `https://github.com/decentralized-identity/delegated-authority-report`,
  `https://github.com/decentralized-identity/delegated-authority-threat-model`,
  `https://github.com/decentralized-identity/governance-of-delegated-authority-report`.
- **Verified licensing finding**: Apache-2.0 confirmed via GitHub API for the
  first repository; this assessment did not establish that the same license
  applies to all three repositories.
- **Verified artifact type**: **These are reports/specifications, not
  runnable code** ("A report on Delegated Authority and an analysis of it
  in today's AuthZ protocols by the TAAWG at DIF"). Recently pushed
  (2026-08-13).
- **Functional comparison to the G26 mock boundary**: none directly; potential
  design input to the identity/authority boundary's conceptual model, not
  an implementation candidate.
- **Integration cost**: Not applicable — there is no code to integrate.
  Relevant only as reading material.

## Candidate 7 — "Dmitri's wallet work" — RM-01 absence

Per the task's request to prioritize this specifically: I searched
`"Dmitri Zagidulin" wallet github 2026`, `"Dmitri Zagidulin" agent wallet
2026 Digital Bazaar`, `"Zagidulin" "agent wallet" OR "AI wallet" spec DIF
2026`, `"Zagidulin" CHAPI credential handler agent wallet 2026`, checked his
GitHub repository listing filtered to "wallet" (one hit: `chapi-demo-wallet`,
a fork last updated February 2022 — stale, and now hosted under the
`credential-handler` org rather than his personal account), and read the
DIF Trusted AI Agents WG's live 2026 meeting notes (HackMD) directly for any
wallet-specific attribution to him.

**Bounded RM-01 absence finding:** those searches did not identify a distinct,
current (2026), Dmitri-Zagidulin-led wallet repository. This is not a claim
that no relevant wallet implementation exists elsewhere in the ecosystem.
What the inspected sources attribute to him is a co-chair role in
DIF's Trusted AI Agents Working Group (alongside Nicola Gallo and Andor
Kesselman) and, per the meeting notes, facilitator of the WG's Delegated
Authority Task Force. His historical wallet-adjacent work (CHAPI, the
Credential Handler API, at Digital Bazaar) last showed up in W3C
Credentials Community Group mailing-list activity from 2023, not 2026. The
repository establishes that Deb asked the wallet-as-Person-Server question in
`knowledge/research/governance_architecture/dif_trusted_ai_agents_debrief_2026_07_13.md`
§7. That debrief and backlog item B-026 record it as an open, unresolved
hypothesis, not as a claim that Dmitri has since built or is currently building
that wallet. No origin beyond Deb's recorded question is attributed here. This
is recorded as an absence per RM-01 rather than inferred or filled in with a
plausible-sounding substitute.
The search did identify Candidate 5 (KYA-OS) and Candidate 6 (the
delegated-authority reports) as current outputs of the working group he
co-chairs; that organizational relationship does not by itself establish his
individual authorship of those artifacts.

---

## Bounded conclusions and possible follow-up

**Verified conclusion:** none of the examined candidates was established as a
drop-in or complete replacement for a G26 mock boundary. The assessment found
overlapping implementations for transport, persistence, mission storage,
signing, identity/delegation evidence, consent, multi-agent execution, and
resource-side authorization. It also found material semantic and interface
differences from the G26 caregiver approval path.

**Verified licensing conclusion:** no license was found in the inspected
checkouts for Candidates 1, 3, and 4. This assessment therefore does not assume
rights to reuse or redistribute them. Licensing could be investigated through
repository history, published package metadata, or author/maintainer inquiry;
it is not made a mandatory next action here.

**Future Research:** a separately authorized evaluation could test a selected
candidate against explicit replacement criteria for one named mock boundary.
That evaluation would need to verify executable behavior, licensing, protocol
and language fit, and preservation of the established G26 semantics before any
replacement claim or architectural recommendation is made.
