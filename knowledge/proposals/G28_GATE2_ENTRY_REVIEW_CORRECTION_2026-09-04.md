# G28 Entry Reconciliation — Gate 2 Corrected Review

Date: 2026-09-04  
Reviewer: Gemini/AGy, constitutional Gate 2  
Reviewed checkpoint: `a70432e497579cbdc047644d8ea2389b33e07035`  
Transport request: `G28-ENTRY-GATE2-CORRECTION-001`  
Ruling: PASS WITH CONDITIONS — advisory only, unchanged  
Status: CORRECTED RESPONSE RECEIVED AND PROVENANCE CHECKED

## Correction

Gemini clarified that the prior response combined current-repository evidence,
historical operational evidence, and a candidate identifier without labeling
those classes precisely enough.

### Evidence classification

- `verify/verify_server.py`: Verified in `soga-clean`; already identified by G27
  evidence as a direct-dispatch/silent-fallback anti-pattern that must not become
  an authorized physical path.
- Misty serial `20221304273` and configuration `060-000006`: reported by Gemini
  as Observed from PI hardware-inventory communications. These values are not
  established by the current repository and must be reverified against the
  physical label or other admissible evidence before use.
- `misty-a-060-000006`: Hypothesis/candidate platform identifier constructed
  from the observed configuration value. It is not canonical unless explicitly
  adopted by Deb in a reviewed artifact.
- `misty_ip.py`, `test_misty_camera.py`, and `test_misty_demo.py`: Gemini
  attributed these to the separate historical `/Users/debb/dev/a2a-gateway`
  checkout, not `soga-clean`.
- `/api/tts/speak`, `/api/led`, `/api/blink`, and `/api/head`: code/operational
  command shapes, not proof that the current Misty A endpoint is reachable or
  physically executes them today.

## CG provenance verification

CG inspected the cited historical checkout read-only and verified:

- checkout HEAD `126c5319677557d99366c880528aa9160edccbd7` on branch
  `soga-runtime-cleanup`;
- `adapters/misty/test_misty_camera.py` and
  `adapters/misty/test_misty_demo.py` exist there;
- `test_misty_demo.py` contains `tts/speak`, `blink`, `led`, and `head` command
  shapes and an RGB-camera path;
- the historical checkout currently has unrelated untracked files and is not a
  clean source for direct reuse; and
- `misty_ip.py` was not present in the inspected checkout, so that filename
  remains unverified unless separately sourced.

The historical files demonstrate prior code and operational context. They are
not authorized implementation inputs and do not prove present network,
endpoint, target, safety, or physical-execution readiness.

## Reconfirmed Gate 2 findings

Gemini reconfirmed concurrence with Claude/Gate 1 that today's bounded Misty A
work should be a formally named precursor mission rather than an in-session
rewrite of the standing G28 Misty B roadmap entry.

Gemini reconfirmed that:

- the native immutable AAuth Mission and mission log remain authoritative;
- G27 target binding, independent local safety, fail-safe containment, and
  truthful unknown-outcome rules remain binding; and
- the temporary HOPE file exchange creates no G28 or physical authority.

## Conditions before PI activation decision

1. Define and name the bounded Misty A precursor mission without modifying the
   G28 Misty B roadmap entry.
2. Before physical authorization, establish the canonical Misty A identifier
   from verified local evidence and complete a network/hardware/safety checklist.
3. Enforce the adopted per-action/session cardinality before physical dispatch.
4. Implement a new target-bound adapter only after Mission Authorization; do
   not copy historical direct-dispatch, fallback, camera, or microphone paths.
5. Select only verified, bounded C1 primitives in the mission specification and
   reverify their present behavior locally before physical execution.

## Nonclaims

This corrected PASS WITH CONDITIONS is advisory evidence. It does not activate
G28 or the proposed precursor, authorize implementation, establish a canonical
Misty A identity, permit network connection or discovery, or authorize physical
execution.
