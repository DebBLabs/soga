# CyberPi literal None observation — supported cold-sign draft

Complete outside-repository implementation draft following PI adoption of
313/314 with recorded drafting requirements. NO execution authority. Accepted
code, evidence, requests, enrolled key and iPad app remain intact. This design
supersedes the old isolation/battery-prerequisite schema only after full draft
review, final reconciliation, PI acceptance and separately authorized commit.
No changed tests have run. This guide is not a physical instruction to act now.

## What the accepted observation establishes

The November 20 operator record reports 15 seconds USB connected, blue lights
and a charging display followed by blank screen, no wheel rotation, sound or
support shift, and blue light out after unplug. Exact blue component, steadiness,
transition durations, electrical rails, charging current and total shutdown
were NOT measured. Do not call the blue light an eye or infer rail isolation.
The actual photo shows a light-blue box/support and dark block under the chassis;
far-wheel clearance and dynamic stability are operator judgements, not facts
proved by that photograph. Deb reported only two drive wheels are motorized.

## Explicit amended configuration

Motors stay connected; chassis rests freely on existing passive support with
both wheels completely clear. No straps, construction, motor-cable removal,
helper, battery access or disassembly is required or authorized by this draft.
Shield OFF is an observed switch state, not proof of motor/battery isolation.
The fresh 15–300-second battery-only power-on observation is RETIRED, not claimed
complete. No fresh battery power cycle is included. Stored programs and USB /
serial-open resets may still occur. Current support adequacy, wheel/object/edge
clearance, cable routing, reachable OFF control and independent Mac-end unplug
must be confirmed cold by Deb before an attempt. No physical certification.

Wheel rotation alone is allowed during USB phases only while both wheels remain
wholly clear and the chassis/support stays still. Any chassis/support shift,
contact/loss of clearance, snag risk, sound, repeated resets/flashing, abnormal
heat/odor or uncertain behavior means immediate Mac-end USB removal and terminal
refusal. Do not reach for rotating wheels, catch or restrain a moving robot.
After power removal and observed wheel cessation, any repositioning requires
its own consent. Continued activity with USB removed and switch already OFF is
recorded as unknown-source continued activity, not shutdown; stay clear and keep
others clear. No electrical, hardware-stop or delayed-behavior guarantee exists.

## Exact cold preflight schema (24 keys)

The parent validates this record without querying an attached device. The
worker later reuses the same cold record, additionally checking live metadata.
Fields labelled at_approval remain historical cold facts after USB is connected.

Retained: confirmed_by, observed_at, device_path, device_rdev, unit_claim,
firmware_claim, wheels_raised, power_controls_accessible, no_competing_owner,
misty_units, attempt_id, host.
Added: shield_switch_off, motor_connection_state, support_configuration,
usb_connection_state_at_approval, usb_startup_evidence_sha256,
device_identity_basis, device_identity_record_sha256, support_clearance_confirmed,
accept_connected_motor_uncertainty, accept_freely_resting_support_uncertainty,
accept_usb_stop_uncertainty, serial_topology_unambiguous.

Exact set equality rejects missing/extra keys and the old battery/isolation
schema. confirmed_by is Deb. Nonempty bounded unit/firmware/attempt/host claims
remain exact bindings. Firmware remains a historical claim, not a fresh query.
Nine true holds (wheels_raised, power_controls_accessible, no_competing_owner,
shield_switch_off, support_clearance_confirmed, the three accepts, and
serial_topology_unambiguous) require literal Boolean true, never integer 1.
Set them only from current facts and Deb's actual explicit acceptance for this
attempt, never a default or static review PASS.

Modes are exactly connected_no_isolation_claim,
assembled_freely_resting_passive_support, disconnected, and
prior_passive_record_rechecked_at_open for their corresponding fields.
usb_startup_evidence_sha256 is fixed to the accepted record
10d86396e771db383e2989712883a05cef4ca9f89ca748f7c030b958af0cdb7f.
device_identity_record_sha256 is a lowercase 64-hex digest bound to the request.
observed_at is actual cold-check completion, positive finite numeric time, with
0 <= initial gateway wall time - observed_at <= 120. Misty inventory must exactly
match these two entries, with literal true exclusion, both powered_off:
Misty A urn:debblabs:misty-a:20221304273;
Misty B urn:debblabs:misty-b:20193802932.
No prior observation supplies current safety facts automatically.

## Prior passive identity record (10 keys; maximum 16384 bytes)

A separately reviewed, PI-authorized passive identification session must produce
a canonical regular external file. That session requires its own powered-exposure
review; it is not a metadata-only formality. No such live record is created here.

Exact keys: schema, confirmed_by, host, unit_claim, device_path, device_rdev,
observed_at, method, approval_reference, namespace_unambiguous.
Require schema=cyberpi-passive-identity-v1, confirmed_by=Deb,
method=manual_usb_namespace_metadata_no_serial_open, namespace_unambiguous=true
(literal Boolean), and a nonempty <=128-character ASCII token reference to the
actual prior approved session. observed_at must be positive finite numeric time
not later than the cold preflight observation. No maximum record age is claimed.
Host/unit/path/rdev must match cold preflight; host/unit also match request.

Path must be a nonempty printable-ASCII /dev/cu.* name with no further slash or
whitespace, at most 1024 characters. rdev must be a nonnegative int excluding
bool. This path/rdev identifies an OS node, not cryptographic robot identity.
Reconnection can change it and therefore refuse. Do not fall back or refresh it
inside the attempt. No historical port is selected by the code.

Parent read_regular rejects symlinks/noncanonical/nonregular files and bounds
identity-file bytes before decoding. Duplicate JSON keys refuse. Its actual
SHA-256 must equal BOTH the stable request and preflight digest fields. The
parent validates its schema/bindings before exclusive evidence reservation;
pins also records its exact bytes in before/after snapshots. Live worker lstat,
canonical /dev parent, character-device/rdev, exact open flags and opened-fd
identity checks remain. Same-account/privileged mutation and TOCTOU limitations
remain; neither prior record nor snapshots are hardware attestation.

## Stable request and signer compatibility

Request schema adds device_identity_record, device_identity_record_sha256,
execution_policy to the old 21 keys: 24 exact keys. execution_policy must equal
cold_sign_supported_usb_v1. Bind actual committed HEAD/status, new controller/
manifest/source/runtime pins, exact unit/host/Misty claims, operation, limits,
new absent evidence path, live record/signature paths, reviewed key and verifier.
Cold preflight binds attempt/host/unit/firmware/Misty inventory and identity hash.
All old requests, including 299/300, are incompatible with changed bytes.

Authority retains exactly the ten existing keys: stable_request_sha256,
preflight_sha256, attempt_id, approved_by, approval_reference, approved_at,
expires_at, attempts, accept_candidate_uncertainty, accept_reset_uncertainty.
Digest fields are lowercase 64 hex; approved_by=Deb, attempts integer 1 and both
uncertainty flags literal true. attempt_id is a <=128-character ASCII token
beginning cyberpi-none-v3-physical- with a nonempty suffix. approval_reference
is a <=128-character ASCII token beginning
cold-sign-lifted-connected-stop-uncertain-v1.
with a nonempty unique actual approval suffix. Allowed token characters are
ASCII letters/digits/period/hyphen/underscore, matching the existing Swift app.
No new signer fields, app rebuild, key enrollment or signature semantics.
Times are integer seconds with 0 <= approved_at < expires_at < 10000000000 and
expires_at-approved_at <=120. The existing stricter runtime chronology also
requires observed_at <= approved_at <= wall_now < expires_at <= observed_at+120.

Deb reviews the actual cold facts/risk accepts and both exact digests before
explicit approval. Authority bytes are compact sorted-key canonical ASCII JSON,
no newline or alternate serialization, for the current iPad parser. Only Deb
signs those bytes; the iPad shows authority fields/hashes, not parsed cold
preflight facts. Use an independently checked new accepted paper stable digest.
The controller verifies the signature through the pinned verifier/dependencies;
it does not prove who touched the signer or factual truth. Private key remains
unavailable to agent processes; no enrollment/private material in the gateway.

## Signing and active USB sequence — separately authorized later

A. All robots off; mBot2 USB disconnected. Record fresh cold conditions and
actual observed_at. Deb accepts the current configuration/risks and exact facts,
then actual approved_at is captured. No timestamp-only refresh.
B. Keep mBot2 USB disconnected through direct Finder transfer to offline iPad,
Inspect once, deliberate digest comparison, confirmation/authentication/signing,
return and receipt verification. Airplane Mode/Wi-Fi-off rules remain. No cloud
route, re-Inspect, second signature or replacement authority. Finish receipt
by observed_at+75 or refuse without connecting. This supersedes the old +90
receipt target but keeps the +90 invocation and hard +120 open deadlines.
Full timing/skew are unmeasured; possible refusal is accepted, not proof of fit.
C. Before USB, finish ALL logging/platform permissions/unlock preparations.
If a human click, unlock, platform approval, typing or Mac action would be
needed during invocation, refuse before connecting. Deb's attention stays on
mBot2 during energization/capture. No chat report until after unplugging.
D. With visible clock/timer ready, connect mBot2 once with switch OFF. Require
blue lights plus charging/startup display followed by blank screen within
15 seconds. NO visible change at connection is a refusal (the unobserved
alternative in proposal r1 is narrowed). Blank screen and visibly STABLE blue
indicator(s) define the prospective connected settled state. Steadiness was
NOT measured in 311/312; it is a fresh acceptance criterion, not historical fact.
Unknown/different/changing/continuing/repeated visuals refuse; unplug, no retry.
E. If settled, CG invokes only the exact approved request command by both
observed_at+90 AND connection+15 seconds, with no human attention shift. If
coordination cannot fit, unplug/refuse. Existing pre-open freshness and cutoff
can still refuse after reservation. No robot movement/output command is added.
F. Deb observes continuously throughout the existing post-open passive window.
No visible change OR one same USB-reference startup pattern is allowed only
within that 12-second window, settled before its end. This reset behavior is
prospective/unobserved, not a tested property of the unit. If Deb cannot reliably
recognize/time the window and act, refuse. The controller prints no real-time
open marker and has no vision gate; automatic write can race with human noticing.
New/continuing visual changes during write/response/close require unplugging.
G. Unplug promptly after capture, and at most 65 seconds after USB connection
regardless of process state, or sooner on stop conditions. The 65-second cap is
PROCEDURAL, not controller-enforced USB-age or hardware shutdown. Parent startup
has no guaranteed 30-second bound; late/stalled work may be cut short. Exposure
up to 65 seconds is unproven by the 15-second sample and needs explicit PI risk
adoption/attempt authority. A timely open can finish after signed expiry under
existing capture bounds. Interrupt after physical unplug if needed, preserve
all partial evidence, and record actual postflight behavior/power state.

## Unchanged protocol, process and evidence limits

The pure observe algorithm/device seam, 16-byte literal None frame, parser,
HUPCL behavior and one-open/one-write policy are unchanged. Passive boot 12s,
final serial quiet 1s, boot cap 4096 bytes, write readiness 0.5s, response 2s/
1024 bytes, worker wall 18s and parent capture 20s/32768 bytes remain. Serial
quiet does not prove physical/visual safety. Existing clock discontinuity and
one-second gateway wall/monotonic divergence checks remain; not iPad clock skew.
Parent startup, hashing and signature validation are outside capture budgets.

Exclusive reservation consumes the attempt even if persistence/worker work
fails; any invocation is consumed as policy even before reservation. Preserve
partial directories. No retry, reopen, suffix write, fallback, stale-fact refresh
or automatic power cycle. Signal forwarding/watchdogs/unknown close behavior
remain: missing worker report means close unknown, parent SIGKILL may orphan
worker until its own budget, watchdog/power loss can lose raw worker bytes.
No process report proves physical shutdown. Record postflight separately.

Strict JSON null/Python None/error responses prove only that exact response to
the candidate expression. Silence is inconclusive. Malformed/wrong-index/mode
frames remain rejection facts. No ACK/completion/neutral, motor readiness,
physical stop, mission, concurrency or gateway switching success is established.

## Static staging and next gates

Six complete files only. The fake-only suite covers policy/schema/hash/identity
and existing algorithm/clock/reservation/signal seams. Static method count is
recorded in the manifest, not a claimed test result. No imports, compilation,
lint or tests are authorized by drafting or PASS. A new exact offline request,
blind review and separate PI execution approval are needed after final package
acceptance/reconciliation and authorized commit.

The final manifest preserves existing protected pins and historical evidence,
including external accepted observation/adoption records. It now pins the complete
proposed canonical records and the inspected pre-change repository basis
0c0ff6fcfe72835a939c4ff197cc369ce17be9b7. Final blind reconciliation review
and separate exact eight-file commit authority remain required. Future exact
requests must bind the actual new HEAD, not this documentary pre-change basis.
No Misty, shared gateway, public Flow A or existing status guard changes. Inspect
actual original-basis coexistence impacts before any commit. Preserve old
accepted packages and evidence at original hashes; do not silently repin.

After accepted revised offline evidence, obtain reviewed passive identity data,
create/review a new exact physical request against actual HEAD and all final
hashes, replace the trusted paper digest, and separately approve cold preflight,
iPad signing and one invocation. This draft does not authorize any powered step.
