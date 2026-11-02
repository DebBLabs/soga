# IIW Flow A Beryl/iPad V11 Rehearsal Evidence

Date: 2026-11-02  
Status: ACCEPTED GATED POSITIVE  
Authority: D-191

## Exact evidence

- Presentation commit:
  `8b6d14781b579aa5a352ed4ceb531ae0257395fa`
- Rehearsal launcher SHA-256:
  `2e8f945dfa6ce79e88a0084dc760197ca781ff337e40b6218c41a16ce1e40430`
- Evidence directory:
  `/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-beryl-ipad-rehearsal-v11`
- `evidence.json` SHA-256:
  `b863e09dede1dfe0462ebbfa12c2ce6e6e7dfb439874e750b5d831659885d9d5`
- `bridge.stdout.txt` SHA-256:
  `669f6f984ee8699fb3182f69a635523b8a6b4047ac7fc77f9c1232f55fd2b81d`
- empty `bridge.stderr.txt` SHA-256:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The directory contains exactly those three files. Claude Gate 1 and AGy Gate 2
independently recomputed the identities and returned PASS in request-109 with
no blockers.

## Accepted result

The evidence records `PI_REHEARSAL_ACCEPTED`, no failure type or detail, and
exactly two associated clients: the controlled laptop and controlled iPad A on
the private Beryl network. All four reviewed paths passed:

1. **Leave before approach.** The leased session returned to `IDLE` without a
   permission decision. Decision and presentation outcomes remained `NONE`.
2. **Approve and Finish.** The decision reached terminal `ALLOW`, `granted`,
   `permitted`, HTTP `200`; Finish closed the presentation as `COMPLETED` and
   returned the table to `IDLE`.
3. **Decline and Finish.** The decision reached terminal `DECLINE`, `declined`,
   `not permitted`, HTTP `403`; Finish closed the presentation as `COMPLETED`
   and returned the table to `IDLE`.
4. **Approve and Withdraw.** The decision first reached terminal `ALLOW`,
   `granted`, `permitted`, HTTP `200`; Withdraw closed the presentation as
   `STOPPED` and returned the table to `IDLE` without rewriting the recorded
   authorization result.

Pending and terminal states were sampled for each decision path with zero
transient-state misses. The evidence records the operator's exact fixed
attestations for Leave, Finish, Decline and Withdraw.

## Preservation and cleanup

- Cleanup: `PASS`.
- Ports `4317` and `4318`: unused before and after execution.
- Presentation listener: active only during the bounded run.
- Associated-client count: exactly two, attested before and after.
- Network before and after: `en0`, `192.168.8.247`, one private IPv4 address.
- Source identity before and after: byte-identical.
- All pinned prior evidence: byte-identical.
- Stopped v1 evidence: preserved empty before and after.
- Firewall state: unchanged.
- Automatic retry: false.
- Stderr: empty.
- Elapsed time: 410.462 seconds, within the reviewed bound.

## Claim boundary

This establishes a real bounded local interaction among the controlled laptop,
Beryl and controlled iPad, including the associated local AAuth/SOGA decision
flow and clean teardown. It does not establish verified identity, parenthood,
legal authority or consent, complete AAuth conformance, public-phone operation,
wallet/WAS integration, or physical robot action.

The public-demo launcher and operator checklist remain create-only work. mBot2,
CyberPi and Misty remain inactive pending a separately reviewed physical-robot
execution.
