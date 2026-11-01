# IIW Flow A Beryl/iPad Rehearsal R2 Evidence

Date: 2026-11-01  
Status: OBSERVED GATED NEGATIVE — PENDING BLIND DUAL REVIEW AND PI ACCEPTANCE  
Authority: D-187

## Exact evidence

- Launcher SHA-256:
  `28393dad720a91230ca7e8e4a03773f3763d201187f692c7c9a7de5b1adfab55`
- Evidence directory:
  `/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-beryl-ipad-rehearsal-v2`
- `evidence.json` SHA-256:
  `3223834ba64914bbd4ec21d6be392aad7560eb1ba54776f1dd5764b3f4a712e3`
- `bridge.stdout.txt` SHA-256:
  `d9a3c2edeea58b2813ad2274190ade7eb6d658faf5742a5ef819ce9dce3988a2`
- empty `bridge.stderr.txt` SHA-256:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The directory contains exactly those three files.

## Observed result

The PI entered `TWO_REVIEWED_CLIENTS`, opened the live Beryl presentation and
then entered `STOPPED`. The evidence records `result=STOPPED`, one initial
client attestation, no completed scenario, and all three scenarios as
`NOT_REHEARSED`. The PI reported that the failing browser address began with
the reviewed `192.168.8.247` address, that remnants of the original demo were
visible, and that selecting the approval control produced `forbidden_origin`.
No screenshot, request header, QR capability, cookie, device identifier or
participant detail was recorded.

The bridge started on literal `192.168.8.247:4317`, verified the accepted pins
and provider, and stopped cleanly. Evidence records cleanup PASS, empty stderr,
both listeners unused after exit, accepted evidence byte-identical, source
identity byte-identical, and stopped v1 preserved empty before and after. The
required external post-exit process and listener check found no bridge,
launcher, 4317 listener or 4318 listener.

`NetworkVariance` is recorded because the launcher's final interface/address
check failed and `network_after` is null. The evidence does not record which
address-check condition failed. This does not change the primary negative
result and authorizes no inference about why the check failed.

## Source-only boundary observation

The accepted bridge contains exact-origin rejection paths for participant
POSTs. Synthetic tests construct the expected Origin header directly. The PI
reports that an approval control on the reviewed Beryl address produced
`forbidden_origin`. The evidence does not record the request, its Origin
header, the device or browser, or whether a lease was claimed. It therefore
establishes neither the mismatch nor the page involved and authorizes no
relaxation of origin protection.

## Claim boundary

R2 is consumed as a gated negative. It establishes successful startup, an
operator STOPPED, bounded STOPPED evidence and cleanup only; the PI-reported
`forbidden_origin` rejection is not instrumented. It does not
establish a successful iPad choice, AAuth/SOGA decision, complete rehearsal,
public-event readiness, identity, authority, consent or physical robot action.
No retry, source change or additional execution is authorized.
