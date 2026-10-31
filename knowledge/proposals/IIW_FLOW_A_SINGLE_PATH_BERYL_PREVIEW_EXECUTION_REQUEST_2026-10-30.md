# IIW Flow A Single-Path Beryl Laptop Preview Execution Request

Date: 2026-10-30
Status: COMPLETED CREATE-ONLY REQUEST — NOT AUTHORIZED FOR EXECUTION
Authority to create: D-178
Review class: mandatory blind dual review

## Purpose

Define the future one-attempt laptop-only preview of the accepted D-177
single-path Permission to Speak table. This document creates no execution
authority.

## Required exact inputs

- Presentation commit:
  `5de1c70c258733d73117101aa556a9baabf4c2a8`.
- SOGA basis commit:
  `0396fda8c43db0de8f7b72ddfc7f94fd73882921`.
- Accepted proposal:
  `knowledge/proposals/IIW_FLOW_A_SINGLE_PATH_BERYL_PREVIEW_PROPOSAL_2026-10-30.md`
  at SHA-256
  `0a1dcbee2669a1d4dc27b9caa89a5776f3a7f8ae59a059f135b1b1ff3cfb2a03`.
- Corrected `run_beryl_visual_preview.py` SHA-256:
  `c6f8a408f864e1e7eedd4220989e8a506ff8a1eac46615e0c97ec89519ff5f09`.
- Reviewed interface: `en0`.
- Reviewed literal Beryl IPv4: `192.168.8.247`.
- Reviewed local settings SHA-256:
  `656b43836a10814c94e1533c036e7149f9f9c88c7d1e3c157b37896cd551cb87`.

The corrected launcher and this completed request must receive blind dual
static review together. This request creates no execution authority.

## Static review requirements

Before a later PI may authorize one execution, reviewers must verify:

1. the exact launcher hash and committed presentation repository;
2. presentation basis `5de1c70c258733d73117101aa556a9baabf4c2a8`
   with only `run_beryl_visual_preview.py` permitted to differ, and SOGA basis
   `0396fda8c43db0de8f7b72ddfc7f94fd73882921` with only this request,
   `knowledge/strategy/DECISION_LOG.md` and
   `knowledge/working/CURRENT_STATE.md` permitted to differ;
3. all D-177 presentation hashes and accepted evidence hashes;
4. a new absent durable evidence directory
   `iiw-beryl-single-path-preview-v1`;
5. interface `en0` and literal Beryl IPv4 `192.168.8.247`, established by the
   D-178 read-only pre-creation preflight and pinned into launcher and request;
6. the exact minimal SOGA and presentation allow-lists;
7. the launcher's own SHA-256 is recorded in the future evidence payload; and
8. the launcher and completed request have blind dual PASS.

## Mandatory operator pre-invocation holdpoint

Before invoking the launcher, the operator performs these read-only checks.
Any mismatch stops before invocation, does not
consume an attempt, and requires correction and review rather than retry:

1. recompute the committed launcher SHA-256 and require
   `c6f8a408f864e1e7eedd4220989e8a506ff8a1eac46615e0c97ec89519ff5f09`;
2. verify `.claude` is a real directory and `.claude/settings.local.json` is a
   regular non-symlink file at SHA-256
   `656b43836a10814c94e1533c036e7149f9f9c88c7d1e3c157b37896cd551cb87`;
3. run `git status --porcelain --untracked-files=all` in both repositories with
   exactly `PATH=/usr/bin:/bin`, `LANG=C`, `LC_ALL=C`,
   `GIT_OPTIONAL_LOCKS=0`, and no `HOME`; require an empty presentation status
   and exactly these two SOGA lines:
   - `?? .claude/settings.local.json`
   - `?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md`
4. perform the presentation and SOGA basis/allow-list checks exactly as stated
   in static review requirement 2;
5. recompute every accepted-evidence hash pinned by the launcher;
6. require the new durable evidence directory to be absent;
7. run `/usr/sbin/ipconfig getifaddr en0` and `/sbin/ifconfig en0 inet`;
   require literal `192.168.8.247` and exactly one IPv4 on `en0`;
8. verify ports 4317 and 4318 are unused with the reviewed `lsof` inventory;
9. verify the reviewed process inventory contains no old bridge or candidate
   process; and
10. verify every other launcher pre-mkdir source/settings/firewall holdpoint.

## Launcher-enforced run conditions

During the future run the launcher must enforce:

- require and record the PI's `ONLY_REVIEWED_CLIENT` attestation before and
  after the preview;
- full-screen operator review of only `/table` and
  `/table-questions/permission`;
- state remains `IDLE`, revision unchanged and terminal outcome `NONE`;
- cleanup removes every child process and listener;
- fixed-label/failure-type evidence only, no MAC, token, exception text or
  client IP other than the reviewed literal address; and
- no automatic retry.

## Operator attestations to encode

The corrected launcher must accept only fixed bounded responses equivalent to:

- `ONLY_REVIEWED_CLIENT` before and after;
- `PREVIEW_SINGLE_PATH_TABLE_OK` or `STOPPED`;
- `PREVIEW_PERMISSION_ENDING_OK` or `STOPPED`;
- `PI_VISUAL_ACCEPTED` or `PI_VISUAL_NOT_ACCEPTED`.

The PI enters an `*_OK` or `PI_VISUAL_ACCEPTED` response only after visually
checking the complete full-screen page. Any other condition stops fail-closed.

## Prohibited actions

No current execution, listener, Beryl access, QR generation or scan,
`/permission-entry`, encounter, choice, Finish/reset, AAuth/SOGA decision,
iPad/device contact, meeting-agent preparation or operation, Project Agent,
wallet/WAS, mBot2, CyberPi, Misty, sensor, speech, movement, G28 or G29 is
authorized.

The unrelated PI routine-tool proposal remains excluded, unread and untouched.
