# M02 AAuth `fcf656d` Minimal Live Exchange Proposal

Date: 2026-09-24  
Status: PROPOSED — NOT AUTHORIZED  
Prepared at: `main @ 90a34b061def0482e52327bfccbb63453f31a1c1`  
Review class: mandatory blind dual review under D-064

## Purpose and single claim

Implement and execute one bounded, in-memory, three-party AAuth exchange at the
exact editor's-copy commit
`fcf656de1926535f5bd6fc0538147ead6646e727`:

1. an identified agent obtains a person token from its Person Server for one
   resource and mission;
2. the resource verifies that person token before issuing a resource token;
3. the agent submits the resource token and presented person token to the Person
   Server's auth-token function;
4. the Person Server verifies the pair, obtains an explicit supervision
   decision and issues an auth token only after an allow decision;
5. the resource verifies and enforces the auth token; and
6. the same resource rejects a person token where an auth token is required.

The exchange is live in the sense that real Ed25519 JWTs and HTTP Message
Signatures are created and verified through all three roles during one bounded
execution. It is intentionally transport-free: no HTTP listener, socket,
external service or network access is part of this claim.

## Accepted basis

- D-108 accepts all 24 Phase 1 focused tests under the pinned provider.
- The accepted `fcf656d` matrix and Phase 1 sources establish strict Ed25519
  JOSE, `typ` rejection, JWK thumbprints, Structured Fields and HTTP Message
  Signature verification.
- The existing Stage 2 Person Server remains a bounded HMAC-based research
  package. This sprint does not silently convert or mutate it. The AAuth
  exchange is a separate profile that may later connect to Stage 2 through an
  explicit adapter.
- AAuth defines supervision as the Person by default or a supervision server
  delegated to by the Person Server; the PS-to-supervisor wire contract is out
  of scope. This sprint therefore models supervision as an explicit injected
  Person Server decision interface, not as a new AAuth wire protocol.

## Exact protocol profile

The implementation must follow these pinned `fcf656d` rules:

- Agent identifier: exact, case-sensitive `aauth:local@domain` syntax. The
  bounded fixture uses a top-level identifier with no `+` delimiter.
- Agent token: `typ=aa-agent+jwt`, `dwk=aauth-agent.json`, `sub` is the agent
  identifier, `ps` names the Person Server and `cnf.jwk` binds the signing key.
- Person token: `typ=aa-person+jwt`, `dwk=aauth-person.json`, `aud` is the
  resource, directed `sub` is opaque, `cnf.jwk` binds the agent key and
  `mission_s256` is present. It carries no `scope` or `account`.
  Its lifetime must not exceed one hour, the agent token presented with the
  request or, because this bounded profile always uses a mission, that mission's
  expiry.
- Resource token: issued only after the resource verifies the person token and
  its signed request; `typ=aa-resource+jwt`, `dwk=aauth-resource.json`, `aud`
  is the Person Server, and `ps`, `sub`, `presented_jti` and `agent_jkt` are
  copied or derived exactly as specified. `mission_s256` is copied unchanged.
  Its lifetime should not exceed five minutes.
- Auth-token request: signed with the agent token and carries the resource token
  and presented person token. The Person Server verifies resource-token
  audience, agent-key thumbprint, presented-token type/signature/audience/key,
  `presented_jti`, `ps`, `sub` and `mission_s256`, and verifies the mission is
  active before supervision.
- Auth token: issued by the Person Server only after supervision allows;
  `typ=aa-auth+jwt`, `dwk=aauth-person.json`, `aud` is the resource, `ps` is the
  Person Server, directed `sub` and authorized `scope` come from the verified
  resource-token chain, `cnf.jwk` binds the agent key and `mission_s256` is
  copied unchanged. Its lifetime must not exceed one hour, and its expiry cannot
  exceed the agent token, presented person token or mission expiry.
- Resource enforcement: the final signed request presents the auth token; the
  resource verifies exact `typ`, signature, issuer key, audience, confirmation
  key, directed subject, mission continuity and authorized scope before
  allowing. A signed request presenting the person token at the same enforcement
  point must fail closed as the wrong token type.

Every JWT must also carry the accepted common claims and exact fully specified
`Ed25519` algorithm. The implementation must not use the Stage 2 HS256 codec.

## Metadata and identities

The bounded profile uses non-routable test identifiers represented as HTTPS
role identifiers in data only; it opens no listener and performs no discovery
fetch. It must create truthful metadata documents in memory for:

- the agent provider, with `issuer` and `jwks_uri`;
- the Person Server, with the four-field conformance floor: `issuer`,
  `auth_token_endpoint`, `person_token_endpoint` and `jwks_uri`; and
- the resource, with `issuer`, `jwks_uri`, `access_mode=auth-token` and
  `authorization_endpoint`.

All metadata endpoints are descriptive fixtures only. Verification uses
explicitly injected, hash-pinned JWKS documents; no URL is fetched.

The AAuth role fixtures must be produced by new, separately named constructors.
The committed `interim_person_server_metadata` and `assert_interim_metadata`
helpers retain their exact current behavior, including the prohibition on
declaring `person_token_endpoint` and `auth_token_endpoint`; the accepted
`test_metadata_is_truthful_and_incomplete` and
`test_metadata_rejects_false_endpoint_claim` tests must pass unchanged. The new
role fixtures are conformance-shaped test data for this transport-free exchange,
not claims about deployed endpoints, and no code path may substitute either
kind of metadata document for the other.

## Supervision contract

The Person Server must call a bounded interface exactly once after validating
the token chain and before signing an auth token. The input must keep these
origins distinct:

- resource-asserted: resource identity, requested scope, account if any,
  resource-token identifier and expiry;
- Person-Server-verified: person-server identity, directed subject, agent-key
  thumbprint, mission identifier and active/expiry state; and
- agent-asserted: justification and agent identifier from the separately
  verified agent token.

The interface returns an immutable decision containing `ALLOW` or `DENY`, a
decision identifier and a reason code. Only `ALLOW` permits issuance. `DENY`,
malformed output or an exception fails closed and produces no auth token. This
interface demonstrates the AAuth supervision holdpoint; it does not claim a
standard PS-to-supervision-server protocol or yet prove the SOGA governance
engine adapter.

## Proposed source and tests

After proposal acceptance, one create-only phase may add or modify only:

- `m02_aauth_fcf656d/identifiers.py` — bounded agent/server identifier checks;
- `m02_aauth_fcf656d/tokens.py` — role-specific claim construction and strict
  verification using the accepted JOSE primitives;
- `m02_aauth_fcf656d/exchange.py` — in-memory Agent, Person Server and Resource
  roles plus the explicit supervision interface;
- `m02_aauth_fcf656d/metadata.py` — extend the existing truthful metadata
  helpers for the three exact role fixtures without weakening existing checks;
- `tests/test_m02_aauth_fcf656d_exchange.py` — complete exchange, refusal and
  negative-chain tests; and
- a later bounded controller under `tools/m02_aauth_fcf656d/`, created only
  after the source and tests are statically accepted.

Existing Phase 1 files may be imported but not modified, except the named
metadata extension. The Stage 2 Person Server and every WAS, wallet, mission,
Misty and runtime-governance file remain byte-identical.

## Required tests and negative cases

Static design and later execution evidence must cover, at minimum:

1. exact case-sensitive agent-identifier acceptance, including that `+` is a
   syntactically valid local-part character; rejection of malformed identifiers
   as syntax errors; and separate, distinguishable refusal of a syntactically
   valid sub-agent identifier containing `+` as out of this profile, because
   this sprint implements no sub-agent behavior;
2. truthful role metadata and public-only, algorithm-pinned JWKS;
3. successful person-token issuance only for an active retained mission and a
   verified agent-signed request;
4. successful resource-token issuance only after verified person-token type,
   signature, audience and confirmation-key binding;
5. unchanged `mission_s256` and directed `sub` across person, resource and auth
   tokens;
6. exact `presented_jti`, `ps`, `agent_jkt`, issuer, audience and expiry-chain
   checks at the Person Server, including rejection of person or auth tokens
   whose `exp - iat` exceeds one hour or whose expiry exceeds its governing
   token or mission ceiling, and the profile's five-minute resource-token
   issuance limit;
7. exactly one supervision call after all token-chain checks and before auth
   token signing;
8. no auth token on supervision deny, exception or malformed decision;
9. successful resource enforcement only for a verified auth token with correct
   audience, key, subject, mission and scope;
10. explicit rejection of a person token at the auth-token enforcement point;
11. fail-closed rejection for each independently altered chain binding:
    `typ`, signature, `aud`, `ps`, `sub`, `presented_jti`, `agent_jkt`,
    `mission_s256`, scope, expiry and confirmation key;
12. proof that no complete token, private key or signature is written to test
    output or durable evidence; and
13. byte identity of the accepted Stage 2 Person Server, Phase 1 package files
    not named above, and unrelated integration packages.

Tests must use deterministic clocks and identifiers. Generated private key and
signature material remains memory-only.

Requiring `mission_s256` in test 3 is a deliberate narrowing of this bounded
profile. AAuth permits a person token without a mission; this sprint does not
claim otherwise. The wrong-token refusal in test 10 models the resource's
fail-closed authorization decision. A transport deployment would express that
decision as the applicable `401` plus `AAuth-Requirement`; this transport-free
profile does not claim to test that response serialization.

## Review and execution sequence

1. Gate 1 reviews this complete proposal for exact `fcf656d` fidelity and
   implementation precision. Gate 2 independently reviews security boundaries,
   negative cases and test completeness. Each reports all blockers in its first
   pass and separates optional improvements.
2. After PI acceptance, create the complete source and tests only. Do not
   import, compile, lint, test or execute them.
3. Both blind gates review every complete created file. Mechanical corrections
   receive hash-pinned diff-only rechecks.
4. After PI acceptance and commit of the static package, create one bounded
   execution controller. Both gates review the complete controller.
5. A separate prospective PI decision may authorize exactly one execution. No
   automatic retry. Both gates review the resulting evidence before acceptance.

This is three claim-sized gates: proposal, complete static package, and one
execution/evidence cycle. It is not a gate per file or per token.

## Stop rules

Stop if exact `fcf656d` requirements cannot be implemented without inventing a
wire rule; if a new dependency, network access, listener, external service,
production credential, personal data or permission change is required; if
supervision inputs cannot preserve assertion provenance; if any token can be
issued before its required verification/decision; or if evidence cannot remain
free of complete tokens, private keys and signatures.

Any later execution stops as a gated negative on timeout, output overflow,
unexpected stderr, import escape, mutation, failed/errored/skipped test or
nonzero exit. Preserve evidence and do not retry automatically.

## Claim boundary and exclusions

A positive result would establish one bounded, transport-free, three-party
AAuth `fcf656d` exchange with explicit supervision and wrong-token refusal. It
would not establish full protocol conformance, metadata discovery, HTTP server
interoperability, four-party AS federation, deferred interaction, clarification,
revocation, a standardized supervision protocol, representative authority,
affected-person consent, wallet/WAS integration, QR admission or Misty
operation.

This proposal authorizes nothing. No source creation, modification, import,
compilation, lint, test, execution, dependency operation, network access,
listener, external service, personal data, payment, wallet/WAS work, Misty
access, physical actuation, G28 or G29 is authorized. The unrelated PI
routine-tool proposal remains excluded and untouched.
