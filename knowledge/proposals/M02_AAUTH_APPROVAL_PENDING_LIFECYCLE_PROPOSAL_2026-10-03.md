# M02 AAuth Approval-Pending Lifecycle Proposal

Date: 2026-10-03
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ 8e83a3c3c3ea67f389a2daa2d4ae6bfb6fc4fc77`
Review class: mandatory blind dual review under D-064

## Purpose and corrected ownership

Add the first complete AAuth `requirement=approval` deferred-response lifecycle
to the D-132-accepted localhost fixture. This stage keeps the Person Server's
existing responsibility unchanged: it issues an auth token only after SOGA
supervision. The resource then holds a directed invocation while it obtains a
separate other-party decision through an out-of-band resource channel.

This allocation follows the governing AAuth editor source at pinned commit
`fcf656de1926535f5bd6fc0538147ead6646e727`, specifically the Approval
Pending and Deferred Responses text recorded at source lines 2184–2280. The
later published `-11` draft independently confirms the same rules in Sections
11.6.4 and 11.8–11.8.4:

- Section 11.6.4 permits a server obtaining approval from another party without
  agent-directed user interaction to return `202 Accepted` with
  `requirement=approval`, `Location` and `Retry-After`;
- Sections 11.8.2–11.8.4 require same-origin `Location`,
  `Cache-Control: no-store`, polling with `GET`, respect for `Retry-After` and
  terminal `200`, `403`, `408` and `410` handling; and
- the held invocation is not resubmitted during polling.

The parent/other-party input is not the AAuth Person represented by the Person
Server. This stage must not merge that input into Deb's authority, withhold the
auth token on its behalf, call it verified identity or legal authority, or
claim that AAuth defines who may act as a parent.

## Additive implementation package

After blind dual review and prospective PI authorization, create only:

1. `m02_aauth_fcf656d/approval_pending.py`;
2. `tests/test_m02_aauth_approval_pending.py`; and
3. `tools/m02_aauth_fcf656d/run_approval_pending_tests.py`.

Do not modify any D-132-accepted source or test. The implementation may use the
accepted localhost handler factory to derive an additive handler that routes
pending `GET` requests, while all existing POST, metadata, error and connection
behavior remains inherited unchanged.

## Exact deferred lifecycle

### Initial directed invocation

The resource first completes the accepted AAuth auth-token, HTTP-signature,
mission, subject and scope checks. If the directed action lacks a currently
active exact other-party receipt, it creates one finite pending record bound to:

- a cryptographically random, opaque pending identifier;
- the exact resource origin and same-origin pending path;
- the authenticated agent key and exact auth-token `jti`;
- participant, mission, scope and the held action body;
- creation and expiry times; and
- the initial explicitly unverified decision state.

The bounded profile permits at most 32 live pending records and gives each a
120-second lifetime, strictly shorter than the fixture's 300-second auth-token
lifetime. A 33rd live request creates no record and fails with controlled
`503` plus `Retry-After: 1`.

It returns exactly:

- `202 Accepted`;
- `AAuth-Requirement: requirement=approval`;
- same-origin relative `Location: /pending/{opaque-id}`;
- finite integer `Retry-After` (zero in the bounded test profile);
- `Cache-Control: no-store`; and
- body `{ "status": "pending" }`.

Ambient `misty.acknowledge_tip` remains outside this lifecycle and continues to
complete without consulting or creating other-party state.

### Out-of-band decision boundary

The pending store exposes no HTTP route that an agent can use to approve,
deny, withdraw or identify an approver. Tests and later operator integration
may call a narrow in-process resource-owned decision method. Its input must be
an exact `OtherPartyApprovalReceipt` retaining:

- `asserted_role="parent"`;
- `assurance="unverified-demo-input"`;
- exact participant, mission and directed scope binding;
- explicit source, observed and expiry times; and
- `APPROVED` or `WITHDRAWN` state.

This method represents an unimplemented out-of-band resource channel. It is not
an authentication mechanism and is not reachable by the agent.

### Signed polling and terminal behavior

The agent polls the exact same-origin `Location` using signed `GET`, no body,
and the same auth token/key binding as the held invocation. The additive client
sends the three signature fields (`Signature-Key`, `Signature-Input` and
`Signature`) as real HTTP headers and sends neither body nor `Content-Length`,
`Content-Type` or `Transfer-Encoding`. The additive handler:

- rejects any body-framing header, missing or duplicate signature header;
- limits each signature field to 16,384 encoded bytes and their aggregate to
  the accepted 65,536-byte HTTP bound;
- extracts only those three security headers, ignoring ordinary HTTP transport
  fields such as `Host` and `Accept-Encoding`;
- constructs `Request("GET", surface.authority, exact_path, headers, b"")`,
  using the configured canonical resource authority and never the received
  `Host`; and
- verifies with `body_request=False` before revealing pending state.

The resource verifies the HTTP signature and auth token before revealing the
record. An unknown pending identifier or mismatched token/key returns an
indistinguishable `404` with identical headers and body.

Every poll uses a distinct integer signature `created` value. The bounded test
clock advances one second per legitimate poll while remaining inside the
accepted signature freshness window and before both pending and auth-token
expiry. The pending endpoint owns a bounded replay cache keyed by the accepted
signature tuple and scoped to the pending store; an exact resend is rejected,
while a freshly signed later poll is allowed. Replay entries are bounded by the
accepted maximum of 1,024, pruned by the signature freshness window, and
discarded when the corresponding pending record terminates or expires.

- unresolved exact record: `202`, `status="pending"`, `Retry-After` and
  `Cache-Control: no-store`;
- active exact approval: freshly re-evaluate the resource-side policy, complete
  the held authorization result once and return the same controlled success
  fields as directed `/enforce`, including the decision receipt, with `200`;
- withdrawn or otherwise denied exact decision: terminal `403`;
- expired pending record: terminal `408`;
- any request after a terminal response: `410` and no repeated completion.

Every store lookup and transition is guarded by one explicit lock; terminal
selection and completion occur atomically so concurrent polls cannot complete
an action twice. The implementation does not use the accepted surface's shared
`last_decision` attribute to communicate between threads. Concurrent pending
records remain independent. Polling never resends or replaces the original
action body. A new invocation after withdrawal creates a new pending decision
and may not reuse an earlier approval or terminal result.

The pending lifetime ends before the held auth token expires, allowing an
authenticated poll to observe terminal `408`. An already-expired or otherwise
invalid polling auth token fails authentication and reveals no pending state.
`Prefer: wait`, `429` linear backoff and RFC 9457 error-body migration are
outside this bounded profile; accepted controlled JSON error shapes remain in
use, so no broader conformance is claimed.

## Required tests

The additive suite must prove in one batch:

1. exact `202` approval headers, body and same-origin location;
2. ambient action completes without a pending record or approval-policy call;
3. a signed GET with the same auth token/key observes pending state;
4. polling sends no original action body;
5. active exact approval produces one `200` completion;
6. withdrawn/denied state produces terminal `403`;
7. expiry produces terminal `408`;
8. a repeated poll after any terminal response produces `410` and never
   completes twice;
9. unknown IDs and mismatched token/key bindings produce indistinguishable
   `404`;
10. unsigned, stale, exact-replayed and malformed poll signatures fail closed,
    while a newly signed later poll to the same location succeeds;
11. participant, mission, scope and time mismatches cannot approve;
12. concurrent pending records remain isolated, terminal transitions are
    atomic, and the 32-record capacity fails closed without creating a record;
13. SOGA DENY, RESTRICT, malformed result or exception still prevents auth-token
    issuance before this resource lifecycle is reached;
14. the out-of-band decision method has no agent HTTP route;
15. all D-132 source/test hashes remain unchanged; and
16. the complete accepted 65-test baseline plus exactly sixteen new test
    methods passes under the bounded runner (81 total).

The runner must pin every D-132 source/test hash plus the complete new package,
use the accepted durable provider manifest, permit only literal `127.0.0.1`
ephemeral listeners, impose the existing 90-second and 2,000,000-byte limits,
prohibit retry, verify pre/post immutability, redact secrets and write once to
the absent durable directory:

`/Users/debb/dev/research-evidence/soga/executions/approval-pending-v1`

## Review and execution sequence

1. Both blind gates review this complete proposal once and list all blockers in
   the first pass, separating optional improvements.
2. After PI acceptance, create the entire three-file package without importing,
   compiling, linting, testing or executing it.
3. Both blind gates review all complete files in one static round. A mechanical
   correction is rechecked only by the gate that raised it.
4. After PI acceptance and commit, a separately reviewed prospective decision
   may authorize exactly one bounded execution.
5. Both blind gates review the resulting evidence before PI acceptance.

## Claim boundary and exclusions

A positive result may establish only that the bounded localhost resource can
hold a directed invocation, emit and resolve the AAuth `requirement=approval`
deferred lifecycle, authenticate the polling agent, and keep the separate
unverified other-party decision necessary but insufficient alongside AAuth and
SOGA.

It does not establish the approver's identity, parent/guardian status or legal
authority; consent, assent or refusal precedence; a production approval
channel; complete AAuth conformance; QR, wallet/WAS, phone, presentation or
Misty integration; physical action; G28; or G29.

This proposal authorizes nothing by itself. No implementation, import,
compilation, lint, test, listener, execution, external service, dependency
operation, personal data, QR, wallet/WAS, presentation, Misty, G28 or G29
activity is authorized. The unrelated PI routine-tool proposal remains
excluded and untouched.
