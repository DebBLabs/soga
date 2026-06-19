
# SOGA (Subject-Oriented Governance Architecture)

SOGA is the governance layer for mission-governed human-agent systems.

The goal is not to replace existing authorization systems or standards. The goal is to make delegation of meaningful work to autonomous agents safe, governed, and trustworthy.

SOGA explores how governance can remain present at the moment of execution — not just at the moment authority is granted.

## The Problem

Authentication answers:

**Who are you?**

Authorization answers:

**What are you allowed to do?**

As software agents become capable of carrying out increasingly meaningful work on behalf of people, organizations, and institutions, a third question becomes important:

**Should this still be allowed now?**

Most authorization systems evaluate authority when it is granted. They do not continuously evaluate whether exercising that authority remains legitimate as conditions change.

Human circumstances change. Missions evolve. New information appears. Reachability changes. Governance conditions change.

A delegation that was appropriate yesterday may not be appropriate today.

SOGA exists to explore how systems can evaluate legitimacy at the moment of execution rather than relying solely on decisions made earlier in time.

## Core Idea

SOGA introduces execution-time governance.

Rather than treating delegated authority as permanently valid until expiration, SOGA evaluates whether a requested action remains appropriate when execution is about to occur.

The architecture is based on a simple principle:

> Delegation is evidence. Execution requires governance.

Authority can be carried through many different delegation systems and protocols. SOGA focuses on the governance decision that occurs when an action is requested.

SOGA does not judge whether an agent is allowed to exist; it gates specific, requested execution events.

## Architectural Direction

SOGA is designed to operate independently of any particular delegation mechanism.

Current exploration includes examples built around delegation and capability systems such as AAuth, UCAN, and ZCAP, but the governance model is intended to remain protocol-independent.

The architecture explores how information about mission, authority, subject state, reachability, execution context, and policy can be evaluated together at execution time.

The objective is not to replace existing authorization infrastructure.

The objective is to complement it.

Authorization determines what authority has been delegated.

Governance determines whether exercising that authority remains legitimate now.

## Current Scope

SOGA is an active open-source exploration.

The project focuses on:

- Execution-time governance

- Delegated authority

- Mission-oriented work

- Human oversight and accountability

- Runtime legitimacy evaluation

The project does not attempt to solve every aspect of agent behavior, alignment, safety, or trust.

Its focus is narrower:

How can systems determine whether delegated authority should still be exercised at the moment an action is requested?

## Why This Matters

As agents move from answering questions to performing actions, governance becomes increasingly important.

Systems will need mechanisms that can evaluate changing human circumstances, evolving missions, and execution context before meaningful actions occur.

SOGA explores one possible approach to that problem.

The goal is not to eliminate autonomy.

The goal is to ensure that autonomy remains governed.

## Status

SOGA is an open-source research and implementation effort under active exploration.

The project welcomes discussion, critique, experimentation, and collaboration from practitioners working in governance, authorization, delegation, identity, security, and human-agent systems.

