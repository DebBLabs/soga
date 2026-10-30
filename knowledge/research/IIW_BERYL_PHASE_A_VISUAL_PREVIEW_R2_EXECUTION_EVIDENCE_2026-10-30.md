# IIW Beryl Phase A Visual Preview R2 Execution Evidence

Date: 2026-10-30

Status: evidence awaiting blind dual review and PI acceptance

Authority: D-174

## Exact execution basis

- SOGA commit:
  `ad87485d5c034147ccfb463ff4eaa875109da1be`
- Presentation commit:
  `3a48a260dc4b94b2163b5b71d0039ad77a1c7f13`
- Corrected launcher SHA-256:
  `39f7036135a9c9d2a41dd55383f675422a4670bb94f80f5b1554672dc30ae688`
- R2 request SHA-256:
  `0deb9ea8d1a9e1901de9bd171b6063c65dfd001dbb567bb5b28999177b32f1b6`

Every D-174 pre-invocation holdpoint passed before the launcher was invoked.
The associated-client check was a direct PI observation of exactly the laptop
on Beryl.

## Durable evidence

Directory:
`/Users/debb/dev/research-evidence/soga/evidence/iiw-beryl-phase-a-visual-preview-v1`

- `evidence.json`: SHA-256
  `f3ebf391e9bc4faf2807b1eda8c692b5d589f401ecf49bdaefe9bf1c56a12d30`
- `bridge.stdout.txt`: SHA-256
  `6580f36e7445f6110f93c45cf3242177e930be7f3c342f87283b1b5576a01300`
- empty `bridge.stderr.txt`: SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Observed result

- Result: `PI_VISUAL_ACCEPTED`.
- Fixed labels recorded:
  - `PREVIEW_TABLE_OK`
  - `PREVIEW_PERMISSION_OK`
  - `PREVIEW_AGENT_OK`
  - `PI_VISUAL_ACCEPTED`
- Both associated-client attestations were `ONLY_REVIEWED_CLIENT`; recorded
  client count was `1`.
- Network before and after was literal `en0` at `192.168.8.247`, with exactly
  one IPv4.
- Firewall state remained unchanged.
- Before and after state was `IDLE`, revision `0`, terminal outcome `NONE`.
- Live listener observation found only the reviewed presentation listener;
  port `4318` remained unused.
- Post-run listener and process cleanup passed. Neither port had a listener
  afterward.
- Accepted prior evidence remained byte-identical.
- Source identity was unchanged before and after.
- `failure_types` was empty.
- Elapsed time was `396.196` seconds, within the 480-second bound.
- Bridge stderr was empty. Bounded stdout recorded successful pin/provider
  verification, the reviewed Beryl listener and clean shutdown.
- No retry occurred.

The PI reported that the browser needed to be placed full screen to make the
far-left view complete and readable. In full-screen mode the PI accepted all
three reviewed screens. This is an operator-layout observation, not a runtime
failure; the final operator checklist should direct the browser to full-screen
mode before visual inspection.

## Claim boundary

This result can establish only PI visual acceptance of the reviewed table,
Permission-to-Speak ending and Project-Agent preview ending on the reviewed
laptop/Beryl origin. It does not establish a QR scan, iPad interoperability,
an encounter, an AAuth/SOGA decision, Project Agent execution, public-event
readiness, complete AAuth conformance, identity, parenthood, legal authority,
legal consent, wallet/WAS, mBot2, Misty, G28 or G29.

Phase B remains blocked until both blind gates review this evidence and the PI
accepts it into the canonical record. No additional execution is authorized.
The unrelated PI routine-tool proposal remains excluded and untouched.
