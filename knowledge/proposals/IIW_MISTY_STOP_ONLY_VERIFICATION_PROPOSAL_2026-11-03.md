# IIW Misty B Stop-Only Verification Proposal

Date: 2026-11-03
Status: PROPOSED — NO IMPLEMENTATION OR EXECUTION AUTHORITY
Repository basis: `f3521f7d6ac828ba701736d0a56f73d282956da8`
Parent decisions: D-193 through D-197

## Purpose and sequence decision

Determine the real bounded HTTP acknowledgement shape returned by the PI-selected Misty B for one idle `StopSpeaking` request. This is the first physical step in the sequence defined by the accepted D-194 amendment. The PI's acceptance decision must explicitly permit this stop-only stage to precede completion-event, runtime-driver and restart/lock stages.

This proposal alone closes no hold. Only accepted blind dual-reviewed physical evidence can close the real StopSpeaking-response hold. It authorizes no speech, event subscription, presentation integration, movement, lights, display, camera, microphone, sensors, skills, discovery, or public robot demonstration. The public Flow A demonstration and accepted gateway remain byte-identical. The instrument does not call `MistyInvitationAdapter.dispatch()` and cannot send Speak.

## Selected unit and identity confirmation

PI-reported target values are platform ID `urn:debblabs:misty-b:20193802932`, serial `20193802932`, MAC `00:D0:CA:00:96:C3`, Beryl reservation `192.168.8.219`, reported firmware `2.0.2.11660`, model Misty II, CONFIG `010-000002`.

Before physical access, an external manual preflight must record a fresh named confirmation by Deb that she read serial `20193802932` and CONFIG `010-000002` from the selected physical unit or its unit-specific label, it is the only powered Misty present, and Beryl's complete wired-and-wireless client view shows MAC `00:D0:CA:00:96:C3` at `192.168.8.219`. This ties the serial-labelled unit to the sole Misty network client without an identity API query. Firmware remains reported, not freshly confirmed. The instrument may not discover, scan, probe, query identity/status, accept or fall back to another address, host, MAC or device.

## Physical and network preflight

The manual preflight must be outside both repositories and evidence directories and no more than five minutes old at invocation. The runner validates its fixed path, schema and oldest-observation age and computes its SHA-256 before evidence creation. It and live checks confirm:

1. Misty is powered on, idle, not speaking and not visibly moving;
2. Deb is beside Misty with immediate access to the documented base power switch; switching power off is the independent local emergency stop for unexpected speech, movement, display, light or other behavior;
3. Misty is stable on its dock or foam block with treads unable to move it across the surface;
4. the exact serial/MAC/address confirmation above;
5. Beryl's complete wired-and-wireless inventory contains exactly the laptop and Misty—no iPad, phone, mBot2, CyberPi or other device;
6. remote administration and port forwarding are disabled;
7. laptop `en0` has exact IPv4 `192.168.8.247`;
8. the route to `192.168.8.219` uses `en0` with source `192.168.8.247`; any VPN or competing route for `192.168.8.0/24` stops;
9. TCP ports `4317` and `4318` have no listeners; and
10. no public demo, rehearsal, Misty Studio or other robot controller is open.

The power-switch location and shutdown behavior are documented in the official Misty II overview at `https://docs.mistyrobotics.com/misty-ii/robot/misty-ii/#turning-misty-off`. Deb must physically locate and touch the switch before recording readiness. The preflight also confirms that macOS Local Network permission is enabled for the exact terminal/Python context; this manual setting check sends no traffic.

An unrelated internet uplink is allowed only if it does not alter the target route. The physical socket binds to `192.168.8.247` before connecting. After closure, the runner re-observes interface/address, target route and ports; Deb attests whether client count stayed exactly two and what she saw/heard. Those are operator attestations, not API results.

## Exact request bytes

One future separately authorized execution may create exactly one TCP connection to `192.168.8.219:80` and send exactly these 150 bytes, with each `\r\n` encoded as CRLF and no bytes after `{}`:

```text
POST /api/tts/stop HTTP/1.1\r\n
Host: 192.168.8.219\r\n
Accept: application/json\r\n
Content-Type: application/json\r\n
Connection: close\r\n
Content-Length: 2\r\n
\r\n
{}
```

SHA-256: `863897eae5c306229ffaed3ebfd943fe1c99a03a8753ef8922df174c2d8f13ab`. These equal the accepted `StrictJsonPostTransport` serialization for `STOP_URL` with `{}`. Evidence preserves both bytes and hash.

No DNS, proxy, redirect, authentication negotiation, retry, alternate method/path/port, keep-alive reuse, discovery or fallback. Total deadline is exactly two seconds. Raw HTTP response is bounded to 73,728 bytes, matching the accepted read ceiling; decoded body is bounded to 65,536 bytes. Every outcome consumes the attempt after evidence creation; no second request is automatic.

Official documentation describes `StopSpeaking` as stopping text-to-speech. The idle-unit expectation is no newly initiated behavior, but the Alpha API may behave unexpectedly. Immediate access to the base power switch is mandatory. API acknowledgement never proves physical stillness.

## Create-only six-file package

After separate PI acceptance, create only:

1. `robot_gateway/misty_stop_probe.py` — fixed request/parser/probe with injected socket and clock;
2. `tools/robot_gateway/run_misty_stop_only_probe.py` — physical-only runner;
3. `tools/robot_gateway/run_misty_stop_only_synthetic_tests.py` — synthetic-only controller;
4. `tools/robot_gateway/misty-stop-only-runtime-manifest.json`;
5. `tests/test_robot_gateway_misty_stop_only_probe.py`;
6. `robot_gateway/STOP_ONLY_VERIFICATION.md`.

The physical runner has no synthetic mode. The synthetic controller has no physical mode and runs the tests in `/usr/bin/python3 -I -B` with an audit hook denying network, process creation and filesystem mutation, a 60-second limit and 2,000,000-byte per-stream limit. Injected evidence/socket seams permit testing under the write-denying hook. No accepted source changes. Creation grants no import, test, execution or physical authority.

## Acyclic pins and distinct evidence

The manifest pins repository/presentation bases; hashes for the probe module, tests and documentation but not itself or either runner; all ten D-195 gateway hashes; preserved SOGA/M01 hashes; presentation hashes at `c943e594270045daa64694f44c33e3602a8181e6`; D-191 v11 evidence hashes; and D-197 synthetic gateway evidence hashes including its committed report.

Both runners pin the final manifest SHA-256. The manifest pins neither runner. External execution requests pin all six file hashes and applicable exact command. Each runner records its own computed SHA-256.

The physical runner contains fixed absolute paths for the reviewed request at `/Users/debb/dev/research-evidence/soga/requests/IIW_MISTY_STOP_ONLY_PHYSICAL_EXECUTION_REQUEST.md`, PI authority at `/Users/debb/dev/research-evidence/soga/authorizations/IIW_MISTY_STOP_ONLY_PHYSICAL_EXECUTION_AUTHORITY.md`, and fresh preflight at `/Users/debb/dev/research-evidence/soga/preflight/iiw-misty-stop-only-physical-v1-preflight.json`. Its exact invocation is `/usr/bin/python3 -I -B /Users/debb/dev/soga-clean/tools/robot_gateway/run_misty_stop_only_probe.py`, without arguments.

The PI authority pins the reviewed request SHA-256. The request pins all six package hashes, including the physical runner, plus manifest hash, fixed paths, schema and command. The runner computes and compares its own and package hashes to the request, and the request hash to the authority. This chain is acyclic.

The fresh preflight cannot be hash-pinned before review. The request pins its fixed path, schema and five-minute maximum age. The runner validates those, computes the preflight SHA-256 itself and records contents/hash. Age is measured from the oldest individual observation timestamp, never filesystem time.

Distinct initially absent evidence paths:

- synthetic: `/Users/debb/dev/research-evidence/soga/evidence/iiw-misty-stop-only-synthetic-v1`;
- physical: `/Users/debb/dev/research-evidence/soga/evidence/iiw-misty-stop-only-physical-v1`.

The synthetic controller requires no Beryl record and cannot call the physical runner. The physical runner requires the Beryl record and has no test mode.

## Physical runner behavior

The runner must fail before evidence unless the fixed request/authority chain, exact hashes, committed basis, clean presentation and allowed repository status match; accept only the excluded PI proposal as SOGA status; validate the fresh preflight's fixed path/schema/oldest-observation age and compute its hash; enforce identity, interface, route, listener and client holds; reject proxy variables and relevant unexpected `GIT_*`; internally build the fixed request; bind locally to `192.168.8.247`; create physical evidence immediately before the only socket call; close in every outcome; make no cleanup request; preserve bounded complete/partial response without exception/environment leakage; record connection, bind, connect, sent-byte and EOF progress; re-observe route/interface/ports; record `operator_attestation_status=pending` without claiming post-request physical observation; write evidence for every consumed outcome; and exit nonzero unless exact `ACKNOWLEDGED`, without retry.

## Parser relationship and outcome table

The probe implements a narrow copy of the accepted HTTP/acknowledgement parser without importing `robot_gateway.strict_json_post` or package initialization. Both runners and tests load the probe by explicit file path, never by importing `robot_gateway`. Synthetic tests load the accepted parser by explicit file path without package initialization and prove identical acknowledgement outcomes over shared fixtures. The physical module contains only the Stop path and cannot serialize Speak.

| Result | Classification |
| --- | --- |
| Complete EOF-terminated 2xx, valid bounded JSON object, no `error`/`Error`, `result` JSON `true`, `status` absent or `Success` | `ACKNOWLEDGED` |
| Complete non-2xx regardless of body validity, or 2xx with valid JSON failing that predicate, including `result=false` | `REJECTED` |
| Invalid HTTP/headers/framing/UTF-8/JSON, duplicate key, non-object, truncated framed body | `MALFORMED` |
| Raw exceeds 73,728 or body exceeds 65,536 bytes | `OVERFLOW` |
| Two-second deadline expires at any phase, including valid-looking response without EOF | `TIMED_OUT` |
| Non-timeout socket creation/bind/connect/send/receive error | `TRANSPORT_FAILED` |

Each class records progress and bounded partial bytes. Timeout/transport failure after any sent byte records delivery `unknown`; before any sent byte, `not_sent`. Neither is a physical-outcome claim.

HTTP status classification precedes body parsing for non-2xx. A post-consumption evidence/control failure is `INTERNAL_FAILED`, exits nonzero, permits no retry and makes no acknowledgement claim.

## Required synthetic tests

Prove without network: exact request bytes/hash/target/local bind; one connection/request; no Speak path/text; no DNS/proxy/redirect/retry/discovery/fallback; exact deadlines and bounds; partial I/O/progress/closure; parser equivalence; every outcome including non-2xx precedence and valid body without EOF; failure consumption; fixed request/authority/preflight chain, oldest-observation age and self-hash comparison; repository/manifest/interface/route/port/evidence holds; 30-second readiness input timeout/refusal and post-input recheck; evidence safety and pending-attestation behavior; distinct evidence paths; all protected hashes unchanged; excluded PI proposal recognized only by status path and never opened/hashed; no public import/invocation; and synthetic-controller audit-hook/runtime/output/immutability controls.

Exact test count, six hashes, manifest hash, both evidence paths, interpreter and commands are fixed before either execution request.

## Repository/external sequence

If accepted, commit only this exact proposal, acceptance decision and state before creating the six-file package. After blind dual static review, commit only the exact package, acceptance decision and state before a synthetic execution request.

At synthetic and physical execution, SOGA `git status --porcelain=v1 --untracked-files=all` contains only `?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md`; presentation status is empty. All post-package execution proposals/requests, authorities and Beryl preflight records reside outside both repositories under `/Users/debb/dev/research-evidence/soga/` and outside evidence directories. The runner verifies the request/authority hash relationship, validates the preflight's fixed path/schema/oldest-observation age, computes the preflight hash and preserves its contents/hash in evidence.

Synthetic execution and blind evidence acceptance are mandatory before a physical request. Physical execution requires a new external request, blind dual review and prospective PI authority.

## Evidence, stops and claim boundary

Physical evidence preserves exact request bytes/hash, complete bounded raw/partial response/hash, parser facts/classification, progress, times/limits, protected before/after identities, interface/route/port observations and external preflight contents/hash. The runner states only what it did and records the post-run operator attestation as pending.

Deb invokes the runner from the laptop positioned beside Misty. Immediately before evidence creation it requires exact fixed input `PI_READY_AT_POWER_SWITCH`, entered only while Deb can operate the base switch. The input has a 30-second timeout; timeout, EOF, any other text or refusal stops before evidence and consumes nothing. After valid input, the runner re-evaluates the oldest-observation age and every live interface, route, listener, repository and evidence-absence hold, then creates evidence immediately before the socket call. No after-observation is requested by or supplied to the runner. After exit, Deb's client-count and seen/heard observations are written to a separate durable external post-run attestation that never changes the evidence directory. Blind evidence review pins that file's SHA-256 and reviews it with immutable runner evidence.

Fixed local read-only observations are `/usr/sbin/ipconfig getifaddr en0`, `/sbin/ifconfig en0 inet`, `/sbin/route -n get 192.168.8.219`, and `/usr/sbin/lsof -nP -iTCP:4317 -sTCP:LISTEN` plus the equivalent for 4318. Fixed repository observations are `/usr/bin/git -C /Users/debb/dev/soga-clean rev-parse HEAD`, `/usr/bin/git -C /Users/debb/dev/soga-clean status --porcelain=v1 --untracked-files=all`, `/usr/bin/git -C /Users/debb/dev/permission-to-speak-work/permission-to-speak rev-parse HEAD`, and the corresponding presentation status command. Commands use direct argument arrays with a reviewed minimal environment and no shell. `lsof` exit 1 with empty output means no matching listener; other nonzero outcomes refuse. These commands send no network traffic and run before readiness and again after valid readiness; interface/route/listener observations also repeat after socket closure.

The physical runner deliberately installs no audit hook because an irreversible process-denying hook would prevent its required after-closure observations. Its fixed source, exact command arrays, literal bind/target, code review and synthetic tests are the physical-run controls. The separate synthetic controller retains the network/process/write-denying audit hook. Synthetic tests cover that hook and every fixed physical command seam. Python's literal-address `socket.create_connection` may internally call `getaddrinfo`; injected tests require only literal `192.168.8.219`, IPv4 port 80 results, followed by exact bind to `192.168.8.247` and exact target connection.

Stop before evidence on any stale/failed preflight, serial/MAC tie, emergency-stop access, inventory, repository, hash, manifest, target, interface, route, port or absence failure. After evidence creation, any timeout, refusal, malformed/ambiguous response, network change, unexpected client, conflict, emergency stop, exception or cleanup uncertainty consumes the attempt. Use the base power switch immediately for unexpected behavior. Do not retry, broaden the parser, query the robot, or proceed to Speak.

At most, accepted evidence establishes the response observed from the serial-confirmed, MAC-bound unit for one idle stop request. It does not establish general safety, physical stillness, speech behavior, completion events, runtime driving, restart persistence, invitation behavior, mBot2 behavior, complete AAuth conformance, or demo integration.

This proposal authorizes no implementation or execution. No import, compilation, lint, test, listener, Beryl access, network request, robot contact/command, speech, light, display, camera, microphone, sensor, movement, skill, update, discovery, presentation change, wallet/WAS work, G28 or G29 is authorized. The unrelated PI proposal remains excluded, unread and untouched.
