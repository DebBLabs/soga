# M02 Mission Formation — Wallet-Assisted AAuth Person Server

Date: 2026-09-06
Status: ADOPTED — Stage 1 research authorized under D-035
Prepared by: Codex/CG
Review target: `main @ ddcdabb7939c3c3e94bab0db95431d88fcbe416d`

## Mission intent

Determine, through current source inspection and bounded local execution,
which AAuth Person Server responsibilities can be supplied by a
person-controlled wallet and Wallet Attached Storage, which require a separate
Person Server service, and whether one wallet- or browser-originated evidence
artifact can traverse a real local AAuth/SOGA decision path to a recording-only
Misty capability surface.

M02 treats the Person Server as reusable infrastructure for many missions and
resources. Misty Tip Jar is the first concrete proving mission, not the owner or
limit of the Person Server.

## Current source candidates

The investigation must pin and inspect, without silently updating the prior
August evidence:

| Candidate | Prior local SHA | Upstream `main` observed 2026-09-06 |
|---|---|---|
| Interop Alliance Freewallet | `403bc554d35f92c2279cf4d7e59b8d676416431b` | `8e806c049b1134e36e72ab243ea3fbeb93153c37` |
| WAS Teaching Server | `9139b1ef9626c40a5f49643adcbf53d61fa19d44` | `2090a606f2723e4d57ef0090db55fd1bdab9427e` |
| W3C CCG Wallet Attached Storage specification | remotely inspected at `5bc3e7319dca4b471c47a051ed382deaf9022b66`, not previously pinned locally | `4e67f5f6d4e4c622f734c55909ab15e3b67a7d07` |
| DID Cooperative WAS server | remotely inspected at `882fc0557ca8103166a7d29c0284ba3f702b945e`, not previously cloned | `882fc0557ca8103166a7d29c0284ba3f702b945e` (fresh `ls-remote` check; unchanged) |

The current AAuth editor sources must also be pinned. Published `-10`, editor
base-protocol changes, and the separate R3 editor draft must not be conflated.
R3 operation vocabularies and `per-call` authorization are investigation
subjects, not adopted protocol behavior.

## Research questions

1. Can Freewallet supply Person Server key custody, signing, person-controlled
   credentials, evidence presentation, and interaction UI without collapsing
   the wallet into the complete Person Server role?
2. Can WAS supply durable mission, pending-decision, revocation, session, and
   audit storage with the atomic and monotonic properties already required by
   G26/G27?
3. Which AAuth Person Server metadata, token issuance, mission-log, permission,
   clarification, revocation, and policy responsibilities remain outside both?
4. Can an authenticated, integrity-protected wallet evidence handoff reach the
   local AAuth/SOGA evaluator without treating wallet possession, QR
   possession, payment, or session admission as authority, without obscuring
   B-038's documented absence of live validity/revocation inputs and while
   preserving B-039's separation of representative approval from
   affected-person assent or refusal?
5. Does R3 `per-call` represent the same responsibility as SOGA action-time
   governance, a compatible carrier for its result, or a distinct authorization
   layer that must remain separate?
6. Can the composition preserve the complete SOGA decision and attribution
   separately from any lossy AAuth projection?

## Proposed four-stage execution sequence

### Stage 1 — Current-source conformance refresh

- obtain clean read-only clones or fetched refs at the exact SHAs above;
- inspect changes since the prior pinned Freewallet and teaching-server SHAs;
- pin the current AAuth base and R3 editor sources;
- update the candidate responsibility matrix using source-level evidence;
- verify each candidate's license and define the usable boundary before any
  reuse or modified local execution is proposed; Freewallet's recorded
  AGPL-3.0 license requires particular attention, Posta's Person Server had no
  license established in the prior checkout, and the WAS-family license status
  must be verified at the selected SHAs;
- make no implementation or adoption decision from repository labels alone.

### Stage 2 — Local Person Server boundary

Subject to a later PI implementation decision, replace the current in-process
mock boundary with a local development service that has explicit keys,
metadata, mission and pending state, token validation/issuance behavior,
revocation state, and SOGA policy evaluation. “Real” means exercised protocol
messages and verification between separately running local components; it does
not mean production, public, conformant, or independently interoperable.

### Stage 3 — Wallet/WAS composition seam

Subject to a later PI implementation decision, run the selected wallet/storage
components locally and demonstrate the narrowest authenticated handoff their
current interfaces support. Keep storage authorization, identity evidence,
representative authority, participant admission, payment/donation, mission
permission, and action execution as separate claims.

B-038 remains a standing constraint: the current AAuth execution bridge cannot
derive live revocation, expiry, delegation-depth, elapsed-time, or attenuation
state from incoming evidence. Merely carrying wallet evidence to that bridge
does not prove that the evidence affected governance. Stage 3 or 4 may claim
live authority evaluation only after that path is implemented, tested, and
separately authorized.

### Stage 4 — Misty Tip Jar recording-surface walkthrough

Exercise:

`wallet or browser → local Person Server → mission permission → SOGA decision
→ target-bound Misty adapter → recording-only surface`

No physical Misty request is part of M02. The Beryl network boundary is a hard
prerequisite to any later robot access and is not bypassed by successful M02
software evidence.

## Explicit nonclaims and prohibitions

- Do not claim that Freewallet is Dmitri Zagidulin's personal implementation;
  it is the Interop Alliance project he encouraged the PI to examine through
  the Person Server lens.
- Do not claim that Freewallet or WAS already implements an AAuth Person Server.
- Do not claim AAuth `-11`, R3, wallet, WAS, MCP, or AIIM conformance without
  the applicable independent interoperability evidence.
- Do not treat a QR/capability URL, wallet possession, payment, credential
  presence, person token, or session admission as representative authority or
  permission for a Misty action.
- Do not modify upstream candidate repositories during investigation.
- Do not use production credentials or personal identity documents.
- Do not expose a service beyond loopback or a specifically reviewed local test
  boundary.
- Do not power, connect, query, configure, discover, or actuate Misty A or
  Misty B.
- Do not activate or rewrite G28.

## Stage 1 acceptance criteria

1. Every candidate is identified by origin, branch/ref, exact SHA, license, and
   observed runnable status.
2. Material changes since the August conformance assessment are reproduced and
   classified by Person Server responsibility.
3. The report distinguishes source-supported capability, demonstrated local
   behavior, inference, absence, and unresolved questions.
4. A responsibility matrix identifies `reuse`, `adapt`, `separate service`, or
   `unresolved` for wallet, WAS, Person Server, SOGA, participant-session, and
   resource-enforcement functions without making the build/reuse decision by
   assertion.
5. Gate 1 and Gate 2 independently review the evidence before the PI is asked
   to authorize Stage 2 implementation.

Stages 2 through 4 intentionally do not receive final acceptance criteria in
this Mission Formation proposal. Each later stage must define its own bounded
criteria and receive a separate PI decision before implementation or service
execution, following the staged pattern used in M01.

## Requested reviews

- **Claude / Gate 1:** architectural conformance, source discipline, authority
  separation, AAuth fidelity, scope, licensing, and whether the proposal can
  proceed without weakening existing decisions.
- **AGy/Gemini / Gate 2:** independently attempt to falsify feasibility,
  role separation, acceptance criteria, provenance, security boundaries, and
  the four-day sequencing claim.

Both reviews are advisory. This proposal authorizes no source update, build,
service execution, network exposure, or robot access. M02 can begin only after
M01 disposition and explicit PI authorization.
