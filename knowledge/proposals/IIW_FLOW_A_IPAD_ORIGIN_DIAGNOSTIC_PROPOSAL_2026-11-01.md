# IIW Flow A real-iPad origin diagnostic proposal

Date: 2026-11-01  
Status: proposal only; no implementation or execution authority

## Objective

Determine the fixed class of the real iPad request rejected during D-187 without
recording the raw Origin value or weakening the exact-origin guard. The diagnostic
may reproduce only the minimum path to a held `PENDING` interaction; it may not
produce a terminal AAuth/SOGA decision or execute a directed response.

## Create-only implementation boundary

After separate PI acceptance, implementation may change only the presentation
repository files needed to:

1. add a pure Origin classifier returning only `EXACT`, `MISSING`, `NULL`,
   `OTHER`, or `MULTIPLE` and a fixed endpoint classifier returning only
   `APPROACH`, `CHOICE`, `PARTICIPANT_LEAVE`, `PARTICIPANT_FINISH`,
   `PARTICIPANT_WITHDRAW`, `TABLE_FINISH`, or `OTHER`;
2. preserve every current rejection status, response body, lease check, Host check,
   content-type check, body limit, and connection-close behavior;
3. add a diagnostic-only mode enabled solely by the dedicated launcher and absent
   from normal presentation operation;
4. in diagnostic-only mode, classify every protected POST before the existing
   route-specific handling, whether its Origin would ordinarily be accepted or
   rejected, without changing validation order in normal mode;
5. record only the fixed Origin class and fixed endpoint class—never the raw
   Origin, Host, cookie, capability, body, address, query, user-agent, referrer,
   page URL, or exception text;
6. expose the bounded diagnostic only in a new durable evidence record controlled
   by a dedicated launcher, never in the participant UI or ordinary server log;
7. add tests for all five Origin classes, duplicate headers, all protected endpoint
   classes, redaction, unchanged fail-closed responses, and absence of secrets; and
8. pin every changed source and the initially absent evidence directory in a
   bounded execution request.

The exact changed-file list and hashes must be supplied before implementation is
accepted. The PI-locked Flow A screens and visitor-visible wording remain
byte-identical.

## Diagnostic execution boundary

Execution is not authorized by this proposal. A later, separately reviewed request
may permit one controlled Beryl/iPad diagnostic attempt with exactly this sequence:

1. the iPad may scan the reviewed QR and claim one lease through
   `/permission-entry`;
2. the iPad may submit `/api/table-approach`; the diagnostic records its fixed
   Origin and endpoint classes;
3. if approach is not `EXACT`, the existing fail-closed response is preserved and
   the run stops;
4. if approach is `EXACT`, normal processing may create the reviewed held
   `PENDING` state and its temporary 4318 gateway, but this is the only AAuth/SOGA
   evaluation permitted and it must remain non-terminal;
5. the reviewed fictional-parent page may load; and
6. the very next protected POST is classified and intercepted before any proxy,
   policy, store-resolution, or terminal-decision call. It receives the fixed
   diagnostic-only response `409 {"error":"diagnostic_complete"}` and the run
   stops, including when its class is `EXACT`.

The later execution request must also:

- require exactly the reviewed laptop and controlled iPad on Beryl;
- stop immediately after either a non-`EXACT` approach or the first protected POST
  after a successful approach is classified;
- prove that the intercepted POST did not reach the 4318 proxy or any terminal
  decision seam, that `last_terminal_outcome` stayed `NONE`, and that the held
  interaction and temporary gateway were closed during cleanup;
- use finite time and output limits, an initially absent durable evidence
  directory, cleanup checks, and no automatic retry; and
- require blind dual review of the resulting evidence before any correction is
  proposed.

## Explicit exclusions

No change to `Referrer-Policy`, accepted Origin values in normal mode, Host
validation, lease or capability handling, participant wording, Flow A navigation,
AAuth/SOGA sources, or robot code is authorized. The diagnostic-only interception
must be unreachable unless the dedicated launcher explicitly enables it. No test,
import, compilation, listener, Beryl access, QR scan, iPad contact, diagnostic run,
retry, mBot2, CyberPi, Misty, sensor, speech, movement, wallet/WAS, G28, or G29
activity is authorized by this proposal.

The unrelated PI routine-tool proposal remains excluded, unread, and untouched.

## Review and stop rules

The complete diagnosis and this proposal require blind dual review. Any raw-value
retention, participant UI disclosure beyond the fixed generic failure already
produced by the page, terminal decision, forwarded choice, broadened allow-list, or
normal-mode security relaxation is a blocker and requires STOP/NOT READY.
