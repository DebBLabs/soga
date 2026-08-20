# G27 Session-Grant Candidate Conformance Assessment

Date: 2026-08-18

Gate/task: G27 — implementation-neutral candidate conformance

Status: RESEARCH INPUT — not a Stage Gate finding, architecture selection, or
implementation authorization

## Scope, method, and evidence basis

This assessment applies the contract in
`knowledge/research/G27_SESSION_GRANT_PERSON_SERVER_CONTRACT_2026-08-18.md`
to two candidate families without deciding which component should own issuance,
consumption, or session state:

1. Christian Posta's AAuth Person Server reference implementation at
   `external-repos/aauth-person-server`, origin
   `https://github.com/christian-posta/aauth-person-server.git`, branch `main`,
   SHA `4e05247134640433b4fb0736e548cc2b1c21a267`;
2. Dmitri Zagidulin's Freewallet at `external-repos/freewallet`, origin
   `https://github.com/interop-alliance/freewallet.git`, branch `main`, SHA
   `403bc554d35f92c2279cf4d7e59b8d676416431b` (release v0.38.0), and the
   Wallet Attached Storage (WAS) work it uses;
3. the current WAS teaching server at `external-repos/was-teaching-server`,
   origin `https://github.com/interop-alliance/was-teaching-server.git`, branch
   `main`, SHA `9139b1ef9626c40a5f49643adcbf53d61fa19d44` (release v0.21.1).

Freewallet is established as the relevant wallet by its repository description,
homepage `https://freewallet.me`, and deployed source correspondence—not by the
name alone. Its repository describes an open-source web application for VCs,
DIDs, and cryptographic keys and links WAS (`README.md:1-21`); the repository is
AGPL-3.0. The current WAS draft source, inspected remotely and not locally
cloned, is
[`w3c-ccg/wallet-attached-storage-spec`](https://github.com/w3c-ccg/wallet-attached-storage-spec)
@ `5bc3e7319dca4b471c47a051ed382deaf9022b66`. The older
[`did-coop/wallet-attached-storage-server`](https://github.com/did-coop/wallet-attached-storage-server)
@ `882fc0557ca8103166a7d29c0284ba3f702b945e` was also inspected remotely and
is not locally cloned. It is older implementation evidence, not evidence that
Freewallet itself implements every server property.

Classifications mean:

- **SATISFIED** — the candidate demonstrates the required behavior for the
  contract, not merely a reusable primitive.
- **PARTIAL** — a demonstrated primitive or adjacent lifecycle could satisfy a
  portion, but the contract behavior or binding is incomplete.
- **ABSENT** — repository-native and source-native functional searches found no
  implementation of the requirement in the inspected scope.
- **UNESTABLISHED** — available public evidence cannot determine the behavior.

RM-02 boundary: capability to store or sign an arbitrary JSON object is not
treated as implementation of that object's semantics. AAuth pending state is not
treated as a pre-permission session grant. A WAS zCap is authority over a storage
resource, not Tip Jar action authority. Freewallet's in-memory `Session` is a
wallet login/unlock session, not the G27 participant session.

## A. Contract conformance matrix

| Contract requirement | Posta PS | Freewallet + WAS | Primary evidence | Integration implication (functional, not a design decision) |
|---|---|---|---|---|
| Issue a single-use, session-scoped participation/session-bootstrap credential | **ABSENT** | **PARTIAL** | Posta's implemented creation paths are mission, token/permission pending, and interaction pending (`ps/http/app.py:407-426,460-479,500-526`; `ps/impl/memory_pending.py:73-161`). Freewallet mints wallet/app-key credentials and handles VCs/zCaps, but no Tip Jar participation credential (`src/lib/walletRequest/appConnect.ts`; `src/lib/walletRequest/processZcaps.ts`; `src/session/applications.ts`). The WAS teaching server implements a QR-oriented ephemeral exchange with an unguessable capability URL, pending-to-complete state, approximately ten-minute expiry, in-memory state, unauthenticated bearer possession, and last-write-wins responses (`external-repos/was-teaching-server/README.md:122-149`; `CHANGELOG.md:41-58`). | WAS demonstrates an adjacent pre-permission session-bootstrap/rendezvous pattern, but not the G27 credential: it lacks mission/notice binding, issuer authority, single-use consumption, durable terminal state, and per-action governance. |
| Bind the credential to immutable `mission_s256` | **PARTIAL** | **ABSENT** | Posta stores `mission_s256` in permission/interaction pending records (`ps/impl/ps_governance.py:73-94,118-147`; `ps/impl/memory_pending.py:99-161`), but there is no bootstrap credential. Case-insensitive local-clone searches for the functional vocabulary `mission` and `mission_s256` returned zero matching files in both `external-repos/freewallet` @ `403bc554d35f92c2279cf4d7e59b8d676416431b` and `external-repos/was-teaching-server` @ `9139b1ef9626c40a5f49643adcbf53d61fa19d44`. | Posta has a reusable mission-reference model; an explicit credential-to-mission binding remains required. WAS could carry a bound record only if another component defines and enforces it. |
| Preserve issuer provenance | **PARTIAL** | **PARTIAL** | Posta missions carry an approver/PS issuer and signed AAuth tokens carry `iss`; pending records identify the request agent (`ps/models.py:56-70,115-129`; `CLIENTS.md:146-155`). Freewallet controls client keys, signs WAS/zCap requests, and produces signed VPs (`ARCHITECTURE.md:60-94`; `src/lib/walletRequest/composeVP.ts`); WAS uses DID verification methods as proof of data-controller consent ([overview, lines 25-30](https://wallet.storage/)). Neither defines the G27 grant issuer assertion. | Both have attributable-key primitives; the authority to issue this participation credential and its provenance statement remain unspecified. |
| Bind notice reference/version | **ABSENT** | **ABSENT** | Searches for `notice`, consent-text version, grant notice binding, and QR bootstrap found no such binding in either candidate. Freewallet's wallet-request UI can show requester text, but it is not bound to a G27 grant (`src/pages/chapi/RequestSourcePanel.tsx`, `src/lib/walletRequest/processRequest.ts`). | Notice presentation and immutable correlation still require contract-specific behavior. |
| Enforce validity/expiry | **PARTIAL** | **PARTIAL** | Posta gives pending rows a configurable TTL and returns terminal expiry (`ps/impl/memory_pending.py:52-61,187-221`; `persistence/sql_pending.py:68-80,251-291`). Freewallet delegates zCaps with expiry and displays grant expiry (`README.md:80-82`; `src/pages/dashboard/ApplicationDetailPage.tsx`), and signed invocations include expiry (`src/stores/wasRemoteStore.ts`). Neither applies expiry to a G27 bootstrap credential. | Existing clocks/expiry primitives are reusable; grant validity and abandonment semantics still need binding to the G27 state machine. |
| Enforce single use and atomic concurrent consumption | **PARTIAL** | **PARTIAL** | Posta generates unguessable pending IDs/codes and makes a terminal result deliver once (`ps/impl/memory_pending.py:73-97,205-221`; SQL equivalent `persistence/sql_pending.py:270-291`), but this consumes delivery, not a session grant; SQL uses load/change/save rather than an established compare-and-swap consumption transaction. The WAS teaching server implements and tests atomic conditional writes: `If-Match`, `If-None-Match: *`, 412 failure, per-resource filesystem locking, and PostgreSQL row-locking (`external-repos/was-teaching-server/src/lib/preconditions.ts:3-80`; `CHANGELOG.md:1209-1221`; `test/storage-backend-contract.ts:1217-1275,1391-1401`). | WAS supplies a tested atomic storage primitive capable of supporting a one-winner transition, but no G27 grant-consumption transaction is implemented. Posta supplies a one-time-delivery pattern, not proof of atomic grant consumption. |
| Maintain authoritative issuance/consumption state | **PARTIAL** | **PARTIAL** | Posta can persist missions and pending flows in one SQL database; default mode is in memory (`DATABASE.md:3-13`). Freewallet uses local-first browser state plus optional WAS replication (`README.md:71-88`; `ARCHITECTURE.md:257-267`), and WAS is a permissioned resource store. Neither has authoritative G27 issuance/consumption records. | Either store family could participate, but authoritative state semantics and source-of-truth rules are not supplied by storage alone. |
| Preserve durable monotonic terminal state | **PARTIAL** | **PARTIAL** | Posta's SQL pending rows persist terminal/delivered flags (`persistence/sql_pending.py:99-127,270-291`), although default state is in-memory and atomicity under concurrent delivery is not established. Freewallet implements continuity/pinning and refuses key/log rollback, plus app/client revocation cascades (`ARCHITECTURE.md:164-200,270-293`; `src/session/revocation.ts:86-191`), but its live wallet session is explicitly memory-only (`ARCHITECTURE.md:257-267`). No G27 session terminal state exists. | Both contain durability/monotonicity techniques; neither demonstrates the required participant-session terminal record. |
| Fail closed on missing, stale, conflicting, or unverifiable grant/session state | **PARTIAL** | **PARTIAL** | Posta rejects unknown/wrong-agent pending IDs, expiry, cancellation, and excessive polling (`ps/impl/memory_pending.py:163-221`), but its no-mission permission branch grants (`ps/impl/ps_governance.py:48-53`). Freewallet/WAS rejects unauthorized signed storage setup with 401 ([Connect Wallet, lines 47-76](https://wallet.storage/user-stories/connect-wallet)) and several continuity failures are fail-closed (`ARCHITECTURE.md:164-200`), but no G27 validation exists. | Candidate security checks are reusable only within their existing units of work; the G27 validator still must define fail-closed inputs. |
| Create a live bounded participant session outside the immutable mission | **ABSENT** | **ABSENT** | Posta pending flows remain token, mission, permission, or interaction units (`ps/models.py:115-164`; `ps/impl/memory_pending.py:73-161`). Freewallet's `Session` is wallet authentication/unlock state and is in-memory (`external-repos/freewallet/ARCHITECTURE.md:60-127,257-267`); its glossary states that “App session” is informal prose and nothing named `appSessionId` is persisted (`ARCHITECTURE.md:1184-1192`). The WAS ephemeral exchange has pending/complete rendezvous state, not a live participant-session state machine (`external-repos/was-teaching-server/README.md:122-149`). | The contract's live bounded-session creation function remains necessary. |
| Bind subsequent semantic-action requests to the live session | **ABSENT** | **ABSENT** | Posta permission requests bind action, agent, and optional mission but have no participant `session_id` (`ps/models.py:209-219`; `ps/http/app.py:460-479`). Freewallet persists no `appSessionId` (`external-repos/freewallet/ARCHITECTURE.md:1184-1192`). WAS verifies capability invocations against the Space controller's key and invocation target/action rather than a participant session (`external-repos/was-teaching-server/src/zcap.ts:1-18,305-314`). Local-clone searches for `session_id` returned zero matching files in all three inspected clones at the recorded SHAs. | A stable session/action correlation input must be supplied outside the immutable mission. |
| Withdraw, terminate, and expire the participant session; stale pending work | **ABSENT** | **ABSENT** | Posta can cancel/expire pending requests and terminate missions (`ps/http/app.py:526-558,611-629`), but those are not participant sessions. Freewallet can end a wallet authentication session and remove application/storage access (`external-repos/freewallet/ARCHITECTURE.md:257-267,487-529`); the WAS exchange expires in memory after approximately ten minutes (`external-repos/was-teaching-server/README.md:143-149`). None is G27 participant withdrawal/closure, and local-clone searches for the exact functional phrases `terminal session` and `bounded session` returned zero matching files in all three inspected clones at the recorded SHAs. | Mission termination, pending cancellation, wallet logout, exchange expiry, and zCap revocation must not be substituted for participant withdrawal. |
| Prevent terminal-session revival | **ABSENT** | **ABSENT** | No G27 participant-session state machine exists. A case-insensitive `reviv` search returned zero matches in `external-repos/aauth-person-server` @ `4e05247134640433b4fb0736e548cc2b1c21a267`. The matches in the Freewallet and WAS clones concern revival of soft-deleted/tombstoned storage resources, not participant sessions (`external-repos/freewallet/src/stores/browserStore.test.ts:225`; `external-repos/was-teaching-server/test/storage-backend-contract.ts:862-867`; `test/storage.test.ts:724-743`). Searches for the exact functional phrases `terminal session` and `bounded session` returned zero matching files in all three inspected clones at the recorded SHAs. | A monotonic `live → terminal` participant-session rule remains required. |
| Correlate `mission_s256 → issuance → consumption/session → SOGA + AAuth → execution → termination` | **PARTIAL** | **PARTIAL** | Posta has mission logs for permission, audit, and interaction and correlates pending IDs to mission `s256` (`ps/impl/ps_governance.py:55-116`; `MISSIONS.md:160-173`), but has no issuance/session/execution chain and no SOGA artifact. Freewallet records wallet activity and signed/logged storage/application events (`src/lib/historyActivity.ts`; `src/session/applications.ts`), but has no AAuth mission/SOGA/action-execution chain. | Existing logs could contribute events; neither alone preserves the complete required chain. |
| Preserve D-019 separation of complete SOGA decision/attribution from lossy AAuth projection | **ABSENT** | **ABSENT** | Posta's permission log stores `result` and `decided_by` for its own approved-tools/user decision (`ps/impl/ps_governance.py:55-100`; `ps/impl/memory_consent.py:173-196`), not a separate SOGA decision plus AAuth projection. The recorded `governance` / `decision` / `projection` search found no SOGA/AAuth projection in Freewallet/WAS; its incidental matches are classified in Section H. | The current governance layer must continue supplying this separation; neither candidate replaces it. |
| Obtain additional claims/evidence when a later action requires them | **PARTIAL** | **PARTIAL** | Posta implements AAuth requirement levels, pending POSTs, interaction UI, clarification, and claims/token federation hooks (`ps/models.py:38-45,115-164,191-203`; `ps/http/app.py:500-558`; `CLIENTS.md:136-164`), but `ps/impl/fake_federator.py` issues synthetic JWT-shaped strings and `provide_claims()` returns only `aa-auth.fake.claims.<count>`. Freewallet stores/verifies VCs and composes holder-signed VPs with selected VCs, DIDAuth, and zCaps (`README.md:5-20`; `src/lib/walletRequest/composeVP.ts`; `src/lib/walletRequest/processRequest.ts`). Public evidence does not demonstrate an AAuth claims exchange between Freewallet and the PS. | Posta demonstrates the AAuth carriage/hook, not authoritative external claim acquisition. Freewallet can be an evidence source, but their interoperability remains unestablished. |
| Permit ordinary-browser initiation without requiring participant identity or a special app | **PARTIAL** | **PARTIAL** | Posta provides browser consent UI, but it is reached from an already-pending agent flow and can require a user session (`ps/http/app.py:560-608`). Freewallet is itself a PWA/CHAPI wallet and supports guest/local sessions, but its credential/capability flows generally invoke wallet behavior; no anonymous G27 bootstrap route is demonstrated (`public/manifest.json`; `ARCHITECTURE.md:60-127`). | Both have browser UI primitives; neither establishes the baseline anonymous QR-to-session consumption contract. |
| Supply wallet/credential evidence for future actions requiring age, identity, or claims | **PARTIAL** | **SATISFIED** | Posta accepts/federates claims but does not itself demonstrate holder-wallet storage/presentation (`ps/models.py:191-196`; `ps/impl/fake_federator.py`). Freewallet is a VC wallet that stores, verifies, selects, and presents credentials and supports DIDAuth/CHAPI (`README.md:5-20`; `src/lib/walletRequest/composeVP.ts`; `src/lib/walletRequest/processRequest.ts`). This is evidence carriage, not proof that any specific age/guardian credential exists or is sufficient. | Freewallet can supply future wallet evidence; the action policy and authoritative meaning remain governance responsibilities. |

### AAuth interaction boundary

Posta's implementation confirms the same distinction recorded in the derived
contract. `post_permission()` creates a pending record only after a permission
request and assigns `requirement=interaction`
(`ps/impl/ps_governance.py:48-100`). The interaction URL/code are then returned
for that pending unit (`ps/impl/memory_pending.py:244-261`). That is the nearest
protocol analogue because a person completes a bounded interaction and the agent
resumes a controlled flow.

It does **not** satisfy G27 bootstrap: the Tip Jar credential is issued and
consumed before the first semantic-action permission request, creates one
multi-action bounded session, and leaves each later action independently subject
to permission. Posta's `POST /interaction` is likewise an agent-originated
protocol request with its own pending record (`ps/impl/ps_governance.py:118-151`),
not evidence of a QR offer available before an action request. This assessment
does not propose an AAuth extension. AAuth interaction remains available later
if one action legitimately needs it.

## B. Functions each candidate demonstrably provides

### Posta AAuth Person Server

- Native AAuth mission creation/reference/lifecycle and mission-scoped logs.
- AAuth `/permission`, `/audit`, `/interaction`, deferred response, polling,
  expiry/cancellation, and agent ownership checks.
- Mission/action correlation, approved-tools gating, and browser-mediated user
  decisions in the prototype.
- Optional SQL persistence for missions and pending flows; in-memory default.
- Agent registration/trust and signed AAuth token machinery documented in
  `CLIENTS.md` and `TRUST.md`.

These are the prototype's implemented AAuth and demo-governance functions. Its
consent UI and approved-tools evaluator are not a demonstrated SOGA replacement,
and its pending record is not a G27 session grant.

### Freewallet + WAS

- Holder/client-controlled keys, passphrase/passkey unlock, DID key material,
  signed VPs, DIDAuth, VC storage/verification/presentation, and CHAPI wallet
  request handling (`README.md:5-41`; `ARCHITECTURE.md:60-127`).
- Local-first wallet data with optional remote WAS replication
  (`README.md:71-88`).
- Signed/capability-authorized WAS requests, encrypted collections, delegated
  app access, zCap expiry, application listing, and access-removal flows
  (`ARCHITECTURE.md`; `src/stores/wasRemoteStore.ts:303-344,509-625`;
  `src/session/applications.ts`).
- A deployed wallet at `https://freewallet.me`; public source at
  `interop-alliance/freewallet`. The deployed routes and source expose
  credentials, storage, connected applications, and wallet history.
- WAS specifies general-purpose permissioned storage, arbitrary media types,
  DID-verification-method proofs, and optional storage-terms receipts
  ([WAS overview](https://wallet.storage/)).
- The current WAS teaching server supplies an unauthenticated, bearer-URL,
  QR-oriented ephemeral exchange with approximately ten-minute expiry and
  pending/complete state (`external-repos/was-teaching-server/README.md:122-149`).
- The teaching server supplies tested atomic conditional writes, including
  one-winner concurrent `If-None-Match: *` creation
  (`external-repos/was-teaching-server/test/storage-backend-contract.ts:1217-1275,1391-1401`).
- Freewallet and the teaching server apply the current-key-set rule to resolved
  `did:webvh` controllers: removal of a verification method causes invocations
  and delegations signed by that removed key to stop verifying
  (`external-repos/freewallet/ARCHITECTURE.md:216-226`;
  `external-repos/was-teaching-server/CHANGELOG.md:181-186`;
  `test/webvh-controller-api.test.ts:267-383`). This is capability/storage
  authority revocation, not participant withdrawal, physical safety halt, or
  governance/post-grant revocation.

These are wallet, credential, and storage-authority functions. A zCap delegates
actions on a WAS resource; it does not establish authority for a Misty semantic
action or implement the G27 participant-session state machine.

## C. Functions neither candidate provides

Within the inspected revisions, neither candidate demonstrates the complete
G27 behavior for:

1. issuance of the G27 single-use participation/session-bootstrap credential;
2. a grant binding to `mission_s256` plus notice/version and optional
   session-policy class;
3. atomic concurrent consumption that creates exactly one bounded Tip Jar
   session;
4. authoritative participant-session live/terminal state and no-revival rules;
5. binding later Misty semantic actions to that participant session;
6. coordinated withdrawal/closure/expiry that makes pending and later actions
   stale without conflating session termination with mission or zCap revocation;
7. the complete cross-component audit chain through physical execution; or
8. D-019's separate preservation of a complete SOGA decision/attribution and its
   AAuth projection.

“Neither candidate” is scoped to these two candidate families and inspected
revisions. It is not an ecosystem-exhaustion or irreplaceability claim.

## D. Demonstrated composition seams without governance-core change

The following are functional seams, not an ownership recommendation:

- Posta's PS already accepts native mission references and action permission
  requests, so trusted session evidence could be supplied to a governance
  implementation behind that boundary if an authenticated interface were
  established.
- Freewallet can hold and present VCs/DID proofs and can sign requests; it can
  therefore supply additional evidence for a later action whose policy genuinely
  requires such claims. No direct Freewallet↔AAuth evidence exchange is yet
  demonstrated.
- WAS can store integrity-controlled grant/session/audit resources and can grant
  scoped access to them. Storage and zCap enforcement alone do not establish
  issue/consume/session semantics; a component implementing those semantics
  could use WAS as a persistence/capability substrate.
- WAS conditional writes provide a tested atomic one-winner storage primitive.
  Reuse would still require a G27 transaction that couples credential validation,
  consumption, session creation, and authoritative receipts; that transaction is
  not implemented by the inspected candidates.
- Posta's SQL pending/mission stores and one-time terminal-delivery behavior are
  implementation patterns for persistence and consumption. They are not natively
  recognized as G27 session state and do not establish atomic concurrent grant
  consumption.
- Mission logs, wallet activity records, WAS receipts, and external execution
  receipts could be correlated by stable identifiers. No inspected candidate
  currently assembles the required chain or preserves the SOGA/AAuth distinction.

## E. Does either candidate alone satisfy the derived contract?

**No, on current demonstrated evidence.**

Posta's PS is closest to the AAuth mission/permission side but has no
pre-permission participation credential or bounded participant-session
lifecycle. Freewallet/WAS is closest to holder-controlled evidence and
capability-governed durable storage but has no AAuth mission binding, Tip Jar
session semantics, action governance, or SOGA/AAuth audit separation.

This is a conformance finding, not a recommendation to build, reuse, or combine
either candidate.

## F. Minimal residual component/service responsibilities

If the inspected candidates remain unchanged, some component or documented
composition still must:

1. verify authority to issue and create a mission-bound, expiring, single-use
   participation credential with notice correlation;
2. maintain authoritative issuance state and atomically consume the grant once;
3. create a unique live participant session outside the immutable mission;
4. authenticate or otherwise make trustworthy the session-state assertion
   supplied for each action;
5. bind phone inputs and semantic-action requests to the same live session;
6. close/withdraw/expire monotonically, reject reuse/revival, and stale pending
   work;
7. correlate grant, session, complete SOGA decision, separate AAuth projection,
   physical execution evidence, and terminal receipt; and
8. expose testable failure, durability, concurrency, privacy, and retention
   behavior.

This list states missing functions only. It does not select a service boundary
or name an owner.

## G. Questions remaining before PI architectural disposition

1. Which principal is authorized to issue Tip Jar participation credentials,
   and what existing assertion establishes that authority?
2. Must the credential bind a separate versioned session/policy class in
   addition to `mission_s256`, and what is the authoritative notice identifier?
3. What expiry and abandonment values satisfy the provisional G27 policy?
4. Which candidate APIs, if any, are stable/public contracts rather than current
   demo or deployment internals?
5. Can Posta's persisted pending machinery provide an atomic conditional state
   transition under concurrent consumers, or would that be new behavior?
6. How would a conformant G27 transaction use WAS's verified conditional-write
   primitive to couple grant validation, one-winner consumption, session
   creation, and authoritative receipts?
7. What authenticated interface would let Freewallet present selected evidence
   into an AAuth permission flow without requiring identity for the ordinary
   unknown-age baseline participant?
8. Where will physical execution receipts originate, and what stable reference
   will connect them to the exact SOGA and AAuth artifacts?
9. What durability, retention, and disclosure rules apply to anonymous session
   records and wallet-provided evidence?

## H. RM-01 / RM-02 absence record

Repository-native/source-native searches were run before the ABSENT findings.

Posta scope: `external-repos/aauth-person-server` at the revision above,
including `ps`, `persistence`, tests, scripts, and top-level documentation.
Terms: `session grant`, `session bootstrap`, `participation`, `QR`, `notice`,
`single-use`, `consume`, `consumption`, `replay`, `session_id`, `mission`,
`s256`, `permission`, `pending`, `interaction`, `claim`, `audit`, `terminate`,
`withdraw`, `expiry`, and `agent`.

Freewallet/WAS scope: `external-repos/freewallet` and
`external-repos/was-teaching-server` at the revisions above, deployed
`freewallet.me` manifest/routes/modules, the remotely inspected WAS draft and
older did-coop server, WAS overview/user stories, and identified public
server/client implementation documentation. Terms:
`session grant`, `session bootstrap`, `participation`, `invitation`, `QR`,
`notice`, `single-use`, `consume`, `atomic`, `replay`, `mission`, `s256`, `AAuth`,
`permission`, `authority`, `approval`, `consent`, `authorization`, `capability`,
`zcap`, `agent`, `application`, `credential`, `holder`, `proof`, `revocation`,
`session`, `history`, `receipt`, `expiry`, and `terminate`.

Recorded targeted negative-search results at the stated local clone paths and
SHAs:

- `mission` / `mission_s256`: zero matching files in Freewallet and the WAS
  teaching server;
- `session_id`: zero matching files in Posta, Freewallet, and the WAS teaching
  server;
- exact phrases `terminal session` and `bounded session`: zero matching files
  in all three clones;
- `reviv`: zero matches in Posta. Freewallet and WAS matches were inspected and
  concern soft-deleted or tombstoned storage-resource revival, not participant
  sessions (`external-repos/freewallet/src/stores/browserStore.test.ts:225`;
  `external-repos/was-teaching-server/test/storage-backend-contract.ts:862-867`;
  `test/storage.test.ts:724-743`).
- `governance` / `decision` / `projection`: the case-insensitive search across
  Freewallet @ `403bc554d35f92c2279cf4d7e59b8d676416431b` and the WAS teaching
  server @ `9139b1ef9626c40a5f49643adcbf53d61fa19d44` was non-zero. Freewallet's
  `governance` matches are a translated “More info on governance” UI string and
  an issuer-registry `policy_uri` link (`src/i18n/locales/en.json:591`;
  `src/i18n/locales/es.json:591`; `src/pages/dashboard/IssuerDetailPage.tsx:79-107`).
  WAS `decision` matches include capability-or-policy request authorization and
  `grant` / `deny` / `verify` provisioning outcomes (`src/authorize.ts:2-7,107`;
  `src/provisioning.ts:58-63`; `src/types.ts:1195-1214`); other `decision`
  matches in both clones concern design records, comments, tests, or the
  `binary-decision-diagram` dependency. `projection` matches in both clones
  concern DID documents, replicated/storage data, KMS key descriptions, wire
  shapes, or UI/view data—not an AAuth projection. No match implements or
  records a complete SOGA decision and attribution separately from a lossy AAuth
  projection.

The searches found adjacent units—AAuth deferred pending requests, wallet unlock
sessions, VCs, app-key credentials, zCaps, WAS resources, current-key-set
revocation, atomic conditional writes, and the teaching server's ephemeral
QR-oriented exchange—but no native object or execution path implementing the
complete G27 pre-permission bootstrap and bounded participant-session lifecycle.
The adjacent WAS behaviors are classified PARTIAL above rather than erased by a
blanket absence claim. Remaining ABSENT classifications are limited to that
inspected public/local evidence. Public deployment behavior without corresponding
source or tests is not promoted to SATISFIED.

RM-02 conclusion: verified implementation facts are separated above from the
functional comparison (“could contribute”) and from unresolved integration
questions. No claim is made that either external candidate replaces SOGA, that
the candidates exhaust the ecosystem, or that any residual function is uniquely
“ours.”
