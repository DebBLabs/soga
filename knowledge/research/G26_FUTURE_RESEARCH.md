# G26 Future Research

Date: 2026-08-14

## FR-G26-01 — Post-grant obligations

Classification: Future Research

Question: How should SOGA represent, enforce, observe, and attribute an
obligation that remains after an AAuth permission has been granted?

G26 does not carry an unenforced residual obligation across the permission
boundary and makes no architectural conclusion about post-grant semantics.
This includes the relationship between `SUPERVISED_EXECUTION` and any durable
post-grant monitoring condition.

Review trigger: G27 entry, or the first running post-grant obligation,
whichever occurs earlier.

## FR-G26-02 — Deferred prerequisite liveness and escalation

Classification: Future Research / open implementation question

Question: Which policy selects the expiry period and escalation behavior for a
pending approval or interaction, and which party has authority to produce each
terminal state?

G26 implements configurable expiry and the AAuth-defined `408 expired` carrier
so pending approval is not immortal. It does not define a caregiver-specific
duration, escalation route, reminder policy, or substitute approver. Those
semantics require additional evidence.

## FR-G26-03 — Mechanism-sensitive validation

Classification: Future Research / standing finding

Finding: a passing end state does not by itself establish that the intended
mechanism produced that state. Multiple green paths have been observed where
adjacent behavior produced the expected result while the named mechanism was
absent.

Question: Which validation pattern should demonstrate causation by a named
governance mechanism across future gates? G26 uses negative controls for absent,
wrong-authority, and wrong-constraint approval evidence as the initial pattern.
