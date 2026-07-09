# Dick Hardt 1:1 Meeting Agenda

Status: Working Discussion Agenda
Date: 2026-07-10

---

# Purpose

The purpose of this meeting is to understand Dick's current architectural
thinking around the AAuth Governance Agent so the SOGA reference
implementation can align with AAuth without making assumptions about the
protocol.

This is an architectural discussion, not a proposal review.

---

# Primary Objectives

1. Understand Dick's Governance Agent concept.

2. Validate our understanding of the current AAuth architecture.

3. Separate what is defined by the specification from implementation choices.

4. Determine how the SOGA Governance Server relates to the Governance Agent
   described in AAuth.

---

# Discussion Flow (30 Minutes)

## 1. Context (3–5 minutes)

Brief background.

- My work has centered on delegated authority.
- Building the SOGA reference implementation led naturally to execution-time
  governance.
- Reading the latest AAuth draft raised architectural questions that I don't
  want to answer through assumptions.

The goal is understanding.

---

## 2. Terminology Alignment (5 minutes)

Confirm terminology before discussing architecture.

Current working understanding:

Governance Server
    = our infrastructure for evidence evaluation, policy, audit, and
      reasoning services

Mission Builder
    = upstream system that creates structured mission intent

Open question for Dick: you've described a Governance Agent performing
non-deterministic reasoning. Is that a logical role or a specific
implementation choice? We're trying to understand whether "Governance Agent"
in your model maps to something inside our Governance Server, or is a
distinct concept.

---

## 3. Walk Dick's Architecture (10 minutes)

Use Dick's email as the starting point.

Current understanding:

Resource
    ↓
Resource Token / R3
    ↓
Person Server
    ↓
Governance Agent

Reviews:

- mission
- mission history
- resource token / R3
- agent justification
- clarifications
- Person Server policies

    ↓

Authorization issued
(by PS or Resource AS)

Primary request:

"Can you walk me through how you envision this flow?"

Listen first.

Avoid presenting our interpretation.

---

## 4. Architectural Questions (10 minutes)

Discuss only questions that remain open after reading the specification.

Primary questions:

1.

Is the Governance Agent a logical architectural role or simply an
implementation?

2.

How does the Governance Agent obtain all required governance context?

3.

What causes the Person Server to invoke the Governance Agent?

4.

If governance were implemented outside the Person Server,
does AAuth envision an interface between the Person Server and an external
Governance Agent / Governance Server,
or is the Governance Agent expected to remain internal to the Person Server?

Secondary questions if time permits:

- Scope of the Person Server
- Mission ownership
- Mission decomposition
- Consequential actions
- Interaction flow

---

## 5. Reference Implementation Context (5 minutes)

Provide only enough context to explain why these questions arose.

The reference implementation exists to explore governance concepts,
not to prescribe an AAuth implementation.

Current implementation:

Intent
    ↓
Mission Builder
    ↓
Agent
    ↓
Governance Server
    ↓
ALLOW / RESTRICT / DENY
    ↓
Execution

Explain only:

- Governance Server = platform/infrastructure.
- Governance Agent = reasoning capability hosted by that platform.

Do not attempt to explain the complete SOGA architecture.

The purpose is simply to understand whether Dick's Governance Agent and the
SOGA Governance Server naturally complement one another.

---

# Discussion Posture

Research first.

Understand first.

Do not assume.

Do not defend architecture.

Do not propose protocol changes.

Allow Dick's explanations to guide the discussion.

---

# Expected Outcome

Leave with:

- Better understanding of the Governance Agent.
- Better understanding of Person Server responsibilities.
- Better understanding of governance placement.
- Clearer understanding of where implementation begins beyond the AAuth
  specification.
- A refined set of questions for the broader Office Hours discussion.

