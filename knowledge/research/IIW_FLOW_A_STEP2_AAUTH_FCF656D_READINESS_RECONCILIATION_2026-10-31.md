# IIW Flow A Step-2 AAuth `fcf656d` Readiness Reconciliation

Date: 2026-10-31  
Status: SOURCE-ONLY DRAFT — PENDING BLIND DUAL REVIEW AND PI ACCEPTANCE  
Authority: D-184  
Author/integrator: Codex

## Purpose and boundary

This report reconciles the visitor-visible protocol screen in the accepted
Flow A presentation with the exact AAuth editor source authorized by D-184. It
does not modify the presentation, authorize a rehearsal, or add any protocol
claim. It distinguishes AAuth-defined concepts from local endpoint names and
the SOGA governance composition.

The report is source-only. No import, compilation, test, listener, network,
Beryl, QR, iPad, robot, sensor, speech or movement operation was performed.

## Exact sources verified

### AAuth editor source

- Official origin recorded in the external-input manifest:
  `https://github.com/dickhardt/AAuth.git`
- Durable source:
  `/Users/debb/dev/research-evidence/soga/inputs/aauth/fcf656d/source/`
- Commit:
  `fcf656de1926535f5bd6fc0538147ead6646e727`
- Tree: `fe5a02d4a965557c0d31620c5bbb8f725fdccb94`
- Protocol file: `draft-hardt-oauth-aauth-protocol.md`
- Recomputed protocol SHA-256:
  `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`
- Working-tree status: clean.

All protocol line references below are to that exact Markdown file.

### Accepted presentation and implementation

- Presentation repository basis:
  `964f12626c9220e45a634d85fa407205aa9d9f3d`
- Visible Flow A file: `flow-a-live.html`
- Accepted SHA-256:
  `6e02bdb5f2bdb8e9dd4a8cbc5fde21c273f93f8ba76fdddf7130a6373b2ce3d7`
- Local transport implementation:
  `m02_aauth_fcf656d/localhost.py`
- Approval-pending implementation:
  `m02_aauth_fcf656d/approval_pending.py`
- Presentation bridge: `bridge.py`

## Exact visible step-2 content

The screen headed **“The proposed interaction is bound to this turn”** shows:

| Visible row | Visible explanation | Visible status |
|---|---|---:|
| `/person-token` | Person token · who the agent acts for | `200` |
| `/authorize` | Resource token · what the resource requires | `200` |
| `/auth-token` | Auth token · bounded authority after supervision | `200` |
| `/enforce` | Enforcement · is this action allowed now? | `202` |

It then shows **“INTERACTION ZONE OPEN”** and explains that one scenario, one
short time window and one proposed robot interaction are in scope, while
multiple participants cause a pause.

The companion phone pane shows **“ACTIVE ENCOUNTER”**, **“Start this child’s
turn”**, the choices **“Allow the robot to ask”** and **“Decline”**, and the
qualification: **“This binds the input to the turn—not to a verified child or
parent identity.”**

## Reconciliation

### 1. `/person-token` — accurate local path for an AAuth-defined token

The draft defines a person token as a PS-issued JWT identifying the person an
agent acts for to one resource. It carries identity and no authorization
(lines 202 and 565–567). The three-party flow begins with the agent obtaining
that token from the PS (lines 349–353 and 380). Every PS publishes a required
`person_token_endpoint` (lines 884–899).

The visible explanation, **“who the agent acts for,”** is accurate. It must not
be read as identity proofing, parenthood, legal authority, consent or
permission. The draft explicitly says the person token is not evidence of
identity proofing, legal identity or assurance level (line 567).

`/person-token` is the local literal endpoint path used by the accepted test
fixture. AAuth specifies the metadata member `person_token_endpoint`, not this
universal literal path.

### 2. `/authorize` — accurate local path for the AAuth resource-token step

In the three-party flow, the agent presents the person token at the resource's
authorization endpoint; the resource verifies it and returns a resource token
(lines 355–360 and 380–382). A resource token describes the access the agent
needs (line 203), and a resource issues one only after verifying a person token
or auth token (lines 643–650). The authorization endpoint is optional metadata
and its URL is resource-defined (lines 662–666).

The visible explanation, **“what the resource requires,”** is accurate as a
short description of the resource-token step. `/authorize` is the accepted
local resource endpoint. It is not a protocol-mandated literal pathname.

### 3. `/auth-token` — accurate local path, with a necessary supervision caveat

The three-party flow sends the resource token and presented token to the PS's
auth token endpoint; the PS returns an auth token (lines 362–369 and 380–383).
The draft defines an auth token as granting an agent access to a resource
(line 204), and the PS's required `auth_token_endpoint` evaluates the request,
handles user consent if needed, and either issues directly or federates with an
AS (lines 884–887 and 945–1005).

The phrase **“bounded authority after supervision”** is consistent with this
demo's governed composition: the PS decides whether to issue based on consent,
mission intent and prior log entries, and the Supervisor performs that
evaluation (lines 457–464). However, the draft defines no wire contract between
the PS and a separate supervision server; that relationship is explicitly out
of scope and may be internal to the PS (line 455). Therefore **“Supervision” on
the screen names the accepted SOGA-as-PS-policy composition, not a complete or
separately conformant AAuth supervision protocol.**

`/auth-token` is the local literal path corresponding to the AAuth metadata
member `auth_token_endpoint`; the pathname itself is not universal.

### 4. `/enforce` — local resource seam, not an AAuth-named endpoint

The draft says the resource enforces the resulting auth token at access time,
including signature verification, proof-of-possession and access rules
(lines 459–464). It does not define a universal `/enforce` endpoint. The
accepted implementation uses `/enforce` as its local protected-resource seam.

The visible explanation, **“is this action allowed now?”**, truthfully describes
the local enforcement and SOGA governance question. It must not be attributed
to an AAuth endpoint named `/enforce`.

The visible `202` uses an AAuth-defined deferred-response primitive. The draft
distinguishes `requirement=interaction`, where the agent directs a user to an
interaction endpoint (line 214; also lines 690, 1005 and 2093–2182), from
`requirement=approval`, where a server is obtaining approval from another party
without requiring the agent to direct a user (lines 2055, 2081–2085 and
2184–2197). The approval response is valid from a Resource, PS or AS and uses
`202 Accepted`, `AAuth-Requirement: requirement=approval`, `Location` and
`Retry-After`; the agent polls the `Location` URL until a terminal response.
The general deferred-response rules additionally require `Cache-Control:
no-store`, a pending body, and bounded terminal outcomes (lines 2200–2284).

The accepted local resource returns that AAuth `requirement=approval` response
from `/enforce`, with `Location`, `Retry-After` and `{"status":"pending"}`; the
bridge follows the signed polling lifecycle. What remains local is the literal
`/enforce` pathname, the unverified fictional-adult approval source and its
one-use capability channel, the SOGA policy applied to that input, the binding
checks, and the demo’s particular timing windows. AAuth defines the approval-
pending transport pattern; it does not establish that the role-play participant
is a parent or standardize this demo’s other-party authority semantics.

### 5. “Bound to this turn” and “interaction zone” — local demo boundaries

AAuth tokens are audience-bound, key-bound and time-limited, and the resource
token/auth-token chain carries the requested access. The accepted demo further
constrains one scenario, one short window and one proposed interaction. The
terms **“this turn”** and **“interaction zone”** are explanatory SOGA/demo
language, not AAuth protocol terms. Multiple-participant pause behavior is
also a local safety rule, not a claim derived from the draft.

## Readiness result

**READY FOR SOURCE-ONLY CLAIM REVIEW, WITH THE DISPLAY CLASSIFIED AS A MIXED
AAuth/SOGA TRACE.**

The visible sequence is faithful to the accepted three-party AAuth token order:

1. obtain a person token;
2. present it to the resource and obtain a resource token;
3. send the resource token to the PS and obtain an auth token; and
4. present the auth token to the resource, which enforces access.

The short descriptions of the three token classes are accurate. The following
qualifications are mandatory whenever the screen is explained:

- `/person-token`, `/authorize`, `/auth-token` and `/enforce` are local paths;
  AAuth standardizes endpoint roles/metadata and token semantics, not all four
  literal pathnames.
- `/enforce`, the fictional-adult approval source and its capability channel,
  the SOGA policy and binding checks, the interaction zone, the
  multiple-participant pause and the demo timing windows are local composition;
  the `requirement=approval` deferred-response and polling primitive is defined
  by AAuth `fcf656d`.
- the PS-to-SOGA supervision connection is an implementation choice because
  `fcf656d` leaves the PS-to-supervision-server wire contract open.
- a person token identifies who the agent acts for but proves neither identity
  assurance nor parenthood/legal authority.
- the screen is not evidence of complete AAuth conformance.

No visitor-visible wording change is required by this reconciliation. The
existing global demo claim boundary and spoken explanation must preserve the
distinctions above.

## Stop condition

Stop before launcher creation or execution. This report requires two blind
independent reviews and PI acceptance. It grants no Beryl, listener, QR, iPad,
device, robot, sensor, speech, movement, G28 or G29 authority.
