# M02 Stage 1 — Wallet-Assisted Person Server Conformance Refresh

Date: 2026-09-06
Status: RESEARCH INPUT — implementation and service execution remain unauthorized
Repository checkpoint: `main @ d252b73d5472f7b648154e544cc042f9d9fa4226`

## Scope and method

This report performs only the current-source research authorized by D-035. Six
clean detached checkouts were created under
`/private/tmp/m02-stage1-sources-20260906`. No candidate service was run, no
dependency was installed, no production credential was used, and neither Misty
robot was accessed.

Evidence labels follow `docs/RESEARCH_METHODOLOGY.md`:

- **VERIFIED SOURCE** — read directly in the pinned checkout;
- **DOCUMENTED, NOT RUN** — a candidate documents a command or behavior that
  this stage did not execute;
- **INFERENCE** — a possible composition consequence, not demonstrated;
- **ABSENCE IN INSPECTED SCOPE** — a bounded source-search result, not an
  ecosystem-wide claim;
- **UNRESOLVED** — evidence is insufficient for a disposition.

## A. Source ledger

| Candidate | Origin and pinned revision | License at revision | Documented runnable status (not executed) |
|---|---|---|---|
| AAuth Person Server | `christian-posta/aauth-person-server`, `main @ 18d9558307240f8fece8c35119548c3f59489672` | Apache-2.0 (`LICENSE:1`); this is the only change since the August G27 SHA `4e052471...` | README documents Python 3.10+, editable install, FastAPI/uvicorn portal, standalone services, demos, and an April 2026 verification claim (`README.md:1-80`). **DOCUMENTED, NOT RUN.** |
| Freewallet | `interop-alliance/freewallet`, `main @ 8e806c049b1134e36e72ab243ea3fbeb93153c37`, release line 0.42.0 | AGPL-3.0 (`LICENSE:1`) | README documents Node 22+, pnpm install, Vite development/build, and static-SPA operation (`README.md:1-80`), while `package.json:25` requires Node 24 or later. The effective runtime prerequisite must be resolved before a later execution stage. **DOCUMENTED, NOT RUN.** |
| WAS teaching server | `interop-alliance/was-teaching-server`, `main @ 2090a606f2723e4d57ef0090db55fd1bdab9427e`, release 0.27.0 | AGPL-3.0-or-later (`LICENSE:1`; `package.json:108`) | Package scripts document build, node/Postgres tests, conformance, and local start paths (`package.json:1-44`). **DOCUMENTED, NOT RUN.** |
| WAS specification | `w3c-ccg/wallet-attached-storage-spec`, `main @ 4e67f5f6d4e4c622f734c55909ab15e3b67a7d07` | Repository contains MIT software terms (`LICENSE`) and W3C Software and Document License 2023 (`LICENSE.md`); applicability must be respected per copied material | README documents ReSpec source and local static rendering, not a storage service (`README.md:1-70`). **DOCUMENTED, NOT RUN.** |
| DID Cooperative WAS server | `did-coop/wallet-attached-storage-server`, `main @ 882fc0557ca8103166a7d29c0284ba3f702b945e` | `package.json` declares MIT; no top-level license file was present. Treat reuse terms as **UNRESOLVED** until copyright/license provenance is confirmed. | README documents Node/npm setup and a localhost development server (`README.md:1-25`). **DOCUMENTED, NOT RUN.** |
| AAuth editor repository | `dickhardt/AAuth`, `main @ 39a017d64c1a35dea6188e3fae71f4a3f3aa03e7` | No top-level software license found. Draft text declares IETF Trust IPR boilerplate; that does not establish a software-reuse license for repository tooling. | Markdown specifications and build tooling are present. Base editor text records `-11`; R3 is exploratory and says there are no known implementations (`draft-hardt-aauth-r3.md:835`). **DOCUMENTED, NOT RUN.** |

Published AAuth `-10` remains the published comparison baseline. The base
editor source above contains the `-11` history and later corrections; R3 is a
separate exploratory document. They are not treated as one adopted protocol.

## B. Material change findings since August

### B1. AAuth Person Server

**VERIFIED SOURCE.** The only commit after the G27 snapshot adds Apache-2.0.
The earlier “no license established” reuse blocker is therefore resolved at
this revision. No implementation change occurred in that range.

The implementation still provides a useful separate-service baseline:
mission and pending state, permission and consent surfaces, persistence,
signing, clarification, and agent-binding revocation. Its permission decision
continues to grant by `approved_tools` membership or create a user pending
request (`ps/impl/ps_governance.py:48-80`). It does not call SOGA and does not
implement the current editor draft's complete person-token model.

### B2. Freewallet

**VERIFIED SOURCE.** Freewallet changed substantially from 0.38.0 to the 0.42.0
line. The changes most relevant to M02 are:

- a non-CHAPI interaction-URL entry path for scanned, pasted, or CLI-provided
  requests (`src/lib/walletRequest/externalRequest.ts:1-18,94-173`);
- pre-consent refusal of malformed, cross-origin, or disallowed grant classes
  (`externalRequest.ts:204-284`);
- explicit agent storage grants, listing, expiry display, current-key-set
  checks, and revocation (`src/lib/connectedApps.ts:29-34,254-320,433-520`;
  `src/session/applications.ts:125-149`);
- transient and credential-anchored wallet sessions, with the live `Session`
  still memory-only (`ARCHITECTURE.md:94-162,520-526,1185-1198`); and
- stronger fail-closed establishment, retirement, and revocation ceremony
  records in source and the repository's decision documents.

This is a credible wallet-originated presentation and zCap-grant seam. It is
not an AAuth Person Server implementation. The interaction URL identifies a
wallet request/exchange and the resulting grants govern WAS storage access;
they do not establish AAuth mission permission or representative authority.

### B3. WAS teaching server and specification

**VERIFIED SOURCE.** The teaching server advanced from 0.21.1 to 0.27.0. It now
adds typed denial reasons, broader DID and client-annex handling, tighter zCap
delegation predicates, revocation behavior, caches with invalidation rules,
and HMAC/encryption descriptor validation.

The earlier atomic-storage finding remains strong. Conditional writes evaluate
`If-Match` and `If-None-Match` and must occur under a filesystem lock or a
Postgres row-locking transaction (`src/lib/preconditions.ts:1-20,31-69`). This
can support a one-winner state transition, but no inspected path couples it to
AAuth session-grant validation, consumption, and session creation.

The specification added chunked resources, an EDV-over-WAS profile, key
epochs, writer attribution, collection metadata, and additional controller
rules after the prior `5bc3e731...` snapshot. Those extend storage semantics;
they do not assign Person Server or SOGA decision responsibility.

The older DID Cooperative server SHA is unchanged from the August remote
inspection. It remains historical implementation evidence, not the preferred
current teaching implementation.

### B4. AAuth base editor source and R3

**VERIFIED SOURCE.** The base editor draft adds a PS-issued person token,
person-token retention and matching, mission expiry and approved resources,
mission updates, consent-presentation distinctions, and clearer separation of
governance from per-act supervision
(`draft-hardt-oauth-aauth-protocol.md:3276-3328`). A person token establishes
recognition and continuity for one resource but is not identity proofing,
legal identity, or authorization (`ibid.:3322,3533-3555`).

**VERIFIED SOURCE.** R3 adds resource-declared, content-addressed operation
descriptions and `per-call` proposals. A resource remains the enforcement
point; it must match operations, bind parameters, consume a per-call grant once,
and answer replay from the retained result
(`draft-hardt-aauth-r3.md:695-702,780-801`). R3 calls itself exploratory and
records no known implementation (`ibid.:835`). Its `per-call` mechanism is
adjacent to SOGA action-time governance, not evidence that SOGA's decision,
attribution, safety state, or representative/affected-person policy has been
implemented.

## C. Responsibility and conformance matrix

The disposition words below classify potential responsibility only. They do
not authorize a build or select a component.

| Responsibility | Current evidence | Stage 1 classification | Boundary |
|---|---|---|---|
| Person-controlled keys and wallet unlock | Freewallet implements local wallet keys, passphrase/passkey entry, transient sessions, and credential presentation | **REUSE candidate** | Wallet authentication is not person-token issuance or legal identity assurance. |
| Wallet-originated evidence/request handoff | Freewallet interaction URLs open exchanges, validate request shape/origin, display consent, and deliver responses | **ADAPT candidate** | Requires an explicitly authenticated mapping into a future PS; possession of the URL or wallet is not authority. |
| Storage capabilities and revocation | Freewallet and WAS issue, inspect, expire, and revoke zCaps governing storage | **REUSE candidate** | zCap authority is over WAS resources, not a Misty action or mission permission. |
| Durable mission, pending, audit, and token records | WAS offers private capability-controlled resources and conditional writes; Posta offers SQL-backed PS stores | **ADAPT candidate / UNRESOLVED selection** | Storage schema, atomic transaction, retention, and authoritative owner remain to be designed and tested. |
| Atomic single-use participant admission | WAS conditional writes can provide a one-winner primitive | **ADAPT candidate** | The complete validate-consume-create-session transaction is absent in inspected candidates. |
| AAuth PS metadata, signing, person-token issuance/retention, mission log, permission, audit, and clarification | Base editor draft assigns these to a PS; Posta supplies many older-draft surfaces but not the complete current model | **SEPARATE SERVICE** | Wallet and WAS may supply keys/UI/storage but do not erase PS protocol responsibility. |
| SOGA policy decision, attribution, safety/degradation, and complete audit artifact | Implemented or modeled in SOGA; absent as a complete unit in inspected candidates | **SEPARATE SERVICE** | Preserve the full SOGA decision separately from AAuth's wire projection. |
| Live authority freshness and revocation inputs | B-038 documents that SOGA's current AAuth bridge hardcodes or lacks live derivation | **UNRESOLVED / SOGA work** | Wallet evidence merely carried through open dictionaries is not decision-relevant until validated and evaluated. |
| Representative authority | No inspected candidate establishes who may act for another person, the evidence basis, scope, or end | **UNRESOLVED** | A credential can carry evidence; policy and legal sufficiency cannot be inferred from carriage. |
| Affected-person assent/refusal | No independent affected-person path is established by the inspected wallet/PS composition | **UNRESOLVED (B-039)** | Must remain distinct from representative approval; precedence is not decided here. |
| Participant session admission | G27 derived a separate short, single-use, mission/platform-bound lifecycle | **SEPARATE SERVICE or ADAPT — UNRESOLVED owner** | Do not conflate wallet session, WAS exchange, person token, payment, or R3 per-call grant with participant admission. |
| Resource-side operation enforcement | AAuth R3 specifies resource enforcement; Posta resource-side projects and SOGA target-bound adapters are adjacent | **SEPARATE RESOURCE/ADAPTER responsibility** | No current candidate proves a real Misty dispatch or outcome. M02 remains recording-surface only. |
| Payment or donation | Wallets may support payment separately | **OUTSIDE current decision** | A tip or donation is never interaction permission or representative authority. |

## D. Answers to the M02 research questions

1. **Freewallet can plausibly supply wallet keys, evidence presentation,
   consent UI, interaction-link handling, and storage-capability management.**
   It cannot be classified as the complete AAuth Person Server from current
   source evidence.
2. **WAS can plausibly supply protected durable records and atomic conditional
   writes.** It does not supply mission, permission, session-grant, or SOGA
   semantics merely by storing those records.
3. **A separate PS boundary remains necessary** for AAuth metadata, person-token
   issuance/retention, mission and pending lifecycle, permission/audit,
   clarification, and protocol projection unless a later design deliberately
   assigns and implements each responsibility elsewhere.
4. **A wallet evidence handoff is technically plausible but not demonstrated.**
   B-038 and B-039 remain blocking design constraints for any claim that the
   evidence affected a live governance decision.
5. **R3 `per-call` is compatible in shape but not equivalent to SOGA.** R3
   carries resource-declared operation meaning and requires resource-side
   per-call enforcement. SOGA separately evaluates human intent, authority,
   state, safety, and attribution. A future projection may connect them; Stage
   1 does not choose that design.
6. **The complete SOGA decision must remain separately preserved.** Nothing in
   the inspected wallet/WAS sources supplies that record, and R3's hashes and
   grants do not contain it.

## E. RM-01 bounded absence record

Searches were run across the six pinned checkouts using each system's own and
SOGA's comparison vocabulary: `person token`, `person server`, `mission`,
`permission`, `representative`, `guardian`, `proxy`, `assent`, `refusal`,
`revocation`, `expiry`, `session`, `single-use`, `consume`, `interaction`,
`agent grant`, `consent`, `authority`, `conditional`, `If-Match`, `audit`,
`governance`, `decision`, and `projection`.

Matches establish many adjacent primitives documented above. No inspected
source implements the complete participant-session lifecycle, representative-
authority evaluation, independent affected-person path, B-038 live-input path,
or complete SOGA-decision-plus-lossy-AAuth-projection separation. These are
bounded source findings, not claims that no external system can address them.

## F. Stage 1 disposition

The evidence supports a **hybrid composition hypothesis** for later review:

`Freewallet UI/keys/evidence + WAS protected storage/atomic writes + separate
AAuth Person Server + separate SOGA governance + separate participant-session
service + resource/adapter enforcement`.

This is not yet a build/reuse decision. The AGPL boundary, WAS-server license
provenance, exact inter-component trust messages, B-038 live authority inputs,
B-039 affected-person policy, and the participant-session owner remain open.
Stage 2 must not begin until this report passes Gate 1 and Gate 2 and the PI
issues a separate authorization.

## G. Preserved prohibitions

No wallet or WAS service execution, dependency installation, integration
implementation, external exposure, production credential use, Misty access,
or G28 activation occurred or is authorized by this report.
