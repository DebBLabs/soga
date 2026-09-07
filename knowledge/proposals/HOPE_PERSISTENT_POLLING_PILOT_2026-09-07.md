# HOPE Persistent Polling Pilot — 2026-09-07

## Authorized pilot

The PI authorized a temporary, read-only polling pilot for Claude Gate 1 and
AGy Gate 2, coordinated by Codex, using only
`/private/tmp/hope-m02-sync-20260907`. The authorization allowed synthetic
readiness, dispatch, duplicate, malformed or missing-request, HEAD-mismatch,
response, and shutdown tests. It prohibited repository modification, session
initialization, external services, Misty access, real stage gates, and any grant
of implementation authority.

## Evidence

The exercised pilot used
`/private/tmp/hope-m02-sync-20260907/pilot-001`.

- Both role pollers wrote readiness records and remained alive across two
  sequential requests without restart.
- Matching request and signal transport worked.
- Duplicate-signal handling worked without reprocessing.
- Missing-request handling produced an error record.
- Both pollers observed `STOP`, wrote stopped records, and exited without an
  orphan process.
- The repository remained clean and unchanged.
- AGy returned the exact requested synthetic tokens.
- Claude returned identifiable PONG responses but did not preserve the exact
  requested response-token strings.
- Out-of-order identifier and expected-HEAD-mismatch cases were not exercised.

## Disposition: not adopted

The pilot proves persistent file transport and orderly lifecycle handling. It
does not prove that a queued substantive request invokes fresh model reasoning:
the pilot responders were scripted. It also failed the PI's visibility need;
the terminals did not show review reasoning as it happened, only readiness and
eventual results. Claude's response-fidelity difference is an additional open
defect.

Persistent background review polling is therefore not adopted. Current real
gates remain visible one-shot Claude and AGy reviews. When Codex coordinates a
gate, Codex must create each request and matching signal together, actively
monitor both response files through completion, read both responses in full,
and report the evidence visibly. A foreground, model-invoking, streaming bridge
requires a separately authorized and validated design.

## Foreground AGy repair test

A later synthetic repair test replaced AGy's scripted responder with a
foreground queue runner that launches a fresh AGy reasoning process for each
queued request and streams its tool activity and answer. The first trial exposed
an unnecessary attempted search outside the repository. The existing allowlist
denied that action; the runner was then corrected so any denied action or empty
answer is recorded as an error rather than accepted as a successful review.

The corrected runner processed two sequential requests without restarting the
queue runner, returned `VISIBLE_ONE ac5cea8` after an actual
`git rev-parse --short HEAD` check, returned `VISIBLE_TWO` without invoking a
tool, returned to waiting after each request, and stopped cleanly on `STOP`.
The repair used only `/private/tmp/hope-m02-sync-20260907`; it did not modify the
repository or enable unrestricted approval.

AGy's stream interface cannot present interactive permission prompts. Commands
outside the narrow pre-existing read-only allowlist are denied. A denied action
must be reported for PI or coordinator disposition and may not be converted into
a PASS. The repair validates synthetic foreground dispatch and visibility, not
unattended approval, a substantive stage gate, or adoption of persistent review.
