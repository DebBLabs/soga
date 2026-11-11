# mBot2 first bounded protocol observation proposal
Date 2026-11-09. Draft for blind static review. Execution requires later approval.

## Purpose and evidence basis
The PI accepted CyberPi synthetic evidence after 177/178 PASS. The candidate
parser and fixtures passed 14 offline tests at HEAD
5ac840123ae9301a415d7631374a03ae8e18d805. This establishes internal candidate
consistency only. The G handoff remains engineering input, with checksum and
return-grammar contradictions. No primary-source proof yet supports selecting
a device-correct wire candidate.

Propose one stationary, bounded observation of a literal no-output expression.
The PI must explicitly accept the uncertainty of one observation under this
candidate before physical execution. A response alone will not establish wire
correctness or a usable adapter. Public Flow A and both accepted gateway paths
remain preserved.

## Proposed exact command candidate
One frame only, using the handoff additive candidate, TYPE_SCRIPT 0x28,
mode 1, index 1, expression bytes 4e 6f 6e 65 (literal None).
The intended meaning is a return value with no requested sensor, output,
movement, mode transition or persistent behavior. Device interpretation is
unverified. Exact proposed wire bytes:
f3 fd 0a 00 28 01 01 00 04 00 4e 6f 6e 65 be f4

Arithmetic for independent review: body length 10, header sum
(0xf3 + 10) mod 256 = 0xfd, body sum
0x28 + 1 + 1 + 0 + 4 + 0 + 0x4e + 0x6f + 0x6e + 0x65 = 446,
446 mod 256 = 0xbe. This is a new observation fixture, not an extension of
the accepted four-fixture module. It must be isolated in its own reviewed
instrument. No caller-provided expression or frame builder is proposed.

## Preflight and operator control
The last PI report has the robots powered off. Fresh preflight records the
selected mBot2 and every present Misty unit individually. All Misty units remain
outside this observation.
Before any open, the PI manually selects one physical mBot2/CyberPi and confirms
unit/firmware claim and USB association. A path is not identity. A separately
reviewed manual preflight must record the exact path from fresh operator
inspection; no wildcard, discovery loop, reconnect or fallback is allowed.
The chassis is stable with wheels raised, immediate power-switch access,
and no competing serial owner. Stored-program preflight is a separately approved operator step,
not authority to power on from this proposal. With USB disconnected and wheels
raised, the PI powers the selected unit from its battery for at least 15 seconds.
The PI records the initial screen/LED state and confirms no wheel/motor motion,
sound, LED animation, autonomous screen changes or visible autonomous program.
If uncertain, or any prohibited behavior occurs, motor power is cut and this
proposal cannot proceed. A quiet 15-second observation is limited observational
assurance, not proof that delayed stored code cannot run; this residual risk
must be explicitly accepted before USB open. No reset, firmware update, upload,
or stored-program deletion is authorized by the check.

Before USB connection, identify and test by operator inspection the control
that removes shield/motor battery power and the separate USB disconnect that
removes USB-supplied CyberPi logic power. Battery power can also feed logic;
the defined complete abort is battery switch off followed by USB disconnect.
If the selected unit cannot be fully de-energized by these controls, stop.
The PI remains within reach of both throughout the attempt.

One serial open may itself reset CyberPi and execute stored boot behavior
through driver DTR/RTS defaults. No software reset or DTR/RTS toggling is
requested, but that cannot eliminate open-induced reset uncertainty. Exact
driver behavior and the operator's acceptance of this risk must be reviewed
and pinned in the later physical request. A manual shutdown is always allowed.

## Bounds and records
Use only standard-library POSIX I/O through os, termios and selectors,
with one os.open using O_RDWR | O_NOCTTY | O_NONBLOCK and O_NOFOLLOW.
Require a character device at the manually pinned canonical path. Configure
raw 8N1: clear input/output/local processing flags, clear CSIZE/PARENB/CSTOPB
and CRTSCTS if present, set CS8 | CLOCAL | CREAD, VMIN=0, VTIME=0, input/output
baud B115200. Retain the existing HUPCL setting and record it. No explicit
DTR/RTS ioctl or break/reset operation. Raw setup occurs after open and cannot
prevent open-time line changes. Pin the actual interpreter and standard-library
native dependency files in the later runtime manifest. No third-party serial
library or dependency installation is proposed.

One owned serial handle at the engineering-input settings 115200, 8N1.
No online/offline transition, REPL, subscription, sensor expression, light,
screen, audio or motor command. One write attempt of exactly 16 bytes only,
with a 0.5-second write deadline. A short or ambiguous write ends the attempt;
no suffix write or retry follows.

Start a monotonic boot clock immediately after open. Collect passively for
the full 12.0 seconds, never ending early on an empty read. The deterministic
write trigger is T=12.0 seconds or the first scheduler opportunity afterward,
only if less than 4096 boot bytes have arrived, no abort/error occurred, the
20-second wall budget still permits the entire write/response budget, and no
serial byte arrived in the last 1.0 second. Boot bytes still arriving at the
deadline therefore end the attempt without writing. Reaching 4096 boot bytes,
read error, character-device change, process SIGINT/SIGTERM or operator abort
ends it without writing. No boot byte pattern is interpreted as permission
to write, and no content-dependent alternate command exists.

The PI watches for wheel/motor motion, sound, LED animation or screen changes
from the recorded baseline throughout USB connection, open, capture and close.
Any such change is an operator abort even if it might be normal firmware
behavior. The PI presses Ctrl-C and immediately turns battery power off and
disconnects USB, prioritizing physical power removal over software response.
The instrument records a caught signal and closes in finally. A separate
operator postflight records any observation and power-removal time; a kill
or abrupt power cut may leave incomplete software evidence, which is itself
recorded without claiming a clean close.

After the one write, collect at most 2 seconds and 1024 bytes; total raw
capture at most 5120 bytes. Frame
assembly remains bounded by the accepted 256-byte body limit. The whole
instrument has a separately enforced 20-second wall deadline. No acknowledgement
may trigger a second command. Close exactly once in finally; record its result.
Closing the tty may drop DTR/HUPCL and cause another reset. Its behavior is
uncertain. Keep wheels raised and both power controls within reach until the
PI has turned the battery switch off and disconnected USB after close.
Regardless of close success, the defined end state is both sources removed
and the unit visibly powered off. Record the close outcome and the PI's
postflight confirmation and time. If close fails, disconnect without reopen.
Nothing after close is serial-captured or interpreted; post-close behavior
is solely an operator observation. A missing postflight leaves the end state
unconfirmed and the observation unusable for adapter decisions.

Capture raw boot and response bytes, exact sent bytes and write return,
timestamps, exceptions, limits reached, close outcome, and parser candidates
with rejection facts. Preserve raw data if grammar fails. Distinguish JSON
null, Python None text, error, silence, and unparseable response. An offline
comparison may use only the accepted explicit fixture grammar; no eval or
arbitrary literal evaluation. Never normalize malformed text into an ACK.
Silence or any fault is a terminal observation, not a retry invitation.

## Ordered authorization
This proposal is design only. First reconcile the accepted offline evidence
into canonical decision/current-state records. Preserve its raw evidence
externally and hash-pin it in the decision. A repository evidence report, if
desired, requires its own explicit D-199 coexistence amendment. Such records
must precede committing this proposal or any observation package.

After both blind proposal reviews and PI acceptance, create exactly six files
in an external staging tree, using these eventual relative paths:
1. robot_gateway/cyberpi_none_observation.py
2. tests/test_robot_gateway_cyberpi_none_observation.py
3. tools/robot_gateway/run_cyberpi_none_synthetic.py
4. tools/robot_gateway/run_cyberpi_none_physical.py
5. tools/robot_gateway/cyberpi-none-runtime-manifest.json
6. robot_gateway/CYBERPI_NONE_OBSERVATION.md

The synthetic controller denies all network/device/filesystem-mutation
capability in its child and uses fake injected I/O for probe tests. It never
imports the physical controller or opens a device. The physical controller
alone owns serial access. Both are separately pinned and reviewed.
Before any proposal/package commit, separately review and accept an exact
D-199 coexistence amendment for the new proposal plus these six paths.
Do not silently widen existing controllers. Any changed Misty protected
hashes require a separately reviewed CyberPi repin before a future CyberPi
execution. Previously accepted evidence remains tied to its historical HEAD.
All new execution requests pin the then-current committed HEAD, exact status
and all protected artifacts. Every complete
created file requires blind dual static review, PI acceptance and commit.
An external execution request then pins the committed HEAD, actual interpreter
and complete serial runtime dependency bytes, exact command, selected device
preflight, new absent evidence directory, output limits, controller wall
deadline and no-retry policy. Both gates review it, then the PI may authorize
one physical attempt. Synthetic tests of the instrument need their own reviewed
request and PI authorization first. Physical evidence needs blind dual review
and PI acceptance before adapter use.

D-195 and all physical holds remain open until the later request explicitly
disposes of completion, restart/lock, stop verification and exact invocation
for this observational scope. Neither this draft nor its static PASS releases
those holds. This proposal does not authorize turning on or connecting a robot.

## Pre-registered interpretation
Only a complete bounded response with the candidate header/body/footer,
additive checksum, TYPE_SCRIPT, mode 1, index 1 and strict envelope grammar
can enter the first three rows. Other modes or indexes are unparsed raw data.

| Outcome | Supported interpretation | Limit |
|---|---|---|
| JSON ret:null | Consistent with one additive-framed response to the None candidate | No claim about output-command ACKs or general wire correctness |
| Explicit ret:None literal fixture | Consistent with the separate Python-text grammar candidate for this expression | Not JSON and not silently converted to an ACK |
| Strict err envelope | Consistent with a response/error path for the frame candidate | No proof of eval semantics or device correctness |
| Silence | No interpretable response observed | Inconclusive among framing, checksum, mode, readiness, timing and reset |
| Different response mode/index, malformed or overflowed bytes | Raw observations preserved with named rejection facts | No acknowledgement or compatibility claim |
| Abort, partial write or close failure | Bounded failed observation with recorded uncertainty | No retry or adapter use |

No outcome establishes supported control, output completion, adapter
suitability or physical safety. Synthetic tests must exercise every write
trigger/abort/outcome row and close-finally path before any physical request.
