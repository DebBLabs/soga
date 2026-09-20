# M02 AAuth `-11` Conformance Gap at `fcf656d`

Date: 2026-09-20
Status: SOURCE-VERIFIED RESEARCH DRAFT — NOT YET INDEPENDENTLY REVIEWED; NO IMPLEMENTATION AUTHORITY

## Source and method

Primary source: Dick Hardt's public `AAuth` editor repository, detached at exact
commit `fcf656de1926535f5bd6fc0538147ead6646e727`, authored 2026-09-14
(`Chaining: reject when the PS cannot identify the calling agent`). The protocol
source `draft-hardt-oauth-aauth-protocol.md` has SHA-256
`295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`.
The local commit range contains **43 commits** after `b6ca19b`, not 25.

Claims below were checked against that exact source and the current SOGA tree at
`72c70f1e706f26c1910cd4903defe613c7b8491c`. This report distinguishes the
protocol's normative requirements from examples and from SOGA design choices.

## Corrections to the preliminary September 18 findings

1. Every AAuth party MUST support `Ed25519`; `alg` is required and fully
   specified, while `EdDSA`, `none`, and symmetric algorithms MUST NOT be used.
   The protocol does not say Ed25519 is the only permitted fully specified
   asymmetric algorithm. SOGA's `HS256` tokens are nevertheless nonconformant.
2. `requirement=approval` means the server is obtaining approval without
   requiring agent-directed user action. It can cover administrator, resource
   owner, compliance, or an established direct-user channel. It is not a token
   meaning only “supervisor clearance.” `requirement=interaction` means the
   agent must direct or relay user action.
3. The exact range from `b6ca19b` to `fcf656d` is 43 commits, of which 25
   touch `draft-hardt-oauth-aauth-protocol.md`. Both counts are correct for
   their scope; the preliminary note did not name that scope.

## Verified `-11` requirements material to SOGA

- A mission is identified by the PS and the hash of immutable approved mission
  JSON. `approver` and the `AAuth-Mission` header are removed.
  `mission_s256` flows in person, resource, and auth tokens. When a resource
  token names a token that carried a mission, the hash is copied unchanged.
- A conformant PS publishes four required metadata fields: `issuer`,
  `auth_token_endpoint`, `person_token_endpoint`, and `jwks_uri`.
- A resource MUST verify a person token or auth token before issuing a resource
  token. The resource token carries `ps`, `sub`, `presented_jti`, `agent_jkt`,
  and the copied mission hash where present. The agent sends the resource token
  and the token it presented to the PS auth-token endpoint.
- The PS verifies both tokens together, including type, issuer, audience,
  confirmation key, `presented_jti`, person, tenant and mission consistency.
  It verifies that a named mission exists, belongs to the agent, is active, and
  has not passed `expires_at`. The PS then issues an auth token directly in the
  three-party mode or obtains one from the resource's AS in four-party mode.
- Token `typ` is security-critical: `aa-person+jwt`, `aa-resource+jwt`, and
  `aa-auth+jwt` are distinct. A person token MUST be rejected wherever an auth
  token is required; the draft explicitly describes omission as fail-open.
- A valid JWT signature is not enough. The resource also checks `aud`, binds
  `cnf.jwk` to the request-signing key, and associates `(iss, sub)` with the
  person record.
- The PS MUST visually or structurally distinguish resource-asserted material
  from agent-asserted material, attribute the latter, and MUST NOT decide only
  from agent assertions when resource assertions cover the same operation.
- The permission endpoint and mission `approved_tools` govern local actions but
  do not enforce them. `approved_tools` is an agreement/audit record. The auth
  token is AAuth's hard control for remote resources. A SOGA gateway can impose
  an additional local execution boundary, but that is SOGA enforcement, not a
  protocol claim that AAuth enforces tool dispatch.
- An interaction code is correlation only and MUST NOT authorize a decision.
  QR participant admission is therefore a separate SOGA mechanism.
- An approval/consent endpoint reachable beyond a single-user local deployment
  MUST authenticate the approving party. The loopback exemption requires local
  trust and OS-level access controls.
- How a PS consults a supervision server is out of scope and a companion
  protocol is TBD. Supervision may remain internal to the PS.

## Current SOGA package: what is established

`m02_person_server` is accurately labelled a bounded, loopback, test-only
Person Server. It persists missions, test person tokens, revocation, pending
approval, re-evaluation and evidence. It reconstructs live expiry/revocation
inputs and can feed the SOGA execution-governance engine. `mission_s256` is
already carried through its test token and permission path. None of those
results should be discarded.

The existing synthetic Person Server/WAS composition establishes that a
bounded decision result can be written to and read from the socket-free WAS
backend. It does not establish AAuth conformance, a live wallet presentation,
or remote-resource enforcement.

## Blocking conformance gaps

1. **Cryptography and token types.** `m02_person_server/crypto.py` deliberately
   emits `HS256` with generic `typ: JWT`. Symmetric algorithms are prohibited;
   the required AAuth token types and JWKS-based verification are absent.
2. **HTTP Message Signatures and agent tokens.** Requests use a test HMAC over
   canonical JSON with an `agent_id` field, not the AAuth HTTP Signature and
   `Signature-Key` agent-token profile.
3. **PS metadata floor.** Current metadata publishes `issuer`,
   `permission_endpoint`, and test-only fields. It lacks the required
   `auth_token_endpoint`, `person_token_endpoint`, and `jwks_uri` fields.
4. **Endpoint shape.** Person-token issuance, agent registration, mission
   retention, revocation and pending resolution are `_test` operator endpoints.
   There is no conformant person-token endpoint, PS auth-token endpoint, mission
   endpoint, interaction flow, JWKS endpoint, or AAuth revocation endpoint.
5. **Resource side.** There is no AAuth resource implementation issuing a
   signed `aa-resource+jwt`, binding it to the presented token by
   `presented_jti`, or verifying an `aa-auth+jwt` before dispatch.
6. **Auth-token issuance.** The PS neither verifies a resource token plus its
   `presented_token` nor issues `aa-auth+jwt`. The real three-party authorization
   sequence is therefore absent.
7. **Mission lifecycle.** The package accepts a supplied `mission_s256` and
   retained mapping. It does not yet implement the `-11` proposal/approval,
   ownership, active/terminated state, update log, completion, expiry, and
   computed canonical mission-hash lifecycle. In particular, it does not bind
   token lifetime to the mission: `-11` requires a person token carrying
   `mission_s256` not to outlive the mission's `expires_at`, a PS-issued auth
   token carrying it not to expire later than the mission, and each PS decision
   path acting on a mission to require it to remain active and unexpired.
   `issue_person_token` currently computes `exp` from the requested lifetime
   without consulting mission expiry. Its one-hour maximum already aligns with
   the independent person-token lifetime ceiling.
8. **Consent provenance.** Current pending approval is a useful local control,
   but it does not yet implement the `-11` distinction and presentation rules
   for resource-asserted versus agent-asserted content.
9. **Permission semantics.** Current code directly treats `approved_tools` as a
   dispatch eligibility rule. SOGA may intentionally enforce that stricter
   rule, but it must be labelled a SOGA gateway policy rather than attributed
   to AAuth protocol enforcement.
10. **Revocation shape.** Local retained-token revocation is implemented. The
    `-11` revocation endpoint is RECOMMENDED for a PS and SHOULD be provided; it
    is therefore a gap below the conformance floor rather than a floor
    violation. Its signed POST carries `jti` and `exp`, both REQUIRED. `iss` is
    deliberately not a body parameter: it comes from the verified signature,
    while retained revocation state is keyed by `(iss, jti)`. The downstream
    person-token/auth-token cascade is also absent.

## Smallest credible San Francisco path

The objective is not “complete AAuth.” It is one real, repeatable,
mission-bound three-party flow for a synthetic Misty resource:

1. Pin all conformance claims and fixtures to `fcf656d`.
2. Add fully specified asymmetric signing with mandatory Ed25519 support,
   AAuth `typ` values, local JWKS, rejection of keys whose `kty` or `crv`
   disagrees with `alg`, and strict wrong-type rejection tests—including a
   person token presented where an auth token is required.
3. Add signed-agent request verification and truthful interim metadata without
   claiming the PS conformance floor before both required token endpoints
   exist. HTTP signatures cover `@method`, `@authority`, `@path`, and
   `signature-key`; requests with bodies to PS endpoints additionally cover
   `content-digest` and `content-type`.
4. Create and approve one immutable Misty Tip Jar mission and compute its
   `mission_s256`; preserve the current governance record while aligning the
   mission lifecycle needed for the demonstration.
5. Implement person-token issuance to the synthetic Misty resource, with a
   directed `sub` per resource, `exp` capped at one hour and at the mission's
   `expires_at`, and refusal when the mission is not active.
6. Implement the resource authorization boundary: verify person token, issue a
   resource token with a lifetime of no more than five minutes, and bind the
   request to the presented token and agent key.
7. Implement the PS auth-token endpoint: verify the resource/presented pair,
   verify the named mission is active and unexpired, evaluate consent and
   mission context, and issue a typed auth token expiring no later than the
   presented token or the mission's `expires_at`.
8. Require the synthetic resource gateway to verify the auth token and request
   key binding before it records dispatch. Demonstrate rejection of a person
   token at this boundary, plus expiry or revocation.
9. Store the resulting authorization and execution evidence in WAS using the
   already demonstrated socket-free composition. WAS storage supports the
   sequence; it is not the purpose of the demonstration.

The QR code remains a separate participant-admission/correlation mechanism and
must never carry a robot credential or directly expose the Misty API. Physical
Misty execution, wallet presentation, representative authority, affected-person
consent/refusal and public deployment remain separately gated. A reliable
terminal demonstration of this real AAuth path is the San Francisco minimum;
recorded physical footage may be added only after its own safety gates.

## Immediate next decision

Independently review this source assessment before adopting it. If accepted,
prepare a prospective implementation proposal for steps 1–3 only: crypto/token
types, truthful interim metadata, and request-verification foundation. Preserve
all accepted Stage 2 fixtures and evidence while creating the new path. Do not rewrite the
current test-only package in place without preserving its accepted evidence and
claim boundary. No implementation, dependency addition, candidate execution,
network listener, wallet, Misty, G28 or G29 work is authorized by this report.
