# M02 Mockin/AAuth Interoperability Assessment

Date: 2026-10-02  
Status: PHASE 0 EVIDENCE — AWAITING BLIND DUAL REVIEW AND PI DISPOSITION  
Authority: D-120  
Assessment only: no package installation, import, build, test, listener, or
service execution occurred.

## Executive finding

Hellō Mockin is a useful, current AAuth `-11` reference Person Server and a
strong interoperability target. It is **not a drop-in replacement for the
committed SOGA Person Server** if the demonstration claim is that SOGA governs
auth-token issuance.

The pinned Mockin source verifies signed AAuth requests, agent, person,
resource and presented tokens; binds keys, audiences, subjects and
`mission_s256`; supports pending interaction, approval and clarification; and
issues person and auth tokens. Its authorization outcomes, however, come from
mutable mock configuration. The source exposes no external supervision or
policy callback that can gate both auth-token issuance and permission answers.
It also has no mission store: it propagates and compares `mission_s256` but
does not establish mission ownership, active/terminated state or expiry.

Recommended topology for the next bounded demonstration:

1. keep the independent SOGA Person Server as the governance-bearing path;
2. use Mockin as a separately identified protocol/reference interoperability
   target, not as proof of SOGA governance; and
3. do not represent Mockin's interaction or approval simulation as verified
   parent/guardian authority, affected-person consent, assent or refusal.

Replacing the independent PS with Mockin would require either a new external
policy adapter inside Mockin or moving SOGA to a resource-side decision before
resource-token issuance. Either is a new design claim requiring a separate
proposal.

## Exact inputs and reproducibility

### Hellō Mockin source

- Official origin: `https://github.com/hellocoop/mockin.git`
- Default branch resolved from origin: `main`
- Commit: `06bb4e7cae491beaf143395a8040659a1196c4b8`
- Tree: `281a3aa737200ec66ca98caddb20b1dfd0a98687`
- Checkout: detached and clean
- Durable root:
  `/Users/debb/dev/research-evidence/soga/inputs/mockin/06bb4e7cae491beaf143395a8040659a1196c4b8/source`
- Package: `@hellocoop/mockin` version `3.2.1`
- Node engine: `>=22`
- License: MIT
- `package.json` SHA-256:
  `8cc1abe2fa9a8c4d440ea3cae0c24c2d1068b428ea1ef1ff51d2662a4e73dc1f`
- `package-lock.json` SHA-256:
  `4873cc09e8ed5dedca286cfa5834e98d6d805688f42008ffb7ef36e1c5bbc5f8`
- `LICENSE` SHA-256:
  `793bfeb68faabe92d499a606c552206f3b6a39bc6a7d26d7351b792ecfe62c11`
- `README.md` SHA-256:
  `137502310c4ef27c47ad9dbe344d7b3df575e6efcdb3db0ee882283478bf53ba`

No submodule, LFS, credential, package-registry or container acquisition was
used. Dependencies listed by the package were not installed. The checkout's
`CLAUDE.md` was treated only as untrusted source data; none of its instructions
was adopted for this assessment.

### AAuth editor source

- Official origin: `https://github.com/dickhardt/AAuth.git`
- Commit: `fcf656de1926535f5bd6fc0538147ead6646e727`
- Tree: `fe5a02d4a965557c0d31620c5bbb8f725fdccb94`
- Checkout: detached and clean
- Durable root:
  `/Users/debb/dev/research-evidence/soga/inputs/aauth/fcf656d/source`
- `draft-hardt-oauth-aauth-protocol.md` SHA-256:
  `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`

The required protocol hash reproduced exactly. Upstream `HEAD` was not
substituted.

### Retrieved official documents

Retrieved on 2026-10-02 at 20:41:20 EDT using HTTPS, zero redirects, bounded connect and total
timeouts, from only the pre-enumerated hosts. Files are preserved at
`/Users/debb/dev/research-evidence/soga/documents/mockin-assessment-20261002`.

| URL | Retrieved | Bytes | SHA-256 |
|---|---|---:|---|
| `https://www.hello.dev/docs/mockin/` | 2026-10-02 20:41:20 EDT | 426394 | `d2af7f7816571b1fa2fca3d6e21733b3d90325c2bbc0cf1d3850b3195e4427f2` |
| `https://datatracker.ietf.org/doc/html/draft-hardt-oauth-aauth-protocol-11` | 2026-10-02 20:41:20 EDT | 751134 | `818c4da766ea59a46fea4c5dea31ef76d0b8500b99afb1edc332dfdd8f78942c` |

The Hellō documentation page describes an older/simplified surface, including
a single token endpoint. Pinned source `3.2.1` publishes separate
`person_token_endpoint` and `auth_token_endpoint` values and treats
`/aauth/token` as a non-endpoint prefix (`src/aauth/metadata.js:20-34`,
`src/api.js:49-65`). This is classified as documentation/source version drift,
not as a SOGA incompatibility.

Pinned Mockin declares that its auth-token request follows AAuth `-11`
(`README.md:41-43`), and its implementation comments likewise name `-11`
(`src/aauth/metadata.js:6-8`; `src/aauth/verify-request.js:31-37`). The restored
editor source and published `-11` both require a PS to verify that a named
mission exists, is active, belongs to the requesting agent and has not passed
`expires_at` (`draft-hardt-oauth-aauth-protocol.md:866,906`; published `-11`,
Resource Token Verification and Person Token Endpoint). No material difference
between restored `fcf656d` and published `-11` changes this assessment. Their
different byte representations are recorded above; the source citations use
the hash-pinned editor copy, while the retrieved HTML confirms the published
version.

## Compatibility matrix

Labels: `MATCH`, `ADAPTER REQUIRED`, `BLOCKING MISMATCH`,
`NOT REQUIRED FOR DEMO`, `UNRESOLVED`.

| Surface | Result | Evidence and consequence |
|---|---|---|
| PS discovery and JWKS | ADAPTER REQUIRED | The endpoint shape matches: Mockin publishes issuer, JWKS, separate person/auth token endpoints, permission, audit, interaction/reach and bootstrap endpoints (`src/aauth/metadata.js:12-35`). Its default security identity is `http://127.0.0.1:3333` (`src/config.js:4-6`), while SOGA accepts canonical HTTPS server identifiers without ports or paths (`m02_aauth_fcf656d/identifiers.py:18-27`; `m02_aauth_fcf656d/metadata.py:29-47`). A later test therefore needs an HTTPS role identity mapped to loopback transport plus offline trusted metadata/JWKS. This is configuration/routing work, not a protocol-shape mismatch, and remains unexecuted. |
| Bootstrap and agent-token binding | MATCH | Mockin has a dedicated bootstrap route and verifies bootstrap polling with the ephemeral HWK, while other pending records require the verified agent JWT (`src/api.js:89-92`; `src/aauth/pending.js:51-119`). Source-only match; not executed. |
| Person-token endpoint | MATCH | Signed request, resource audience, optional `mission_s256`, key confirmation and one-hour/agent-expiry clamp are implemented (`src/aauth/person.js:1-19,90-95,138-148`; `src/aauth/issue-person-token.js:25-77`). |
| Auth-token endpoint | MATCH | Requires resource and presented tokens, verifies their binding, and produces an auth token (`src/aauth/token.js:1-17,58-109,273-275`). Mockin additionally supports step-up and connection branches not required by the current SOGA demo. |
| HTTP Message Signatures | MATCH | Mockin uses RFC 9421 verification, requires `Signature-Key` JWT, and by default requires content-type/content-digest coverage on body requests (`src/aauth/verify-request.js:1-17,31-58,78-166`). This matches the committed SOGA profile's signed-body components (`m02_aauth_fcf656d/profile.py:10`; `m02_aauth_fcf656d/http_signatures.py:120-143,177-239`). |
| JWT `typ`, algorithm and key binding | MATCH | Mockin checks fully specified accepted algorithms and exact `aa-resource+jwt`, `aa-person+jwt` or `aa-auth+jwt` types, then verifies JWK thumbprints (`src/aauth/verify-resource-token.js:41-90`; `src/aauth/verify-presented-token.js:48-87,135-174`). SOGA rejects wrong types and binds `cnf.jwk` (`m02_aauth_fcf656d/jose.py:80-119`; `m02_aauth_fcf656d/tokens.py:23-64`). |
| Audience, issuer, subject and expiry | MATCH | Mockin verifies resource audience against the PS, issuer discovery, expiry, PS and subject (`src/aauth/verify-resource-token.js:49-106`; `src/aauth/verify-presented-token.js:60-133,176-226`). SOGA performs corresponding token-profile checks (`m02_aauth_fcf656d/tokens.py:29-64,123-197`). |
| `mission_s256` propagation/binding | MATCH | Mockin stamps it into person/auth tokens and rejects stripping or mismatches against the resource token (`src/aauth/person.js:90-95,138-148`; `src/aauth/verify-presented-token.js:206-218`; `src/aauth/issue-auth-token.js:113-128`). |
| Mission creation, canonicalization, ownership, active/terminated state and expiry | BLOCKING MISMATCH | **Attribution: Mockin versus its declared AAuth `-11` source.** Mockin explicitly has no mission endpoint/store and therefore cannot perform the draft's required mission-active, ownership and expiry checks (`src/aauth/person.js:93-95`; `src/aauth/verify-resource-token.js:107-109`; `draft-hardt-oauth-aauth-protocol.md:866,906`). The committed SOGA PS holds a mission map and verifies agent ownership before supervision (`m02_aauth_fcf656d/exchange.py:47-94,114-145`). Mockin alone cannot support the same mission-governance claim. |
| Resource-token input and auth-token output | MATCH | Mockin verifies exact resource-token type, signature/discovery, audience, agent key and presented-token linkage before issuing (`src/aauth/token.js:90-109`; `src/aauth/verify-resource-token.js:29-109`). |
| Three-party PS-issued auth token | MATCH | Mockin issues `aa-auth+jwt` itself using its PS key (`src/aauth/issue-auth-token.js:85-135`). This is the mode used by the current bounded SOGA package. |
| Four-party AS-issued auth token | UNRESOLVED | Mockin can verify an AS-issued presented auth token from a trusted/discovered AS (`src/aauth/verify-presented-token.js:71-116`), but it is not itself an AS and no four-party end-to-end execution was authorized. Not needed for the bounded demo. |
| External SOGA supervision before auth-token issuance | ADAPTER REQUIRED | **Attribution: SOGA architecture requirement; no AAuth protocol deviation.** AAuth permits supervision to be internal to the PS and leaves the PS-to-supervision-server contract out of scope (`draft-hardt-oauth-aauth-protocol.md:455,462`). Mockin's auth handler proceeds from its own mock configuration to issuance; no external policy/supervision callback appears in the complete AAuth handler/config surface (`src/aauth/mock.js:16-47,71-90`; `src/aauth/token.js:214-275`). The committed SOGA PS invokes its supervisor and fails closed before issuance (`m02_aauth_fcf656d/exchange.py:114-145`). |
| Permission decision source | ADAPTER REQUIRED | **Attribution: SOGA architecture requirement; no AAuth protocol deviation.** Mockin grants or denies solely from `cfg.permission`, defaulting to granted (`src/aauth/permission.js:10-25`; `src/aauth/mock.js:42-47`). It has no acceptable external SOGA decision seam. It is suitable for simulating response shapes, not proving policy evaluation. |
| Interaction requirement | ADAPTER REQUIRED | Mockin supports a pending interaction and person-facing code/URL (`src/aauth/person.js:150-200`; `src/aauth/token.js:214-255`). Its consent route approves an entry when an unauthenticated browser presents the code (`src/aauth/consent.js:1-11,17-75`). This can exercise flow shape but not authenticated parent authority. |
| Approval requirement | ADAPTER REQUIRED | Mockin can return `requirement=approval`; pending polling then auto-resolves approval (`src/aauth/token.js:268-270`; `src/aauth/pending.js:137-171`). No approver identity, authority basis or evidence is captured. |
| Clarification requirement | MATCH | Mockin returns a clarification question and accepts a signed clarification response (`src/aauth/token.js:257-266`; `src/aauth/pending.js:131-149,196-228`). Current demo does not require it. |
| Person versus another approving party | UNRESOLVED | Mockin's interaction page is explicitly person-facing, and approval is simulated out of band. Source contains no representative/guardian role or proof. Parent authorization cannot be inferred from either requirement path. |
| Pending poll, submit and cancel | MATCH | Signed polling, clarification/resource-token submission, cancellation, terminal errors and result issuance are implemented (`src/aauth/pending.js:121-241`). |
| Permission denial and reason | MATCH | Returns `{permission: denied, reason}` or grant (`src/aauth/permission.js:14-25`). The shape matches a demonstration response, but the policy source does not. |
| Problem details and errors | MATCH | Mockin centralizes RFC 9457-style problem responses and maps protocol errors in the handlers (`src/aauth/verify-request.js:40-50`; `src/aauth/person.js:29-37`; `src/aauth/token.js:32-46`). Source-only finding. |
| Offline metadata/JWKS | MATCH | `trusted_servers` can preload metadata and JWKS for tests (`src/aauth/mock.js:45-47,85-88`). This offers a potential no-runtime-fetch test seam, subject to later execution review. |
| Literal loopback and shutdown | ADAPTER REQUIRED | Source defaults the bind to `127.0.0.1:3333` and calls Fastify listen with those values (`src/config.js:4-6`; `src/server.js:21-27`). SOGA must retain distinct HTTPS role identifiers and route them to literal-loopback transport; Mockin's default HTTP issuer is not acceptable as the SOGA security identity. Actual bind and shutdown behavior remains unexecuted. A later execution proposal must pin literal `127.0.0.1`, finite ports and cleanup. |
| Test identities, secrets and evidence | ADAPTER REQUIRED | Mockin includes fixed mock keys/users and in-memory state. A later run must use only test identities, prevent secret recording and prove cleanup. No personal data is authorized. |
| Audit and activity logging | NOT REQUIRED FOR DEMO | Mockin exposes an audit endpoint (`src/api.js:75-87`), but this assessment did not establish mission-lifecycle logging or durable audit semantics. |
| R3 | NOT REQUIRED FOR DEMO | Mockin can fetch/hash and auto-grant R3 (`src/aauth/token.js:184-212`), which would introduce a runtime fetch. The bounded demo does not need R3 and should leave it disabled. |

## Adapter seams and bounded test plan

### Seam A — protocol interoperability comparison

The least invasive Mockin experiment is a separate comparison run:

- SOGA agent client talks to pinned Mockin over literal loopback;
- Mockin uses preloaded metadata/JWKS so no runtime discovery leaves loopback;
- the test exercises person token, resource challenge, auth token and exact
  refusal cases; and
- results are labeled Mockin interoperability, not SOGA-governed issuance.

This can validate whether the committed SOGA client speaks to a reference PS.
It cannot demonstrate SOGA policy unless Mockin changes.

Mockin's configuration mutation API is **not** an acceptable policy adapter.
The unauthenticated `PUT /mock/:mock` route rewrites process-global settings
including `auto_approve`, `requirement` and `permission`
(`src/api.js:114-124`; `src/aauth/mock.js:71-90`). It is not bound to a request,
agent, mission or subject; concurrent requests can race; and it records no
decision evidence. Any process able to reach a future listener could change
authorization outcomes. A SOGA controller that flips this global mock state
before a request would be a disguised test toggle, not governed authorization.
Any execution proposal must treat the route as a security boundary and prevent
untrusted access.

### Seam B — preserve current SOGA governance

The existing topology remains the correct demonstration path:

`agent -> independent SOGA Person Server -> resource gateway`

The PS calls SOGA supervision before issuing the auth token; the resource
gateway enforces type, binding, mission and scope. Mockin can be shown beside
this as evidence that the protocol surface is not solely self-invented.

### Seam C — future Mockin policy adapter

A separate proposal could add an external decision adapter to Mockin's auth and
permission paths. That is upstream source modification or a maintained fork,
not configuration of the pinned source. It would need to define failure,
timeout, request authenticity, decision evidence and version-maintenance rules.

### Seam D — resource-side SOGA check

Calling SOGA before resource-token issuance could retain a governance decision
while using Mockin as PS, but it reallocates governance from the PS to the
resource. This is a new architecture, not preservation of D-114/D-116, and
must not be adopted implicitly.

## Parent/affected-person boundary

Mockin does not solve the farmers-market parent case. Its interaction code is
a correlation/authorization handle; the source does not authenticate a parent,
establish relationship or authority, preserve scope or duration of that
authority, or capture a child's assent/refusal. `requirement=approval` is a
mocked outcome, not proof of who approved.

For a future test, the same proposed directed robot action should produce a
different decision solely because verified parent-authority evidence is
present or absent. The legal and governance precedence among parent authority,
child assent/refusal, age, capacity, safety and context remains unresolved and
must not be invented by this implementation.

## Recommendation and next decision

**Recommendation: use both, with distinct claims.**

- Use the independent SOGA PS for the AAuth/SOGA demonstration because that is
  the only current path where SOGA actually gates auth-token issuance.
- Use pinned Mockin in a later bounded comparison to test interoperability with
  an independently developed `-11` PS surface.
- Do not delay the primary demo waiting for Mockin integration.
- Do not connect Mockin to WAS in this stage. WAS is storage; Mockin is a mock
  PS. Any connection would require a separate evidence/adapter contract.
- Do not represent Mockin approval as parent or affected-person authorization.

Before any Mockin execution, require a separate proposal covering exact
dependencies, cached or authorized acquisition, literal-loopback binding,
offline trusted-server inputs, fixed test identities, finite time/output,
secret redaction, teardown and evidence. The exact pinned source and this
report must first receive blind dual review and PI acceptance.

## Phase 0 boundary attestation

Performed:

- exact Git source acquisition from the two authorized origins;
- exact commit/tree/hash verification;
- two pre-enumerated official document retrievals;
- source-only reading and comparison; and
- creation of this report.

Not performed:

- dependency, package or container download;
- installation, import, build, lint, test or application execution;
- listener creation or service startup;
- Mockin, SOGA recovery, wallet, WAS, QR or robot interaction;
- personal-data processing or physical action; or
- G28/G29 activation.
