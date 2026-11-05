# IIW mBot2/CyberPi Protocol-Verification Proposal

Date: 2026-11-05
Status: PROPOSED — NO IMPLEMENTATION OR EXECUTION AUTHORITY
Repository basis: `6aeb117a21445a90e52c81705f151d7c8afc7d8c`
Parent decisions: D-193 through D-198

## Decision and departure requested

This proposal supersedes the stationary-endpoint proposal that received NOT READY in request 139. It does not create an adapter and cannot connect mBot2 to `RobotGateway` or `RobotInvitationCoordinator`.

D-193 required a supported mBot2/CyberPi interface before an implementation proposal. The G handoff is useful engineering input but contains contradictions that prevent it from satisfying that hold. The PI is therefore asked to authorize a bounded protocol-verification phase before adapter design. This is an mBot2-specific departure from the D-193 sequence and creates no precedent. D-194's unavailable binding remains authoritative throughout this phase. D-195 states that physical work additionally requires reviewed completion-event driving, restart/lock behavior, harmless stop-only response verification and an exact execution command. This create-only/synthetic phase performs no physical work and requests no release from D-195. Whether and how those holds apply to a first mBot2 observational probe is expressly left to that later proposal, blind review and prospective PI decision; acceptance here does not decide it. Equivalent mBot2 lifecycle holds remain open before any adapter or public integration.

## Purpose and preserved boundaries

Establish a reviewable, internally consistent model of factory CyberPi `f3f4` serial framing and response grammar before any gateway adapter, persistent display/light behavior or physical invitation is proposed.

The accepted public Flow A demonstration, accepted shared gateway, accepted Misty package and in-progress Misty stop-only package remain unchanged. mBot2 remains `urn:debblabs:mbot2-iiw:unavailable`. No public endpoint, QR change, robot selector, movement or fallback is introduced.

## Engineering input and unresolved discrepancies

Read-only input: `/Users/debb/dev/research-evidence/soga/handoffs/MBOT2_CYBERPI_F3F4_G_HANDOFF_2026-11-03.txt`, SHA-256 `169e866c5e079406538e51df7708fd04df4acc5cdcedb09398c8e55a91434c93`.

The handoff reports firmware `44.01.016`, CH340 USB serial at 115200 8N1, a single owned handle, DTR/RTS-triggered reset, about 10.5 seconds of passive boot drain, `TYPE_SCRIPT=0x28`, and a raw `TYPE_ONLINE=0x0d` transition. None is accepted evidence.

The following contradictions are recorded, not normalized away:

1. The reported readiness-probe vector ends with checksum `0x59`, while the handoff's stated checksum formula produces `0x84` for the same expression and index.
2. The reported offline frame ends with checksum `0x0e`, while the online-frame arithmetic suggests `0x0d` for the offline value.
3. The reported parser does not validate footer, payload checksum or inner length and can resynchronize inside an active payload.
4. The handoff uses `ast.literal_eval` and silently returns raw text on parse failure, so it does not establish whether void-return responses contain JSON `null`, Python `None`, another form or no acknowledged payload.

Synthetic work may prove behavior only against explicitly named candidate assumptions. It may not claim Makeblock/device parity. Any physical probe waits for a separately reviewed request and prospective PI authorization.

## Phase 0 create-only package

After prospective PI acceptance, create only:

1. `robot_gateway/cyberpi_f3f4_protocol.py` — pure bounded frame/parser candidates with no serial import and no general expression API;
2. `tests/test_robot_gateway_cyberpi_protocol.py` — offline tests and discrepancy fixtures;
3. `tools/robot_gateway/run_cyberpi_protocol_tests.py` — isolated bounded synthetic controller;
4. `tools/robot_gateway/cyberpi-protocol-runtime-manifest.json` — exact bases, protected hashes and limits;
5. `robot_gateway/CYBERPI_PROTOCOL_VERIFICATION.md` — assumptions, contradictions and claim boundary.

Do not modify `robot_gateway/__init__.py`, `gateway.py`, `coordinator.py`, `README.md`, any Misty file, any accepted presentation file or any D-198 file. Created modules are loaded only by exact path in synthetic testing.

## Exact non-capabilities

The protocol module has no import, call target or dynamic import for `serial`, `pyserial`, `makeblock`, `cyberpi`, subprocess, sockets, Bluetooth, network or device-node operations. It has no device path, serial opener, DTR/RTS operation, REPL switch, reset mode, subscription mode, audio, display, LED, motor or arbitrary-script capability and cannot send bytes anywhere. The literal fixture bytes may encode the reported text `cyberpi.get_bri()`; this is a claimed ambient-brightness sensor expression used only as inert fixture data and is barred from defaulting into the first physical probe. Tests may name forbidden surfaces in AST assertions, the controller may name them in runtime deny-lists, and documentation/filenames may describe them; those textual references are not capabilities. Static rules are file-specific and distinguish imports/calls from inert literals and documentation.

The pure frame builder accepts only a closed enumeration of named test fixtures embedded in the module. It exposes no caller-provided string-to-frame method. Candidate fixtures include the handoff's claimed readiness expression solely as bytes under test; the package cannot execute it.

## Parser invariants and limits

The parser consumes a byte stream and emits complete frames. Before an active frame, bounded non-`0xF3` boot/noise bytes are counted and skipped. A candidate `0xF3` start with an invalid header checksum or impossible/over-limit length is rejected, counted and advances by one byte; it never allocates from the untrusted length. Once a valid bounded header begins an active frame, bytes are accumulated to that declared length without resynchronizing on payload patterns. Any inner-length, packet-type, mode, index, payload-checksum, footer, UTF-8 or payload-grammar failure rejects that complete frame and returns to the pre-header state. Bytes after one complete frame are a subsequent stream unit, not “trailing bytes”; extra bytes inside the declared complete frame or after a standalone complete-frame fixture are rejected by the complete-frame API. A false valid-looking frame start in boot noise is bounded by the manifest limit, rejected on its first failed invariant and returns to pre-header state. Each transition and rejection is a named test.

For each candidate assumption, a complete frame requires exact `0xF3` header; correct header checksum; declared length within a small manifest-pinned maximum; minimum frame length; exact expected packet type/mode/index; exact inner payload-length relationship; candidate payload checksum; exact `0xF4` footer; strict UTF-8; and bounded total noise/frame bytes. Duplicate, stale and late indexes are rejected, including a response arriving after a timed-out index has been retired. False header patterns inside active payloads remain payload bytes.

Response payload parsing is strict duplicate-key-rejecting JSON for the JSON candidate and separately explicit Python-literal fixtures only for discrepancy comparison. No fallback raw string is accepted as acknowledgement. No candidate is labeled device-correct without accepted physical evidence.

## Required synthetic proof

Without importing or executing a device library, prove:

- the checksum discrepancy over this closed rule set only: the handoff's stated additive rule, additive sums over data-only and script-only bytes, their 8-bit complements/two's-complements, and XOR over data-only/script-only bytes. Record which rule yields each value or that no rule in this named set yields it; never imply that excludes every possible rule;
- this exact closed fixture set: the reported `cyberpi.get_bri()` TYPE_SCRIPT vector, the same expression rebuilt under the handoff additive formula, the reported TYPE_ONLINE frame, and the reported TYPE_OFFLINE frame. Each fixture records exact bytes, provenance, packet class and assumption label; none is a device-correct oracle;
- incremental parsing across every byte split;
- rejection of malformed header, header checksum, outer length, inner length, packet type, mode, index, payload checksum, footer, UTF-8, duplicate keys, non-object payload, overflow and trailing bytes;
- false-header patterns inside payload, stale/late response, duplicate response and retired-index behavior;
- strict distinction among JSON `null`, Python `None`, device error and malformed payload;
- no general expression input or non-enumerated frame construction;
- file-specific AST/static absence of imports, calls, dynamic import, `eval` and `exec` for serial/device-node access, subprocess, network, movement, display, light, audio, REPL, reset and subscription surfaces in executable created code, while permitting inert named fixture bytes, test deny-list names and documentation; the ambient-brightness fixture is explicitly reported as sensor-related inert data;
- accepted Flow A, gateway, Misty and D-198 file hashes unchanged;
- an isolated child audit hook denying network, process creation, filesystem mutation, every open of `/dev/cu.*` or `/dev/tty.*`, and imports of `serial`, `makeblock` or `cyberpi`; each denial is exercised by a controller self-test. The controller uses finite streaming output limits and timeout and writes only to a new absent durable evidence directory.

The exact test count, hashes, manifest hash, interpreter, command and evidence path are fixed before execution review.

## Acyclic pins and repository sequence

If accepted, this proposal is copied byte-identically to `knowledge/proposals/IIW_MBOT2_CYBERPI_PROTOCOL_VERIFICATION_PROPOSAL_2026-11-05.md` and committed with its prospective decision and synchronized state before package creation.

This phase does not freeze, delay or constrain correction, review or commit of the six D-198 files. Before committing this proposal, a read-only reconciliation must inspect the D-198 manifest/controller for HEAD, canonical-state or exact-status dependencies and record whether the proposal commit would invalidate them; if it would, D-198 is resolved first or its bases are separately corrected and re-reviewed. If D-198 changes after this proposal review, every affected hash/base in this phase is regenerated and blindly re-reviewed. During create-only work, the exact then-current D-198 paths and the excluded PI proposal may coexist with this phase's five files; the excluded proposal is never read. No execution controller may run until D-198 is separately accepted and committed or its exact coexistence is explicitly pinned in the execution proposal.

The manifest pins the three created source/test/doc files and every protected accepted/D-198 file, but not itself or the controller. The controller pins the manifest SHA-256, records its own SHA-256, verifies exact permitted status and before/after hashes, and refuses every other path. This avoids a hash cycle.

Ordered sequence: (1) PI accepts and commits the exact proposal, decision and synchronized state after the D-198 reconciliation; (2) create only the five files; (3) both blind gates review every complete file and exact hash; (4) PI accepts and commits only the exact package, decision and synchronized state; (5) create an external execution proposal/request pinning the committed HEAD, controller, manifest, exact command, new absent evidence directory, expected test count and exact permitted status; (6) blind dual review; (7) prospective PI authorization; (8) exactly one bounded no-retry synthetic execution; (9) blind dual evidence review before acceptance or use. At execution, repository status contains only the unrelated excluded PI proposal unless a separately reviewed request explicitly pins another exact coexistence.

## Later physical-probe boundary

No physical probe is authorized here. A later proposal must select one exact USB device through a fresh manual preflight, record the selected unit and firmware claim without treating a device path as identity, keep the chassis stationary with wheels raised, establish immediate power-switch access, address stored boot programs and DTR/RTS reset behavior, and specify one candidate frame, one connection/open, finite boot/read/write deadlines, exact byte limits, no retry and immutable evidence.

Physical evidence must capture bounded raw boot/response bytes and parser facts without claiming the candidate was correct merely because a response arrived. If no candidate has adequate primary-source support, the PI must explicitly accept the risk of one bounded observational probe. No display, LED, sound, sensor, movement, online transition or arbitrary expression is permitted in that first probe unless separately reviewed.

## Future adapter and lifecycle holds

Only after protocol evidence is accepted may an adapter proposal map the accepted gateway constants `pts.ask_dance_question.v1` and `pts-robot-invitation-v1` to internal commands. `dispatch()` and `stop_to_neutral()` remain methods, not gateway action names.

That proposal must resolve persistent-output completion truthfully. It must either add a separately reviewed lifecycle owner or define a truthful completion source compatible with the coordinator; prove expiry after successful invitation reaches neutral; define single-handle ownership across boot/dispatch/stop/close and stop during boot; serialize stop against dispatch; cancel remaining invitation frames so a late invitation cannot be the last write; define stop-before-dispatch, partial neutral, exact neutral including online-mode disposition, who invokes close and consumes its result, receipt caching and the accepted one-stop rule; pin numeric budgets against the coordinator's 10-second completion and 3-second waits; pin exact receipt fields; and bind a real unit/firmware without overstating identity. Public endpoints remain a later authenticated, rate-limited, replay-protected phase with no arbitrary device commands.

## Claim and authority boundary

This proposal authorizes no implementation or execution. No import, compilation, lint, test, dependency operation, serial or device-node access, Beryl access, listener, QR change, network request, robot contact, display, light, audio, sensor read, movement, REPL, reset, subscription, public endpoint, wallet/WAS work, G28 or G29 is authorized. The unrelated PI routine-tool proposal remains excluded, unread and untouched.

At most, later accepted synthetic evidence can establish internal consistency of explicitly labeled protocol candidates. It cannot establish device behavior, supported control, identity, safety, mBot2 gateway integration, physical action, complete AAuth conformance or suitability for public use.
