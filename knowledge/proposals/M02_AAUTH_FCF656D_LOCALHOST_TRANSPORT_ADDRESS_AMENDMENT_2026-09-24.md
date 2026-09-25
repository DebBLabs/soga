# M02 AAuth `fcf656d` Localhost Transport-Address Amendment

Date: 2026-09-24
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ c01f571`
Review class: mandatory blind dual review under D-064

## Discovered holdpoint

D-114 requires literal-loopback HTTP transport and also requires served metadata
to reuse the accepted fixture constructors. Its metadata paragraph incorrectly
requires each document's `issuer` to equal the bound
`http://127.0.0.1:<port>` address.

That cannot be implemented while preserving AAuth `fcf656d`:

- `fcf656d` server identifiers require lowercase HTTPS with only scheme and
  host—no port, path, query or fragment;
- `metadata.py` enforces HTTPS for fixture metadata;
- `identifiers.py` enforces HTTPS and no port for server identifiers; and
- `tokens.py` calls that validation on issuance paths.

Changing metadata alone would either leave token `iss` and document `issuer`
inconsistent or require reopening accepted identifier and token rules to create
a deliberate protocol deviation. No D-114 implementation source has been
created and no code has been imported, compiled, linted, tested or executed.

The earlier unaccepted metadata-only amendment is withdrawn and superseded by
this proposal.

## Narrow correction

Preserve the accepted HTTPS AAuth role identifiers in tokens and metadata,
including the existing fixture constructors and validation, byte-for-byte.
Treat `http://127.0.0.1:<ephemeral-port>` only as an injected transport address.

The localhost client receives an explicit immutable mapping from each HTTPS role
identifier to one exact literal-loopback base URL. It must:

- validate the mapping before any request;
- require an exact lowercase `http` scheme, exact host string `127.0.0.1`, an
  explicit decimal port from 1 through 65535 with no leading zero, no user
  information, path, query or fragment;
- require exactly one mapping for the configured Person Server and exactly one
  for the configured resource;
- reject unknown, duplicate or unused role mappings;
- use the transport address only to select the local socket destination; and
- retain the HTTPS role identifier for token issuer/audience, metadata issuer
  and security comparison values; and
- use only the authority component of that HTTPS role identifier—its lowercase
  host, such as `ps.example` or `resource.example`, with no scheme or port—as
  the HTTP Message Signature `@authority`, exactly as in the accepted D-113
  requests.

Each server handler derives `@method` and `@path` from the received HTTP request
line and supplies `@authority` from its own configured HTTPS role identifier.
No method, authority or path value carried in the request body is used for
verification; a body carrying any such extra security field is rejected. The
client cannot influence the server-side authority, and each role verifies
against its own configured host, so cross-role replay fails closed.

The injected mapping is test-only routing data. It is not identity evidence,
authorization evidence, discovery output or an alias asserted by AAuth.

## Metadata and discovery claim

The two localhost GET routes continue to use the exact specification paths:

- `/.well-known/aauth-person.json`; and
- `/.well-known/aauth-resource.json`.

They serve the accepted conformance-shaped fixture documents with their HTTPS
role identifiers, `test_only` and `fixture_role` markers. The endpoint fields in
those documents also remain HTTPS role endpoints. The localhost transport does
not perform issuer-based metadata discovery and does not claim that
`{iss}/.well-known/{dwk}` was resolved over the loopback connection.

The purpose of serving the documents in this sprint is bounded serialization
and route-shape verification only. A later deployment/discovery sprint must map
the real HTTPS identifiers to reachable services without weakening the
identifier rules.

## Source and test impact

No change to `metadata.py`, `identifiers.py`, `tokens.py` or any accepted D-113
source is authorized by this amendment. The transport mapping and validation
live only in the already authorized new file
`m02_aauth_fcf656d/localhost.py`, with positive and negative cases in the already
authorized `tests/test_m02_aauth_fcf656d_localhost.py`.

Tests must cover exact positive mappings and rejection of uppercase schemes,
`localhost`, wildcard or non-loopback hosts, IPv6, missing/zero/out-of-range or
leading-zero ports, credentials, path, query, fragment, unknown roles,
duplicates and unused mappings. They must prove that socket routing uses the
loopback address while signed-request `@authority` remains the exact bare,
lowercase host component of the HTTPS role identifier and all token/metadata
security identifiers remain exact HTTPS role identifiers. They must also prove
that a request body carrying an authority, method or path value is rejected as
an extra security field rather than used in signature verification.

The `AAuth-Requirement` challenge at `/enforce` must carry the exact resource
token produced by the prior successful `/authorize` verification for the same
exchange; it may not synthesize or recover a token from unrelated state.

## Review and authority boundary

Both blind gates must review this complete amendment. If accepted, it becomes
part of the D-114 create-only implementation and the final files are reviewed as
one complete static package. No extra execution or gate is created.

This amendment authorizes nothing. No source modification, import, compilation,
lint, test, listener, execution, dependency operation, network access, external
service, wallet/WAS work, QR flow, Misty access, physical actuation, G28 or G29
is authorized. The unrelated PI routine-tool proposal remains excluded and
untouched.
