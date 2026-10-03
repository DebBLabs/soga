# M02 Mockin/AAuth Interoperability Assessment Proposal

Date: 2026-10-02  
Status: DRAFT — NOT AUTHORIZED FOR ACQUISITION OR EXECUTION  
Repository basis: `main @ b1521f89e4db77daa37a88a6b282dd2209a06e6a`  
Author/integrator: Codex  
Review class: mandatory blind dual review, batched as one source-assessment claim

## Purpose

Determine whether Hellō Mockin can serve as the AAuth Person Server in the
bounded demonstration without silently removing SOGA from the authorization
decision. In the committed package, SOGA supervision is inside the independent
Person Server and runs before that PS issues an auth token. The resource and
localhost transport enforce token, binding, mission and scope conditions but
do not invoke SOGA. Replacing that PS with auto-approving Mockin therefore does
not preserve the existing governance claim unless the pinned Mockin source has
a usable external policy hook. Preserve the D-119 recovery path as the
independent implementation and fallback.

This is a source and compatibility assessment. It does not install or run
Mockin, modify the AAuth implementation, integrate WAS, connect a wallet or
robot, or claim that Mockin establishes representative authority.

## Trigger and currently verified public facts

Dick Hardt pointed the public AAuth channel to the Hellō Mockin documentation
as the mock Person Server he uses in testing.

The official public documentation states that Mockin can exercise AAuth agent
client code for bootstrap, token issuance, R3 and governance without a real
wallet. It documents discovery, Ed25519 keys, permission, audit, interaction,
pending and token behavior; configurable `interaction`, `approval` and
`clarification` requirements; real HTTP Message Signature and JWT checks; and
an in-memory, auto-approving default with no durable state or real consent UI.

The official sources are not yet pinned and currently expose an important
surface discrepancy:

- the Hellō documentation page lists a single `/aauth/token` endpoint; while
- the current GitHub README describes `/aauth/token/person` and
  `/aauth/token/auth`, discovered through `person_token_endpoint` and
  `auth_token_endpoint` metadata.

The public package file identifies `@hellocoop/mockin`, version `1.4.0`, Node
`~22`, MIT license and repository `https://github.com/hellocoop/mockin.git`,
but the fetched public view may lag the repository. No version or capability
claim may rely on that unpinned view.

## Question to answer

Can the exact pinned Mockin source interoperate with the committed SOGA AAuth
package, and can it preserve SOGA's existing PS-supervision role closely enough
to support a bounded demonstration?

```text
SOGA test agent -> Mockin Person Server -> cryptographic resource gateway
                         ?
                 external SOGA policy hook
```

The question mark is deliberate. If Mockin has no external supervision/policy
hook, this topology removes SOGA from auth-token issuance. Moving governance to
a resource-side check before resource-token issuance is a possible new design
claim, not preservation of the accepted implementation, and requires a later
proposal.

The assessment must separately answer:

1. which exact Mockin commit, package version and lockfile describe the source;
2. which AAuth draft/version and endpoint metadata that source implements,
   compared separately with the SOGA package's pinned `fcf656d` editor source
   and the published `-11` draft;
3. whether its HTTP Message Signature, token type, mission hash, audience,
   requirement, polling and error shapes match the committed SOGA package;
4. whether Mockin can be driven on literal loopback with test-only identities
   and no external runtime fetches;
5. whether Mockin exposes a supervision or policy hook through which an
   external SOGA decision can gate auth-token issuance and permission answers;
6. what source or adapter work would be required without changing SOGA's
   governance boundary, or whether a resource-side SOGA check would constitute
   a separate new design claim;
7. whether the demo should use Mockin, the independent SOGA Person Server, or
   both as an interoperability comparison; and
8. which claims remain out of scope, especially parent/guardian authority,
   child assent/refusal, durable wallet evidence and WAS integration.

## Proposed Phase 0 — exact-source acquisition and source-only assessment

After independent review and separate prospective PI authorization, permit:

1. resolve the exact remote default branch and commit from only
   `https://github.com/hellocoop/mockin.git`;
2. create one clean detached checkout at
   `<repository-parent>/research-evidence/soga/inputs/mockin/<commit>/source`;
3. prohibit submodule, Git LFS and credential-helper acquisition;
4. record origin, full commit, tree, package version, license identity,
   `package-lock.json` SHA-256, Node engine, clean-source state and complete
   file manifest;
5. read the complete AAuth implementation, discovery metadata, package and
   relevant tests without installing dependencies or executing source;
6. restore Dick Hardt's public AAuth editor repository from only
   `https://github.com/dickhardt/AAuth.git` at exact commit
   `fcf656de1926535f5bd6fc0538147ead6646e727`, require
   `draft-hardt-oauth-aauth-protocol.md` SHA-256
   `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`,
   place it at
   `<repository-parent>/research-evidence/soga/inputs/aauth/fcf656d/source`,
   and never substitute upstream `HEAD`;
7. retrieve only `https://www.hello.dev/docs/mockin/`, the exact official
   AAuth draft references named by the pinned Mockin source, and published
   `draft-hardt-oauth-aauth-protocol-11` from `datatracker.ietf.org`, recording
   each exact URL, retrieval time, byte length and SHA-256;
8. produce a standalone repository report containing an endpoint/claim matrix,
   incompatibilities, adapter seams, test plan and recommendation; and
9. add the pinned Mockin and restored `fcf656d` sources to
   `EXTERNAL_INPUT_MANIFEST.md` only after the
   evidence receives blind dual review and PI acceptance.

Network access is limited to Git HTTPS operations against exact origins
`https://github.com/hellocoop/mockin.git` and
`https://github.com/dickhardt/AAuth.git`, and document retrieval from exact
URLs on `www.hello.dev` and `datatracker.ietf.org`. The execution request must
enumerate every URL before access; references discovered outside those hosts
are recorded but not retrieved. No package registry, container registry,
application endpoint or unrelated URL is permitted.

## Required compatibility matrix

The report must compare pinned Mockin source with the exact committed SOGA
package, the restored `fcf656d` editor source governing the SOGA profile, and
published `-11`. Every mismatch must be attributed to SOGA-versus-governing-
source, Mockin-versus-its-declared-source, or intentional version drift. The
matrix must cover:

- Person Server discovery and JWKS;
- bootstrap ceremonies and agent-token binding;
- person-token and auth-token endpoints;
- HTTP Message Signature covered components, `alg`, `keyid`, content digest
  and signature-key rules;
- token `typ`, issuer, audience, expiry and `mission_s256`;
- mission proposal/approval, ownership, active/terminated state, expiry and
  canonical JSON-to-`mission_s256` computation;
- resource-token input and auth-token output;
- three-party PS-issued auth-token mode versus four-party resource-AS mode,
  including which mode each implementation supports;
- the PS supervision/policy hook, the permission endpoint decision source and
  whether external SOGA policy can gate both auth-token issuance and permission
  answers;
- `interaction`, `approval` and `clarification` requirements;
- the party represented by each requirement path, distinguishing the Person
  from approval obtained from another party;
- pending polling, submission, cancellation and terminal outcomes;
- permission grant/denial and denial reasons;
- RFC 9457/problem-details versus other error shapes;
- offline trusted-server/JWKS configuration;
- literal-loopback binding, port selection and shutdown;
- test identity, secret and evidence boundaries;
- audit endpoint and mission/activity logging; and
- R3 behavior as a separately classified, non-required capability.

Every row must be labeled `MATCH`, `ADAPTER REQUIRED`, `BLOCKING MISMATCH`,
`NOT REQUIRED FOR DEMO` or `UNRESOLVED`, with exact source citations.

## WAS and parent-authority boundaries

Mockin and WAS are complementary, not substitutes. Mockin provides a mock
AAuth Person Server surface. WAS provides wallet-controlled storage. No direct
Mockin/WAS connector is documented. A later composition could let a Person
Server consult WAS-held evidence or issue an auth token for a WAS-backed
resource, but that adapter is not part of this assessment.

Mockin can simulate `requirement=approval`; it does not establish that the
approver is a parent or guardian, capture genuine consent, or preserve child
assent/refusal. Those remain explicit governance and protocol research
questions.

## Stop rules

Stop before assessment adoption if:

- either origin, commit, tree, package identity or license cannot be established;
- the exact source requires submodules, LFS, credentials or another origin;
- source inspection requires dependency installation, build or execution;
- the Mockin AAuth surface cannot be tied to an exact source revision;
- the `fcf656d` protocol file does not reproduce its pinned SHA-256;
- published `-11` cannot be pinned by exact URL and byte hash;
- documentation and source disagree without the discrepancy being traced and
  classified;
- any requested URL leaves the permitted official origins;
- the checkout or evidence would overwrite an existing durable path; or
- the SOGA repository or unrelated D-082 preservation material would change.

## Review and decision points

1. **Proposal gate:** blind dual review of this complete proposal.
2. **Assessment evidence gate:** blind dual review of the pinned-source report
   and compatibility matrix.
3. **Topology decision:** PI chooses Mockin, independent SOGA PS, or comparison.
4. **Execution proposal:** only after that choice may a separate proposal name
   exact dependencies, processes, listeners, tests, cleanup and evidence.

## Exclusions

This proposal authorizes nothing by itself. It does not authorize Git or HTTP
access, checkout creation, package or container download, dependency
installation, import, build, lint, test, listener, Mockin execution, SOGA
execution, recovery execution, wallet or WAS integration, personal data,
payment, parent/guardian claims, QR flow, Misty access, physical actuation,
external exposure, G28 or G29.

The D-119 recovery instrument remains committed and unexecuted. The unrelated
PI routine-tool proposal remains excluded and untouched.
