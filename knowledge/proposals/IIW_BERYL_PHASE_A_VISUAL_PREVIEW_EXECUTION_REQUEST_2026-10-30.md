# IIW Beryl Phase A laptop-only visual-preview execution request

Date: 2026-10-30
Status: CREATE-ONLY — NOT AUTHORIZED FOR EXECUTION
Authority: D-171
Review class: mandatory blind dual review under D-064

## Purpose

Request prospective authority for exactly one bounded laptop-only visual
preview of the accepted IIW table opening and both path-specific endings on
Deb's private Beryl network. This is Phase A of the proposal accepted by D-171.
It does not authorize Phase B, a QR scan, iPad contact, an encounter, an
AAuth/SOGA decision, Project Agent execution or physical action.

## Exact reviewed inputs

- Accepted proposal:
  `knowledge/proposals/IIW_BERYL_IPAD_LIVE_REHEARSAL_PROPOSAL_2026-10-29.md`
  at SHA-256
  `d7a3fca4cd60a1967576ef6f8452a10ecfeee28fcf9c2a05f1374affd160523c`.
- SOGA basis: commit
  `709b17d7b5a42a4eed1bc7d143acebdb85301e0e`, with only the later reviewed
  execution request, decision log and canonical-state records permitted to
  differ.
- Accepted presentation basis: commit
  `fa6ccaa2f2fe65c043219380e127cb14f454eae9`.
- Create-only Phase A launcher:
  `/Users/debb/dev/permission-to-speak-work/permission-to-speak/run_beryl_visual_preview.py`
  at SHA-256
  `82f701c0ad1d1825eeb98b988796d0161223616a2e2e2863da99bb746cfcacbe`.
  The launcher is the only presentation-repository addition permitted after
  the accepted basis.
- The launcher pins all eight accepted presentation hashes, including
  `warmup.sh`, the D-170 report at SHA-256
  `f5dd4f7e85c157ee9dd64ba0ddf92d6c7f37e4a16a70307d7fe151c45f8eb5e0`,
  and all nine accepted durable evidence-file hashes from v1, v2 and
  path-endings-v1.
- The accepted provider manifest remains SHA-256
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`
  and is checked by the unchanged accepted `bridge.py` before service start.

No source, dependency, accepted evidence or runtime may change.

## Read-only network preflight

Under D-171, Deb manually joined the laptop to Beryl and ran the bounded
read-only interface preflight. It recorded, without contacting a service:

- capture time: `2026-10-30T05:55:44Z`;
- interface: literal `en0`;
- exactly one interface IPv4: literal `192.168.8.247`;
- architecture: `arm64`;
- `/usr/bin/python3`: Command Line Tools Python `3.9.6`;
- macOS application firewall: disabled, state `0`, to be re-read before and
  after the preview with any change treated as a gated negative; and
- TCP ports 4317 and 4318: unused.

The launcher pins `en0` and `192.168.8.247` exactly. A DHCP change, a missing
address, more than one IPv4 on the interface or any other interface/address
causes a pre-start stop. There is no discovery, hostname, DNS or fallback.

Immediately before launch, Deb must inspect the Beryl associated-client list
and attest that it contains exactly this laptop and no other client. The iPad
must remain disconnected for Phase A. The launcher requests the same
attestation again before its final state snapshot. An unexpected client or an
inability to make either observation stops the run.

## Exact bounded execution

Only after both blind gates PASS the complete launcher and this request, and
the PI gives prospective execution authority, run exactly:

```text
/usr/bin/python3 -B /Users/debb/dev/permission-to-speak-work/permission-to-speak/run_beryl_visual_preview.py
```

The launcher must be committed unchanged before execution and its hash must
still equal the value above. It enforces:

- total runtime no more than 480 seconds and readiness no more than 15 seconds;
- bridge output no more than 1,000,000 bytes per stream;
- one presentation listener only at literal `192.168.8.247:4317`;
- no listener on TCP port 4318 throughout Phase A; a 4318 listener would prove
  that the prohibited encounter path started;
- accepted bridge socket guards that prohibit DNS, UDP, wildcard, IPv6,
  internet and every other application bind or connection;
- exact Host/origin behavior already accepted in `bridge.py`;
- no old bridge, Start LIVE demo, Start FALLBACK demo or `dist/` candidate;
- initially unused ports 4317 and 4318;
- an initially absent durable evidence directory at
  `/Users/debb/dev/research-evidence/soga/evidence/iiw-beryl-phase-a-visual-preview-v1`;
- fail-closed termination of the bridge process group on success, refusal,
  timeout, interruption or error; and
- post-run absence of both listeners and every bridge process, unchanged
  source identity, unchanged firewall state, unchanged reviewed
  interface/address and byte-identical accepted evidence.

No automatic retry is permitted.

## Operator path

Before launch Deb closes every earlier demo, localhost-preview, file-preview
and hash-slide tab and does not open a camera or QR-reader application. The
laptop browser is the only origin client. The stable QR may render on `/table`,
but no device may scan it.

The launcher prints, one at a time, only these reviewed laptop-browser URLs:

1. `http://192.168.8.247:4317/table`
2. `http://192.168.8.247:4317/table-questions/permission`
3. `http://192.168.8.247:4317/table-questions/agent`

Deb opens them only on the laptop. She must not open `/permission-entry`,
submit an approach, create a lease, begin an encounter, exercise a decision or
use the Finish/reset control. Back to start may return to `/table` only.

The only preview labels are:

- `PREVIEW_TABLE_OK` or `STOPPED`;
- `PREVIEW_PERMISSION_OK` or `STOPPED`;
- `PREVIEW_AGENT_OK` or `STOPPED`; and
- `PI_VISUAL_ACCEPTED` or `PI_VISUAL_NOT_ACCEPTED`.

The launcher records associated-client count `1` and the two fixed
`ONLY_REVIEWED_CLIENT` operator attestations separately from these preview
labels.

## State invariance

The launcher reads `/api/state` from the reviewed laptop address immediately
after readiness and immediately before shutdown. It records only
`table_state`, `revision` and `last_terminal_outcome`. Both snapshots must be
exactly `IDLE`, the revision must be the same integer and the terminal outcome
must be `NONE`. Any lease, reset, encounter, terminal transition, unreadable
state or revision change is a gated-negative stop.

## Visual checks

Deb verifies the complete D-171 Phase A checklist:

- the opening shows active Permission to Speak and inactive Talk with Deb's
  Project Agent — NEXT INCREMENT;
- the Permission ending is path-specific, names permitted, declined and
  expired, and says no completed encounter is retained;
- it contains no Project-Agent-specific questions;
- the Project Agent page says NEXT INCREMENT — PREVIEW, NOT EXECUTED and does
  not claim that an agent ran;
- it contains no Permission-to-Speak outcome or parent/child authorization
  questions in its path-specific sections;
- both endings repeat the same common standards and research framing;
- the persistent unverified fictional-parent boundary remains visible; and
- Back to start returns to the current opening without changing state.

A wrong, stale, shared or misleading screen requires `STOPPED` or
`PI_VISUAL_NOT_ACCEPTED`. It may not be accepted by explanation.

## Evidence and privacy

The launcher may write only to the new evidence directory. It records exact
source/runtime identities, the reviewed interface/address, fixed pre/live/post
listener observations, pre/post firewall state, accepted-evidence hashes, the
two three-field state snapshots, fixed labels, the two fixed client
attestations, elapsed time, bounded bridge streams and cleanup status. Once the
evidence directory is created, interruption, child cleanup failure and bounded
post-run inspection errors are converted to fixed failure types so the launcher
still writes the durable negative record before returning non-zero.

It records no names, faces, voice, real-child information, device identifiers,
MAC addresses, Wi-Fi credentials, tokens, capabilities, leases, browser
history or screenshots. The reviewed Beryl address is the only permitted
recorded IP. No screenshot is authorized by this request.

## Result and claim boundary

A positive result requires `PI_VISUAL_ACCEPTED`, every fixed preview label,
both client attestations, invariant IDLE state, unchanged accepted evidence,
unchanged network/firewall state and complete listener/process cleanup.

It could establish only Deb's visual acceptance of the reviewed laptop screens
on this reviewed Beryl origin. It would not establish an AAuth decision,
QR/iPad interoperability, public-event readiness, complete AAuth conformance,
verified identity, a real parent-child relationship, parental or legal
authority, legal consent, Project Agent execution, wallet/WAS, mBot2, Misty,
G28 or G29.

Phase B remains blocked until both blind gates review Phase A evidence and Deb
records visual acceptance. This request authorizes no execution, listener,
QR scan, iPad/device contact, source correction, dependency operation, Project
Agent, physical action or automatic retry. The unrelated PI routine-tool
proposal remains excluded and untouched.
