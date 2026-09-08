# M02 Stage 3A-R2 Proposal — Fixed-Port Localhost Containment

Date: 2026-09-08
Status: DRAFT FOR INDEPENDENT REVIEW — NOT AUTHORIZED FOR CODE OR EXECUTION
Prepared from checkpoint: `main @ ee4eebc6530ab0cc37a0b95e3720adc2f59b4e6e`

## Purpose

Test a narrower, technically expressible macOS containment rule without
weakening the application-facing literal-IPv4 boundary. The previous attempt
failed before Node ran because the macOS sandbox profile language rejects a
dotted-quad IP predicate and accepts only `localhost` or `*`. This proposal does
not relabel that failure as success. It changes the proposed OS boundary from
one literal address across all ports to two symbolic-localhost endpoints at two
fixed, reviewed ports, while requiring each application listener and URL to
remain literal `127.0.0.1`.

Stage 3A-R2 is a runtime-reproduction recovery only. It is not Stage 3B and
contains no wallet handoff, adapter, Person Server integration, storage client,
credential interpretation, governance decision, or execution surface.

## Evidence basis

- Stage 3A established that WAS `2090a60` hardcodes `0.0.0.0` in its standalone
  executable but publicly exports `createApp` and `FileSystemBackend` so a
  downstream caller can own `listen` without modifying upstream source.
- Stage 3A-R established that `/usr/bin/sandbox-exec` on this host rejects
  `(remote ip "127.0.0.1:*")` during profile parsing.
- Current Apple-supplied sandbox profiles use symbolic `localhost` or `*` in
  `ip` predicates. This is local implementation evidence, not a claim that the
  deprecated sandbox language is a supported long-term deployment mechanism.

## Selected containment design

Use one SOGA-owned Node research harness and two fixed ports selected in the
authorization record before execution:

- WAS: `127.0.0.1:46321`
- Freewallet static surface: `127.0.0.1:46322`

The application layer must use those literal IPv4 addresses. The OS profile may
use only the syntax the host accepts, with a deny-network baseline and narrow
exceptions for TCP bind, inbound, and outbound operations at
`localhost:46321` and `localhost:46322`. No wildcard port exception is allowed.
The complete profile must be committed or quoted in the pre-execution evidence
before it runs; a generated or hidden profile is prohibited.

Because symbolic `localhost` may cover both `127.0.0.1` and `::1`, the sandbox
exception is explicitly broader in address family than the application-facing
listener rule. Port restriction contains that difference: only the two fixed
candidate ports are eligible. The preflight must characterize IPv6 behavior
rather than assume it, and actual application sockets must still prove literal
IPv4 binding.

## Proposed harness

The prior unexecuted launcher and profile were removed and must not be reused.
A new reviewable harness may be written only after PI authorization. It may:

1. create an explicit temporary harness root and WAS filesystem data directory;
2. create a temporary harness-local `node_modules/was-teaching-server` symlink
   to the exact detached `2090a60` checkout;
3. import only the package-root `createApp` and `FileSystemBackend` exports;
4. configure finite byte, upload, Space, Collection, and Resource limits;
5. set both WAS `serverUrl` and its actual listener to
   `http://127.0.0.1:46321`;
6. use only `node:http` and `node:fs` to serve the exact built Freewallet
   `8e806c0` static output at `http://127.0.0.1:46322`;
7. refuse every Freewallet asset URL that is not same-origin with that exact
   literal-loopback origin;
8. impose a maximum 30-second holdpoint followed by unconditional `finally`
   cleanup; and
9. produce no wallet, WAS-write, Person Server, governance, or Stage 3B
   semantics.

## Mandatory pre-start sequence

Nothing may import or serve either candidate until every step passes:

1. Verify both fixed ports have no listener. Any collision stops the run; do
   not select substitute ports.
2. Parse and run a synthetic process under the exact proposed profile.
3. Prove a nonce exchange succeeds on literal `127.0.0.1:46321`, then close it.
4. Prove a bind to `0.0.0.0:46321` fails.
5. Characterize `::1:46321`: if bind or connection succeeds, record that the OS
   exception includes IPv6 loopback; this is permitted only for the synthetic
   characterization. Candidate listeners still may not bind IPv6.
6. Prove a connection to unused `127.0.0.1:46323` is denied by policy rather
   than merely refused because no server is present. The test must distinguish
   sandbox denial from `ECONNREFUSED`.
7. Prove a connection to TEST-NET-1 `192.0.2.1:46321` is denied locally by the
   sandbox, not timed out or refused remotely.
8. Use an external socket inspection to prove the synthetic listener closed.

If the sandbox language cannot express and empirically enforce this fixed-port
rule, stop. Do not fall back to application monkey-patching, periodic-only
observation, a firewall, Docker, a VM, broader localhost access, or unrestricted
runtime execution.

## Candidate holdpoint evidence

If and only if the preflight passes:

- start the one sandboxed harness;
- verify externally that its only listeners are exactly
  `127.0.0.1:46321` and `127.0.0.1:46322`;
- fetch WAS `/health` and one documented, non-mutating WAS route response;
- fetch the Freewallet root and one independently same-origin-validated built
  asset;
- record status and content type without credential, token, secret, or response
  body disclosure;
- release the holdpoint before 30 seconds; and
- verify externally after process exit that neither fixed port has a listener
  and no candidate process remains.

An empty sandbox log is not evidence that no connection was attempted. The OS
profile is the containment control; socket inspection establishes actual bind
state; surfaced denials are supplementary evidence.

## Stop conditions

Stop before candidate startup if:

- either exact checkout, build output, or dependency tree is absent or changed;
- either fixed port is occupied;
- the complete profile is absent, hidden, unparsable, or differs from the
  reviewed text;
- any expected preflight allow or deny result differs, including inability to
  distinguish policy denial from ordinary network failure;
- tracked upstream source is modified;
- package-root import would require installation, publication, copying, or a
  private deep import;
- any runtime needs package-registry or external access, remote DID/context
  resolution, graphical browser, Playwright, WebAuthn/WebCrypto ceremony,
  Postgres, Docker, production credentials, or undocumented trust;
- a listener is not literal `127.0.0.1` on its fixed port;
- an asset is not same-origin; or
- cleanup or external post-check does not prove both ports and the process are
  gone.

## Explicit nonauthorization

This proposal authorizes nothing. It permits no code, profile, symlink,
preflight, candidate startup, dependency installation, registry access,
external access, Stage 3B work, wallet interaction, Person Server integration,
personal data, payment, Misty access, physical actuation, R3, G28, or G29.

The proposal requires independent Gate 1 and Gate 2 review and explicit PI
authorization before any implementation or execution. Success would establish
only bounded local reachability of the two exact built candidates. Stage 3B
would remain separately unauthorized.
