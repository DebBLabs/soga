# IIW Flow A Single-Path Beryl Laptop Preview Execution Request

Date: 2026-10-30
Status: DRAFT CREATE-ONLY REQUEST — NOT EXECUTABLE
Authority to create: D-177
Review class: mandatory blind dual review

## Purpose

Define the future one-attempt laptop-only preview of the accepted D-177
single-path Permission to Speak table. This document creates no execution
authority.

## Required exact inputs

- Presentation commit:
  `5de1c70c258733d73117101aa556a9baabf4c2a8`.
- SOGA commit at request creation:
  `af387b39823231d2d441b40dadfea9337405ea12`.
- Accepted proposal:
  `knowledge/proposals/IIW_FLOW_A_SINGLE_PATH_BERYL_PREVIEW_PROPOSAL_2026-10-30.md`
  at the exact hash returned by blind dual review.
- Corrected `run_beryl_visual_preview.py`: not yet created or hash-pinned.

This request is deliberately non-executable until the corrected launcher is
created under separate PI authority. The completed request must replace the
last item with the launcher's exact SHA-256, updated bases and allow-lists, then
receive blind dual static review together with the complete launcher.

## Static review requirements

Before a later PI may authorize one execution, reviewers must verify:

1. the exact launcher hash and committed presentation repository;
2. the exact SOGA basis and complete permitted diff;
3. all D-177 presentation hashes and accepted evidence hashes;
4. a new absent durable evidence directory
   `iiw-beryl-single-path-preview-v1`;
5. the exact interface and literal Beryl IPv4 established by an authorized
   read-only pre-creation preflight and pinned into both launcher and request;
6. the exact minimal SOGA and presentation allow-lists;
7. the launcher's own SHA-256 is recorded in the future evidence payload; and
8. the launcher and completed request have blind dual PASS.

## Mandatory operator pre-invocation holdpoint

The completed request must replace this section with the exact reviewed
literal values and expected outputs. Before invoking the launcher, the operator
performs these read-only checks. Any mismatch stops before invocation, does not
consume an attempt, and requires correction and review rather than retry:

1. recompute the committed launcher SHA-256 and match its reviewed value;
2. verify `.claude` is a real directory and `.claude/settings.local.json` is a
   regular non-symlink file at its newly pinned SHA-256;
3. run `git status --porcelain --untracked-files=all` in both repositories with
   exactly `PATH=/usr/bin:/bin`, `LANG=C`, `LC_ALL=C`,
   `GIT_OPTIONAL_LOCKS=0`, and no `HOME`; match the exact reviewed output;
4. perform both reviewed repository basis/allow-list checks;
5. recompute every accepted-evidence hash pinned by the launcher;
6. require the new durable evidence directory to be absent;
7. run `/usr/sbin/ipconfig getifaddr <reviewed-interface>` and
   `/sbin/ifconfig <reviewed-interface> inet`; require the exact pinned literal
   private IPv4 and exactly one IPv4 on that interface;
8. verify ports 4317 and 4318 are unused with the reviewed `lsof` inventory;
9. verify the reviewed process inventory contains no old bridge or candidate
   process; and
10. verify every other launcher pre-mkdir source/settings/firewall holdpoint.

## Launcher-enforced run conditions

During the future run the launcher must enforce:

- exactly the laptop on Beryl before and after;
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
