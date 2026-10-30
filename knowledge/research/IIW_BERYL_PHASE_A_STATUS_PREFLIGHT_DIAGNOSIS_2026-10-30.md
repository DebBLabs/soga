# IIW Beryl Phase A Status-Preflight Diagnosis

Date: 2026-10-30

Status: source-only diagnosis; no correction or rerun authorized by this record

## Observed stop

The exact D-172 launcher was invoked once and stopped before creating the
durable evidence directory, opening a listener, displaying the preview, or
contacting another device. It raised:

`RuntimeError: SOGA working-tree status differs from reviewed boundary`

The launcher remained at reviewed SHA-256
`82f701c0ad1d1825eeb98b988796d0161223616a2e2e2863da99bb746cfcacbe`.
The durable `iiw-beryl-phase-a-visual-preview-v1` evidence path remained
absent.

## Root cause

`run_beryl_visual_preview.py` intentionally replaces the child Git process
environment with only `PATH`, locale variables and `GIT_OPTIONAL_LOCKS`. It
therefore omits `HOME`.

With Deb's ordinary environment, Git loads
`/Users/debb/.config/git/ignore`, whose first rule ignores
`.claude/settings.local.json`. Ordinary `git status --porcelain` therefore
reports only the separately excluded untracked PI routine-tool proposal.

With the launcher's exact minimal environment, Git cannot locate that global
ignore file and reports two untracked paths:

- `?? .claude/`
- `?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md`

The reviewed `EXCLUDED_SOGA_STATUS` set contains only the PI proposal, so the
equality check fails closed. The local settings file predates this sprint:
filesystem birth and modification time are both 2026-08-16 06:45:31 EDT. Its
observed SHA-256 is
`656b43836a10814c94e1533c036e7149f9f9c88c7d1e3c157b37896cd551cb87`.
Its contents were not needed for this diagnosis.

## Classification

This is a deterministic launcher preflight defect, not a presentation-source,
Beryl, listener or device failure. The stop was fail-closed at the first source
identity holdpoint.

Because D-172 authorized exactly one execution and prohibited automatic retry,
the invocation is treated as a consumed stopped attempt. Any correction and
later execution require prospective review and authorization.

## Boundary

This diagnosis authorizes no source modification, commit, listener, preview,
QR activity, device contact or rerun. The unrelated PI routine-tool proposal
remains excluded and untouched.
