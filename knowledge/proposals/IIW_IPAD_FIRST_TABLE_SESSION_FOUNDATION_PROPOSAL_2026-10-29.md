# IIW iPad-First Table Session Foundation Proposal

Date: 2026-10-29  
Status: PROPOSED — no implementation or execution authority  
SOGA basis: `73ec1af35f9214036125ab4fd2ca2c0e29bdb893`  
Presentation repository: `/Users/debb/dev/permission-to-speak-work/permission-to-speak`  
Committed presentation basis: `8aa6eec5d40eb671940b73238f8c08cc0c87be76`  
Uncommitted D-157 draft: preserved, unaccepted and prohibited from execution

## Purpose

Create the smallest truthful foundation for the IIW table experience: Deb's
controlled iPad joins the Beryl private network, opens the Permission to Speak
entry point, claims the only active table session, starts the recreated
farmers-market scenario, and supplies one unverified fictional-adult choice to
the real local AAuth/SOGA held-request flow. The laptop shows the real
`202 -> signed poll -> 200/403` result and returns safely to idle.

This proposal does not implement a visitor queue, Project Agent, mBot2,
unattended operation, child detection, identity or relationship verification,
legal authority, consent, standing approval or post-approval withdrawal.

## Review basis and factual reconciliation

Request 030 produced independent feedback from Claude Gate 1 and AGy Gate 2.
Both reviewers agreed on the material gaps between the six-screen target and
the present code: loopback-only transport, inverted scan/hold ordering, no
busy response, one-use rather than revocable input, no actuator, no Project
Agent, incomplete reset behavior and insufficient persistent disclaimers.

Two Gate 2 observations are not adopted as facts:

1. `m02_aauth_fcf656d` exists directly at
   `/Users/debb/dev/soga-clean/m02_aauth_fcf656d`; adding the SOGA repository
   root to `sys.path` is sufficient to locate it. A missing
   `SOGA/aauth_profile` path is therefore not recorded as an established import
   failure.
2. The visible fictional-parent capability expires after 30 seconds. The
   60-second presentation ceiling and 120-second pending-store cap do not
   extend that effective choice window.

The following static defects in the unaccepted D-157 draft are accepted as
proposal inputs and must be corrected before any run:

- reset UI calls the wrong route;
- the fresh-composition age check is evaluated under a frozen clock and is
  therefore ineffective;
- presentation state still contains legacy schema assumptions;
- the visual sequence and current code disagree;
- visible role-play and authority boundaries are not persistent on every
  applicable screen.

Request 030 was feedback only and supplied no gate verdict or implementation
authority.

## Chosen experience

The target two-path opening remains the product direction. This phase activates
only the Permission to Speak entry. The Project Agent tile may appear only as
plain roadmap text marked `NEXT INCREMENT`; it must not display a QR code,
accept free text or imply that an agent service exists.

The Phase 1 experience is:

1. The laptop idle screen displays one active Permission to Speak QR and a
   separate non-interactive Project Agent roadmap tile.
2. Deb's controlled iPad, already joined to the Beryl network, scans the QR.
3. A presentation-owned entry service atomically claims one short-lived table
   lease for that iPad. If a lease or encounter is active, another client gets
   a read-only busy page and no capability or state mutation.
4. The iPad states: `You are the real visitor: the nearby adult,
   role-playing the fictional child's parent.`
   It presents the recreated scene: the adult encourages an illustrated
   fictional child to approach the unicorn installation. No camera or sensor
   classifies a child.
5. The iPad's explicit `The fictional child approaches` action starts a fresh
   bounded AAuth/SOGA composition. The bridge obtains person, resource and auth
   tokens, performs the declared demo-profile SOGA supervision check and calls
   `/enforce`.
6. Only after `/enforce` returns `202 requirement=approval` may the bridge
   create the accepted one-use fictional-parent encounter and bind it to the
   active table lease.
7. The bridge redirects the leased iPad to the accepted, byte-preserved
   fictional-parent choice page. That accepted page presents exactly two
   substantive choices: approve or decline the directed response in this
   fictional scenario. It also permits the visitor to leave without choosing.
8. The accepted connection records the one-use held input. The agent learns
   the result only through the accepted signed poll.
9. The laptop displays terminal `200` or `403`, or the fail-closed expiry. No
   endpoint command is created in this phase.
10. After a short result dwell, explicit Finish, leave or expiry, the bridge
    performs complete teardown, invalidates the table lease and returns to the
    idle Permission QR.

## Claim boundary

Every bridge-owned laptop and iPad screen must visibly retain:

- `LIVE LOCAL AAuth/SOGA ROLE-PLAY` only when the exact live path is active;
- `UNVERIFIED FICTIONAL-PARENT INPUT`;
- `No identity, relationship, parenthood, parental/legal authority or legal
  consent is verified`;
- `The illustrated child and approach are recreated for this demonstration`;
- `No robot acts`;
- `local-operator-demo-control identifies the software path, not the visitor`.

On the accepted byte-preserved choice page, the accepted `DISCLOSURE`,
`SOURCE_DISCLOSURE` and `SCOPE_DISCLOSURE` are the visible boundary. While that
page is open, the laptop simultaneously displays all six bridge-owned boundary
lines.

`Directed response authorized`, `Permission verified`, `parent verified`,
`consent granted`, `withdrawal`, `revocation` and equivalent claims are
prohibited. Terminal success copy is:

`Directed response permitted in this fictional scenario using unverified
role-play input.`

The role-play input is an additional resource-side condition. It is not
described as an AAuth-verified parent or as SOGA's own governance decision.
The `/auth-token` screen states that SOGA used a declared demonstration profile,
not observed human or environmental state.

## Screen and route ownership

The presentation bridge owns the entry, scene, progress, busy, expiry, error,
result and reset views. The accepted fictional-parent gateway remains the sole
owner of the choice view and submitted choice. Its accepted HTML, JavaScript,
strings and request behavior remain byte-identical.

The bridge exposes the accepted choice assets through a byte-preserving,
lease-gated same-origin reverse proxy at `/fictional-parent`,
`/fictional-parent.js` and `/fictional-parent-choice`. The accepted gateway
itself remains bound to literal loopback `127.0.0.1:4318`; it is never exposed
directly on Beryl. The proxy adds no CORS relaxation and does not reinterpret a
choice. The laptop owns the visible countdown. Internally, the accepted
`WITHDRAWN` result is rendered to the visitor as `declined`; protocol and
evidence records retain the accepted internal term.

The iPad shows no countdown or expiry copy while it is on the accepted choice
page; expiry copy appears on the laptop. Bridge-owned iPad text describes the
role as `the nearby adult, role-playing the fictional child's parent`,
consistent with the accepted page.

The proxy returns the accepted gateway's status, body and all accepted security
headers—Content-Security-Policy, X-Content-Type-Options, Referrer-Policy and
Cache-Control—unchanged. It sets upstream Host to `127.0.0.1:4318`, strips the
lease Cookie before forwarding and enforces the exact Beryl Origin on the
choice POST itself. The accepted gateway checks Host but does not check Origin.

## Network boundary

This proposal requests source creation only. It authorizes no listener, network
configuration or execution.

A future execution proposal must establish the exact Beryl-connected laptop
interface and iPad client before starting either service. It must:

- expose exactly one presentation listener at the reviewed Beryl private IPv4
  address on port `4317`;
- keep the accepted fictional-parent gateway on literal loopback
  `127.0.0.1:4318` and every reviewed internal AAuth/SOGA listener on
  loopback only;
- reject wildcard, public, non-Beryl private, IPv6 and hostname binds;
- prohibit DNS and every external connection;
- make the iPad URL use the exact literal private IPv4 address;
- enforce the exact Beryl Host/Origin on the presentation service and exact
  loopback Host on the accepted gateway; the presentation proxy enforces the
  Beryl Origin before forwarding a choice;
- preserve `Cache-Control: no-store`, `Referrer-Policy: no-referrer`, bounded
  bodies, finite timeouts and fixed sanitized errors on every response;
- prohibit logging of URL fragments, capabilities, choices, tokens, keys,
  signatures, pending paths, receipt IDs, headers, IP addresses or User-Agent;
- state accurately that no camera, audio, name or account data is requested or
  stored while transient local Wi-Fi/HTTP metadata is necessarily processed by
  the laptop, iPad and Beryl router;
- fail closed rather than fall back to a LAN simulation if the exact live path
  cannot start.

The presentation server must use a reviewed `HTTPServer` subclass whose
`server_bind` invokes `socketserver.TCPServer.server_bind` directly and assigns
`server_name` and `server_port` from the literal bound address. It must not call
`socket.getfqdn`, `getaddrinfo`, `gethostbyname`, `gethostbyaddr` or any other
name-resolution function.

For accepted loopback `ThreadingHTTPServer` implementations that retain the
standard-library bind path, the audit hook answers every
`socket.gethostbyaddr`, `getnameinfo` and `gethostbyname_ex` event by raising
`OSError`. This makes `socket.getfqdn` fall back locally without any packet. It
never raises another exception type for those events, so accepted loopback
servers construct unchanged.

The current loopback-only socket audit guard must not be weakened generally.
A replacement audit may permit only one bind to the exact Beryl address and
port `4317`, the accepted gateway bind to `127.0.0.1:4318`, and the already
reviewed internal loopback listeners. Outbound connects may target loopback
only. UDP, `sendto`, `sendmsg`, wildcard, IPv6, public, other-private, DNS and
every external connection fail closed. No route to the internet is permitted.

## Table-session lease

The stable Permission QR points only to `/permission-entry` on the exact Beryl
presentation origin. It contains no AAuth token, held-request capability or
authorization material. It is rendered by a self-contained inline QR encoder
inside the seven-file boundary: no CDN, package, remote font, generated asset
or new source file is permitted.

The first valid entry atomically creates one table lease containing at least
256 bits of generated entropy. The entry response is a `302` that places the
opaque lease only in an `HttpOnly; SameSite=Strict` cookie and redirects to the
bridge-owned scene route. The server stores only a digest, generation and
deadlines. The Beryl network is an explicit operational trust boundary: only
Deb's laptop, her controlled iPad and named rehearsal devices may join it.
Cleartext HTTP is accepted only on that private network for this bounded demo.
The lease:

- is unrelated to identity, authority or consent;
- is bound to one active encounter generation;
- cannot resolve a held request by itself;
- has a fixed 60-second pre-encounter reading lifetime and expires no later
  than the 30-second choice deadline once the encounter begins;
- is invalidated on finish, leave, error, expiry, reset or shutdown;
- cannot be transferred to a later encounter;
- is never exposed through laptop state, logs, errors or durable files.

Once a lease is claimed, the laptop hides the active Permission QR and displays
`Interaction in progress`. A second client receives a fixed busy page with no
mutation and no active capability. The Project Agent roadmap tile remains
non-interactive.

The accepted fictional-parent 64-character capability is generated only after
the real `202` hold. A lease-authenticated bridge response returns `303` to
`/fictional-parent#<capability>` with an empty body. No response without the
matching live lease may deliver that redirect or capability. The capability is
delivered once, remains a separate one-use secret and is not replaced or
reinterpreted by the table lease. It may appear only where required by the
accepted choice request and may never appear in bridge state, logs, errors or
durable evidence.

## State machine

Only these top-level states are allowed:

1. `IDLE` — Permission QR visible; no lease, composition or held request.
2. `LEASED` — one iPad holds the table lease; no AAuth request yet.
3. `BUILDING` — fresh composition is being constructed; QR hidden.
4. `PENDING` — exact one-use held request exists; approve/decline enabled.
5. `TERMINAL_ALLOW` — signed poll returned `200` for the single request.
6. `TERMINAL_DECLINE` — signed poll returned `403` for the single request.
7. `TERMINAL_EXPIRED` — visitor choice or held request expired fail closed.
8. `ERROR` — fixed sanitized failure; no action.
9. `RESTART_REQUIRED` — fail-closed terminal state after an invariant or
   capacity failure; process restart is required before another encounter.

Every transition is serialized under one presentation-owned lock and checked
against the active generation. The accepted gateway transition is serialized
with the bridge transition. A terminal state can transition only to teardown
and `IDLE`; it cannot start another encounter through a repeated tap. Laptop
state reads are observational and may never poll, mutate or perform actuation.

Exactly one bridge-owned poll driver operates per encounter. It performs the
accepted signed poll independently of browser GET requests, polls before
declaring expiry and records only sanitized state. Browser GET routes read that
state without side effects. Explicit Finish is laptop-owned and performs the
same teardown as result dwell, leave or expiry. Errors tear down the lease,
choice capability, polling task and transient composition; an invariant or
capacity error enters `RESTART_REQUIRED` rather than silently recycling state.

The process accepts at most 64 encounters. The accepted pending-store maximum
of 32 records is unchanged. Either limit fails closed with no capability or
partial next encounter. Simulated mode, if retained for rehearsal, must be
visibly labeled `SIMULATION`, must never replace failed live mode and must use
state separate from the live path.

One valid approval or decline consumes the fictional capability exactly once.
Repeated, conflicting or late submissions return a fixed terminal response and
cannot mutate either the completed or next encounter. No standing policy is
created. A new proposed action always requires a fresh encounter and choice.

## Timing

- Pre-encounter lease reading period: exactly 60 seconds.
- Fresh composition: all first signed operations must begin within five real
  elapsed seconds of construction. This check is outside every frozen-clock
  context.
- Fictional-parent choice: strictly before the accepted 30-second capability
  deadline. The accepted implementation rejects a submission when
  `now >= expires_at`. A choice at T+29 is valid. The poll driver issues at most
  one signed poll per integer clock second; a second same-second poll is an
  accepted-replay `404` and is prohibited. It declares `TERMINAL_EXPIRED` only
  after a signed poll created at or after T+30 returns `202` or `408`. A choice
  at T+30 is late and fails closed. A `404` from the poll driver is `ERROR`,
  never a decline.
- Result dwell: recommended five seconds before idle return, with a visible
  Finish control.
- Pending-store 120-second lifetime remains a defense-in-depth cap and is not
  described as the visitor's available time.
- No browser poll or page reload extends any deadline.

The laptop displays a countdown while the choice is active. Expiry states:
`Session expired — no response was permitted. Scan the current QR to begin a
new scenario.`

## Exact create-only change boundary

After independent review and separate PI authorization, implementation may
modify only the seven D-157 presentation files:

1. `bridge.py`
2. `index.html`
3. `README.md`
4. `CHECKLIST.md`
5. `warmup.sh`
6. `test_fictional_parent_presentation.py`
7. `run_fictional_parent_presentation_tests.py`

It may add no file and modify no SOGA source. The exact inputs are:

- `bridge.py` — `d1140481f89f6de89cc17879258b271c62512a604e221b4497ac67f5ef3ae19c`
- `index.html` — `ad32ab8775d7a54e82162d29bb274741c28c53a5730b7043a0afc2a5510b89ef`
- `README.md` — `07ed0b1d52d9a4188063358971b0461d667e9e2d815591043e3047ad04ee3f5b`
- `CHECKLIST.md` — `5baed9edd3057418c3a901ed76e09860281c649ac390b3614aa288fd062f44df`
- `warmup.sh` — `c2951b273d9bda40e1d9e99c9567e1f81ac3dd048c2fcd680bdc23923e4120ce`
- `test_fictional_parent_presentation.py` —
  `4d394ab6de88ae7197745c7c061b1dd4274564782202ffc44a128286c6e9ac1f`
- `run_fictional_parent_presentation_tests.py` —
  `70e6d3359db39311ffa65b392659741bd8a5db12637562f50898ffe6b694c27e`

Any mismatch or subsequent unreviewed change stops work.

The implementation must correct the reset route, elapsed-age check, state
schema defects and literal leading `+` characters in `warmup.sh` already
identified. The D-157 uncommitted draft is an input, not accepted evidence,
and may be replaced only within this reviewed boundary. Acceptance of this
proposal closes and supersedes the unexecuted create-only authority in D-157;
it does not preserve a parallel implementation path.

## Required source tests

The focused suite must include, at minimum:

### Entry and busy behavior

- first valid iPad entry atomically claims the only lease;
- second client receives busy without a capability or state mutation;
- QR is hidden while leased and restored only after teardown;
- lease alone cannot approve, decline or poll a held request;
- wrong, missing, malformed and expired lease fail closed;
- stale lease cannot bind to a later encounter.

### Ordering and composition

- no fictional capability exists before `/enforce -> 202`;
- phone approach creates exactly one fresh composition and held request;
- repeated approach during `BUILDING` or `PENDING` creates nothing;
- real elapsed age is measured outside the frozen clock;
- build failure tears down without partial reuse;
- accepted same-tick creation invariant remains intact.

### Choice, replay and concurrency

- concurrent approve and decline produce exactly one accepted choice;
- repeated choice and replay fail closed without changing the result;
- bridge polling concurrent with submission is serialized safely;
- a T+29 choice made after a T+29 `202` poll is reported by the first T+30
  poll as `200/403`, not as expired; no second same-second poll is issued; a
  T+30 choice fails closed;
- stale capability cannot resolve a new encounter;
- late submission after timeout cannot revive an encounter;
- repeated laptop state reads have no side effects;
- terminal state cannot create a second action without full teardown.

### Transport and privacy

- only exact loopback and selected Beryl private IPv4 binds are allowed;
- wildcard, IPv6, other private/public addresses, DNS and external connections
  are rejected;
- exact Host/Origin, method, content type, body size and security headers are
  enforced;
- capability and lease never appear in laptop state, bridge response bodies,
  logs, errors, evidence or durable files, except that the capability is
  delivered once in the lease-gated redirect fragment and then used by the
  byte-preserved accepted choice page;
- fixed busy, expired, stale and error pages disclose no active state;
- application logging remains disabled and tests prove no stored client
  metadata.
- the presentation server and an accepted `ThreadingHTTPServer`-based server
  both construct under the audit guard with zero completed name-resolution
  calls;

### UX and claim fidelity

- persistent unverified-role boundary appears on every bridge-owned
  choice-adjacent and result view; the accepted choice page is byte-identical;
- laptop and iPad use the exact one-use approve/decline semantics;
- no post-approval withdrawal, actuator or Project Agent control is rendered;
- phone sees only `fictional choice recorded`; terminal AAuth result appears
  on laptop;
- expiry and offline states are visible and truthful;
- Finish and automatic dwell perform the same complete teardown;
- reset calls the real reset endpoint and returns to `IDLE`;
- a full sequence can be repeated without carrying encounter state.

No test is executed in the create-only phase. The complete test sources are
created for static review only. A future separately reviewed execution may
open the exact loopback listeners required by existing tests; no test may bind
the Beryl interface until an execution proposal explicitly authorizes the
exact listener and audit. That controller must pin every source and run only
under separately reviewed prospective authority.

## Explicit exclusions

This proposal grants no authority to:

- modify any repository or source;
- import, compile, lint, test or execute the presentation or SOGA code;
- bind a listener or access Beryl, LAN, DNS, internet or any external service;
- generate or expose a live phone/iPad QR;
- contact or control mBot2, Misty, Reachy Mini, Raspberry Pi, unicorn
  electronics or any physical device;
- implement Project Agent, free-text chat, LLM/API calls or external logging;
- implement a queue, multiple concurrent sessions or unattended operation;
- claim identity, relationship, parenthood, legal authority, legal consent,
  complete AAuth conformance or production readiness;
- implement standing approval, revocation or post-approval withdrawal;
- activate G28, G29 or any physical actuation authority;
- read, adopt or modify the unrelated PI routine-tool proposal.

## Holdpoints

1. Both independent gates review this complete proposal.
2. The PI accepts the exact reviewed proposal and separately authorizes
   create-only implementation.
3. Both gates review all seven complete implementation files.
4. The PI accepts the exact files and separately authorizes creation of an
   execution proposal and manifest.
5. Both gates review the exact execution proposal, controller and manifest.
6. The PI prospectively authorizes one bounded run.
7. Both gates independently review evidence before any result is accepted or
   used in the IIW demonstration.

Project Agent and mBot2 each require their own subsequent proposal, review,
implementation and execution sequence.
