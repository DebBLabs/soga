# IIW Flow A Beryl/iPad Live-Rehearsal Proposal

Date: 2026-10-31
Status: PROPOSED — CREATED ONLY; NOT REVIEWED OR AUTHORIZED FOR EXECUTION
Authority to create: D-183
Review class: mandatory blind dual review

## Purpose

Propose one operator-attended rehearsal of the accepted Permission to Speak
Flow A using Deb's laptop and one controlled iPad on Deb's private Beryl
network. The laptop uses two explicit tabs: `/table` displays the real QR and
control state, while `/flow-a` displays the PI-locked narrative and completion
screens. The rehearsal would run the accepted local AAuth/SOGA composition and
exercise the accepted adult role-play controls.

This is the first proposed live device-to-laptop rehearsal. It is not a public
table run and does not activate mBot2, CyberPi, Misty or physical action.

## Exact accepted basis

Presentation repository:
`/Users/debb/dev/permission-to-speak-work/permission-to-speak`

Accepted commit and `origin/main`:
`964f12626c9220e45a634d85fa407205aa9d9f3d`

Exact accepted controller package: the ten D-180 files and hashes recorded in
D-180 and the D-183 evidence report. The rehearsal launcher must pin all ten
files, `warmup.sh`, the durable provider manifest, the SOGA source files and
protected trees already pinned by `bridge.py`.

Accepted synthetic evidence:

- D-183 report SHA-256
  `c11615021ad5b7e0c796d9e5ee522752e230aaf5ccdcc8061dfa34b97d046a29`
- D-182 evidence payload SHA-256
  `99922ab2e0806ca39c4fd1048dfcdab3e512947e5a1665d80c7064692c43e835`
- D-182 stdout SHA-256
  `96bc51ef212452290ad9ab25a006df67af58feee1ebad3c2aafb9fffc565e350`
- D-182 stderr SHA-256
  `04eb8c99f04a8cedac9d4fa25833ae99c6e19ed327a58e1544bb8adfaf84c67a`

The future launcher must verify before and after rehearsal all five earlier
durable evidence sets (fifteen files) pinned by
`run_fictional_parent_presentation_tests.py`, plus the three
`iiw-flow-a-real-ipad-v1` files and the D-183 report. Every accepted source and
evidence hash must match before and after rehearsal.
No source, dependency, runtime, screen wording, image, navigation or accepted
evidence may change.

## Separate launcher and execution request

This proposal does not authorize launcher creation. After this proposal and
its companion checklist receive blind dual PASS and PI acceptance, a separate
create-only authorization may produce one bounded launcher and one execution
request. They must receive blind dual static review before execution.

The future launcher must:

- require an exact literal Beryl IPv4 and exact interface obtained by a later
  read-only preflight;
- reject loopback, wildcard, IPv6, hostname-derived, unassigned or multiple
  candidate presentation addresses;
- set `PTS_BERYL_HOST` to that literal address and keep TCP 4317 as the only
  Beryl listener;
- keep the fictional-parent gateway and every AAuth/SOGA service on literal
  `127.0.0.1:4318` or in-process only;
- invoke only the exact accepted `bridge.py --mode live` through
  `/usr/bin/python3 -B` with the reviewed durable provider;
- enforce a 15-minute total deadline, bounded output and fail-closed cleanup;
- refuse occupied ports 4317 or 4318 and any prior bridge/controller child;
- write only to one initially absent durable rehearsal-evidence directory;
- terminate the bridge and every child on success, stop, timeout, interruption
  or error; and
- prohibit automatic retry or fallback to simulated mode.

## Network and device boundary

Before launch, the Beryl associated-client list must contain exactly two
reviewed devices: Deb's laptop and controlled iPad A. Record only the count and
operator attestation—never MAC addresses, hostnames, device IPs or credentials.

Permitted network activity is limited to:

- the laptop presentation listener on the reviewed literal Beryl IPv4:4317;
- the iPad's HTTP requests to that exact presentation origin; and
- the laptop-only fictional-parent listener on literal 127.0.0.1:4318.

DNS, internet application access, UDP application traffic, wildcard binds,
IPv6, public or other private-network listeners, and every additional device
are prohibited. Cleartext HTTP is accepted only for this controlled rehearsal
on Deb's private Beryl network. The Beryl administrative page may be used only
before launch to confirm the two-device count and must then be closed.

## Rehearsal sequence

The laptop opens exactly two tabs at the same reviewed Beryl origin:

- `/table` is the operator/control tab. It alone shows the real scannable QR,
  the live table state and any `Finish / reset` control.
- `/flow-a` is the narrative tab. Its QR artwork is illustrative and must never
  be scanned. It shows the PI-locked walkthrough and runtime-mapped endings.

The rehearsal permits at most three sequential encounters, never concurrent.
Deb remains present throughout. Each encounter starts when `/table` visibly
shows `Scan to begin` with a fresh QR. `/flow-a` may continue to show the prior
completed or stopped ending while the bridge is already `IDLE`; this is correct
behavior, not a failed reset. The next `/permission-entry` scan advances the
runtime mapping into the fresh encounter. If `/table` does not show the fresh
idle QR, use only its accepted `Finish / reset` control; otherwise stop.

Runtime windows are mandatory: scan-to-approach and the overall hard encounter
deadline are 60 seconds; the choice window after approach is 30 seconds; and
Finish or Withdraw must be selected within the terminal completion window of
at most 15 seconds, further capped by the 60-second hard deadline. Automatic
completion before a required operator action is `STOPPED`, not PASS.

1. **Allow and finish.** The iPad scans only the real QR on `/table` and stays
   in the same browser context. It enters the fictional-adult role-play,
   acknowledges the persistent unverified-input boundary, selects
   `The fictional child approaches`, then selects
   `Approve the directed response in this fictional scenario` within the
   30-second choice window. `/flow-a` shows the permitted-question state. The
   iPad selects `Finish this interaction` within the completion window.
   `/flow-a` reaches the approved completion/research screen and `/table`
   returns to `Scan to begin` with a fresh QR.
2. **Decline and finish.** A fresh scan and lease records Decline. The iPad
   again selects `The fictional child approaches`, then
   `Decline the directed response in this fictional scenario` within the
   choice window. `/flow-a` shows the declined ending; the iPad shows the
   declined terminal state and `Finish` closes the interaction. After Finish,
   `/flow-a` shows the common completion/research screen and `/table` returns
   to `Scan to begin`.
3. **Allow then withdraw.** A fresh scan repeats `The fictional child
   approaches` and `Approve the directed response in this fictional scenario`.
   After `/flow-a` reaches the permitted-question state and before the terminal
   window closes, the iPad selects `Withdraw and stop this interaction`. It
   must then show `INTERACTION STOPPED`, `The adult stopped this interaction`
   and `The earlier permission result remains recorded, but no robot action
   will proceed.` The iPad's local `Finish` closes its view. `/flow-a` shows the
   stopped ending, the accepted authorization result is not rewritten, no
   action remains pending, and `/table` returns to `Scan to begin`.

If time or safety permits only one encounter, it must be Allow and Finish; the
other two are recorded `NOT_REHEARSED`. No silent retry is allowed after any
failed or stopped encounter.

The child-response and physical-action outcomes shown in explanatory screens
remain target-state explanation only. No child, sensing, spoken question,
dance or robot action occurs in this rehearsal.

## Mandatory readiness holdpoints before launcher creation

The future launcher and request remain blocked until all three are complete:

1. a separately reviewed static reconciliation verifies the visible step-2
   protocol screen against AAuth commit
   `fcf656de1926535f5bd6fc0538147ead6646e727` and protocol SHA-256
   `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`;
2. the PI explicitly confirms that the exact accepted mBot2/CyberPi, question,
   five-second pause and no-dance wording may be displayed as target-state
   explanation during this no-robot rehearsal, or separately approves exact
   fallback wording through review; and
3. the PI confirms that every accepted on-screen image used in the rehearsal
   contains no identifiable real child or undisclosed personal information and
   may be displayed under the no-screenshot rehearsal rule.

## Operator confirmations and stop rules

The future launcher/request may use only fixed operator responses defined in
the reviewed checklist. Any unexpected screen, stale demo, wrong wording,
unresponsive control, capability/session error, extra Beryl client, source or
evidence mismatch, firewall prompt, wrong address, socket variance, timeout,
secret exposure or cleanup failure stops the rehearsal and produces bounded
evidence. No repair, fallback or rerun is authorized.

The operator must not type or preserve names, faces, voice, real child data,
device identifiers, network credentials, tokens, capabilities or browser
history. Screenshots are excluded from the first rehearsal.

## Evidence

The future evidence may record only:

- reviewed source/runtime/evidence identities;
- the literal reviewed laptop Beryl IPv4 and interface;
- start/stop times and fixed operator labels;
- bridge return/cleanup status and bounded stdout/stderr;
- pre/post 4317/4318 listener and bounded process observations;
- pre/post accepted-source and evidence hashes;
- pre/post hashes for all eighteen files across the six preserved evidence
  sets, plus the D-183 report;
- the attested associated-client count of two; and
- for each of three scenarios, only `PASS`, `NOT_REHEARSED` or `STOPPED` plus
  the accepted fixed terminal outcome label.

Both blind gates must review resulting evidence before acceptance or public
use.

## Claim boundary and exclusions

A positive rehearsal could establish only that the exact accepted laptop Flow
A and one controlled iPad interoperated over the reviewed private Beryl network
for the scenarios actually observed, with local AAuth/SOGA decisions and
cleanup. It would not establish public-event readiness, multi-device
concurrency, verified identity, parenthood, parental or legal authority, legal
consent, complete AAuth conformance, wallet/WAS integration, physical robot
action, mBot2, CyberPi, Misty, sensors, speech, movement, G28 or G29.

This proposal authorizes no source change, launcher creation, execution,
listener, Beryl access, QR generation or scan, device contact or physical
action. The unrelated PI routine-tool proposal remains excluded, unread and
untouched.

## Holdpoints

1. Both blind gates review this proposal and companion operator checklist.
2. The three mandatory readiness holdpoints are completed and recorded.
3. PI may accept the reconciled plan and authorize create-only launcher/request
   work.
4. Both blind gates review the exact launcher and completed execution request.
5. PI may authorize at most one controlled rehearsal.
6. Both blind gates review resulting evidence before PI acceptance or use.
