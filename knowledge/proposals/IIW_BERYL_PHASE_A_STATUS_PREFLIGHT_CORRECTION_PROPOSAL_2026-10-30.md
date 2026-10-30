# IIW Beryl Phase A Status-Preflight Correction Proposal

Date: 2026-10-30

Status: proposed; not adopted; no implementation or execution authority

## Purpose

Correct the deterministic status-preflight defect documented in
`IIW_BERYL_PHASE_A_STATUS_PREFLIGHT_DIAGNOSIS_2026-10-30.md` without weakening
the reviewed source boundary or changing the presentation, network or evidence
controls.

## Exact create-only correction

Modify only
`/Users/debb/dev/permission-to-speak-work/permission-to-speak/run_beryl_visual_preview.py`.

1. Change only the SOGA status call to
   `status --porcelain --untracked-files=all`. Set `EXCLUDED_SOGA_STATUS` to
   exactly these two full paths:
   - `?? .claude/settings.local.json`
   - `?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md`
   The presentation-repository status call remains unchanged.
2. Add an explicit directory, path and hash holdpoint requiring:
   - `/Users/debb/dev/soga-clean/.claude` is a real directory and not a
     symlink;
   - `/Users/debb/dev/soga-clean/.claude/settings.local.json` is a regular
     file, is not a symlink, and has SHA-256
     `656b43836a10814c94e1533c036e7149f9f9c88c7d1e3c157b37896cd551cb87`.
3. Set `SOGA_BASIS` to the currently accepted commit
   `63353fdfb45912f74b314943002002401c385ac8` and set
   `SOGA_ALLOWED_SINCE_BASIS` to exactly:
   - `knowledge/research/IIW_BERYL_PHASE_A_STATUS_PREFLIGHT_DIAGNOSIS_2026-10-30.md`
   - `knowledge/proposals/IIW_BERYL_PHASE_A_STATUS_PREFLIGHT_CORRECTION_PROPOSAL_2026-10-30.md`
   - `knowledge/proposals/IIW_BERYL_PHASE_A_VISUAL_PREVIEW_R2_EXECUTION_REQUEST_2026-10-30.md`
   - `knowledge/strategy/DECISION_LOG.md`
   - `knowledge/working/CURRENT_STATE.md`
4. Preserve `PRESENTATION_BASIS` at
   `fa6ccaa2f2fe65c043219380e127cb14f454eae9` and
   `PRESENTATION_ALLOWED_SINCE_BASIS` as only
   `run_beryl_visual_preview.py`; this continues to admit only the reviewed
   launcher lineage from presentation commit `7d857f5` and its exact
   correction.
5. Verify that the existing PI proposal exclusion remains exact and unchanged.
6. Preserve every other launcher byte and control unless a reviewer identifies
   a mechanically necessary adjacent edit.

The correction must not restore `HOME` to the Git child environment or rely on
the user's mutable global Git configuration. The minimal environment remains
the execution boundary.

## Review and execution sequence

1. Create the corrected launcher only; do not execute it.
2. Obtain blind dual static review of the complete corrected launcher and this
   proposal.
3. Commit the exact reviewed launcher only after PI acceptance.
4. Prepare
   `knowledge/proposals/IIW_BERYL_PHASE_A_VISUAL_PREVIEW_R2_EXECUTION_REQUEST_2026-10-30.md`
   with a new prospective decision, the corrected launcher hash, the exact
   SOGA and presentation basis/allow-list values above, and a pre-invocation
   read-only check of the pinned local-settings hash plus minimal-environment
   `git status --porcelain --untracked-files=all`. Do not launch on any
   difference.
5. A later authorization may permit one bounded execution using the still-
   absent `iiw-beryl-phase-a-visual-preview-v1` directory. No automatic retry.

## Preserved controls

All D-171 and D-172 controls remain unchanged: literal `en0`, literal Beryl
IPv4 `192.168.8.247`, only the laptop associated with Beryl, no iPad or other
device, no QR scan, no encounter, no AAuth/SOGA decision, no Project Agent,
no mBot2, no Misty, no G28 and no G29. The unrelated PI routine-tool proposal
remains excluded and untouched.

## Stop rules

Stop without execution if either exact local excluded path or hash differs,
the presentation or SOGA basis differs, the evidence directory exists, or a
reviewer does not return PASS.
