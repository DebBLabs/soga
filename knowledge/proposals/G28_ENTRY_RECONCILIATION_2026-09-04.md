# G28 Entry Reconciliation — Review Proposal

Date: 2026-09-04  
Status: PROPOSED — G28 remains inactive  
Requested disposition: Independent Gate 1 and Gate 2 review, then explicit PI
decision

## Purpose

Resolve the recorded G28 identity and entry discrepancy before Mission
Formation is treated as an activated sprint and before any implementation or
physical connection begins.

## Verified current state

- `knowledge/working/CURRENT_STATE.md` states that G28 is not activated and may
  be activated only through a new explicit PI decision.
- `knowledge/strategy/SPRINT_ROADMAP_G0_G30.md` names G28 `Governed Misty B
  Runtime Prototype` and assigns Misty A the comparative-control role.
- G27 closure authorizes no Misty power, connection, discovery, query, hardware
  adapter, external-network access, actuation, or public demonstration.
- G27's physical-safety, isolation, network, target-binding, cardinality, and
  truthful-outcome requirements remain authoritative.

## Proposed entry disposition

Authorize Mission Formation for a bounded Misty A G28 candidate mission because
Misty A is the unit available for the planned controlled work. Use the native
AAuth Mission object and mission log as the authoritative executable-mission
representation. A human-readable mission specification may explain boundaries,
risks, allowed actions, prohibitions, and acceptance criteria, but may not become
a competing mission type.

This proposal does not silently rewrite the roadmap. Gate 1 and Gate 2 must
determine whether using Misty A is:

1. a bounded G28 rescope requiring an explicit roadmap/decision update;
2. a separately named precursor mission; or
3. inconsistent with G28's existing purpose and therefore not ready to proceed.

## Inherited boundaries

- No implementation begins before Deb authorizes the completed mission.
- No Misty power, network connection, discovery, status query, or actuation is
  authorized by this proposal.
- Physical safety remains an independent local boundary and is not replaced by
  governance ALLOW or Deb's project authorization.
- The execution target must be canonical, explicit, allowlisted, and rechecked
  at the final adapter before dispatch. No address-derived or fallback target is
  permitted.
- Permission, dispatch, physical start, completion, interruption, and neutral
  outcome remain distinct claims and receipt events.
- HTTP success is not evidence of physical completion.
- Physical completion remains unknown unless independently observed and bound
  to the request. For the first controlled run, Deb may serve as the recorded
  human observation source; that observation must not be converted into an
  automated-observation claim.
- The finite action catalog and per-action/session cardinality must be specified
  and enforced before physical authorization.
- Network-loss, late-ALLOW, replay, wrong-target, timeout, and safety-halt cases
  must fail safely and must not resume an old action automatically.

## Existing roles retained

- Claude: constitutional Gate 1 architectural-conformance review.
- Gemini/AGy: constitutional Gate 2 coherence and demonstration-readiness
  review.
- Codex/CG: implementation and evidence preparation after authorization.
- Deb: sole sprint-activation, architectural, mission, physical-execution, and
  acceptance authority.

Human decisions should be called `Mission Authorization`, `Physical Execution
Authorization`, and `Mission Acceptance`. They do not rename or replace the
constitutional Gate 1 and Gate 2.

## Evidence required before Deb is asked to activate G28

- exact branch, HEAD, and affected-files list;
- Gate 1 ruling with findings;
- Gate 2 ruling with findings;
- explicit disposition of the Misty A/Misty B identity conflict;
- confirmation that the native AAuth Mission model remains authoritative;
- unresolved conditions and nonclaims;
- a clear statement of what Deb's decision would and would not authorize.

## Questions for independent review

1. Does this proposal preserve the constitution, D-008 authority model,
   research methodology, and existing gate roles?
2. Is Misty A appropriately handled as a G28 rescope, a precursor, or neither?
3. Does the native AAuth Mission plus explanatory mission specification avoid a
   competing mission model?
4. Are any G27 requirements bypassed, weakened, duplicated, or silently
   renamed?
5. What must change before this proposal may be presented to Deb for an
   activation decision?

Required advisory ruling: PASS, PASS WITH CONDITIONS, or FAIL. A reviewer PASS
is advisory and is not PI authorization.

