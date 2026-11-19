# CyberPi literal None observation, revision 3

Staged outside the repository for static review. The accepted v2 package
and historical evidence remain intact. This successor follows the
two-stage review procedure approved by Deb after gates 217/218.

## Operator and approval sequence

1. Review the exact stable request, schema, facts collection procedure
   and deterministic validation before any preflight. It binds Deb,
   host, attempt ID, exact unit and firmware claims, excluded Misty units,
   literal None operation, controller/manifest/runtime and command,
   reviewed P-256 approval public key, local verifier and its dependencies,
   private fact and approval paths, new evidence path and all limits.
2. Obtain separate approval for live operator preflight. Record each
   Misty powered off and excluded. Close mBlock, serial monitors and
   other robot controllers and verify the intended USB association.
   With USB disconnected, chassis stable and wheels raised, observe
   battery-only stored boot for 15–300 seconds. Record display/LED
   baseline and no wheel movement or sound. Record the observed startup visuals
   using the schema below. Quiet observation cannot
   exclude delayed stored behavior. Confirm both power disconnects are
   within reach, turn motor/battery power off, then connect USB only if
   logic USB power and motor power off are independently confirmable.
   Use one operator-selected canonical /dev/cu.* path and st_rdev.
   Preflight takes metadata only; it does not open serial. Abort if any
   required fact is uncertain. No scan, fallback or competing tool.
3. Record the actual facts, including host, attempt ID and observed_at
   when the check completes. Deb directly approves the exact stable
   request digest, preflight digest, attempt and expiry and accepts
   both candidate and reset uncertainty. Capture the actual approval
   reference. Only Deb signs the exact authority bytes. A review PASS,
   presence of files or successful preflight confers no authority.
4. Key enrollment review must verify that the private key cannot be
   reached by agent processes on the same macOS account. Use an
   independently controlled signer, preferably a separate device or
   non-exportable hardware key requiring Deb's presence. Verify signer
   provenance and public-key fingerprint through Deb out of band, verify
   signing requires her physical action, and inspect enrollment/storage
   paths for absence of a private key or unlock material in agent-visible
   files or environment. This controller verifies a signature, not who
   operated the signer. Verifier executable, linked dependencies and
   signature semantics need exact review before use. Nothing here enrolls
   a key, produces a signature or runs the verifier.
5. If approvals or the run cannot fit within the window, remove both
   sources and stop. No timestamp-only refresh, reopen or retry. Before
   exclusive evidence reservation, the one-invocation rule is policy:
   a refusal before reservation may leave no software marker. After
   exclusive directory creation the attempt is consumed even if
   persistence or device work fails. Preserve partial reservations.
   Same-account or privileged deletion/tampering is outside this local
   guarantee; evidence custody is part of the operator procedure.

## Clock, process and device limits

The parent checks provenance and validates initial wall/monotonic samples.
After repo/runtime checks and durable reservation, it rechecks chronology
and time divergence and calculates the stricter cutoff. Immediately before
its sole open call the worker checks device identity, then verifies
observed_at <= approved_at <= wall_now < expires_at <= observed_at + 120,
monotonic now strictly below cutoff, and at most one second divergence
between paired elapsed wall and monotonic samples from the parent's final
sample. This catches stale facts after pinning and clock discontinuity or
sleep before open. Scheduling and device changes at the kernel boundary
cannot be made atomic by this check. Recheck opened fd identity before
configuration. Verify loaded parent and child module paths against pinned
runtime files. The Python inventory alone does not attest native linked
libraries or changes after verification.

After open, observe 12 seconds of passive boot and require the final
one second quiet under the 4096 boot-byte cap. Make at most one 16-byte
literal None write, with a 0.5-second readiness bound and no suffix write
or retry, then capture at most two seconds/1024 response bytes. Use the
18-second worker and 20-second parent capture budgets and retain at most
32768 worker-output bytes. Keep accepted HUPCL behavior. No additional
command, Misty contact, gateway, listener, output or movement is in scope.

Use explicit SIGINT/SIGTERM handlers and single forwarding. A missing
worker report means close unknown even when watchdog kill is false. Parent
SIGKILL can orphan the worker up to its independent budget, and watchdog
kill or power loss can lose worker raw bytes. Any wheel movement or sound, or a visual change outside the narrowly allowed
startup sequence described below, means immediately turn off motor/battery and unplug USB,
then interrupt the process if still running. After any outcome remove both
sources and record power-off, time and anomalies separately. No process
record proves physical shutdown.

## Interpretation and static staging

A failed quiet/boot trigger means no write and a readiness refusal. One
strict JSON null, separate explicit Python None or strict error response
is evidence only for that exact response to the candidate expression.
Silence is inconclusive. Wrong modes/indexes, malformed or excessive bytes
remain raw rejection facts. Abort, partial write and close failure are
failed observations. No outcome proves action ACKs, completion, neutral or
physical safety. Evidence needs separate blind review and PI acceptance.

The synthetic controller preloads dependencies, installs audit denials
and uses only fake device, process, signature, reservation and clock seams
in its test child. It does not load the physical controller. No run or
test is authorized here. The reviewed coexistence and canonical commit
sequence requires final reviewed repins against actual post-amendment
records. This final draft pins the complete proposed canonical record bytes.
Coexistence is reconciled without changing any Misty or operator-runtime file.


## Adopted startup baseline amendment (285/286)

The preflight replaces `no_motion_sound_animation` with
`no_wheel_motion_or_sound_observed: true` and requires
`battery_startup_visual_baseline` to equal exactly
`white_near_wheels_blue_eye_flashes_screen_flash_then_blank`.
The old schema refuses. This records Deb's USB-disconnected observation;
it is not a firmware-normality or safety assertion. G subsequently described
a blank screen as typical. Deb did not press Home. No Home-button result,
exact flash count or measured duration is established by that earlier session.

`boot_baseline_record` remains a string, now containing a JSON object with
exactly `duration_seconds`, `screen`, and `lights`. The duration must be a
finite number equal to the actually measured `standalone_observed_seconds`
(15 through 300 seconds). Both narratives must be strings of 12 through
400 stripped characters. Empty, enum-only and recognized placeholder text
refuse; duplicate or extra keys refuse. These structural checks cannot prove
truth or detect every possible placeholder. Deb must supply the actual
observation, not copy a sample or infer unmeasured facts.

For a later separately approved attempt, continuously watch the robot and
use a visible gateway timer. At most one matching visual startup sequence
is allowed within the existing 12-second passive window after serial open,
and only if it settles to the confirmed stable display/light baseline before
the window ends. If it is not clearly settled in time, remove power before
the window ends. Repeated, differing, uncertain or ongoing flashing refuses.
Any visual change before serial open, including USB cable connection, still
refuses. Any new or continuing visual change during write, response, close
or afterward requires immediate removal of both power sources. Wheel motion
or sound always requires immediate power removal. A refusal is terminal for
that preflight/attempt; do not reclassify it or retry while continuing.

Serial quiet does not detect visual stability. There is no automatic visual
gate, and the write can race with a human noticing a change. If Deb cannot
recognize the sequence and act within this window, refuse the attempt.
Independent motor isolation and confirmed USB logic power remain required.

G's November 3 handoff contains a driver that opens serial once, passively
drains for 10.5 seconds, probes brightness, then sends an online frame.
That historical report supplies context; this package does not import or
execute that driver, probe brightness, enter online mode, or write a label.
The literal None frame, parser, capture algorithm and limits are unchanged.

This six-file draft contains 32 statically counted test methods, not test
results. Historical accepted evidence stays at its original hashes. The
manifest records the inspected pre-change HEAD as repository basis and pins
the complete proposed canonical records. All other protected pins are unchanged.
The exact final eight-file reconciliation still needs blind review and separate
commit approval; the future execution request must bind the actual new HEAD.
A new exact offline request and separate execution approval are required;
275/276 cannot authorize changed bytes. Accepted revised offline evidence
must precede a new reviewed physical request and separate physical approval.

Use concise ASCII screen/light narratives in the live procedure to avoid JSON
escaping expansion beyond the overall 1024-character boot-record limit. Write
them from that live run; do not copy the synthetic fixture narratives.
