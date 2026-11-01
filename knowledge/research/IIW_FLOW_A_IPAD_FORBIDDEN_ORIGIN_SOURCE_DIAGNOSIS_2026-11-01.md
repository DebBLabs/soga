# IIW Flow A real-iPad `forbidden_origin` source diagnosis

Date: 2026-11-01  
Status: source-only diagnosis; no source modification or execution

## Accepted observation boundary

The D-187 rehearsal is a consumed gated negative. The operator reported seeing
`forbidden_origin` after selecting approval from the controlled iPad. The accepted
evidence does not preserve the request's `Origin` header, the exact page, or the
specific rejected endpoint. This diagnosis therefore does not claim which Origin
value Safari sent.

## Source facts

The reviewed presentation bridge has three relevant properties:

1. `bridge.py` emits `Referrer-Policy: no-referrer` by default on every response.
2. Browser POST handling rejects a present Origin that is not byte-for-byte equal
   to the configured presentation origin. The protected table, fictional-parent,
   and participant-action routes additionally require the exact configured origin.
3. `index.html` performs the fictional-parent and participant actions with browser
   `fetch()` POST requests.

The accepted tests prove rejection of a deliberately wrong Origin and acceptance
of a manually supplied exact Origin. They do not launch Safari and do not observe
the headers Safari constructs under the served response policy.

## Diagnosis

The failure is consistent with an untested boundary between the served browser
policy and the bridge's exact-origin requirement. The bridge fails closed as
designed, but the current test seam assumes the exact header rather than measuring
the real iPad request.

The local source is sufficient to establish that this compatibility boundary is
missing from the tests. It is not sufficient to choose safely among a missing,
`null`, exact, duplicate, or other Origin value. Relaxing the origin check now
would be guesswork and could weaken the protection that binds participant actions
to the reviewed Beryl origin.

## Required next evidence

A bounded diagnostic must classify, without retaining the raw header, the rejected
request as exactly one of `EXACT`, `MISSING`, `NULL`, `OTHER`, or `MULTIPLE`, along
with a fixed endpoint class. The existing rejection behavior must remain unchanged.
Only that evidence can support a later correction to response policy or request
validation.

## Claim boundary

This record establishes a source-level test and observability gap. It does not
establish a Safari defect, a particular Origin value, a safe relaxation, a working
iPad flow, or any AAuth/SOGA, robot, identity, parenthood, authority, or consent
claim.
