# July 16 Office Hours Preparation
## AAuth Office Hours — Dick Hardt
**Date:** July 16, 2026
**Status:** Active — Phase 3 Deliverable
**Owner:** Deb Bucci
**Program:** Pre-July 16 Program v1.0

---

## Context

Dick Hardt is the author of the AAuth Protocol and AAuth Events.
He acknowledged Deb's Slack post in the AAuth channel. In our
earlier discussion he suggested the PS is a natural place for
governance-related functions. He published AAuth Events on
June 26, 2026 — the same day the soga-governance-experiment
branch was forked from christian-posta/aauth-full-demo.

The fork is visible to the community. Christian Posta and Dick
are both aware of the integration work.

The conversation on July 16 starts warm. Credibility is
established. The goal is architectural dialogue, not
introduction or pitch.

---

## Two-Minute SOGA Description

Use this when Dick asks what SOGA is:

AAuth establishes what authority an agent has been delegated.
AAuth Events answers how the agent receives triggers.
SOGA answers whether the agent should act on that trigger now —
given the current state of the subject, the mission context,
and the policy in force at execution time.

We have a working integration on Christian's demo repository.
When an AAuth execution request crosses the boundary, SOGA
evaluates it and produces a Canonical Decision Package —
ALLOW, RESTRICT, or DENY — before the agent executes.

The same request produces different governance outcomes
solely because runtime conditions changed.
The delegated authority does not change. The protocol does
not change. Only the runtime conditions change —
including Subject Agency State.

That is the gap SOGA fills.

---

## Question Set

### Question 1 — Governance placement in AAuth Events

AAuth Events defines how agents receive triggers and leaves
what happens after delivery to the implementation.

When an agent receives an event and is about to act on it,
where does execution-time governance belong in the AAuth flow —
at the AP before delivery, at the agent before action,
or as a distinct governance endpoint the agent consults?

Purpose: Invites Dick to think about where SOGA fits without
requiring us to explain it. His answer will clarify the
integration architecture.

### Question 2 — The PS boundary

In our earlier discussion you suggested the PS is a natural
place for governance-related functions. In the AAuth Events
flow, the PS evaluates the mission and gathers consent.
Is there a natural place in the PS where execution-time
subject state — not just authorization — would be evaluated
before an agent acts on an event?

Purpose: Builds on his prior Slack statement. Shows we
remembered and built on it. Opens the subject state question.

### Question 3 — Delegation chains and events

When an event fires on a subscription established through a
delegated agent, how does the AAuth Events model handle
authority that may have changed between subscription time
and event delivery time?

Does the eid carry enough provenance to reconstruct the
delegation context at execution time?

Purpose: Connects AAuth Events to the delegation chain question
Martin raised. Shows architectural depth without claiming
per-hop governance evaluation exists.

### Question 4 — Mission context locality

Your statement that a mission is agreed-upon context —
not authorization — maps directly onto what we are building.

In AAuth Events, the agent maps eid to mission context locally.
Should that mission context be available to the AP or the PS
during event delivery, or is it intentionally local to the agent?

Purpose: Dick's own framing used back to him. Opens the
mission context question that the RuntimeEnvelope answers.

---

## Discussion Strategy

Lead with the integration, not the architecture.

Say: We have a working integration on Christian's demo.
The governance boundary is live. We can show ALLOW and RESTRICT
from the same request with only runtime conditions changing.

Let Dick ask questions. Do not present SOGA as a system.
Present it as an answer to a question he has already identified.

If Dick asks to see code: point to the soga-governance-experiment
branch. The integration is visible.

If Dick asks about standards trajectory: the RuntimeEnvelope
Specification v0.1 is in the repository. It is
protocol-independent and explicitly incorporates AAuth Events.

If Dick pushes back on governance placement: agree that the
placement question is open and ask where he would put it.
His answer is more valuable than our assertion.

---

## Expected Follow-Up Questions from Dick

### "Where exactly does governance sit?"

Answer: At the execution boundary — immediately before the
agent acts on a delegated request. In our AAuth integration
this is immediately before client.send_message() in the
A2A service. The RuntimeEnvelope is produced at that point
and evaluated before execution proceeds.

### "How does this relate to the PS?"

Answer: The PS evaluates mission and gathers consent.
SOGA evaluates whether the authority established by that
consent remains appropriate at the moment of execution.
They are adjacent, not competing. The PS establishes authority.
SOGA evaluates whether exercising that authority remains
legitimate now.

### "What happens when governance says RESTRICT?"

Answer: Execution enters a holding state. The mission does
not fail. The authority is not rejected. A governed path
forward exists — notification, approval, re-evaluation,
resumption. RESTRICT is a first-class outcome. It is not a
degraded ALLOW.

### "How does this handle delegation chains?"

Answer: The delegation chain arrives as authority evidence.
SOGA performs a single governance evaluation at execution time.
Per-hop governance evaluation is on the roadmap but not yet
implemented. We answered that question honestly in a public
GitHub issue and logged it as B-020.

### "Is this a standards proposal?"

Answer: Not yet. It is a reference implementation and a
specification. The RuntimeEnvelope Specification v0.1
is in the repository. The next step is community validation
before any standards submission.

---

## Standards Positioning

SOGA complements AAuth. It does not replace it.

AAuth establishes delegated authority.
SOGA evaluates whether that authority should be exercised now.

The RuntimeEnvelope Specification v0.1 explicitly positions
SOGA as protocol-independent and AAuth Events-aware.

The three-sentence foundation:

Authentication answers who you are.
Authorization answers what you were permitted to do.
Governance answers whether that authority should still be
exercised now.

AAuth answers the second question.
SOGA answers the third.

---

## What Success Looks Like

Dick engages with the governance placement question seriously.

Dick confirms or refines where SOGA sits relative to the PS
and the AAuth Events delivery flow.

Dick identifies one architectural question we had not considered.

The conversation advances the architecture rather than
validating it.

Dick leaves understanding that SOGA is a complementary
execution-time governance layer rather than an authorization
protocol.

---

## What to Avoid

Do not pitch SOGA as a product.
Do not claim standards readiness.
Do not present SOGA as competing with AAuth.
Do not over-explain. Let Dick ask.
Do not claim per-hop governance evaluation exists.
Do not use PDP/PEP terminology.

---

## Post-Meeting Actions

Record Dick's key observations immediately after the meeting.

Commit observations to:
memory/decisions/2026-07-16-dick-hardt-observations.md

Update:
knowledge/working/CURRENT_STATE.md
project/process-backlog.md

Open Phase 5 — Post July 16 Assessment.

