# IIW Beryl Visual Preview and iPad Live Rehearsal Proposal

Date: 2026-10-30
Status: PROPOSED — NOT AUTHORIZED
Accepted presentation commit: fa6ccaa2f2fe65c043219380e127cb14f454eae9
Accepted SOGA state: D-170
Review basis: request-052 dual PASS on the rehearsal controls, re-pinned and
extended under D-170
Review class: mandatory blind dual review under D-064

## Purpose

Advance the accepted IIW table package through two separately authorized
operator-attended phases on Deb's private Beryl network:

1. **Phase A — laptop-only visual preview.** Deb inspects the current table
   opening and both path-specific endings. No iPad, QR scan, lease, encounter
   or AAuth/SOGA decision occurs.
2. **Phase B — controlled iPad rehearsal.** Only after Phase A is accepted, one
   controlled iPad scans the Permission to Speak QR and performs the bounded
   fictional-parent role-play.

Neither phase is a public-table run. Neither activates Project Agent, mBot2,
Misty or any physical action. Phase A does not authorize Phase B.

## Exact accepted package

Both phases use presentation commit
fa6ccaa2f2fe65c043219380e127cb14f454eae9 with a clean working tree and these
accepted hashes:

- index.html:
  343b861999625b7397dcce05b2ac28eb3af9e54249f3eec292f3c65513872d52
- bridge.py:
  242395156a760bfc9cd8e33474274c7c5302a903e793cc36a26f1d5d435f4a27
- test_fictional_parent_presentation.py:
  56ab1fdd2e5a3200229bfb25d481fdb2d938b757bc9ca8738f965164f0e8b1b4
- run_fictional_parent_presentation_tests.py:
  e07b168fd9728c2ce8e32040becdd51dd2a47ff01a978567cec78b664962c8e4
- table-runtime-manifest.json:
  4228ef92300b73934c734a0568e7f22d83779e7310cf2ad04c5c3d5543388b86
- README.md:
  033c30683c99994fdc47c93426743cc27c6e290d0d725d2b44bcf74da1b061b7
- CHECKLIST.md:
  035cda302df01b4ecf6fc0f2846737443a9d8e3d59266bae9d135bd1eb9d7004
- unchanged warmup.sh:
  e5615e3629547fc09bb7755dc6dc407582ac787476b56c9d7ae5a224962d12f2

The accepted provider manifest remains
7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e.
The D-170 evidence report and all three durable evidence sets must remain
byte-identical.

No application source, test, dependency, runtime or accepted evidence may be
changed by either phase.

## Common preflight and old-demo exclusion

Before either later execution request may be authorized, a read-only preflight
must record:

- the exact presentation commit, clean tree and hashes above;
- the current accepted SOGA commit and the permitted governance-only delta;
- exact Beryl interface name and its single literal private IPv4 on Deb's
  laptop;
- /usr/bin/python3 resolved to Command Line Tools Python 3.9.6 on Darwin arm64;
- ports 4317 and 4318 unused;
- the macOS firewall disposition known before launch, with no unreviewed
  mid-run change;
- the Beryl router associated-client list contains only the laptop,
  controlled iPad A and any other specifically named rehearsal device; record
  only count and operator attestation, never client names, MACs, hostnames or
  device IPs;
- no presentation bridge or Python process from any old launcher or bundle;
- the D-170 report and all nine durable evidence files match these accepted
  SHA-256 values:
  - D-170 report:
    f5dd4f7e85c157ee9dd64ba0ddf92d6c7f37e4a16a70307d7fe151c45f8eb5e0
  - v1 evidence.json / stdout.txt / stderr.txt:
    5e5a5ad498a24a6bee1917fb76bdf8853081968b814cafdfc2801c295ea4bb33,
    7358f9848273c939efba7c596d6d5a27d1fd16cb08582facb5b953c18cb28315,
    cf09f5c4f2f080e2ac7662a8281aa132ee05f71b9519a2446b18d0b03551acb3
  - v2 evidence.json / stdout.txt / stderr.txt:
    0880071a0d3b4290bca4f3160a4e1ee67063df4c12a9de6a249cbcd08ee7eaed,
    60060ef0b76ccc13deb55fb3414d17c125e1ee57234cbae2c0f65cb23b1e360a,
    455b0a00f3c3823a55f2b6dbd90f946032ba853c11e8c6e5e47064da24f210d7
  - path-endings-v1 evidence.json / stdout.txt / stderr.txt:
    9609063de1faf0ab2f8f12be6d3936d7ef548a74864e8f32059015a851431989,
    752fb3cf069d5c9bbfc0914818d8b7c0bfeafe6c4b7411f1e867eb61adad5415,
    b7fc17d365eb1f3623c53dcc39f3126231c718aad84dee058a6ce4b6b14baa9c;
  and
- a new absent durable evidence directory specific to the authorized phase.

Repeat the associated-client check immediately before launch. Any additional
client stops the phase before launch or when observed during the run.
Repeat every accepted-evidence hash immediately after each phase. Any
pre-launch difference stops before launch; any post-run difference is a gated
negative.

Only a later reviewed bounded launcher may start either phase. The repository's
Start LIVE demo.command, Start FALLBACK demo.command and every candidate under
dist/ are prohibited before and during both phases. Close every file,
hash-slide, localhost-preview and earlier-demo tab before launch.

## Network boundary

The only permitted non-loopback listener is the accepted presentation bridge
on the reviewed Beryl IPv4 and TCP port 4317. Port 4318 and every AAuth/SOGA
service remain literal loopback. Outbound application connections remain
literal 127.0.0.1 only.

DNS, internet, UDP, wildcard, IPv6, public, hostname-derived and every other
private-network bind or application connection are prohibited. Cleartext HTTP
is accepted only for these controlled phases on Deb's private Beryl network.

## Phase A — laptop-only visual preview

Phase A requires its own reviewed launcher and prospective PI execution
authorization. It is limited to eight minutes and one laptop browser. The
controlled iPad must not navigate to, scan or contact the presentation origin.

The laptop opens only:

1. http://REVIEWED_BERYL_IP:4317/table
2. http://REVIEWED_BERYL_IP:4317/table-questions/permission
3. http://REVIEWED_BERYL_IP:4317/table-questions/agent

The table page may render the stable Permission QR because it is part of the
accepted screen, but no device may scan it. The operator must not open
/permission-entry, submit an approach, create a lease, start an encounter or
exercise a terminal decision. The laptop browser must be the only client to
request the origin; no QR-reader or camera app may be opened on an associated
device while the table page is displayed.

The Phase A launcher must read the laptop-only /api/state immediately after the
bridge becomes ready and immediately before shutdown. It may record only
table_state, revision and last_terminal_outcome. Both snapshots must be exactly
IDLE, the same revision and NONE. Any other value or any change is a
gated-negative stop.

Deb verifies:

- the table opening shows active Permission to Speak and inactive Talk with
  Deb's Project Agent — NEXT INCREMENT;
- the Permission ending is specific to Permission to Speak, names all three
  bounded outcomes and says no completed encounter is retained;
- the Permission ending contains no Project-Agent-specific questions;
- the Project Agent page says NEXT INCREMENT — PREVIEW, NOT EXECUTED and makes
  no claim that a Project Agent ran;
- the Project Agent page contains no Permission-to-Speak outcome or
  parent/child authorization questions in its path-specific sections;
- both pages repeat the same common standards and research framing;
- both pages show the persistent unverified fictional-parent boundary; and
- Back to start returns to the current table opening without creating state.

The launcher must record only fixed labels:
PREVIEW_TABLE_OK, PREVIEW_PERMISSION_OK, PREVIEW_AGENT_OK,
PI_VISUAL_ACCEPTED, PI_VISUAL_NOT_ACCEPTED or STOPPED.

Phase A stops on any wrong screen, stale/shared ending, misleading claim,
unexpected client, source/pin variance, socket variance, application state
change, firewall prompt or cleanup failure. It performs no synthetic result and
does not establish an ALLOW, DECLINE or EXPIRED encounter.

## Phase B — controlled iPad rehearsal

Phase B remains blocked until Phase A evidence is reviewed and Deb records
visual acceptance. It requires a separately reviewed execution request and
prospective authorization. Its launcher enforces a 15-minute total runtime,
bounded streams, fail-closed cleanup and at most three sequential encounters,
one active lease at a time:

The operator script must name the 60-second pre-approach lease deadline as well
as the 30-second choice window and five-second terminal dwell.

1. **Allow:** controlled iPad A scans the QR, enters through /permission-entry,
   lands on /table-scene, submits The fictional child approaches, confirms the
   unverified fictional-parent boundary, chooses allow within 30 seconds and
   observes the laptop result during the five-second dwell.
2. **Decline:** a fresh encounter records decline and verifies that the
   directed response is not permitted.
3. **Expiry or reset:** a fresh encounter expires or uses the laptop reset and
   safely returns to the opening.

The iPad must never open /table; that route's state is laptop-only. A Camera-app
QR navigation that loses the SameSite lease cookie and displays Session
unavailable is a gated-negative stop, not permission to alter the run.

If only one encounter is attempted, it must be Allow and evidence must mark the
others NOT_REHEARSED. Fixed Phase B outcome labels are TERMINAL_ALLOW,
TERMINAL_DECLINE, TERMINAL_EXPIRED, RESET_TO_IDLE, NOT_REHEARSED and STOPPED.
No silent fallback or automatic retry is permitted.

## Evidence and privacy

Each phase writes only to its separately reviewed, initially absent durable
evidence directory. Evidence may contain exact source/runtime identities,
pre/post listener observations, start/stop times, bounded bridge streams, the
fixed labels for that phase, operator attestations and, for Phase A only, the
two three-field state snapshots described above.

Optional screenshots require manual review before preservation and must exclude
capability fragments, tokens, leases, client addresses, Wi-Fi credentials and
personal content. Do not record names, faces, voice, real child information,
device identifiers, device IPs, tokens, capabilities or browser history. The
reviewed laptop Beryl address is the only permitted recorded IP.

The fictional-parent input remains unverified role-play and must never be
characterized as identity, parenthood, legal authority or legal consent.

## Stop and cleanup

The bounded launcher terminates the presentation bridge and every child service
on completion, timeout, interruption or error. Post-run checks confirm no
listeners on 4317 or 4318 and no residual bridge process. Incomplete cleanup is
a gated negative. Post-run checks also recompute the D-170 report and all nine
accepted durable evidence hashes listed in the preflight. No automatic retry.

## Claim boundary and exclusions

A positive Phase A could establish only Deb's visual acceptance of the reviewed
laptop screens on the reviewed Beryl origin. It would not establish an AAuth
decision, QR/iPad interoperability or public-event readiness.

A later positive Phase B could establish only that the accepted laptop table
flow and controlled iPad interoperate over the reviewed private Beryl network
for the observed scenarios. It would not establish public-event readiness,
multi-device concurrency, verified identity, a real parent-child relationship,
parental or legal authority, legal consent, complete AAuth conformance, Project
Agent execution, wallet/WAS, mBot2, Misty, G28 or G29.

This proposal authorizes no execution, listener, QR scan, Beryl access, device
contact, source change, dependency operation or physical action. The unrelated
PI routine-tool proposal remains excluded and untouched.

## Holdpoints

1. Both blind gates review this exact corrected proposal.
2. PI may authorize read-only Beryl preflight and create-only Phase A launcher
   and execution request.
3. Both blind gates review the exact Phase A launcher, pinned network values and
   execution request.
4. PI may authorize one laptop-only visual preview.
5. Both blind gates review Phase A evidence; PI records visual acceptance or
   rejection.
6. Only after visual acceptance may a Phase B launcher and execution request be
   created and reviewed.
7. PI may separately authorize one controlled iPad rehearsal.
8. Both blind gates review Phase B evidence before acceptance or use.
