# IIW Flow A real-iPad Origin diagnostic execution request

Date: 2026-11-01  
Status: non-executable pending blind dual static review and prospective PI authorization

## Exact package

Presentation basis: `bdb3b75cd3c88629968b3636b26e480da80d3e63`  
SOGA basis: `bf81e2fc57f24e4de3ed6b6f20afb9c90bc934c9`

- `bridge.py` SHA-256
  `67157d1afeaab13c5f81c238b34e7e82f43ca80ee0f42681f57f1324bc6f176d`
- `index.html` unchanged SHA-256
  `f2023fb096e0bf59567ee6efbcef45f22ef65fec294332f08b2ac8cacd9e8c86`
- `test_fictional_parent_presentation.py` SHA-256
  `c46ab4435ce6926e72a5ffff90b505d51a9dbeb26d52f5a5d12cc4ad57e4cb3c`
- `run_beryl_origin_diagnostic.py` SHA-256
  `86237f9e4d45a663ddfbad669fc7f83d9de5b5d3a2603a88f9baf20da784a969`

Accepted D-188 report SHA-256:
`312e574c4d1a3bfab5439b46f5593a66c351e39e8636667e0b526ed47cb43dd8`.
The D-187 v2 evidence hashes are pinned inside the launcher.

## Requested execution

After the exact package is committed and separately authorized, permit exactly
one execution of the exact diagnostic launcher. The initially absent durable
evidence directory must be:

`/Users/debb/dev/research-evidence/soga/evidence/iiw-flow-a-ipad-origin-diagnostic-v3`

The stopped v1 and v2 diagnostic evidence must remain present and byte-identical.

Before the evidence directory is created, the launcher must enforce these
pre-invocation holdpoints. A failure here does not consume the attempt:

- report exactly one fixed, non-sensitive `PREFLIGHT_STOPPED:<STAGE>` label
  identifying the failed holdpoint without disclosing exception text or values;

- exact committed presentation and SOGA bases, exact source hashes and exact
  allow-lists limited to this request plus the authorizing decision/current state;
- exact pinned SOGA `.claude/settings.local.json` identity while Git runs in
  the reviewed stripped environment;
- unchanged protected SOGA trees, the complete accepted evidence set, D-183 and
  D-188 reports, provider manifest, D-187 v2 evidence, and preserved-empty v1;
- interface `en0` with literal Beryl IPv4 `192.168.8.247`, unchanged firewall,
  ports 4317/4318 unused, and no old presentation process; and
- exactly the reviewed laptop and controlled iPad A on Beryl, attested by the
  operator.

After those holdpoints pass, the launcher must enforce:

- a 300-second total limit and 2,000,000-byte limit for each child stream;
- diagnostic-only bridge mode with background polling disabled;
- print the exact table URL and open that exact URL automatically in Safari
  after bridge readiness and before waiting for the iPad interaction;
- one QR scan, lease claim and approach submission;
- if approach is not `EXACT`, preservation of its existing fail-closed response
  and immediate stop;
- if approach is `EXACT`, one held non-terminal `PENDING` state and the reviewed
  fictional-parent page, followed by exactly one participant protected POST;
- classification and interception of that next protected POST before proxy,
  policy, store resolution or terminal decision, returning only the fixed
  diagnostic completion response;
- evidence containing only the fixed Origin and endpoint classes, bounded state,
  hashes and control results—no raw header, Host, cookie, capability, body,
  address, query, user-agent, referrer, page URL, screenshot or exception text;
- bounded in-memory child-stream validation followed by fixed normalized stdout
  evidence and empty stderr evidence; raw child output is never persisted;
- proof that `last_terminal_outcome` remains `NONE`, both listeners close, source
  and accepted evidence remain unchanged, firewall and interface classes remain
  invariant, the exact child PID is absent, a second exact-client attestation is
  obtained, and exactly three evidence files exist;
- handlers for `SIGINT`, `SIGTERM`, `SIGHUP` and `SIGQUIT`, exception-safe child,
  listener, process, source, evidence, network and firewall cleanup checks, and
  unconditional bounded evidence writing after the evidence directory is created;
- bounded tolerance of transient diagnostic-state reads for less than ten seconds;
  and
- no automatic retry.

## Operator sequence

1. Confirm Beryl contains only the reviewed laptop and controlled iPad A.
2. Start the exact committed launcher on the laptop.
3. On iPad A, use Safari to scan the reviewed QR.
4. Select that the fictional child approaches.
5. If the fictional-parent choice page appears, make exactly one role-play choice.
6. Do nothing further. The launcher stops the diagnostic automatically.

Any unexpected page, terminal Allow/Decline/Expired outcome, forwarded choice,
non-`APPROACH` first protected request, exact approach that does not reach
`PENDING`, non-`CHOICE` second protected request, raw-value disclosure, extra
client, source mismatch, existing evidence directory, port/process conflict,
timeout, overflow, cleanup failure or preservation variance is a gated negative.
Stop without retry. A mandatory post-exit listener/process check must confirm both
ports unused and the exact reviewed child absent before evidence is accepted.
If that exact reviewed child survives normal shutdown, cleanup may signal only
that exact PID: `SIGTERM` first and `SIGKILL` only after the bounded wait fails.
The accepted 194-test controller and D-187 rehearsal launcher become stale when
this corrected diagnostic package is committed and must be recorded as superseded.

## Exclusions

This request grants no authority by itself. No `Referrer-Policy` change, normal-
mode Origin relaxation, visitor-visible wording or navigation change, test
execution, additional encounter, directed response, robot, mBot2, CyberPi, Misty,
sensor, speech, movement, wallet/WAS, G28 or G29 activity is requested.

The unrelated PI routine-tool proposal remains excluded, unread and untouched.
