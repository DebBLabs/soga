# IIW Path-Specific Completion Pages Proposal

Date: 2026-10-29
Status: PROPOSED — NOT AUTHORIZED
Presentation basis: `b7772026f54196c0b370fd70012ca0f30b0c4ef3`
SOGA basis: D-167
Review class: mandatory blind dual review under D-064

## Purpose

Correct the accepted IIW iPad-first table experience so each path has its own
completion material. The current single `/table-questions` screen combines
Permission to Speak and Project Agent questions. That does not match the PI's
intended visitor experience.

The correction must preserve the common standards and next-step framing on
both endings while keeping each path's outcome, lessons and questions specific
to that path.

## Exact seven-file boundary

Create-only implementation may later change only these presentation files:

1. `index.html`
2. `bridge.py`
3. `test_fictional_parent_presentation.py`
4. `run_fictional_parent_presentation_tests.py`
5. `table-runtime-manifest.json`
6. `README.md`
7. `CHECKLIST.md`

No SOGA production source, accepted AAuth/SOGA behavior, dependency, image,
launcher, distribution bundle or evidence may change.

## Required visitor experience

### Permission to Speak ending

The active Permission to Speak card and its terminal result must lead only to
`/table-questions/permission`. Its page must:

- identify **Permission to Speak** as the path just explored;
- show the three bounded outcomes—permitted, declined and expired—and, when a
  completed encounter exists, identify its sanitized retained outcome as
  `ALLOW`, `DECLINE` or `EXPIRED`; when no encounter has completed, state
  **No completed Permission to Speak encounter is retained** and make no result
  claim;
- retain the persistent statement that the nearby-adult input is unverified
  fictional-parent role-play and does not establish identity, parenthood,
  legal authority or legal consent;
- ask only Permission-to-Speak questions, including the boundary between
  ambient and directed interaction, respecting a nearby adult's choice without
  forced identity proof, changed conditions after Allow, and permission across
  devices; and
- offer **Back to start**.

It must contain no Project-Agent-specific questions about disclosure, model
provenance, tool escalation or responsibility across agent/service hops.

Both completion pages render on the laptop. The controlled iPad flow remains
unchanged and ends on the accepted choice page. During the five-second terminal
dwell the laptop terminal view links to the Permission ending; the active
Permission card may also open it before an encounter, in which case it shows
the no-completed-encounter state.

### Project Agent ending preview

The inactive **Talk with Deb's Project Agent — NEXT INCREMENT** card may link
only to `/table-questions/agent`. Because no Project Agent service or QR exists,
this page must be labeled **NEXT INCREMENT — PREVIEW, NOT EXECUTED** and must not
claim that a Project Agent path completed. It must:

- explain that the future path asks how a visitor may talk with Deb's agent
  without receiving Deb's authority;
- ask only Project-Agent questions about permitted disclosure, separation of
  accepted records from model-generated explanation, prevention of visitor
  input escalating into tools or commitments, and hop-by-hop responsibility;
  and
- offer **Back to start**.

It must contain no fictional-parent outcome or parent/child authorization
questions.

This informational link is an explicit amendment to D-158's non-interactive
Project Agent roadmap tile. The tile remains operationally inactive: it has no
QR, free-text input, conversation service, model, tool or authority. Its only
action opens the fixed local preview page.

### Common content on both pages

Both pages must contain the same shared section:

- the question of how authority, governance, provenance and responsibility
  remain connected from intent to action;
- AAuth as authorization and SOGA as runtime governance;
- GNAP as negotiated delegation, AuthZEN as policy decisions, Transaction
  Tokens as internal call-chain context and wallets as evidence; and
- the exact caveat that these are open research questions, not a claim that
  one protocol should solve every layer.

## Route and state requirements

- Replace the shared `/table-questions` served route with
  `/table-questions/permission` and `/table-questions/agent`.
- The retired `/table-questions` route must return controlled `404`; it must not
  silently select a path or display the old shared page.
- The Permission to Speak page may read only the existing laptop-only bounded
  state plus one new display-only `last_terminal_outcome` enum needed to label
  the latest accepted terminal result. The enum is initialized to `NONE`, set
  only to `ALLOW`, `DECLINE` or `EXPIRED` by the existing terminal transition,
  retained across the automatic five-second dwell reset, and cleared when a
  fresh lease is successfully claimed. It contains no lease, capability,
  token, receipt, reason, policy, identity or free text. Reading either ending
  must not mutate the enum or create or mutate any lease, request, choice,
  token or policy.
- The Project Agent preview is informational only. It must not call a model,
  service, tool or AAuth/SOGA seam.
- Existing `Cache-Control: no-store`, `Referrer-Policy: no-referrer`, Host,
  laptop-client, lease, QR, listener and secret-confinement controls remain
  unchanged.
- The active Permission to Speak flow, terminal dwell/reset behavior and all
  D-167 accepted production behavior remain unchanged except for the expressly
  reviewed display-only enum, which does not extend a lease, preserve a
  capability or alter an authorization decision.
- The accepted D-158 six-line persistent boundary remains on both pages,
  including the unverified fictional-parent and recreated-child statements.
  Project-Agent exclusion tests must be scoped only to that page's outcome and
  question sections; they must not reject the required shared boundary.

## Static tests

The presentation test module must expand from 31 to exactly 35 tests. The four
new focused tests must establish:

1. the Permission to Speak ending contains its required path-specific content
   and excludes every Project-Agent-specific question;
2. the Project Agent preview contains its required path-specific content,
   states that it is not executed and excludes fictional-parent outcome and
   authorization questions from its path-specific outcome/question sections;
3. both endings contain byte-identical shared standards and research framing;
   and
4. the old `/table-questions` route is not served, both new routes are served,
   and behavioral GETs of both routes leave revision, stage, generation and
   `last_terminal_outcome` unchanged. Additional assertions must prove the enum
   accepts only its four fixed values, survives automatic dwell reset, clears
   on a fresh successful lease and never contains or exposes a secret.

The bounded controller must expect exactly 163 tests: the accepted 128-test
fictional-parent baseline plus 35 presentation tests. Within the reviewed
seven-file boundary it must update `EXPECTED_TEST_COUNT` to `163`, the second
child's expected count to `35`, the hashes of the reviewed presentation
sources, and these exact repository controls:

- `PRESENTATION_BASIS` becomes
  `b7772026f54196c0b370fd70012ca0f30b0c4ef3` and its allow-list is exactly the
  seven files in this proposal;
- `SOGA_COMMIT` becomes the accepted SOGA commit current when implementation is
  authorized; its allow-list is limited to this proposal plus the prospective
  decision-log and canonical-state records. The Beryl rehearsal proposal must
  remain untracked until it is later re-pinned, unless a subsequent reviewed
  controller explicitly allow-lists its committed path; and
- `PRESENTATION_SOURCES`, the manifest mirror fields and every changed source
  hash are updated consistently. `warmup.sh` remains pinned and unchanged.

The controller must use a new absent durable evidence directory
`/Users/debb/dev/research-evidence/soga/evidence/iiw-table-path-endings-v1`,
preserve byte-identical both the accepted D-163 v1 evidence and D-167 v2
evidence—including their recorded payload, stdout and stderr hashes—and retain
all existing finite, confinement, immutability and cleanup controls. The
runtime manifest must pin the corrected files, controller, bases, allow-lists
and evidence path.

## Visual verification holdpoint

Static review and synthetic tests do not substitute for the PI's visual
verification. After both gates pass the exact seven files and a separately
authorized bounded synthetic execution passes, a later controlled Beryl
laptop-only preview must show the PI both endings before the Beryl/iPad
rehearsal is accepted or executed. That preview uses the rehearsal's reviewed
network and cleanup controls but performs no QR scan or iPad contact. Because
the Permission page always shows all three bounded outcome labels, its layout
can be verified when no encounter has completed; no simulated result is
needed. No rehearsal request may continue to pin presentation
commit `b7772026`; it must re-pin the accepted corrected presentation commit and
all affected source, controller and manifest hashes.

## Claim boundary and exclusions

This is a presentation routing and copy correction. It does not activate or
implement Project Agent and does not change AAuth, SOGA, the fictional-parent
role-play, QR semantics, identity, authority, consent or physical action.

This proposal authorizes no source change, import, compilation, lint, test,
execution, listener, Beryl access, QR generation, device contact, Project Agent
service, model call, tool use, wallet/WAS work, mBot2, Misty, G28 or G29. The
unrelated PI routine-tool proposal remains excluded and untouched.

## Holdpoints

1. Both blind gates review this exact proposal.
2. The PI may authorize create-only implementation of the exact seven files.
3. Both blind gates review every complete changed file.
4. The PI may authorize commit and one bounded synthetic execution.
5. Both gates review the evidence; the PI may accept it.
6. The PI visually verifies both endings in a separately authorized preview.
7. Only then may the Beryl/iPad rehearsal proposal and execution request be
   re-pinned and advanced.
