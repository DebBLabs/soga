# IIW Flow A Beryl/iPad Live-Rehearsal R2 Execution Request

Date: 2026-11-01  
Status: CREATE-ONLY DRAFT — NOT AUTHORIZED FOR EXECUTION  
Review class: mandatory blind dual static review

## Exact instrument

- Launcher: `/Users/debb/dev/permission-to-speak-work/permission-to-speak/run_beryl_ipad_rehearsal.py`
- Launcher SHA-256: `28393dad720a91230ca7e8e4a03773f3763d201187f692c7c9a7de5b1adfab55`
- Presentation basis: `1e3e4928d80e9bd1f2ef12af162d0e70862f929a`
- SOGA basis: `4fdb93969e0ecd7d9f43fe3fb7276311cca10982`
- Interface/address: `en0` / `192.168.8.247`
- Presentation listener: `192.168.8.247:4317`
- Encounter-only internal listener: `127.0.0.1:4318`
- New evidence directory, initially absent:
  `/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-beryl-ipad-rehearsal-v2`
- Preserved stopped attempt:
  `/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-beryl-ipad-rehearsal-v1`
  must remain an empty directory before and after R2.
- Total deadline: 900 seconds; per-stream limit: 2,000,000 bytes; no retry.

## Requested authorization after review

Commit the exact corrected launcher without changing its hash, commit and push
the recovery record and this request with synchronized governance, then permit
one operator-attended R2 rehearsal only after the following external read-only
pre-invocation holdpoint passes. A mismatch stops before invocation and does
not consume R2:

1. launcher hash equals the exact value above;
2. presentation status is clean and its diff from the full presentation basis
   contains only `run_beryl_ipad_rehearsal.py`;
3. SOGA status contains only the unrelated excluded PI proposal and its diff
   from the full SOGA basis is a subset of the recovery record, R2 request,
   decision log and current state;
4. `en0` has exactly literal IPv4 `192.168.8.247`;
5. ports 4317 and 4318 are unused and no bridge/rehearsal process exists;
6. all eighteen accepted-evidence files, the D-183 report and provider
   manifest match their reviewed hashes;
7. v1 is a real, non-symlink, empty directory; and
8. v2 is absent.

Exactly the laptop and controlled iPad A may join Beryl. `/table` displays the
real QR; `/flow-a` is display-only; all encounter choices occur on the iPad.
The operator follows the accepted checklist and the launcher's fixed prompts.
The launcher automatically observes state and requires the explicit fixed
attestations that the operator personally tapped Finish or Withdraw.

The launcher must preserve exactly three v2 evidence files on success, stop,
timeout, `SIGHUP`, `SIGINT`, `SIGTERM`, `SIGQUIT`, refusal or error; terminate its bridge
and children; and confirm both ports unused. The empty v1 directory and all
accepted evidence must remain unchanged. No automatic retry is permitted.
`SIGKILL`, forced application termination and power loss cannot be handled by
the launcher.

After every launcher exit, normal or abnormal, the integrator must perform a
read-only `lsof` check for listeners on 4317 and 4318 and a process check for
the exact presentation-repository `bridge.py`. If that exact reviewed bridge
remains, the only permitted cleanup is `SIGTERM`, followed only if necessary by
`SIGKILL`, to that exact PID. The observation and any cleanup action must be
recorded in the durable R2 evidence or stopped-attempt report before review.

## Claim boundary and exclusions

A positive R2 result could establish only one controlled iPad interoperating
with the accepted laptop Flow A over private Beryl for the rehearsed fictional
role-play scenarios. It would not establish verified identity, parenthood,
legal authority or consent, complete AAuth conformance, public-event readiness,
wallet/WAS or physical robot action.

No execution, Beryl access, listener, QR scan, iPad contact, mBot2, CyberPi,
Misty, sensor, speech, movement, G28 or G29 activity is authorized by this
request. The unrelated PI routine-tool proposal remains excluded, unread and
untouched.
