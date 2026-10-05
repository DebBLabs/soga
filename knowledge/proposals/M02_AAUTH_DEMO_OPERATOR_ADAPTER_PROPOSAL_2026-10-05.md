# M02 AAuth Demo Operator Adapter Proposal

Date: 2026-10-05
Status: PROPOSED — NOT AUTHORIZED
Prepared at: `main @ e2cfe0d`
Review class: mandatory blind dual review under D-064

## Purpose

Add the smallest reusable operator-control seam between the D-140-accepted
approval-pending lifecycle and a presentation or later physical-resource
adapter. The seam lets a local operator supply explicitly unverified synthetic
other-party input either as standing resource policy or as the resolution of an
already-created pending invocation. The agent continues to observe only the
accepted signed polling interface.

This is core demo plumbing, not slide code. Claude's presentation bridge remains
outside the SOGA repository. It already uses the two accepted in-process seams
formalized here—`OtherPartyApprovalPolicy.replace()` and
`ApprovalPendingStore.resolve()`—plus the accepted HTTP surfaces and signed
polling. The adapter fits those seams; it does not replace the bridge or D-140.
The bridge may keep using the accepted seams directly while the adapter is under
review, but it must not use the D-132 shared `last_decision` attribute.

## Accepted basis and ownership boundary

D-140 establishes the bounded localhost approval-pending lifecycle with 81/81
tests. Its accepted production module is
`m02_aauth_fcf656d/approval_pending.py` at SHA-256
`18717f7b64007c92f6fb893498f1329b8ed049bb6636eb586a44267588bea47b`.

The resource owns both its standing other-party policy and each pending
invocation. The operator adapter may call only the existing in-process
`OtherPartyApprovalPolicy.replace()` and `ApprovalPendingStore.resolve()`
methods. It must not:

- mint, inspect, retain, log or return AAuth tokens or signing keys;
- expose an HTTP approval/decision endpoint;
- impersonate the AAuth Person or merge the other party into Deb's delegated
  authority;
- decide SOGA supervision or bypass the accepted resource policy; or
- invoke a presentation, wallet, WAS, QR flow or physical resource.

## Proposed additive package

Create only:

1. `m02_aauth_fcf656d/demo_operator.py`;
2. `tests/test_m02_aauth_demo_operator.py`; and
3. `tools/m02_aauth_fcf656d/run_demo_operator_tests.py`.

All accepted D-140 source remains frozen.

### Operator adapter

`DemoOperatorAdapter` receives at construction:

- the exact `ApprovalPendingStore` instance;
- the exact `OtherPartyApprovalPolicy` instance used by the resource;
- fixed `participant`, `mission_s256` and directed scope;
- the same injected integer clock callable used by that store; and
- an injected receipt-identifier factory.

The constructor rejects any nonmatching or mutable configuration. The adapter
serializes its own operator writes and offers two in-process methods.

The held-request method accepts only:

- the opaque pending path returned by the resource; and
- an operator choice from the exact set `APPROVED` or `WITHDRAWN`.

The method derives the pending identifier, creates an exact
`OtherPartyApprovalReceipt`, and calls `store.resolve()`. Receipt fields are
fixed as follows:

- `asserted_role="parent"`;
- `assurance="unverified-demo-input"`;
- `participant`, `mission_s256` and `scope` from the immutable adapter binding;
- `state` from the exact operator choice;
- `observed_at=clock()` and `expires_at=clock()+120`, using one sampled integer
  time for both;
- `source="local-operator-demo-control"`; and
- a unique 32-character URL-safe receipt identifier from the injected factory.

The standing-policy method accepts only an operator choice from the exact set
`APPROVED`, `WITHDRAWN` or `CLEARED`. For `APPROVED` or `WITHDRAWN`, it creates
the same fixed receipt and calls `policy.replace(receipt)`. For `CLEARED`, it
calls `policy.replace(None)` and creates no receipt. Operator writes are
serialized by the adapter, but this does not claim atomicity with concurrent
resource evaluation; the presentation controller must not start a directed
request while changing standing policy.

Each method returns one immutable sanitized event object containing only:

- event version;
- `event="held_other_party_input_recorded"` or
  `event="standing_other_party_input_recorded"`;
- receipt identifier, or `None` for `CLEARED`;
- asserted role and assurance;
- participant, mission, scope and state;
- observed and expiry time, with expiry `None` for `CLEARED`; and
- source.

It returns no token, key, signature, pending identifier, pending path, HTTP
authority or raw request body. It keeps no mutable `last_decision` or event
history. It retains only a bounded set of at most 1,024 receipt identifiers to
reject duplicates; reaching the bound fails closed. The caller owns any
presentation history.

Every invalid path, identifier, state, clock value, duplicate receipt ID,
expired/terminal/unknown pending record, exhausted identifier bound or accepted
store/policy failure fails closed without a sanitized success event. Failures
return only fixed sanitized reason codes; they expose no exception text,
pending data or private store state. A held receipt with a participant, mission
or scope mismatch is intentionally accepted by the public `resolve()` seam;
the accepted signed poll performs the binding check and returns terminal `403`
with its fixed mismatch reason. The adapter never reads private store internals.
Replacing held `APPROVED` with `WITHDRAWN` before the agent's first terminal poll
remains allowed because it models withdrawal before action. After any terminal
poll, further held operator input fails closed through the accepted store.

### Tests and runner

Add twelve tests covering:

1. exact held approved receipt and sanitized event;
2. exact held withdrawn receipt and sanitized event;
3. standing `APPROVED` produces immediate resource `200`;
4. standing `WITHDRAWN` produces resource `202` pending;
5. standing `CLEARED` produces resource `202` pending;
6. held approved input followed by signed polling returns one allowed
   completion;
7. held withdrawn input followed by signed polling returns terminal denial;
8. a binding-mismatched held receipt is accepted by `resolve()`, then signed
   polling returns terminal `403` with the exact fixed mismatch reason, without
   any private-store inspection;
9. held approval replaced by withdrawal before polling produces denial;
10. input after terminal completion and unknown or malformed pending input fail
    closed with fixed sanitized reason codes;
11. invalid state, clock and receipt identifier, duplicate IDs, the bounded ID
    limit and concurrent operator writes fail closed without exposing secrets;
    and
12. all D-140 production and test files remain byte-identical.

The bounded runner derives from the D-138/D-140 runner trust chain, pins every
accepted and new source, and requires exactly 93 tests: the accepted 81-test
baseline plus twelve new tests. Preserve the accepted provider verification,
literal-`127.0.0.1` socket guard, isolated child, 90-second limit,
2,000,000-byte output limits, redaction, module-origin checks, pre/post
immutability, stderr rule and no-retry behavior. A later execution proposal
must select a new absent durable evidence directory.

## Review and execution sequence

This proposal authorizes nothing by itself. If accepted, it may authorize only
create-only implementation of the three additive files. Do not import,
compile, lint, test, execute or open a listener during creation. Both blind
gates must review every complete file before commit or execution.

Execution requires a separate prospective PI authorization after review of an
exact bounded runner and fresh evidence target. Resulting evidence requires
blind dual review before acceptance.

## Claim boundary and exclusions

A later positive result may establish only that a local operator can feed
synthetic, explicitly unverified other-party state into the accepted standing
resource policy and resource-held pending lifecycle without exposing secrets or
creating an agent decision route. It does not establish verified identity,
parental or legal authority, consent or assent, presentation correctness, complete AAuth
conformance, wallet/WAS, QR, phone, Misty or physical-resource integration.

No repository modification, execution, dependency operation, external service,
non-loopback listener, presentation modification, personal data, wallet/WAS,
QR, Misty access, physical action, G28 or G29 is authorized by this proposal.
The unrelated PI routine-tool proposal remains excluded and untouched.
