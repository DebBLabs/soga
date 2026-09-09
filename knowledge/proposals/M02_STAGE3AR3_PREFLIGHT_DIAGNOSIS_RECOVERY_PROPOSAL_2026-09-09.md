# M02 Stage 3A-R3 Synthetic Preflight Diagnosis and Recovery Proposal

Date: 2026-09-09

Status: **PROPOSED — NOT AUTHORIZED FOR IMPLEMENTATION OR EXECUTION**

Governing checkpoint: `b141edf922e7f819339a3762ac7faf23df042881`

Governing decision: D-048

## Purpose

Determine why the exact D-047 synthetic Docker containment preflight did not
make its nonce endpoint observable through `127.0.0.1:46321`, without mounting,
starting, importing, serving, or contacting either candidate.

This proposal does not reopen or reinterpret the accepted D-048 negative
result. That run failed closed and cleaned up successfully. It did not establish
the cause of the readiness failure.

## Evidence basis

The accepted evidence localizes the failure to `wait_for_nonce()` after Docker
accepted the synthetic container start and before any later containment probe.
The run did not preserve container state, exit code, logs, elapsed readiness
time, per-attempt socket outcome, live port-binding state, or in-container
readiness. Those missing observations prevent a causal conclusion.

Read-only inspection also found one definite defect: when `fetch_nonce()`
connects but returns a response without the nonce, the loop retries without
sleeping. The effective readiness interval is therefore path-dependent and can
be much shorter than the nominal 30-by-0.1-second budget. The D-048 evidence
remains accurate as a failure record, but its phrase “finite readiness window”
must not be interpreted as proof that a fixed three-second interval elapsed.

The embedded egress probe's top-level `await` under `node -e` is a separate
execution-compatibility risk. It was never reached in the accepted run and is
not established as its cause. A recovery script should remove the ambiguity by
wrapping the probe in an explicit async entry function rather than relying on
evaluation-mode inference.

No conclusion is adopted that Docker `--internal` necessarily blocks published
host-loopback ingress, that the container process crashed, that tmpfs
permissions caused the failure, or that the gateway argument index is wrong.
Each remains unproved or unsupported by the recorded run.

## Proposed work

### Phase 1 — Create a corrected diagnostic preflight; do not execute it

Phase 1 may begin only after this complete proposal receives PASS from Claude
Gate 1 and Gemini/AGy Gate 2 and the PI records prospective authorization to
create—but not execute—the corrected script. The proposal itself creates no
implementation authority.

Modify only `tools/m02_stage3ar3/preflight.py`:

1. Preserve the exact full-digest Node image, fixed names, internal network,
   literal-loopback publication, non-root user, read-only filesystem, finite
   CPU/memory/PID limits, dropped capabilities, and no-new-privileges control.
2. Remove automatic `--rm` from the synthetic container so bounded diagnostics
   can be captured before the existing unconditional cleanup removes it. This
   deliberately replaces a daemon-level automatic-removal guarantee with a
   script-level cleanup guarantee. A terminal loss, process kill, or host crash
   could therefore leave the fixed-name container or port behind. Compensating
   controls are mandatory: the existing start-of-run absence check must refuse
   a pre-existing R3 container, network, or occupied fixed port; after every run
   the operator must independently verify that no R3 container or network and
   no listener on ports 46321 or 46322 remains. A cleanup-verification failure
   is a PI holdpoint and cannot be reported as success.
3. Replace the iteration-dependent readiness loop with a monotonic wall-clock
   deadline no longer than 10 seconds. Sleep after every unsuccessful attempt,
   whether the attempt raises an `OSError` or returns a non-matching response.
4. Record only bounded per-attempt categories and elapsed time: connection
   refused, timeout, reset/other named socket error, or response-without-nonce.
   Do not record response bodies.
5. Add a bounded synthetic-server listening marker and error handler. Capture
   no more than the last 20 container log lines and 2,000 characters.
6. Before cleanup on success or failure, capture bounded container state,
   exit code, OOM flag, and actual Docker port-binding metadata.
7. If the container remains running, perform one bounded self-readiness probe
   with Node inside that same synthetic container. Record only nonce match or
   failure category; do not record bodies.
8. Replace the egress probe's top-level `await` with an explicit async entry
   function whose rejected promise produces a nonzero exit.
9. Give every Docker and host-inspection subprocess an explicit finite timeout.
   Timeout must produce failure, never success.
10. Preserve cleanup as unconditional and fail closed if the synthetic
    container, internal network, or fixed-port availability is not restored.

The complete corrected file—not only its diff—must receive PASS from Claude
Gate 1 and Gemini/AGy Gate 2 before execution.

### Phase 2 — One diagnostic preflight execution, only after PI authorization

Run the exact committed and independently reviewed corrected preflight once.
The run must use only the existing cached digest-pinned Node image and synthetic
resources. No candidate checkout may be mounted or referenced.

The diagnostic interpretation is limited to:

- container not running or nonzero exit plus bounded state/log evidence:
  synthetic-server startup failure;
- self-readiness succeeds but host-loopback readiness fails: host-publication
  path failure under the tested topology;
- container remains running with no recorded error while both self-readiness
  and host readiness fail within the deadline: consistent with initialization
  exceeding the tested budget; this establishes neither startup failure nor
  publication failure, and any longer deadline requires a separately reviewed
  and authorized decision;
- both become ready: prior failure consistent with the corrected timing path or
  a transient condition, without claiming which;
- any containment negative control fails: containment preflight remains
  negative and candidates remain prohibited.

No result may be generalized beyond this exact host, Docker configuration,
image digest, script commit, and run.

## Explicitly excluded

- execution before both full-script reviews return PASS and the PI records a
  new authorization decision;
- Phase 1 script modification before both proposal reviews return PASS and the
  PI prospectively authorizes creation of the corrected, unexecuted script;
- `candidate_startup.py` execution or modification;
- Freewallet or WAS mounting, import, serving, startup, or contact;
- non-internal-network comparison;
- image pull, build, load, import, tag, push, registry access, dependency
  operation, or upstream-source modification;
- Stage 3B code, tests, wallet interaction, or Person Server integration;
- external exposure, personal data, production credentials, or payment;
- Misty power, discovery, connection, query, configuration, or actuation;
- R3 protocol work, G28, or G29.

Every privilege, license, update, network-access, subscription, or security
prompt remains a PI holdpoint.

## Required evidence and exit

Execution, if later authorized, must produce a standalone report containing the
exact commit, command, complete bounded output, exit status, interpretation,
and independent cleanup checks. Both gates must review that report. Candidate
startup remains prohibited unless the corrected preflight passes every control
and the PI subsequently authorizes it separately.
