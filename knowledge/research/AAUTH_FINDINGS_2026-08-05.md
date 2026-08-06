# AAuth Findings — 2026-08-05

Source: `draft-hardt-oauth-aauth-protocol.md`, repo `main`, retrieved 2026-08-05.
Line references are to the repository markdown, NOT rendered draft section
numbers (G23).

## Verified

- Missions are approved up front by a person, then immutable and bound by
  `s256`. They evolve only through the mission log. (401)
- Missions have no step structure. Review occurs once, at approval.
  Clarification chat is pre-approval, during consent. (401, 979)
- `approved_tools` entries carry only `name` and `description`. No conditions,
  no flags. Omission from the list is the only routing control. (1090, 1391)
- Governance is not mission-scoped. Permission and interaction endpoints work
  with or without a mission; only audit requires one. (469, 1088, 1152, 1206)
- Governance is not centralizable. Four server roles each evaluate from their
  own vantage, in their own scope, for their own principal. No single party is
  the policy decision point. (386-392)
- Mission revocation is specified: PS marks the mission revoked, denies
  subsequent requests against that `s256`, and revokes outstanding auth tokens
  at the resource regardless of issuer. (2315, 2320)
- Token lifetimes: auth tokens MUST NOT exceed 1 hour; resource tokens SHOULD
  NOT exceed 5 minutes. Each issuance is a re-evaluation point. (393, 813, 1674)
- The AS is present in only one of four access modes. Roles may collapse into a
  single deployment. (214, 374, 378)
- The PS decides using consent plus, under a mission, mission intent and prior
  log entries against the PS's governance policy. That policy is named and left
  unspecified. (389, 3260)
- Mission description is Markdown because it represents human intent, not
  machine policy; `approved_tools` supplies the structured elements. (3262)

## Hypothesis

- The GS occupies the tier between `approved_tools` and interaction: on-list
  bypasses governance, off-list routes to the GS, user interaction is the
  fallback when the GS cannot decide. Basis: one sentence of Dick Hardt's
  written reply. Not confirmed by him.
- Actions that commit the person are the class requiring runtime evaluation.
  This is our judgment. The spec does not rank actions by consequence.

## Corrected

- Prior framing that a Governance Server attaches somewhere in the AAuth flow
  is superseded. SOGA is the implementation of the PS's governance policy. It is
  an engine, not a protocol party.
- Prior assumption that governance was mission-scoped is withdrawn.
- Line 1417 defers mission administrative lifecycle to a companion spec. It does
  NOT mean revocation is unspecified. These were conflated.
