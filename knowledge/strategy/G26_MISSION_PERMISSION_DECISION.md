# G26 Mission Model and Permission Endpoint Decision

Status: AUTHORIZED — Deb, following Claude Stage Gate PASS with the required
amendment incorporated

Date: 2026-08-14

## Decision

SOGA adopts the AAuth mission object natively: `approver`, `agent`,
`approved_at`, `approved_tools`, and `description`, bound by `s256` over its
canonical form and immutable after approval. Mission evolution is represented
only by an append-only mission log. The adapter boundary remains because the
AAuth draft may change and ecosystem neutrality remains required.

The AAuth permission endpoint is the first integration surface. SOGA is the
Person Server's governance policy implementation, not a new protocol party.
Permission evaluation works with or without a mission.

## Vocabulary and projection

SOGA and AAuth name different artifacts:

- A SOGA governance decision is `ALLOW`, `RESTRICT`, or `DENY` and retains its
  dimensions, reason, restriction mode, provenance, and attribution.
- An AAuth permission response is `granted` or `denied`; a pre-decision request
  may instead remain pending through the deferred-response mechanism.

The AAuth projection is intentionally lossy. `granted` does not establish that
the underlying SOGA decision was `ALLOW`: it may follow a `RESTRICT` completely
discharged inside the Person Server. `denied` does not establish that the
underlying SOGA decision was `DENY`: it may be the authorized fallback for a
`RESTRICT` that the current protocol or implementation cannot safely carry.
The mission log therefore preserves the actual SOGA decision and decision
attribution independently of the AAuth response.

## Pre-grant RESTRICT behavior

1. If a restriction can be completely discharged inside the Person Server,
   the resulting action may proceed and the final AAuth response may be
   `granted`. No unenforced residual obligation crosses the boundary.
2. If pre-grant restriction requires agent participation, the decision remains
   pending and uses AAuth deferred response.
3. `clarification` is not assumed to be the normative carrier for arbitrary
   SOGA requirements. Verified evidence defines it as a question posed to the
   agent, not a general structured remediation object.
4. If the current protocol or implementation cannot safely represent the
   required structured interaction, the authorized August fallback is AAuth
   `denied` with its specification-defined Markdown `reason` field.

Deferred-interaction termination is an open implementation question. G26
defines no timeout, expiry, cancellation, or other implicit termination
semantics.

## Authorized correction — HOLDING approval path

The following correction was authorized after primary-source verification and
Stage Gate review on 2026-08-14. It narrows and replaces the G26 implementation
direction above where they conflict; the earlier text remains visible as the
decision chronology.

`HOLDING` and `SUPERVISED_EXECUTION` are distinct operational RESTRICT paths.
`HOLDING` requires human clearance before execution. `SUPERVISED_EXECUTION`
allows execution to proceed under human monitoring without prior clearance;
its relationship to post-grant conditions remains Future Research.

Subject agency state may cause a SOGA dimension to enter `REVIEW` and contribute
to `RESTRICT`, but it does not select an operational path. Authorized
mission/policy constraints select that path. A `RESTRICT` without an authorized
path fails closed: no path is inferred and AAuth `granted` is prohibited.

The canonical caregiver constraint declares `restrict_path=HOLDING`,
`required_evidence=supervisor_confirmation`, and
`authority_reference=authority-caregiver-001`. G26 recognizes authority only
through the Person Server's authenticated assertion that the approval is
attributable to a holder of that referenced authority. It does not resolve the
authority holder or independently authenticate the human approver.

HOLDING uses AAuth `requirement=approval`. Explicit approval records provisional
G26 approval evidence and causes governance to re-evaluate the same mission,
action, and `SUPERVISED` subject state. Only a resulting SOGA `ALLOW` projects
to AAuth `granted`. Explicit decline terminates polling with the AAuth `403`
`denied` error and is not recorded as SOGA `DENY`. Pending approval has a
configurable expiry policy and uses the AAuth `408 expired` terminal response;
G26 defines no caregiver-specific duration or general escalation semantics.

The provisional evidence has an explicit convergence obligation to a future
canonical Stage Gate clearance-evidence schema. G26 does not change
`StageGateEngine` or declare its provisional structure canonical.

The June artifacts contain conflicting combined terminology. They are
preserved and annotated as historical evidence; this decision resolves the
meanings prospectively without asserting an established historical mistake or
silent supersession.

## Neutrality statement

The adopted fields express generic approval provenance, delegate identity,
approval time, approved capabilities, and human intent. Equivalent information
can enter through other delegation substrates. Native shape agreement with
AAuth does not make the governance engine AAuth-specific.

## Boundaries

G26 does not implement a token endpoint, authorization server, federation,
HTTP Message Signatures, live revocation, or expanded agent identity. It does
not solve post-grant obligation semantics.
