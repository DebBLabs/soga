# IIW Flow A Beryl/iPad Live-Rehearsal Execution Request

Date: 2026-10-31  
Status: CREATE-ONLY DRAFT — NOT REVIEWED; NOT AUTHORIZED FOR EXECUTION  
Authority to create: D-185  
Review class: mandatory blind dual static review

## Decision requested after review

Authorize exactly one operator-attended execution of the exact reviewed
`run_beryl_ipad_rehearsal.py` launcher, with no automatic retry, under the
D-184 proposal and checklist and the controls below. This document does not
itself authorize execution.

## Exact launcher and bases

- Launcher:
  `/Users/debb/dev/permission-to-speak-work/permission-to-speak/run_beryl_ipad_rehearsal.py`
- Launcher SHA-256:
  `f92ab65eb2b40e222afeb0d297cfcf28823f1f01b87156cebca69b22292ecdad`
- Presentation basis:
  `964f12626c9220e45a634d85fa407205aa9d9f3d`
- SOGA basis: `238e44b910719af6133775f7e001eb8bfecdb62b`
- Reviewed interface: `en0`
- Reviewed literal Beryl IPv4: `192.168.8.247`
- Presentation listener: `192.168.8.247:4317` only
- Internal fictional-parent listener: `127.0.0.1:4318` only and only during an
  encounter
- Durable evidence directory, initially absent:
  `/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-beryl-ipad-rehearsal-v1`
- Total deadline: 900 seconds
- Output limit: 2,000,000 bytes per stream
- Automatic retry: prohibited

The launcher pins all ten D-180 presentation files plus `warmup.sh`, the two
accepted SOGA fictional-parent test/controller sources, the four protected
governance trees, the accepted provider manifest, all eighteen files in the
six preserved evidence sets, and the D-183 report. It verifies those identities
before and after the rehearsal.

## Required operator and network holdpoints

Before invocation, Deb manually joins exactly the laptop and controlled iPad A
to Beryl, confirms the associated-client count is exactly two, and closes the
Beryl administrative page. mBot2, CyberPi, Misty and every other device remain
off and disconnected.

After blind dual PASS and PI authorization, the exact reviewed launcher must
first be committed in the presentation repository without changing its hash.
Before invoking it, the integrator performs and records this read-only
pre-invocation holdpoint. A mismatch stops before invocation and does not
consume the one authorized attempt:

1. recompute the committed launcher's SHA-256 and require the exact reviewed
   value above;
2. require clean `git status --porcelain` in the presentation repository and
   require `git diff --name-only 964f12626c9220e45a634d85fa407205aa9d9f3d --`
   to contain only `run_beryl_ipad_rehearsal.py`;
3. require the SOGA diff from `238e44b910719af6133775f7e001eb8bfecdb62b`
   to be a subset of the execution request, decision log and current state;
4. require `ipconfig getifaddr en0` and `ifconfig en0 inet` to show only
   `192.168.8.247`;
5. require ports 4317 and 4318 unused and no old bridge/rehearsal process;
6. recompute all eighteen accepted-evidence hashes, the D-183 report and the
   provider manifest; and
7. require the new evidence directory to be absent.

The launcher then independently verifies:

1. the reviewed interface has exactly `192.168.8.247` as its sole IPv4;
2. ports 4317 and 4318 are unused and no prior bridge/rehearsal child remains;
3. reviewed sources, trees, provider manifest and accepted evidence match;
4. the new durable evidence directory is absent; and
5. the operator enters exactly `TWO_REVIEWED_CLIENTS`.

Only then may it invoke:

```text
/usr/bin/python3 -B bridge.py --mode live
```

with `PTS_BERYL_INTERFACE=en0`, `PTS_BERYL_HOST=192.168.8.247`, and
`PTS_PORT=4317`. No simulated fallback is permitted.

## Operator sequence

The laptop opens exactly:

- `http://192.168.8.247:4317/table`
- `http://192.168.8.247:4317/flow-a`

The iPad scans only the real QR on `/table` and remains in the same browser
context. The illustrative QR on `/flow-a` is never scanned.

The fixed rehearsal sequence is:

1. `ALLOW_AND_FINISH`: approach, approve, verify permitted-question state,
   select `Finish this interaction`, and verify fresh `/table` QR.
2. `DECLINE_AND_FINISH`: fresh scan, approach, decline, verify declined state,
   select `Finish`, and verify fresh `/table` QR.
3. `ALLOW_THEN_WITHDRAW`: fresh scan, approach, approve, verify permitted-
   question state, select `Withdraw and stop this interaction`, verify the
   stopped ending and fresh `/table` QR.

The launcher automatically polls the laptop-only `/api/state` surface. It
captures each pending, terminal and closed transition without requiring Deb to
switch to Terminal during the 15-second terminal window. Because the bridge's
manual and automatic close states are identical, the launcher does not infer
which occurred from timing. After closure, Deb must explicitly attest with
`I_TAPPED_FINISH_ALLOW`, `I_TAPPED_FINISH_DECLINE` or `I_TAPPED_WITHDRAW` that
she personally used the required iPad control before automatic close. Anything
else is `STOPPED`. The launcher tolerates and counts transient state-read misses
for less than ten consecutive seconds, while `ERROR` or `RESTART_REQUIRED`
stops immediately. It
records no QR capability, token, cookie, device identifier, address other than
the reviewed laptop address, person name, face, voice or browser history.
Screenshots are prohibited. After the first successful Allow-and-Finish
scenario, Deb may enter `CONTINUE_ALL` or `END_AFTER_ALLOW`. The latter leaves
the Decline and Withdraw scenarios explicitly `NOT_REHEARSED`; it is not a
claim that they passed.

The accepted timing windows remain mandatory: 60-second encounter ceiling,
30-second choice window and at most 15 seconds for Finish or Withdraw, capped
by the encounter ceiling. Any unexpected screen, stale demo, wrong wording,
unresponsive control, automatic close before the required tap, extra Beryl
client, firewall prompt, source/evidence/address mismatch, timeout or cleanup
variance produces `STOPPED`. No repair, fallback or rerun is authorized.

## Evidence and cleanup

The launcher writes exactly:

- `evidence.json`
- `bridge.stdout.txt`
- `bridge.stderr.txt`

under the initially absent evidence directory. Evidence is limited to reviewed
identities, fixed labels, bounded state summaries, timing, fixed listener and
cleanup observations, the reviewed interface/address, the attested client
count of two, and before/after hashes. It contains no screenshot or participant
or device detail. It records each scenario as only `PASS`, `NOT_REHEARSED` or
`STOPPED`, with fixed outcome `ALLOW`, `DECLINE`, `WITHDRAWN` or `NONE`. A
failed second client attestation records no client count rather than falsely
recording two.

The launcher records the macOS application firewall state before and after and
requires it to remain unchanged; it authorizes no firewall change. During
each pending encounter it requires the internal listener to be the reviewed
child on literal `127.0.0.1:4318`; after each decision and close it requires
that listener to be absent.

On success, stop, timeout, interruption, preflight refusal or error, the
launcher writes exactly the three bounded evidence files, terminates the
bridge and its children and verifies that ports 4317 and 4318 are unused and no
reviewed child remains. A consumed attempt requires blind dual evidence review
and PI acceptance before any use or further execution.

## Claim boundary and exclusions

A positive result could establish only that the exact accepted laptop Flow A
and one controlled iPad interoperated over the reviewed private Beryl network
for the three observed role-play scenarios, with local AAuth/SOGA decisions and
cleanup. The on-screen mBot2/CyberPi, question, pause and no-dance material is
target-state explanation only.

It would not establish public-event readiness, verified identity, parenthood,
parental or legal authority, legal consent, complete AAuth conformance,
wallet/WAS integration, physical robot action, mBot2, CyberPi, Misty, sensing,
speech, movement, G28 or G29.

No execution, Beryl access, listener, QR generation or scan, iPad/device
contact or robot action is authorized by this request. The unrelated PI
routine-tool proposal remains excluded, unread and untouched.
