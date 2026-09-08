# M02 Stage 3A-R3 Synthetic Containment Preflight Evidence

Date: 2026-09-08

Repository commit executed: `8f6ec01b395e8229b7fa64d00759810a56882c42`

Decision boundary: D-047

Result: **NEGATIVE — SYNTHETIC PREFLIGHT DID NOT PASS**

## Scope

D-047 authorized execution of only the independently reviewed synthetic Docker
containment preflight in `tools/m02_stage3ar3/preflight.py`. Candidate startup
remained prohibited unless the preflight passed and the PI separately
authorized proceeding.

The script executed was committed before execution. Claude Gate 1 and
Gemini/AGy Gate 2 had independently returned PASS on the complete script after
its fail-closed corrections.

## Command

```text
python3 tools/m02_stage3ar3/preflight.py
```

## Complete preflight output

```json
{"control": "internal_network", "gateway": "172.19.0.1", "result": "PASS"}
{"control": "containment_preflight", "error": "loopback nonce endpoint did not become ready", "result": "FAIL"}
{"control": "cleanup", "result": "PASS"}
```

Process exit status: `1`.

## Interpretation

The synthetic internal Docker network was created successfully. The synthetic
nonce endpoint published to the authorized literal-loopback port did not become
ready within the script's finite readiness window. The preflight therefore
failed closed before its later containment probes could establish the required
controls.

This result does not establish why the nonce endpoint failed to become ready.
It does not establish that Docker containment is unsuitable, and it does not
support candidate execution. It establishes only that this exact reviewed
preflight did not satisfy its required controls in this run.

No Freewallet or WAS candidate was imported, served, started, or contacted.
`tools/m02_stage3ar3/candidate_startup.py` was not executed.

## Cleanup verification

After the script exited, independent read-only checks confirmed:

- no container whose name matched `soga-m02-r3` remained;
- no Docker network whose name matched `soga-m02-r3` remained;
- no TCP listener remained on host port `46321`;
- no TCP listener remained on host port `46322`.

The exact digest-pinned Node image remains cached as the previously accepted
D-046 research input. Docker Desktop remains running. The unrelated untracked
PI routine-tool-approval proposal was neither read nor modified as part of this
execution.

## Boundary after execution

Candidate startup remains prohibited. Stage 3B and every exclusion preserved
by D-047 remain in force. Any diagnosis, script modification, repeated
preflight, or alternative containment attempt requires a separately reviewed
and authorized next step.
