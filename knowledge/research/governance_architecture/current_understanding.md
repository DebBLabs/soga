# AAuth Governance Alignment Notes

Status: Working Research
Author: Deborah Bucci
Last Updated: 2026-07-09

---

# Purpose

This document captures the ongoing architectural analysis comparing the emerging
AAuth Governance Agent model with the SOGA Governance Server architecture.

The goal is to distinguish verified specification behavior from hypotheses and
open architectural questions before proposing implementation approaches.

No assumptions should be treated as architectural truth until verified against
the current AAuth specification or clarified by the editors.

---

# Verified (Current Draft)

- AAuth has a mission concept.
- AAuth defines an interaction mechanism (`requirement=interaction`).
- Governance policy authoring is outside the protocol.
- Dick's current conceptual model describes a Governance Agent that evaluates:
  - mission
  - mission history
  - resource token / R3
  - agent justification
  - Person Server policies

---

# Likely (Requires Confirmation)

- Mission proposal may begin as natural language.
- The Governance Agent could be implemented in multiple ways (human, LLM,
  rules engine, hybrid reasoning, etc.).
- The Governance Agent (reasoning capability) and the SOGA Governance Server
  (governance infrastructure) may be complementary rather than competing
  concepts.

---

# Open Questions

1. Is the Governance Agent a logical role or an implementation?

2. Can the Person Server consult an external Governance Server?

3. What triggers the Person Server to invoke the Governance Agent?

4. How does the Governance Agent obtain all required governance context?

5. Does all governance context naturally flow through the Person Server?

6. Is the Person Server intended to represent the subject across multiple
   resources?

7. Does AAuth define mission decomposition?

8. Does AAuth define consequential actions?

9. If governance is provided outside the Person Server, is there an intended
   interface or invocation point between the Person Server and an external
   Governance Agent / Governance Server?

---

# Working Rule

Investigate first.

Hypothesize second.

Propose last.

Every architectural question should first be checked against the current
specification before treating it as an open design question.

