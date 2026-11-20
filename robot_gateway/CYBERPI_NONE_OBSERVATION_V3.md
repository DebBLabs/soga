# CyberPi literal None observation — shield-ON cold-sign draft

Complete outside-repository draft following Deb's acceptance of proposal369/370,
USB evidence367/368 and identity371/372. NO execution authority. Accepted files,
repository, Misty/public FlowA/shared gateway, prior evidence and signer stay
intact. Commit, tests and physical work each require later explicit authority.
No candidate code was imported, compiled, linted, tested or executed to draft it.

## What the accepted observation establishes

The November 20 operator record reports 15 seconds USB connected, blue lights
and a charging display followed by blank screen, no wheel rotation, sound or
support shift, and blue light out after unplug. Exact blue component, steadiness,
transition durations, electrical rails, charging current and total shutdown
were NOT measured. Do not call the blue light an eye or infer rail isolation.
The actual photo shows a light-blue box/support and dark block under the chassis;
far-wheel clearance and dynamic stability are operator judgements, not facts
proved by that photograph. Deb reported only two drive wheels are motorized.

The later operator-authorized replacement cable AND changed Genesys hub port
produced USBSerial 1a86:7523 at location 0x00120000. Exact365/366 one-shot metadata
capture saved /dev/cu.usbserial-120, rdev 150994951, and a matching AppleUSBCHCOM
registry entry carrying that callout path. The flattened archive does not save
raw parent links; physical identity is Deb's attestation, not cryptography.
Deb accepted367/368 evidence and371/372 R2 identity and confirmed current OFF,
unplugged, stable. Exact prior powered duration, prompt/click and in-session
wheel/sound/support recall remain unknown; ask once before any future powered
step and retain unknowns. No cable-alone cause or firmware attestation is claimed.

G's recovered original Gemini notes distinguish the source iMacPro bundle and
old1470 port from laptop migration. Vendor serial instructions use switchON;
neither source proves OFF cannot enumerate on the new cable/port. Deb chose ON
design without another OFF-only diagnostic, accepting necessity is unproven.

## Explicit amended configuration

Motors stay connected; chassis rests freely on existing passive support with
both wheels completely clear. No straps, construction, motor-cable removal,
helper, battery access or disassembly is required or authorized by this draft.
Shield OFF remains the cold pre-signing state, not proof of motor/battery isolation.
The later active phase explicitly switches ON after USB insertion. Battery power
can start stored programs; unplugging alone cannot be treated as a stop.
The fresh 15–300-second battery-only power-on observation is RETIRED, not claimed
complete. No fresh battery power cycle is included. Stored programs and USB /
serial-open resets may still occur. Current support adequacy, wheel/object/edge
clearance, cable routing, reachable OFF control and independent Mac-end unplug
must be confirmed cold by Deb before an attempt. Both shield OFF and Mac-end
unplug must be reachable without crossing wheels. No physical certification.

Wheel rotation alone is allowed during USB phases only while both wheels remain
wholly clear and the chassis/support stays still. Any chassis/support shift,
contact/loss of clearance, snag risk, sound, repeated resets/flashing, abnormal
heat/odor or uncertain behavior means immediate shield OFF FIRST, then Mac-end USB removal and terminal
refusal. Both actions, not either alone, are required; their effect is not guaranteed. Do not reach for rotating wheels, catch or restrain a moving robot.
After power removal and observed wheel cessation, any repositioning requires
its own consent. Continued activity after switchOFF and USB removal is
recorded as unknown-source continued activity, not shutdown; stay clear and keep
others clear. No electrical, hardware-stop or delayed-behavior guarantee exists.

## Exact cold preflight schema (25 keys)

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
accept_usb_stop_uncertainty, serial_topology_unambiguous, accept_shield_on_battery_program_uncertainty.

Exact set equality rejects missing/extra keys and the old battery/isolation
schema. confirmed_by is Deb. Nonempty bounded unit/firmware/attempt/host claims
remain exact bindings. Firmware remains a historical claim, not a fresh query.
Ten true holds (wheels_raised, power_controls_accessible, no_competing_owner,
shield_switch_off, support_clearance_confirmed, the four accepts, and
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

accept_shield_on_battery_program_uncertainty must be literal true. It binds cold
acceptance of the later ON phase, possible stored battery programs, freely
resting connected-motor support and two-action stop uncertainty. shield_switch_off
must still be literal true because the cold fact is taken BEFORE signing, all
robots OFF and mBot USB absent. No software switch sensor or stop guarantee exists.

## Prior passive identity record (10 keys; maximum 16384 bytes)

A separately reviewed, PI-authorized passive identification session must produce
a canonical regular external file. That session requires its own powered-exposure
review; it is not a metadata-only formality. Deb accepted the367/368 capture
and371/372 R2 record. The final external identity is
robot-gateway-work/accepted/MBOT2_PASSIVE_IDENTITY_2026-11-20.json,
SHA-256 ad9aefa7a48e2c33d5498e5f352283dcc288348e5fac7e72e6272e60aab807c2.
Its companion binds shield ON, same replacement cable/hub port0x00120000 and
snapshot 48cde73ada109a64657c97108b6c0f3cc7bd298c2e2a037ddbac718a047b50c7.
These records are protected by the draft manifest. No new live session occurs
while drafting. Identity belongs to hostMac and exact unit_claim
"Debs assembled mBot2 with CyberPi from the November 5 setup handoff".
The future preflight/request must reuse that exact text and the accepted
path/rdev; if live checks refuse after reconnect, do not change the record.

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
cold_sign_supported_usb_shield_on_v2. Bind actual committed HEAD/status, new controller/
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
cold-sign-shield-on-lifted-connected-stop-uncertain-v2.
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

A. All robots OFF; mBot2 USB disconnected. Record fresh cold conditions, actual
observed_at and the 25 exact fields, including new ON-risk acceptance and truthful
shield_switch_off. Obtain Deb's recall once of the prior manual session and
record supplied details/unknowns without inventing timing or motion facts. This
is not another power/display trial. Deb accepts actual cold facts/risks and exact
request/preflight digests, then actual approved_at is captured. No time-only refresh.

B. Keep mBot USB absent through direct Finder transfer to offline iPad, Inspect
once, deliberate digest comparison, authentication/signing, return and receipt
verification. Airplane Mode/Wi-Fi-off rules remain. No cloud, re-Inspect, second
signature or replacement authority. Finish receipt by observed_at+75 or refuse.
The existing invocation observed_at+90 and hard observed_at+120 open deadlines
remain. After receipt disconnect iPad from the Genesys hub BEFORE mBot USB goes
in. Hub stays connected; use SAME replacement cable and SAME mBot hub port whose
accepted location is0x00120000. No other USB changes while mBot is connected.
No claim that this topology bypasses accessory policy. Later live path/rdev
checks can refuse after reconnect; no scanning fallback or automatic port change.

C. Finish logging/platform permissions/unlock preparations before USB. Position
robot/wheels, Mac screen/pointer and independent clock/timer in one sightline,
both stop controls safely reachable. No human Mac action during invocation or
capture. The sole exception is ONE identifiable accessory Allow click BEFORE
invocation while robot remains continuously visible; no typing, credentials,
settings/navigation, screenshots, Home-button presses or window hunting. If a
click/coordination cannot fit, decline/refuse, never extend the timer. A granted
approval persists as OS state: record action, later retention/revocation is Deb's
decision. No agent policy change or approval clicking is authorized.

D. Insert USB once with shield OFF, start timer AT insertion, then promptly switch
shield ON only if no motion, sound, support/clearance change, heat/odor or unknown
behavior occurs. Initial OFF insertion may show no immediate visual change, blue
light(s), charging/logo display or blank/dark; DO NOT wait for OFF startup to end.
ON startup prospective allowed classes are white light, blue light on Pi, one
logo transition, then blank/dark. These combine reported visuals
and a prospective acceptance rule, not a claim all transitions were measured.
Require a visually settled blank/dark display with no continuing transitions/
repeated flashing/resets by connection + 12s, leaving up to 3s for invocation by
connection + 15s. Settling after 12s, an unclear cue, or invoking after 15s refuses;
no deadline extension. Lights do not prove data readiness. No Home
tap is permitted to achieve settling. Unexpected/uncertain visuals stop/refuse.
Host node validation, not display appearance, is the later serial-identity guard.

E. If settled, CG invokes only the exact separately approved command by BOTH
observed_at+90 AND connection + 15s. No extra pre-invocation /dev query is included;
the existing worker checks the exact accepted path/rdev at open. If it is absent,
changed or not yet published, refuse; no fallback and the invocation is consumed
even if failure precedes reservation. Platform prompt, late cue or coordination
failure means shield OFF+unplug/refuse, not an extension. Parent startup has no
30s guarantee. Signing/transfer/timing fit has not been demonstrated end-to-end.

F. Deb watches throughout the unchanged 12s post-open passive window. Allowed:
no visible change OR one startup sequence from D's ON classes that settles to
blank/dark before that window ends. Reset behavior on this unit is prospective,
not proven by G's record. No real-time open marker or vision gate exists; write
can race with noticing a problem. If Deb cannot identify/time this reliably,
decline/refuse. Continuing/new visual changes during write/response/close or any
physical stop condition require shield OFF+unplug. No post-start button actions.

G. Stop promptly after capture: shield OFF FIRST, Mac-end unplug SECOND, BOTH by
65s from USB insertion or earlier on any stop/refusal condition, regardless of
process state. Start stopping early enough to finish BOTH actions by the cap.
Battery ON exposure starts only after insertion and ends by OFF, so it is also
bounded procedurally by 65s; neither switch state nor USB age is controller-sensed.
This exceeds the 15s diagnostic samples and is UNPROVEN exposure requiring later
explicit physical approval, not execution permission from proposal adoption.
Unplug alone does not stop battery power; OFF alone is not proof USB is removed.
No stop guarantee. Stay clear, no catching. Any continued activity is recorded,
not called shutdown. A timely open may finish after signed expiry under existing
capture bounds. Interrupt only after physical stop actions if needed; preserve
partial evidence and actual postflight facts, including approximate ON/OFF/USB
and Allow times from memory, wheels/sound/support and final switch/USB/activity.

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

Six complete files only. The new policy, prefix and25th risk key reject old
authority scope; cold OFF stays true. Existing fake-only guard tests now cover
missing/false/non-bool new risk hold, exact old policy/prefix refusal and the
new prefix accepted at 128 characters. No test has run.

The same fake-only suite covers policy/schema/hash/identity
and existing algorithm/clock/reservation/signal seams. Static method count is
recorded in the manifest, not a claimed test result. No imports, compilation,
lint or tests are authorized by drafting or PASS. A new exact offline request,
blind review and separate PI execution approval are needed after final package
acceptance/reconciliation and authorized commit.

The final manifest preserves existing protected pins and historical evidence,
including external accepted observation/adoption records. It now pins the complete
proposed canonical records and the inspected pre-change repository basis
10b9dd657d564e80deec80a044776b7711ffeb06. Final blind reconciliation review
and separate exact eight-file commit authority remain required. Future exact
requests must bind the actual new HEAD, not this documentary pre-change basis.
No Misty, shared gateway, public Flow A or existing status guard changes. Inspect
actual original-basis coexistence impacts before any commit. Preserve old
accepted packages and evidence at original hashes; do not silently repin.

The accepted passive identity/companion already exist, but are not firmware
attestation or proof of future node stability. After accepted revised offline
evidence, create/review a new exact physical request against actual HEAD and all final
hashes, replace the trusted paper digest, and separately approve cold preflight,
iPad signing and one invocation. This draft does not authorize any powered step.

Final reconciliation notes: module/test bytes remain exactly the373/374 accepted
bytes. This final guide narrows prospective visual allowance to blank/dark only
(no CyberOSmenu class), and sets initial settling by connection + 12s so invocation
can still fit connection + 15s. All other action/signer/core budgets remain. Three
source hashes changed from committed baseline; protocol source hash retained.
Canonical D-210 and currentstate are proposed complete outside-repo files; their
hashes are protected by the final manifest. Final8filehashes live only in external
RECONCILIATION.json/txt, avoiding a manifest/canonicalrecord hashcycle. No accepted
373/374 source or historical evidence was modified. This remains unexecuted.
