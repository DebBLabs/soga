# DECISION LOG
## Deb B Labs Embodied Governance Research Program

Status: DRAFT v0.1 — decisions below are PROPOSED until the G0
initialization commit; the PI's commit is the act of adoption.
Precedence: subordinate to `knowledge/working/CURRENT_STATE.md`

Format: ID — Date — Decision — Rationale (brief) — Status

---

- **D-001** — 2026-07-20 — Adopt the research-question sprint model:
  sprints produce verified evidence, architectural clarification,
  measured implementation, or research artifacts — not merely code —
  Completes the intent of G23 and the repository methodology —
  PROPOSED.

- **D-002** — 2026-07-20 — Introduce Initialization Sprint G0,
  separating program initialization from research synchronization
  (G24) — The two have different failure modes; separation makes each
  sprint's exit binary — PROPOSED.

- **D-003** — 2026-07-20 — Separate the program into three layers:
  program governance (continuous), program tracks (continuous),
  research sprints (time-boxed); establish five continuous tracks with
  registers in TRACKS.md — Standards participation and funding are
  ongoing commitments, not milestones — PROPOSED.

- **D-004** — 2026-07-20 — Adopt the merged G24–G30 sequence from the
  three-agent review, including: G25→G26→G27 dependency chain; G27
  owns the A/B state-isolation specification and bystander threat-model
  extension; G28 entry requires the G27 isolation spec; G29 precedes
  any public demonstration — Evidence-driven ordering per
  RESEARCH_METHODOLOGY.md — PROPOSED.

- **D-005** — 2026-07-20 — Mission terminology: retain "Mission"
  pending G26; G26 evaluates a minimum of three candidate models on
  evidence, with switching costs as legitimate criteria; the layered
  hierarchy is a candidate, not the assumed answer — Prevents
  confirmation bias; protects the AAuth interoperability asset —
  PROPOSED.

- **D-006** — 2026-07-20 — Misty platform roles: Misty B (new unit,
  advanced perception) is the higher-capability embodied research
  platform; Misty A is the stable comparative baseline and
  lower-capability control — Two-point test of capability-relative
  governance (H3) — PROPOSED.

- **D-007** — 2026-07-20 — Document precedence: CURRENT_STATE.md
  remains the sole synchronization contract; all strategy artifacts are
  subordinate and referenced; the charter cites
  docs/RESEARCH_METHODOLOGY.md rather than restating it — Prevents
  parallel sources of truth — PROPOSED.

- **D-008** — 2026-07-20 — Authority model: PI holds singular editorial
  and decision authority; agent gate verification (Gate 1: Claude) is
  advisory pass/fail with findings; sprint activation is authorized by
  the PI — Consistent with the established repository operating model —
  PROPOSED.

- **D-009** — 2026-07-20 — Fellowship relationship: fellowships fund
  and accelerate the charter's plan; the charter remains the source of
  truth; no funded opportunity redefines the program — Protects
  long-term direction — PROPOSED.

- **D-010** — 2026-07-20 — Tooling/subscription review established as a
  standing quarterly governance item under the Funding & Partnerships
  Track; no cancellation decisions made today — Portfolio review
  follows demonstrated need, not anticipation — PROPOSED.

- **D-011** — 2026-07-20 — Defer
  `knowledge/working/deferred/live_governance_workbench.py` as an
  unadopted exploratory artifact pending conceptual clarification and
  discussion with Dick Hardt. It is not part of the canonical runtime,
  is not authorized for execution or further development, and creates
  no architectural commitment — Preserves incomplete exploratory work
  without treating it as active implementation or concealing it as
  ignored local drift — DEFERRED.

- **D-012** — 2026-07-20 — Adopt pre-commit editorial findings from
  cross-agent review: (a) Outreach Track renamed Living Laboratory &
  Outreach Track — research in human environments, with outreach as
  one activity within it; (b) charter sentence added: standards
  participation informs but does not determine the research agenda;
  (c) optional Outcome field added to track registers; (d) subscription
  review confirmed as standing governance, not procurement —
  Refinements only; no architectural change — PROPOSED.

## D-011 — RESOLVED 2026-08-05
Conceptual clarification obtained via written exchange with Dick Hardt.
Governance is not a single function requiring an attachment point; SOGA is the
PS's governance policy. G0 exit unblocked.

## D-013 — Adopt AAuth mission structure natively
Adopt the AAuth mission object rather than translating into it. Requires a G19
neutrality statement: the fields are generic and map to other substrates.
Retain the adapter boundary despite shape agreement — the draft will move.

## D-014 — Permission endpoint is the first integration surface
Chosen over the token endpoint. Works with or without a mission, requires no
resource or AS participation, and carries the residual decisions that fall
outside `approved_tools`.

## D-015 — AuthZen MCP hook deferred
Extension approval requires a dedicated working group and a vote of all nine
core maintainers. Not an IIW-timeframe deliverable.

## D-016 — PECOSE dropped
Requires letters from five people working on the open source tool. Not
satisfiable this round.

## D-017 — Close G0, G24, and G25
G0 deliverables complete; Gate 1 verified 2026-08-06. G24 satisfied: PIC
resolved, office-hour reconciliation superseded by Dick Hardt's written
answers, research notes synchronized. G25 satisfied for the specification half;
connector and repository inspection carried forward into G26 rather than
deferred.

## D-018 — Activate G26, rescoped
G26 rescoped to mission model plus permission endpoint implementation. The
mission model ADR is narrower than originally planned: two of three candidate
models are eliminated by the specification. The permission endpoint work is
added because it is the first integration surface (D-014) and because an
external commitment exists to Dick Hardt for end of August. This resolves the
roadmap conflict recorded 2026-08-05.

## D-019 — Implement the reviewed G26 mission and permission decision

Authorized by Deb following Claude Stage Gate PASS with the required amendment
incorporated. Adopt the immutable native AAuth mission shape and append-only
mission log; project SOGA `ALLOW` to AAuth `granted` and SOGA `DENY` to AAuth
`denied`. A completely internally discharged pre-grant `RESTRICT` may
ultimately project to `granted`; agent-participation `RESTRICT` remains pending
through AAuth deferred response. If required structured interaction cannot be
represented safely, use the August fallback of AAuth `denied` plus its
specification-defined `reason`. Preserve the underlying SOGA decision and
attribution separately because AAuth `granted`/`denied` cannot reconstruct it.
Do not assign arbitrary SOGA requirements to `clarification`, invent deferred
termination semantics, or solve post-grant obligations. Full rationale and
boundaries: `knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md`.

## D-020 — Resolve G26 pre-grant RESTRICT path semantics

Authorized after Stage Gate review on 2026-08-14. Going forward, `HOLDING`
means that nothing executes until human clearance; `SUPERVISED_EXECUTION`
means execution proceeds under human monitoring without prior clearance.
Subject agency state may contribute to `RESTRICT` but does not select its
operational path. An authorized mission/policy constraint selects the path;
absence of such a declaration fails closed. The canonical caregiver constraint
selects `HOLDING`, requires `supervisor_confirmation`, and references
`authority-caregiver-001`. AAuth `requirement=approval` carries the deferred
prerequisite. Approval evidence causes governance re-evaluation with the same
mission, action, and `SUPERVISED` subject; approval alone never implies
`granted`. Earlier combined terminology remains historical evidence and is
resolved prospectively, not characterized as an established historical error
or supersession. Full semantics and boundaries are recorded in
`knowledge/strategy/G26_MISSION_PERMISSION_DECISION.md`.

## D-021 — Resolve B-035 at the evidence-schema boundary

PI disposition accepted on 2026-08-16. B-035 resolves as a schema-level
convergence obligation; no mechanism-level relationship is required or
established between StageGateEngine and G26. StageGateEngine operates on a
mission-execution step in the older step-bearing model. G26 operates on a
permission request/action under the native immutable, step-free AAuth mission
adopted by D-013. The repository binds G26 provisional approval evidence to a
future canonical Stage Gate clearance-evidence schema, not to StageGateEngine
itself.

Future schema convergence must preserve the assurance and binding properties
established by G26 and must not weaken D-019, D-020, or the recorded G26 trust
boundary. Mechanism-level convergence, replacement, or coexistence is neither
required nor established. The future disposition of StageGateEngine is deferred
to Gate 1b, where the continuing role of the older step-bearing governed-mission
model will be evaluated. This decision authorizes no runtime change, defect
repair, or Gate 1b work.
