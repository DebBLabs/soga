# IIW Flow A Real-iPad 194-Test Execution Proposal

Date: 2026-10-31
Status: PROPOSED — CORRECTED AFTER REQUEST 086; NOT AUTHORIZED FOR EXECUTION
Authority to create: D-180
Review class: mandatory blind dual review

## Purpose

Define one future bounded verification of the exact D-180 Flow A real-iPad
reconciliation package. The future run may exercise only the accepted 128-test
SOGA fictional-parent baseline and the 66 presentation tests already encoded by
the committed controller. This document grants no execution authority.

## Exact accepted presentation package

Presentation repository:
`/Users/debb/dev/permission-to-speak-work/permission-to-speak`

Accepted local commit: `964f12626c9220e45a634d85fa407205aa9d9f3d`.
After D-180, the PI authorized durable preservation. The complete repository
and tags were pushed to the private remote
`https://github.com/DebBLabs/permission-to-speak.git`; `origin/main` was
independently checked to equal the accepted local commit.

Exact reviewed files:

- `bridge.py`: `ce732d1ce8be18618e6187b35e1770680785365c99782501075c7338983292b2`
- `flow-a-live.html`: `6e02bdb5f2bdb8e9dd4a8cbc5fde21c273f93f8ba76fdddf7130a6373b2ce3d7`
- `flow-a-approved.html`: `6e02bdb5f2bdb8e9dd4a8cbc5fde21c273f93f8ba76fdddf7130a6373b2ce3d7`
- `index.html`: `f2023fb096e0bf59567ee6efbcef45f22ef65fec294332f08b2ac8cacd9e8c86`
- `test_fictional_parent_presentation.py`: `59463258334b2febbe22ea4924c66c6527dd45592f0e7a87decf778f6d245d48`
- `run_fictional_parent_presentation_tests.py`: `e66d8a9063ef8050cbba3259f45a6196b7d7b54f26040ccf20ecd74f25f0a3e3`
- `table-runtime-manifest.json`: `b9cf7cf9f6994cd8f23fcad9b9a9a61515cf0a7fb5ae5d921d88bfce67fe0f67`
- `FLOW_A_RUNTIME_MAPPING_2026-10-31.md`: `45f1eb905a5a798daafbcd4f4c6b650629430727530cefb57ba8a6e7d2628572`
- `README.md`: `824d6113fbc382912eff0fc519536d5ee765b369559e83e4708689ae7ab55b03`
- `CHECKLIST.md`: `dd71f30704130c08a6257977f342e418180d028b8387b6a5c4f3b1305aaba022`

The PI-locked Flow A mirrors are byte-identical. No visible wording, images,
ordering, behavior or navigation may change through this proposal.

## Exact future controller and test boundary

Only the committed controller at SHA-256
`e66d8a9063ef8050cbba3259f45a6196b7d7b54f26040ccf20ecd74f25f0a3e3`
may be considered for a later run. It requires exactly:

1. 128 accepted SOGA fictional-parent baseline tests; and
2. 66 Flow A presentation tests;

for exactly 194 passing tests total.

It pins SOGA source basis
`8746e0cc383ec9d48ab16c89bcea5a88c79ed4d8`, presentation source basis
`3a8a919b80b674b4681b961e932133c2ec38488d`, the exact package hashes,
protected SOGA tree identities and all five preserved presentation evidence
sets. The controller does not hash itself or `table-runtime-manifest.json`;
their exact reviewed hashes are prospective operator holdpoints. Reviewers must
verify that its ancestry and allow-list checks remain correct after the D-180
commits.

The two execution-planning artifacts, any later execution request and any
prospective execution authorization must remain untracked until after the run
and blind evidence review. Before the run, only the decision log and canonical
state may be committed in SOGA. This is required because the accepted
controller permits only those two tracked paths after its pinned SOGA basis.

## Proposed bounded execution

A separately reviewed and prospectively PI-authorized invocation may run only
the committed controller through `/usr/bin/python3`. The controller's existing
finite limits apply:

- 150-second parent timeout;
- 2,000,000-byte limit per child output stream;
- encoded tests bind literal `127.0.0.1` loopback listeners only;
- exact source, repository, tree and accepted-evidence immutability checks;
- no automatic retry; and
- writes only beneath the initially absent durable directory
  `/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-real-ipad-v1`.

DNS, internet, Beryl/LAN, wildcard, public, non-reviewed private and IPv6
listeners are prohibited. The controller does not provide OS-level network
confinement; loopback-only operation rests on the statically reviewed encoded
tests plus the before/after listener and process observations below. A positive
result therefore makes no general network-confinement claim. No QR may be
generated or scanned and no iPad or other device may be contacted.

## Pre-start holdpoints

Before a later execution, the operator and reviewed instrument must establish:

1. both repositories satisfy the exact reviewed ancestry and allow-lists;
2. every package, controller, SOGA source, protected tree and accepted-evidence
   hash matches the reviewed manifest;
3. `uname -sm`, `/usr/bin/python3 --version`, and read-only path resolution of
   `/usr/bin/python3` establish the reviewed Darwin, arm64, Python version and
   resolved executable;
4. the durable evidence directory is absent;
5. a bounded `lsof -nP -iTCP -sTCP:LISTEN` inventory and `ps` inventory record
   that ports 4317 and 4318 are unused and no earlier bridge/controller child
   is active;
6. the execution proposal and runtime manifest have blind dual PASS and a
   separate prospective PI execution authorization; and
7. the proposal, manifest, execution request and authorization remain
   untracked, while the SOGA tracked diff after the pinned basis contains only
   `knowledge/strategy/DECISION_LOG.md` and
   `knowledge/working/CURRENT_STATE.md`.

Any mismatch stops before invocation and does not authorize correction,
fallback or retry.

## Evidence and stop rules

Any nonzero child result, wrong count, failure, error, skip, timeout, overflow,
measured mutation or accepted-evidence change is a gated negative. After the
controller returns, record the same bounded listener and process inventories
and verify that no reviewed child remains and ports 4317 and 4318 remain unused.
List the new evidence directory and require exactly `evidence.json`,
`stdout.txt` and `stderr.txt`. Any mismatch in those recorded observations is a
gated negative. These are operator observations recorded with the evidence,
not controller-enforced OS confinement. Preserve bounded evidence. Both blind
gates must review resulting evidence before any acceptance, rehearsal or use.

## Claim boundary and exclusions

A positive result could establish only the bounded synthetic-loopback behavior
of the exact accepted Flow A package and the preserved 128-test SOGA baseline.
It would not establish live Beryl/iPad operation, a live QR or phone interaction,
verified identity, parenthood, parental or legal authority, legal consent,
complete AAuth conformance, wallet/WAS integration, presentation rehearsal,
mBot2, CyberPi, Misty, sensors, speech, movement, G28 or G29.

This proposal authorizes no source change, import, compilation, lint, test,
execution, listener, network access, Beryl access, QR generation or scan,
device contact or physical action. The unrelated PI routine-tool proposal
remains excluded, unread and untouched.

## Holdpoints

1. Both blind gates review this proposal and companion runtime manifest.
2. The PI may accept the exact reviewed artifacts and separately authorize at
   most one bounded execution, while the execution documents remain untracked
   through execution and blind evidence review.
3. Both blind gates review resulting evidence before acceptance or use.
