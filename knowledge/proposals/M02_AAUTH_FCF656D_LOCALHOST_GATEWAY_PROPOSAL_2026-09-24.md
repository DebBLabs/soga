# M02 AAuth `fcf656d` Localhost Transport and Gateway Proposal

Date: 2026-09-24
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ b18995d0e4a155f099f83ca55ee08359a09f1984`
Review class: mandatory blind dual review under D-064

## Purpose and single claim

Prove that the exact D-113 transport-free AAuth exchange can cross real,
literal-loopback HTTP boundaries and remain fail-closed at the resource
execution boundary while SOGA supplies the Person Server's supervision
decision.

One bounded test process will contain three distinct roles:

1. an agent client;
2. a Person Server HTTP surface; and
3. a resource HTTP surface that is the enforcement gateway.

The agent will request a person token, request a resource token, request an auth
token after SOGA supervision, and present the auth token to the resource. The
resource will allow the bounded semantic action only after the exact D-113
verification chain succeeds. The same endpoint will reject a person token where
an auth token is required.

This is a localhost protocol-integration proof. It is not a public service,
production deployment, wallet flow, WAS flow, QR flow or robot action.

## Accepted basis

- D-113 accepts 35/35 bounded tests for the exact transport-free minimal AAuth
  exchange under the pinned Ed25519 provider.
- `m02_aauth_fcf656d.exchange` already owns token issuance, signed-request
  verification, `mission_s256` continuity, supervision ordering and final
  resource enforcement. This sprint must wrap those accepted roles rather than
  duplicate their security decisions in HTTP handlers.
- `m02_person_server.http_server` and `g27_tip_jar.localhost` establish local
  repository patterns for literal `127.0.0.1`, ephemeral ports, bounded JSON,
  no-store responses, finite client timeouts, quiet handlers and complete
  shutdown. They are patterns only; their HMAC/test-person-token protocols are
  not AAuth `fcf656d` and must not be reused as protocol evidence.
- `engines.aauth_execution_runtime_bridge.evaluate_aauth_execution_request`
  is the existing SOGA governance bridge. It accepts explicit verified live
  authority state and returns the governance determination plus canonical
  decision package. If that state is omitted, the bridge silently uses a
  compatibility-only default path; this profile forbids that fallback and must
  always pass the explicit argument.

## Architecture and trust boundaries

### Agent client

The client is an explicit test-only state machine. It sends JSON requests over
HTTP to exact injected base URLs and follows no redirects. It accepts only
literal `http://127.0.0.1:<ephemeral-port>` URLs, uses finite two-second request
timeouts, sets `Content-Type: application/json`, bounds response bytes and
rejects non-object JSON.

The client constructs the same Ed25519-signed request objects used in D-113.
Complete tokens and signatures remain memory-only and must not appear in logs,
exceptions or durable evidence.

### Person Server HTTP surface

The Person Server surface exposes only:

- `GET /.well-known/aauth-person.json`;
- `POST /person-token`; and
- `POST /auth-token`.

The POST body transports the exact signed-request fields required to reconstruct
the accepted `Request` value. The handler performs only bounded parsing and
calls the accepted `PersonServer.person_token` or `PersonServer.auth_token`
method. It must not issue a token, infer identity, decide supervision or weaken
verification itself.

### Resource enforcement gateway

The resource surface exposes only:

- `GET /.well-known/aauth-resource.json`;
- `POST /authorize`; and
- `POST /enforce`.

`/authorize` calls the accepted `Resource.authorize` method. `/enforce` calls
the accepted `Resource.enforce` method with the configured subject,
`mission_s256` and required scope. An allow response is emitted only after
`Resource.enforce` returns verified auth-token claims. The handler must never
translate malformed, wrong-type, denied or unverifiable input into success.

The enforcement response is a synthetic receipt containing only bounded public
identifiers and `authorization=allowed`. It dispatches no tool and performs no
physical or external action.

### SOGA supervision adapter

The Person Server receives a new injected supervisor adapter. It maps the
accepted, provenance-separated supervision input into an AAuth execution
request for `evaluate_aauth_execution_request` and supplies an explicit
`verified_authority_state` fixture owned by this bounded profile.

The fixture must contain all seven bridge-required fields: `revoked`, `expired`,
`delegation_hops`, `max_delegation_hops`, `elapsed_seconds`,
`max_elapsed_seconds` and `attenuated`. It must also carry `source`,
`observed_at` and `unavailable`, and must be validated before the bridge is
called. No bridge compatibility defaults may be used. The implementation must
record the exact derivation or policy basis for each value. `expired` is derived
from successful token verification; this top-level, no-sub-agent profile
establishes `delegation_hops=0`; limits are explicitly profile policy; and
elapsed time must name its selected clock basis. `revoked` is unavailable
because this profile implements no revocation endpoint. `attenuated` has no
AAuth counterpart and is unavailable unless separately established as profile
policy. Any fact not established by the token chain or declared profile policy
must be listed in `unavailable`, never silently invented.

The execution request policy must list every unavailable fact that is required
for an allow decision in `required_authority_facts`. The bridge's existing
intersection check then fails closed before governance evaluation. A bounded
positive test may use a policy that does not require a fact only when that
non-requirement is explicit and independently reviewed; the unavailable marker
remains present in the canonical evidence. Creation stops if this separation
cannot be preserved.

The adapter returns `SupervisionDecision("ALLOW", ...)` only when SOGA returns
`governance_determination == "ALLOW"`. `RESTRICT`, `DENY`, exceptions,
malformed results or missing canonical evidence become `DENY` and produce no
auth token. Resource-asserted, Person-Server-verified and agent-asserted values
remain distinguishable in the bridge input and evidence.

## HTTP profile and failure behavior

- Bind only literal `127.0.0.1` with port `0`; reject hostnames, wildcard,
  non-loopback and IPv6 for this profile before binding.
- Use only Python standard-library HTTP facilities already in the repository;
  add no dependency.
- Limit request and response bodies to 64 KiB and require an exact nonnegative
  decimal `Content-Length`.
- Require `application/json`; reject duplicate or unsupported security fields
  through exact body-field sets.
- Never follow redirects and emit none.
- Every response carries `Cache-Control: no-store`, exact JSON content type and
  length.
- A `401` caused by HTTP Message Signature or `Signature-Key` token verification
  failure carries `Signature-Error: error=<code>`, using only the existing
  `SignatureProfileError` code space.
- A wrong-token `401` at `/enforce` carries
  `AAuth-Requirement: requirement=auth-token; resource-token="<token>"` with
  the exact verified resource token for this exchange. The token remains
  memory-only and is redacted from logs and evidence. The payment-required
  `402` variant is deliberately outside this non-payment profile.
- Unknown path or method returns 404/405 without fallback.
- Authentication or token verification failure returns 401; a verified but
  unauthorized final request returns 403; malformed input returns 400; internal
  exceptions fail closed with a generic 500 and no secret-bearing detail.
- Error bodies contain stable codes and stages, never complete tokens,
  signatures, private/public key coordinates or raw exception text.
- Start both servers inside one bounded test process, record their assigned
  literal-loopback ports, and always call `shutdown`, `server_close` and bounded
  thread joins in `finally` blocks.

## Proposed source and tests

After proposal acceptance, one create-only phase may add or modify only:

- `m02_aauth_fcf656d/localhost.py` — strict JSON codec, literal-loopback server
  factories, Person Server and resource handlers, and finite agent client;
- `m02_aauth_fcf656d/soga_supervision.py` — the narrow SOGA supervision adapter
  and explicit verified-authority-state validation;
- `tests/test_m02_aauth_fcf656d_localhost.py` — complete transport,
  supervision, enforcement, refusal and cleanup tests; and
- existing `m02_aauth_fcf656d/__init__.py` only if required to export the new
  public test-profile types.

Both GET routes must reuse the accepted conformance-shaped fixture constructors
in `m02_aauth_fcf656d.metadata`; they must not introduce a second metadata
builder. Each document's `issuer` must equal the actual bound literal-loopback
base URL, and its `test_only` and `fixture_role` markers remain present. This
makes every token's `dwk` name coherent with `{iss}/.well-known/{dwk}`.

The accepted D-113 sources and tests otherwise remain byte-identical. The
existing HMAC `m02_person_server`, WAS integration, G27 mission runtime, wallet,
QR and Misty packages remain byte-identical.

A later controller may be proposed only after the complete static package
passes both blind reviews.

## Required tests and negative cases

The complete static design and later execution evidence must cover:

1. one successful four-hop localhost flow: person token, resource token, SOGA-
   supervised auth token and resource enforcement;
2. unchanged `mission_s256`, directed subject, confirmation-key binding and
   scope across the HTTP-carried chain;
3. proof that SOGA is called exactly once, after token-chain verification and
   before auth-token signing;
4. proof that only SOGA `ALLOW` becomes `SupervisionDecision("ALLOW", ...)`;
5. SOGA `RESTRICT`, `DENY`, malformed output and exception each fail closed and
   produce no auth token;
6. a person token at `/enforce` receives 401 with the exact
   `AAuth-Requirement` auth-token challenge and never an allow receipt;
7. altered token type, signature, audience, mission, subject, key binding,
   scope and expiry each fail before enforcement;
8. malformed JSON, non-object JSON, wrong content type, missing/invalid/oversize
   length, unknown route, unsupported method and extra security field rejection,
   plus exact `Signature-Error` codes on signature-verification failures;
9. no redirect following or emission;
10. literal-loopback-only binding and client URL validation;
11. exactly one semantic allow receipt, with no tool dispatch, external side
    effect or physical outcome claim;
12. bounded server shutdown and no remaining listener or server thread after
    every success and failure case;
13. no complete token, signature, key coordinate or raw sensitive exception in
    test output or durable evidence;
14. byte identity of all accepted D-113 files not explicitly named for change;
    and
15. regression passage of the existing 35-test D-113 suite unchanged.

Tests use deterministic clocks, identifiers, mission data and injected SOGA
outputs. Tests may bind ephemeral literal-loopback ports only during a later,
separately authorized execution.

## Review and execution sequence

1. Gate 1 reviews this full proposal for `fcf656d` fidelity, HTTP mapping and
   compatibility with the accepted exchange. Gate 2 independently reviews the
   network boundary, fail-closed behavior, test completeness and cleanup. Each
   returns all blockers in its first pass and separates optional observations.
2. After PI acceptance, create the complete source and tests only. Do not
   import, compile, lint, test, bind or execute them.
3. Both blind gates review every complete file. Corrections remain create-only
   and receive hash-pinned recheck.
4. After PI acceptance and commit of the static package, create one bounded
   execution controller and evidence plan. The controller must receive blind
   dual static review before commit or execution.
5. A separate prospective PI decision may authorize exactly one execution with
   ephemeral literal-loopback listeners. No automatic retry. Both gates review
   the resulting evidence before acceptance.

This is one proposal gate, one complete static-package gate and one controller/
execution-evidence gate—not a gate per endpoint or file.

## Stop rules

Stop if the exact AAuth wire mapping is absent from `fcf656d` and would need to
be invented; if the SOGA bridge requires an authority-state claim the accepted
token chain and explicit bounded fixture cannot honestly establish; if the
gateway can return allow without the exact auth-token verification; if the
Person Server can issue an auth token before SOGA ALLOW; if any code needs a
non-loopback address, fixed port, redirect, new dependency, external service,
production credential, personal data or broader permission; or if complete
tokens, signatures or key material cannot be excluded from evidence.

Any later execution stops as a gated negative on failed preflight, unavailable
pinned provider, occupied/invalid binding, timeout, output overflow, unexpected
stderr, listener escape, incomplete cleanup, mutation, failed/errored/skipped
test or nonzero exit. Preserve bounded evidence and do not retry automatically.

## Claim boundary and exclusions

A positive result would establish one bounded localhost HTTP transport for the
D-113 minimal AAuth exchange, with SOGA supervision and resource-boundary
enforcement. It would not establish complete AAuth conformance, public network
deployment, standardized PS-to-supervisor transport, production identity,
representative authority, affected-person consent, deferred interaction,
clarification, wallet or Freewallet integration, live ZCAP/WAS routing, QR
admission, payment, Misty operation or physical execution.

This proposal authorizes nothing. No source modification, import, compilation,
lint, test, listener, execution, dependency operation, network access, external
service, personal data, wallet/WAS work, QR flow, Misty access, physical
actuation, G28 or G29 is authorized. The unrelated PI routine-tool proposal
remains excluded and untouched.
