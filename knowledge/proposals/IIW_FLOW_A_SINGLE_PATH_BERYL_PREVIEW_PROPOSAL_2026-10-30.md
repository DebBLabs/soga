# IIW Flow A Single-Path Beryl Laptop Preview Proposal

Date: 2026-10-30
Status: PROPOSED — NO IMPLEMENTATION OR EXECUTION AUTHORITY
Authority to create: D-177
Review class: mandatory blind dual review

## Purpose

Visually verify the accepted D-177 single-path Permission to Speak table on
Deb's laptop over the private Beryl origin before any iPad/QR rehearsal.

This is a laptop-only visual preview. It must not begin an encounter, scan or
generate a live phone QR, contact the iPad or another device, invoke AAuth/SOGA
decision paths, or activate a robot, sensor, speech or movement.

## Accepted source basis

- Presentation repository commit:
  `5de1c70c258733d73117101aa556a9baabf4c2a8`.
- SOGA decision/state commit:
  `af387b39823231d2d441b40dadfea9337405ea12`.
- PI-locked Flow A visual reference SHA-256:
  `f47935a08aa5d3680efa4c4d6ef76f625791ea91187ca763ed1d4bc901b43f1c`.
- Exact seven-file D-177 package hashes are recorded in D-177 and must match.
- Existing launcher source, not executable for this phase:
  `run_beryl_visual_preview.py` at SHA-256
  `39f7036135a9c9d2a41dd55383f675422a4670bb94f80f5b1554672dc30ae688`.

The existing launcher is intentionally not reused unchanged. It pins the
superseded presentation package, expects an obsolete Project Agent page and
writes to an already-consumed evidence directory.

## Proposed create-only launcher correction

After this proposal is accepted, the PI may authorize one read-only local
interface/address preflight before launcher creation. With the laptop manually
joined to Beryl and without opening the Beryl admin page, that preflight must:

1. identify the candidate interface from the local route/interface inventory;
2. run `/usr/sbin/ipconfig getifaddr <reviewed-interface>`;
3. run `/sbin/ifconfig <reviewed-interface> inet`;
4. require exactly one private IPv4 address on that interface; and
5. record the exact interface and literal IPv4 in the corrected launcher and
   completed execution request.

The preflight is read-only and creates no launcher or execution authority. If
the interface or address cannot be established exactly, creation stops. The
completed launcher must never discover or select either value at runtime.

After that preflight, separately authorized create-only correction may modify exactly:

`/Users/debb/dev/permission-to-speak-work/permission-to-speak/run_beryl_visual_preview.py`

The correction must:

1. pin presentation commit `5de1c70c258733d73117101aa556a9baabf4c2a8`
   and the exact D-177 presentation source hashes;
2. pin SOGA commit `af387b39823231d2d441b40dadfea9337405ea12` and
   an explicit minimal allow-list for later reviewed records;
3. preserve and verify every accepted durable evidence set already protected by
   the D-177 controller, including `iiw-table-path-endings-v1` and
   `iiw-beryl-phase-a-visual-preview-v1`;
4. use a new initially absent evidence directory:
   `/Users/debb/dev/research-evidence/soga/evidence/iiw-beryl-single-path-preview-v1`;
5. open and attest only these laptop pages:
   - `/table`;
   - `/table-questions/permission`;
6. remove every Project Agent page, prompt and attestation;
7. require the browser to be in full-screen mode before visual acceptance;
8. require PI confirmation that the landing is single-path, the controlled-iPad
   boundary is visible, the Permission ending is correct, and the locked Flow A
   target remains unchanged;
9. keep state `IDLE`, revision unchanged and terminal outcome `NONE` throughout;
10. pin the preflight's exact interface and literal IPv4 as constants and
    re-check those same values read-only before invocation; any mismatch stops
    before invocation, does not consume an attempt, and requires a re-pinned,
    re-reviewed launcher;
11. retain the previously reviewed finite time/output limits, source checks,
    literal-interface/address checks, listener audit, process-group cleanup and
    fail-closed stop behavior;
12. retain fixed-label evidence and failure-type recording only, with no client
    MAC, token, exception text or client IP other than the reviewed literal
    address, and record the launcher's own SHA-256 in `evidence.json`.

## Network and operator boundary

The later preview may use only the exact interface and literal Beryl IPv4
address established by the authorized pre-creation preflight and pinned into
the reviewed launcher and completed request. The prior values were `en0` and
`192.168.8.247`; they are not assumed merely because they were previously
observed.

Before any future invocation:

- Beryl must show exactly the laptop as its sole associated client;
- the iPad, Misty, mBot2/CyberPi and every other device remain disconnected;
- ports `4317` and `4318` must be unused;
- no old bridge or candidate process may exist;
- presentation and SOGA repositories must match their reviewed bases and
  allow-lists;
- the new evidence directory must be absent; and
- read-only `ipconfig` and `ifconfig` checks must reproduce the pinned interface
  and address exactly; a mismatch stops before invocation without consuming an
  attempt and requires re-pinning and re-review;
- the exact corrected launcher and final execution request must both have blind
  dual PASS and prospective PI execution authority.

## Future bounded preview

A later authorization may permit one attempt, no automatic retry, with:

- one presentation listener on the reviewed literal Beryl IPv4 and port 4317;
- no listener on 4318;
- no DNS, UDP, wildcard, IPv6, internet or other application connection;
- only laptop GETs for `/table`, `/table-questions/permission` and `/api/state`;
- no `/permission-entry`, encounter, choice, Finish/reset or decision call;
- durable bounded evidence and independent evidence review.

## Stop rules

Stop before invocation, without consuming an attempt, on any launcher hash,
settings-file, repository-status, basis/allow-list, accepted-evidence,
evidence-path, interface/address, existing-listener or old-process variance.
Stop during the attempt on any source, hash, repository, interface,
address, firewall, client-list, port, listener, state, revision, evidence,
process, time, output or cleanup variance. Stop if any visitor-facing screen
differs from the PI-approved single-path target. Do not retry automatically.

## Claim boundary

A positive result would establish only PI visual acceptance of the reviewed
single-path laptop screens over the reviewed private Beryl origin. It would not
establish QR/iPad interoperability, a live AAuth/SOGA encounter, public-event
readiness, identity, parenthood, legal authority, consent, complete AAuth
conformance, meeting-agent operation, Project Agent, wallet/WAS, mBot2,
CyberPi, Misty, sensors, speech, movement, G28 or G29.

This proposal authorizes no preflight, implementation or execution. A later PI
acceptance must expressly authorize the read-only local preflight and subsequent
create-only launcher correction. The unrelated PI
routine-tool proposal remains excluded, unread and untouched.
