# Literal-None CyberPi observation instrument

This is a staged unexecuted package implementing the accepted physical design
proposal e4f77a818fd291a69f853d86df9d24cc3afac3bd3c65bb456c060ca4db20f398.
No device has been opened by its authoring. The pure algorithm receives fake
or real I/O from its caller; only the physical controller owns POSIX serial I/O.
The synthetic controller never imports or executes the physical controller.

Before an eventual physical request, the PI must approve the exact synthetic
instrument run, accept its reviewed evidence, and then approve a fully pinned
physical request. The physical request pins committed HEAD/status, controller,
manifest, complete loaded runtime inventory, exact command, absent evidence
directory, one manually selected device, fresh preflight and authority record.
Live interface/D-195 holds require explicit scope disposition in that request.

## Operator preflight to be separately authorized
1. Record selected unit/firmware claim and every Misty unit individually.
   Misty remains excluded. Device path is not unit identity.
2. With USB disconnected, chassis stable and wheels raised, perform the
   separately approved battery-only stored-boot check for at least 15 seconds.
   Record screen and LED baseline and no motion, sound or animation.
   Unknown behavior stops the procedure. Quiet observation does not exclude
   delayed stored behavior; explicit PI uncertainty acceptance is required.
3. Turn motor/battery power off before USB connection. The physical probe
   requires that motor power remain off and logic be USB powered. If this
   cannot be established, stop rather than widen the request.
4. Identify the battery switch and separate USB disconnect. Verify both power
   sources can be removed. Keep both in reach. Close all competing tools.
5. The manually selected canonical /dev/cu.* character device and st_rdev are
   pinned by fresh preflight. No scan, wildcard selection or fallback.
6. Watch during connect/open/capture/close. Any wheel/motor motion, sound,
   LED animation or screen change from baseline means immediate Ctrl-C,
   battery switch off, USB disconnect. Prioritize power removal.
7. After close remove battery and USB power. Record power-off confirmation
   and timestamp in a new postflight record. Nothing after close was captured.

Physical controller must record SIGINT and SIGTERM through explicit handlers.
The outer 20-second worker watchdog may kill a stuck child; then close is
unknown and manual power removal plus postflight is mandatory. No reopen.

## Algorithm and outcome interpretation
Exactly one 16-byte frame:
f3 fd 0a 00 28 01 01 00 04 00 4e 6f 6e 65 be f4.
Full 12-second passive boot, less than 4096 bytes and final one second quiet,
then one nonblocking write syscall with at most 0.5-second readiness wait.
No suffix write or retry, including short write and EAGAIN. Capture at most
2 seconds/1024 response bytes, total 5120. Parser body limit remains 256.

- No write because trigger/cap/budget failed means a bounded readiness refusal.
- JSON null, explicit Python None, or strict error is consistent only with
  that candidate response for this one expression.
- Silence is inconclusive among framing, checksum, mode, timing and resets.
- Other modes/indexes, malformed or excessive bytes remain raw rejection facts.
- Abort, partial write or close failure is a terminal failed observation.
None proves output-command ACK semantics, completion, control or adapter safety.

## Pinning and tests
Manifest sources exclude both controllers and the manifest to avoid hash cycles.
Each controller embeds manifest SHA-256. Its external execution request pins
its own controller and runtime. Protected accepted files are separately pinned.
Synthetic tests use only injected FakeIO and the accepted pure protocol.
Test count is fixed in the manifest and checked before execution.
Staging and review confer no execution or hardware authority.

## Revision 2 signal and gate corrections
The worker has an 18-second internal wall budget inside the 20-second parent
watchdog. It runs in its own process session. Parent SIGINT/SIGTERM handlers
latch the first signal, forward it once to the worker and allow up to one
second for handler/close/report within the original hard deadline. Repeated
parent signals do not interrupt evidence writes. Once the evidence directory
exists, result.json is written in finally. A killed worker means raw bytes
may be lost and close is unknown; result.json explicitly records that fact,
with incomplete observations barred from adapter use. SIGKILL/power loss can
always prevent software evidence and require operator postflight.

The pure module now contains injected SerialIO, preflight/authority validators
and AbortPolicy. It imports no OS/device module. Synthetic tests exercise these
functions with fake os/termios/selectors/stat and fake signal/time facts. They
never import or execute the physical controller, create a child or open /dev.
The physical controller wires only those reviewed pure seams to real stdlib
interfaces after the full authority preflight. A failed raw configuration is
closed through the algorithm's finally. EOF is an abort rather than a poll.
The record distinguishes an attempted write operation from an actual syscall.

Preflight now lists individually excluded, powered-off Misty units. It requires
motor power off and USB logic power confirmed. Response classification uses a
single complete-frame API; extra bytes are unparseable and kept raw.
