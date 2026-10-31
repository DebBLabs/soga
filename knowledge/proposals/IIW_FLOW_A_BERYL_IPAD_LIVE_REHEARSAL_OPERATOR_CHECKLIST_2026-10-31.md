# Permission to Speak — Beryl/iPad Rehearsal Operator Checklist

Date: 2026-10-31
Status: DRAFT ONLY — NOT REVIEWED; DOES NOT AUTHORIZE REHEARSAL

This checklist is deliberately usable while the laptop is on Beryl and Codex
is unavailable. Do not begin until the exact launcher and execution request
have blind dual PASS and Deb has prospectively authorized one rehearsal.

## Set out and charge

- [ ] Laptop connected to power.
- [ ] Controlled iPad charged; no keyboard required.
- [ ] Beryl router powered and stable.
- [ ] mBot2, CyberPi, Misty and other devices remain off and disconnected.
- [ ] Close every old demo, file preview and localhost tab.

## Join only the reviewed devices

- [ ] Join the laptop to Beryl.
- [ ] Join controlled iPad A to Beryl.
- [ ] Confirm the Beryl associated-client list contains exactly two devices:
      this laptop and controlled iPad A.
- [ ] Record only `TWO_REVIEWED_CLIENTS`; do not record device details.
- [ ] Close the Beryl administrative page.

If a third client appears, stop. Do not launch.

## Run the reviewed launcher

- [ ] Open Terminal from the launcher folder.
- [ ] Run only the exact command printed in the reviewed execution request.
- [ ] Type a fixed confirmation only when its statement is visibly true.
- [ ] Do not improvise a command, change an address, restart or use fallback.

The launcher must display the exact laptop table address and wait until it has
verified the accepted sources, provider, evidence and ports, and until you have
attested `TWO_REVIEWED_CLIENTS`. The launcher cannot inspect the Beryl client
list itself.

Open exactly two laptop tabs at the reviewed address:

- `http://REVIEWED_BERYL_IP:4317/table` — real QR and control state
- `http://REVIEWED_BERYL_IP:4317/flow-a` — locked narrative and endings

Never scan the illustrative QR artwork on `/flow-a`. The iPad enters only by
scanning `/table`'s real QR to `/permission-entry`; it must stay in the same
browser context and must never open `/table`, `/flow-a` or `/api/state`.

Timing for every encounter: reach approach within the 60-second lease/hard
deadline; choose within 30 seconds after approach; use Finish or Withdraw
within at most 15 seconds after the terminal result and before the 60-second
hard deadline. Move promptly: approach immediately and make the choice within
about 20 seconds of scanning so the terminal controls retain usable time. An
automatic close before the required tap is `STOPPED`.

## Encounter 1 — Allow and Finish

- [ ] `/table` shows `Scan to begin` and the real QR.
- [ ] `/flow-a` shows the locked Flow A start screen; its QR is illustrative.
- [ ] iPad scans only `/table`'s QR and opens the exact Beryl address.
- [ ] iPad shows the fictional-adult role-play and unverified-input boundary.
- [ ] Select `The fictional child approaches`.
- [ ] Select `Approve the directed response in this fictional scenario` within
      the 30-second choice window.
- [ ] `/flow-a` shows the real permitted-question state.
- [ ] iPad shows `Finish this interaction` and
      `Withdraw and stop this interaction`.
- [ ] Select `Finish this interaction` within the terminal completion window.
- [ ] `/flow-a` shows the approved completion/research screen.
- [ ] `/table` shows `Scan to begin` with a fresh QR. `/flow-a` may correctly
      remain on the completed ending.

## Encounter 2 — Decline and Finish

- [ ] Begin only after `/table` shows `Scan to begin` with a fresh QR.
- [ ] Scan that QR and enter a fresh encounter in the same browser context.
- [ ] Select `The fictional child approaches`, then
      `Decline the directed response in this fictional scenario` within the
      30-second choice window.
- [ ] `/flow-a` shows the declined ending.
- [ ] iPad shows Declined and Finish.
- [ ] Select Finish within the terminal completion window.
- [ ] Confirm `/table` returns to `Scan to begin`; `/flow-a` shows the common
      completion/research screen and may remain there.

## Encounter 3 — Allow then Withdraw

- [ ] Begin only after `/table` shows `Scan to begin` with a fresh QR.
- [ ] Scan that QR, select `The fictional child approaches`, then select
      `Approve the directed response in this fictional scenario` within the
      30-second choice window.
- [ ] Confirm `/flow-a` shows the permitted-question state.
- [ ] Select `Withdraw and stop this interaction` within the terminal
      completion window and before Finish.
- [ ] iPad shows `INTERACTION STOPPED`, `The adult stopped this interaction`
      and `The earlier permission result remains recorded, but no robot action
      will proceed.`
- [ ] Confirm the accepted authorization result is not rewritten.
- [ ] Confirm no action remains pending and the interaction safely closes.
- [ ] Select the iPad's local `Finish` button.
- [ ] Confirm `/table` shows `Scan to begin`; `/flow-a` may remain on the
      stopped ending.

If only encounter 1 is authorized or completed, mark encounters 2 and 3
`NOT_REHEARSED`. Do not run them later without a new authorization.

## Stop immediately if

- the screens or words differ from the PI-locked Flow A;
- a button does not follow the reviewed sequence;
- an old demo or simulated label appears;
- the iPad reports session/capability unavailable;
- another client joins Beryl;
- macOS requests an unreviewed firewall change;
- any port, process, source, evidence or address check fails;
- any secret, token, capability or device detail appears in evidence; or
- the launcher reports `STOPPED`, timeout or cleanup failure.

Do not repair, edit, switch to simulation or rerun.
Using `/table`'s accepted `Finish / reset` control when the fresh idle QR does
not appear is the single reviewed reset action, not an improvised repair.

## After the launcher returns

- [ ] Confirm Terminal returned to its prompt.
- [ ] Confirm the laptop has no listener on 4317 or 4318.
- [ ] Close the iPad browser tab.
- [ ] Disconnect the iPad from Beryl.
- [ ] Reconnect the laptop to normal Wi-Fi only after cleanup completes.
- [ ] Return to Codex and report only the fixed labels produced by the launcher.
      Do not paste raw launcher output or any address other than the reviewed
      literal laptop Beryl address.

No robot, child, voice, sensing, speech, movement or dance is part of this
rehearsal. The adult input remains unverified fictional role-play and does not
establish identity, parenthood, legal authority or legal consent.
