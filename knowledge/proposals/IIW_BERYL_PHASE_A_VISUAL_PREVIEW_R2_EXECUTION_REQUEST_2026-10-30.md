# IIW Beryl Phase A laptop-only visual-preview R2 execution request

Date: 2026-10-30
Status: CREATE-ONLY — NOT AUTHORIZED FOR EXECUTION
Authority: D-173
Review class: mandatory blind dual review under D-064

## Purpose

Request prospective authority for one corrected bounded Phase A laptop-only
visual preview after the D-172 invocation stopped at its first source-identity
holdpoint. D-172 is consumed. This request creates no execution authority.

## Exact reviewed inputs

- Accepted Beryl/iPad proposal SHA-256:
  `d7a3fca4cd60a1967576ef6f8452a10ecfeee28fcf9c2a05f1374affd160523c`.
- Accepted diagnosis SHA-256:
  `694225bd6bc6989aff9604530d455168793f2907a25b9ba778a89fdade675827`.
- Accepted correction proposal SHA-256:
  `8f25ea14c72518fb3ab2c9d108807975b8a554f8a34c0645c61c1baf2f39bd45`.
- Corrected create-only launcher:
  `/Users/debb/dev/permission-to-speak-work/permission-to-speak/run_beryl_visual_preview.py`
  at SHA-256
  `39f7036135a9c9d2a41dd55383f675422a4670bb94f80f5b1554672dc30ae688`.
- Presentation basis:
  `fa6ccaa2f2fe65c043219380e127cb14f454eae9`, with only
  `run_beryl_visual_preview.py` permitted to differ.
- SOGA basis:
  `63353fdfb45912f74b314943002002401c385ac8`, with exactly these paths
  permitted to differ:
  - `knowledge/research/IIW_BERYL_PHASE_A_STATUS_PREFLIGHT_DIAGNOSIS_2026-10-30.md`
  - `knowledge/proposals/IIW_BERYL_PHASE_A_STATUS_PREFLIGHT_CORRECTION_PROPOSAL_2026-10-30.md`
  - `knowledge/proposals/IIW_BERYL_PHASE_A_VISUAL_PREVIEW_R2_EXECUTION_REQUEST_2026-10-30.md`
  - `knowledge/strategy/DECISION_LOG.md`
  - `knowledge/working/CURRENT_STATE.md`

The launcher continues to pin the eight accepted presentation files, the
D-170 report, all nine accepted durable evidence files, literal interface
`en0`, Beryl IPv4 `192.168.8.247`, TCP port `4317`, unused TCP port `4318`,
finite limits, state invariance and cleanup.

## Mandatory pre-invocation holdpoint

The operator must complete these read-only checks before invoking the
launcher. Any mismatch stops before invocation and does not consume a future
authorized attempt.

1. The corrected launcher is committed and hashes exactly to
   `39f7036135a9c9d2a41dd55383f675422a4670bb94f80f5b1554672dc30ae688`.
2. `/Users/debb/dev/soga-clean/.claude` is a real directory, not a symlink.
3. `.claude/settings.local.json` is a regular file, not a symlink, and hashes
   exactly to
   `656b43836a10814c94e1533c036e7149f9f9c88c7d1e3c157b37896cd551cb87`.
4. The launcher's exact minimal Git environment—`PATH=/usr/bin:/bin`,
   `LANG=C`, `LC_ALL=C`, `GIT_OPTIONAL_LOCKS=0`, with no `HOME`—and
   `git status --porcelain --untracked-files=all` reports exactly:
   - `?? .claude/settings.local.json`
   - `?? knowledge/proposals/PI_ROUTINE_TOOL_APPROVAL_DELEGATION_PROPOSAL_2026-09-08.md`
5. The presentation repository is clean and its basis/allow-list check passes.
6. The SOGA basis/allow-list check passes.
7. The durable evidence directory
   `/Users/debb/dev/research-evidence/soga/evidence/iiw-beryl-phase-a-visual-preview-v1`
   is absent.
8. Both blind reviewers have returned PASS on the exact corrected launcher and
   this request, and the PI has prospectively authorized one R2 execution.

The unrelated PI proposal is status-observed only and remains unread and
untouched.

## Exact bounded R2 execution

Only after every holdpoint passes, a later prospective authorization may run
exactly:

```text
/usr/bin/python3 -B /Users/debb/dev/permission-to-speak-work/permission-to-speak/run_beryl_visual_preview.py
```

The reviewed controls remain unchanged:

- exactly the laptop associated with Beryl, attested before and after;
- total runtime at most 480 seconds and readiness at most 15 seconds;
- at most 1,000,000 bytes per child output stream;
- one presentation listener at literal `192.168.8.247:4317` only;
- no listener on `4318`, no DNS, UDP, wildcard, IPv6, internet or other
  application connection;
- no old bridge or candidate process;
- fail-closed child-process-group cleanup and post-run absence of listeners;
- unchanged source identity, firewall, interface/address and accepted evidence;
- writes only beneath the initially absent v1 evidence directory; and
- no automatic retry.

## Operator path

The iPad, Misty, mBot2 and every other device remain disconnected. Deb closes
old demo tabs and opens only the three launcher-printed laptop URLs for
`/table`, `/table-questions/permission` and `/table-questions/agent`.

She records only the reviewed labels:

- `PREVIEW_TABLE_OK` or `STOPPED`;
- `PREVIEW_PERMISSION_OK` or `STOPPED`;
- `PREVIEW_AGENT_OK` or `STOPPED`;
- `PI_VISUAL_ACCEPTED` or `PI_VISUAL_NOT_ACCEPTED`; and
- `ONLY_REVIEWED_CLIENT` before and after.

She must not scan a QR, open `/permission-entry`, begin an encounter, submit a
choice or use Finish/reset. The pre/post `/api/state` snapshots must remain
`IDLE` with unchanged revision and terminal outcome `NONE`.

## Claim boundary

A positive result could establish only Deb's visual acceptance of the reviewed
laptop screens on the reviewed Beryl origin. It would not establish QR/iPad
interoperability, an AAuth decision, public-event readiness, Project Agent
execution, complete conformance, identity, parenthood, legal authority,
consent, wallet/WAS, mBot2, Misty, G28 or G29.

Phase B remains blocked pending blind dual evidence review and explicit PI
visual acceptance. This request authorizes no execution, listener, QR scan,
device contact, source change, dependency operation, physical action or retry.
All prior exclusions remain in force. The unrelated PI routine-tool proposal
remains excluded and untouched.
