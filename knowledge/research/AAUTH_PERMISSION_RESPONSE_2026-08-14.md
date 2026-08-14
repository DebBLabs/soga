# AAuth Permission Endpoint Response — Primary-Source Verification

Date: 2026-08-14
Gate/Task: G26 — primary-source verification (inspection only; no architecture,
code, or strategy/working file changes made)
Checkpoint at time of research: main @ e00beabf7b503d6c7150058ad996bc7bfeeecdb1

---

## Correction annotation — 2026-08-14

Status: architectural correction authorized after Stage Gate review. The
original search log, findings, and conclusion remain below as research-history
evidence.

The absence finding in this artifact is valid only for a terminal permission
response with `permission: denied`: revision `-10` defines no structured
remediation field on that response beyond the optional Markdown `reason`.
That true terminal-response finding was incorrectly generalized to the
permission flow as a whole.

AAuth `-10` already defines deferred prerequisite mechanisms that may operate
before a terminal permission decision:

- `requirement=approval`: another party's approval is pending; the agent polls
  for the result without directing a user.
- `requirement=interaction`: a user must act at an interaction endpoint; the
  agent receives and relays the required interaction URL and code.
- `requirement=clarification`: the recipient must answer a question carried in
  the `clarification` response field.
- `requirement=claims`: identity claims are required; in `-10` this is an
  AS-to-PS mechanism during token issuance.
- `updated_request`: not a requirement value, but an action available in
  response to clarification. The defined shape carries a replacement resource
  token and optional justification; `-10` does not define an equivalent
  resource-token-free reformulation body specifically for the permission
  endpoint.

The initial search began with SOGA vocabulary such as `restriction`,
`constraint`, `remediation`, and `obligation`. Those searches correctly found
no corresponding fields on the terminal denied response, but they did not by
themselves test the draft's own prerequisite vocabulary and interaction model.
The later searches for `requirement`, `clarification`, and `updated_request`
show that the permission flow has structured deferred mechanisms even though
the terminal denied object has no structured remediation carrier.

Accordingly, the statements in F6 and the original conclusion that the
registered requirement values do not define a reformulation or prerequisite
path are corrected by this annotation. They remain below to preserve the
chronology of the research finding and its subsequent narrowing.

### G26 implementation application — 2026-08-14

The canonical caregiver `HOLDING` prerequisite uses the verified approval
shape: HTTP `202`, `AAuth-Requirement: requirement=approval`, same-origin
unguessable `Location`, `Retry-After`, `Cache-Control: no-store`, and polling.
Explicit approver decline uses the polling `403 denied` error; configured
expiry uses `408 expired`; a terminal result is delivered once and subsequent
polls return `410`. Approval triggers governance re-evaluation and does not
itself mean AAuth `granted`.

The implementation deliberately does not assign `SUPERVISED_EXECUTION` to this
pre-grant flow. It records temporary approval material as provisional G26
evidence with an explicit convergence obligation rather than treating it as a
canonical Stage Gate clearance schema.

---

## 1. Source

Primary source read directly: **`draft-hardt-oauth-aauth-protocol-10.txt`**
(Internet-Draft, "AAuth Protocol", D. Hardt, Hellō)

- Retrieval URL: `https://www.ietf.org/archive/id/draft-hardt-oauth-aauth-protocol-10.txt`
- Revision: `-10`
- Document date (from document header): 6 August 2026
- Expires: 7 February 2027
- Retrieved: 2026-08-14, via direct `curl` fetch of the plain-text archive copy
  to local disk, followed by direct `grep`/`Read` inspection of the raw file.
  Saved locally at
  `/private/tmp/claude-501/-Users-debb-dev-soga-clean/548c9272-4c90-4ac5-82b5-0cae21a7f1b2/scratchpad/draft-hardt-oauth-aauth-protocol-10.txt`
  (scratch copy, not committed to the repository).

**Explicit statement:** The primary source was read directly and recently
(same session, 2026-08-14). No local copy of the draft existed anywhere in
`/Users/debb/dev/soga-clean` or elsewhere on disk prior to this retrieval —
only implementation repositories (`external-repos/aauth-full-demo`,
`external-repos/aauth-person-server`, `external-repos/extauth-aauth-resource`)
and a citation to the draft in `knowledge/research/AAUTH_FINDINGS_2026-08-05.md`
(a prior findings file, not consulted as a source for this task per the task's
instruction to answer only from the primary source).

An initial `WebFetch` call against the datatracker HTML page and against the
raw `.txt` URL returned AI-summarized prose rather than verbatim text; that
summarized output was **discarded** and is not used anywhere below. All
quotations in this report come from the raw `curl`-downloaded plain text,
located by line number with `grep -n` and read verbatim with the file-read tool.

No cloned copy of the companion specifications
(`I-D.hardt-httpbis-signature-key`, `I-D.hardt-aauth-bootstrap`,
`I-D.hardt-aauth-events`, `I-D.hardt-aauth-r3`) was found locally or fetched;
per RM-01 clause 3 these were checked only for whether the main draft *defers*
permission-response content to them (see §4). Their own text was not read.

---

## 2. Question

> Beyond the two-valued granted/refused result, what may a permission endpoint
> response carry? Does the draft define a response object, error structure,
> challenge, problem-details format, restriction or remediation field, or an
> extension point that would let a refusal communicate what would make a
> subsequent request grantable?

---

## 3. Search Log

All searches run with `grep -ic -- "<term>"` against the full raw text
(8008 lines) unless noted otherwise.

| Term (as run) | Hits |
|---|---|
| `permission endpoint` | 9 |
| `permission request` | 5 |
| `permission response` | 2 |
| `granted` | 5 |
| `refused` | 0 |
| `denied` | 11 |
| `error` | 85 |
| `error_description` | 1 |
| `challenge` | 14 |
| `step-up` | 3 |
| `insufficient` | 2 |
| `remediation` | 0 |
| `restriction` | 2 |
| `constraint` | 2 |
| `obligation` | 0 |
| `retry` | 25 |
| `extension` | 23 |
| `additional information` | 0 |

Extended searches, using the draft's own vocabulary discovered while reading
Section 7.4 and its neighbors:

| Term (as run) | Hits |
|---|---|
| `reason` | 3 (one is the `reason` field in the permission response itself; the other two are unrelated prose — "reasonable," "reasons they cannot") |
| `clarification` | 47 (Section 7.3 "Clarification Chat" and its many cross-references) |
| `requirement` (as part of `AAuth-Requirement` / `requirement=`) | inspected directly via section reads, not bulk-counted |
| `problem+json` / `RFC9457` / "problem details" | inspected directly via Section 12.6.2 |
| `IANA` / `registry` | inspected directly via Section 16 headers |
| `I-D.hardt` (companion-spec citations) | inspected directly; none fall within Section 7.4 (lines 2272–2367) or Section 8.6 (lines 2888–2926) |

---

## 4. RM-01 Clause 3 Check — Deferral to a Companion Specification

Before recording any absence, checked whether structured refusal/remediation
content for the permission response is deferred elsewhere in the same
document or to a named companion specification.

- Within Section 7.4 (Permission Endpoint, lines 2272–2367) and Section 8.6
  (Mission Status Errors, lines 2888–2926): no citation to
  `I-D.hardt-httpbis-signature-key`, `I-D.hardt-aauth-bootstrap`,
  `I-D.hardt-aauth-events`, or `I-D.hardt-aauth-r3` appears in or adjacent to
  either section. Confirmed by `grep -n "I-D\.hardt"` across the full file and
  manually checking that no hit falls in the 2272–2367 or 2888–2926 line
  ranges.
- The permission response (Section 7.4.2) instead cross-references two
  sections *within the same document*: Section 8.6 (mission status error) and
  Section 12.5 (Deferred Responses). Both were read directly (quoted below).
  This is not a deferral to a companion specification — it is an in-document
  cross-reference, so RM-01 clause 3's "check elsewhere in the same document"
  branch applies, not the companion-specification branch.
- Conclusion: no companion specification was found to govern permission-response
  refusal content, and none needed to be checked externally, because the
  cross-references resolve within the draft itself.

---

## 5. Findings

### F1 — Verified: The `permission` field is two-valued, using `granted`/`denied`, not `granted`/`refused`

Section 7.4.2, quoted verbatim:

> "The permission field is one of:
>
> *  granted: The agent MAY proceed with the action.
> *  denied: The agent MUST NOT proceed.  The response MAY include a
>    reason field with a Markdown string explaining why."

(lines 2343–2347)

The draft's own vocabulary is `granted` / `denied`. `refused` does not occur
anywhere in the document (0 hits).

### F2 — Verified: On denial, the only defined additional content is an optional, unstructured `reason` string

Same citation as F1. The `reason` field is explicitly typed as "a Markdown
string explaining why" — free text for explanation, not a structured field,
and its stated purpose is to explain the denial, not to specify what change
would make a subsequent request succeed. No schema, enum, or sub-object is
defined for `reason`.

### F3 — Verified: A structurally distinct error path exists for mission-status failures, but it is not part of the granted/denied response and does not carry remediation content beyond a fixed code

Section 7.4.2 continues:

> "If the mission is no longer active, the PS returns a mission status
> error Section 8.6."
> (line 2357–2358)

Section 8.6, quoted verbatim:

> "When an agent makes a request to any PS endpoint with a mission
> parameter referencing a mission that is no longer active, the PS MUST
> return an error:
>
> HTTP/1.1 403 Forbidden
> Content-Type: application/problem+json
>
> {
>   "error": "mission_terminated",
>   "mission_status": "terminated"
> }"
> (lines 2890–2900)

Table 6 (lines 2917–2926) defines exactly one row: `mission_terminated` /
`terminated` / "The mission is permanently ended. The agent MUST stop acting
on this mission." This is a fixed, closed enumeration — not an open
restriction or remediation field, and it addresses mission lifecycle state,
not the substance of why a specific action was denied.

### F4 — Verified: The general AAuth error-response format (RFC 9457 problem+json) applies to protocol errors, not to permission denials, and its extensible members are unstructured

Section 12.6.2, quoted verbatim:

> "Error response bodies use the HTTP problem details format ([RFC9457])
> with Content-Type: application/problem+json.  The body is a JSON
> object with the following members:
>
> *  error (REQUIRED): String.  A single error code, as defined by the
>    endpoint returning the error.  This is an RFC 9457 extension
>    member; receivers MUST determine how to proceed from this member.
> *  detail (OPTIONAL): String.  A human-readable explanation specific
>    to this occurrence of the error.
>
> Other RFC 9457 members (type, title, status, instance) MAY be present
> with their RFC 9457 semantics.  AAuth does not define problem type
> URIs; receivers MUST NOT rely on type to identify AAuth errors."
> (lines 4752–4773)

This format is not the format used by a `denied` permission response — that
response is `200 OK` with `Content-Type: application/json` and the
two-field `permission`/`reason` body (F1–F2), not `403`/`application/problem+json`.
The problem+json format governs a different category (malformed requests,
auth failures, expired tokens, mission-status errors), and even there its
only free members are `error` (a code) and `detail` (free text) — no
structured restriction, remediation, or constraint member is defined.

### F5 — Verified (RM-01 absence): No `restriction`, `constraint`, `remediation`, or `obligation` field is defined anywhere in the document

Search counts: `remediation` = 0, `obligation` = 0. `restriction` appears
twice, neither as a field name: once in the boilerplate IETF Trust legal
notice (line 72, "rights and restrictions with respect to this document"),
and once in a non-normative rationale appendix:

> "The mission's description is Markdown because it represents human
> intent, not machine policy. ... The mission is a further restriction
> applied by the PS, and only the PS has sufficient context to evaluate
> it."
> (lines 7720–7734, Appendix B.3, "Why Missions Have Only Two States" /
> preceding rationale — non-normative, discussing why mission semantics
> stay at the PS rather than propagate to resources; not a response field)

`constraint` appears twice, both in non-normative rationale prose (lines
3660, 7763), not as a defined field or mechanism. Neither term names any
element of the permission response object.

### F6 — Original finding; narrowed by the correction annotation above

A general, named extension point exists in the protocol
(`AAuth-Requirement` / `requirement` value), and one of its registered values
(`clarification`) allows a question to flow to the agent pre-decision. The
original text below incorrectly treated this as the only relevant deferred
mechanism and did not account for `updated_request` as a clarification response
action or for the distinct approval, interaction, and claims prerequisites.

Section 12.4.2, quoted verbatim:

> "The requirement value is an extension point.  This document defines
> the following values:"
> (lines 4272–4275)

The requirement-value table (Table 8, lines 4317–4348) includes, among
others:

> "| clarification | 202 | Question posed to the recipient | Y | Y | Y |"
> (lines 4340–4342; the three Y columns are headed Resource / PS / AS,
> lines 4317–4320 — the PS column is marked Y, meaning the PS may issue
> this requirement)

This mechanism is generic across "any endpoint in AAuth":

> "Any endpoint in AAuth — whether a PS token endpoint, AS token
> endpoint, or resource endpoint — MAY return a 202 Accepted response
> ([RFC9110]) when it cannot immediately resolve a request.  This is a
> first-class protocol primitive, not a special case."
> (lines 4599–4604, Section 12.5)

The permission response itself (Section 7.4.2) cross-references this
generic mechanism rather than the requirement-value table directly:

> "If the PS requires user input, it returns a deferred response
> Section 12.5 using the same pattern as other AAuth endpoints.  The
> agent polls until the PS returns a final response."
> (lines 2360–2362)

Section 12.5.2 ties the deferred-response body shape back to the
requirement-value mechanism:

> "Additional body fields may be present depending on the AAuth-
> Requirement value — for example, clarification and timeout with
> requirement=clarification, or required_claims with
> requirement=claims.  See the specific requirement definitions for
> details."
> (lines 4666–4670)

**Boundary of what is verified vs. inferred:** the text verifiably (a) names
`requirement` an extension point, (b) lists `clarification` as a PS-issuable
value carrying a Markdown question to the recipient, and (c) has the
permission endpoint explicitly invoke "the same pattern as other AAuth
endpoints" for its 202/deferred path. It does **not** explicitly state, in
Section 7.4 or elsewhere, "the permission endpoint supports
requirement=clarification" by name — that specific instantiation is an
inference from the generic cross-reference, not a direct statement, and is
recorded here as an inference rather than a verified fact per RM-02.

Separately — and this bears directly on the question asked — `clarification`
is defined as the PS posing "a question ... to the agent" (Section 7.3,
line 593: "*Clarification*: A Markdown string containing a question posed to
the agent"), i.e., the PS asks the agent something. It is not defined as the
PS telling the agent what would make a denied request grantable. Even where
this extension point is reachable, its defined content is a question, not
remediation guidance.

---

## 6. Conclusion

**Historical conclusion — narrowed and corrected by the annotation at the top
of this artifact.** The statements below remain unchanged as the original
research record; they must not be read as applying to the entire deferred
permission flow.

**An extension point exists whose content is undefined for the specific
question asked.**

The permission response object itself (Section 7.4.2) is closed and fully
specified: `permission` (`granted`/`denied`) plus an optional, unstructured
`reason` string on denial. No restriction, remediation, constraint, or
obligation field is defined anywhere in the document (F5, RM-01 absence,
search-confirmed). The adjacent error path for inactive missions (Section 8.6)
and the general AAuth error format (Section 12.6.2) are both closed
enumerations or free-text fields, not structured remediation carriers (F3,
F4).

The one genuine, self-described extension point in the protocol — the
`requirement` value on `AAuth-Requirement` (Section 12.4.2, explicitly "an
extension point," with an IANA registry at Section 16.7) — is generically
reachable from the permission endpoint's deferred-response path (F6), but its
currently-registered values do not define "what would make a subsequent
request grantable" as content. Its `clarification` value defines only a
question posed *to* the agent, and this path is pre-decision (202
pending/deferred), not a payload attached to a `denied` outcome. Whether a
future or private registry value under this extension point could carry
remediation content is not addressed by the draft; that would be a matter for
a new registered `requirement` value, undefined at revision -10.
