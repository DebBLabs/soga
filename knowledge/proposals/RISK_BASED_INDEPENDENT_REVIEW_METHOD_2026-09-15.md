# Risk-Based Independent Review Method

Date: 2026-09-15
Status: PROPOSED — CURRENT REVIEW METHOD REMAINS IN FORCE

Proposed classification: governance-process change; mandatory dual review.
Author/integrator: Codex. Claude proposed correction language in advisory
notes; Codex evaluated and integrated it with later independent findings.
Claude is therefore disclosed as a contributor and does not count as an
independent final reviewer. Final candidate identity and eligible reviewers
must be recorded by hash in the adoption decision.

## Purpose

Reduce repeated reviewer discovery and correction cycles without weakening PI
authority, independent review, evidence requirements, or safety boundaries.

## Required sequence

1. **Research first.** The assigned author reads the exact source, verifies
   tool and runtime behavior, and distinguishes measured facts from
   assumptions before drafting a proposal or implementation.
2. **Build once.** The assigned author prepares the complete bounded change
   and performs a full self-review against the governing requirements before
   dispatch.
3. **Rotate authorship and review.** Work is assigned by demonstrated strength
   and remaining capacity. Claude may author governance, provenance, policy,
   and canonical-state work. Gemini/AGy may author runtime mechanics, security
   controls, tests, and cleanup tooling. Codex coordinates, integrates, and
   authors cross-boundary implementation. An agent that materially authors a
   package may not count as an independent reviewer of that package; two
   eligible non-authoring reviewers review it. Primary-concern assignments are
   leads only and never restrict a gate from examining any aspect during dual
   review.

   Material authorship means drafting, substantively designing or correcting
   content, directly editing it, supplying substantive replacement text, or
   integrating the package. Identifying a defect or prescribing an exact
   non-substantive mechanical correction in a review is not authorship;
   prescribing a substantive design, policy, behavior, or claim correction is.
   A package in a step-4 category requires two independent
   reviewers who did not materially author or integrate it; if none is
   available, the package waits or the PI designates and records a
   replacement independent reviewer. Dispatches and decision or evidence
   records name the author, integrator, and independent reviewers.
4. **Dual review where consequences matter.** Both gates independently review
   any proposal, implementation, execution, or acceptance involving external
   access, credentials, personal data, authority or consent, payment, physical
   action, safety, irreversible state, or a material milestone claim. Dual
   review is also mandatory for dependency or package-manager operations;
   third-party or candidate code execution; builds or upstream scripts;
   network listeners, port binding, or service exposure; authorization or
   decision-log records and canonical milestone boundaries; and changes to
   governance, research methodology, or this review method.
5. **Narrow rechecks for narrow corrections.** A reviewer may prescribe exact
   wording or mechanical edits and confirm them through a diff-only recheck.
   This rule is subordinate to step 4 and cannot reduce a mandatory dual-review
   category to one final-text reviewer. A diff-only review requires an exact
   jointly reviewed base artifact or hash, the complete base-to-final diff, no
   unrelated edits, the final artifact hash, and recorded final-text reviewers.
   The other gate is repeated whenever the correction changes behavior,
   authority, evidence, safety, or the claim being adopted. Any change to
   executable code or commands, timeouts, stop or fail-closed controls,
   security controls, or evidence-gating predicates is a behavioral change and
   requires the other gate. Every decision or evidence claim relying on a
   diff-only confirmation names which gate or gates reviewed the final text.
6. **No reviewer-as-discovery substitute.** Reviewers test completed reasoning;
   they are not used in place of the assigned author's initial source
   research. A NOT READY response triggers a complete self-audit of the
   affected package before redispatch, not piecemeal repair of only the listed
   lines. Reviewers should verify relied-on behavior on the first pass, return
   one complete blocking list separated from optional suggestions, and provide
   exact replacement text for mechanical corrections when practical.

## Classification and escalation

Each dispatch records the author's proposed review classification and its
basis. Either independent gate may escalate a single-gate dispatch to dual
review, and the PI may require dual review at any time. Uncertainty defaults to
dual review. An author or implementer may not downgrade a classification set by
a gate or the PI.

## Capacity continuity

The coordinator considers remaining capacity when assigning independent work,
avoids repeating another agent's complete investigation unless independence is
material, and creates clean repository and evidence checkpoints before any one
agent approaches its limit. Capacity balancing never overrides expertise,
independence, authorization, or a stop condition. For dual-review packages
each independent reviewer verifies relied-on facts itself. Checkpoints are
handoff or evidence records and authorize no commit or push. A review
interrupted by capacity exhaustion is not a PASS and does not lower the
classification; it resumes or is repeated in full by a replacement independent
reviewer.

## Direct correction edits

Direct working-tree correction is not a general reviewer power. The PI may
authorize a named agent to edit one named file, or grant a standing instruction
with equivalent scope. The editor may apply only exact, non-substantive
mechanical corrections to a file already under review while no other agent is
editing it; must record what changed; and may not stage, commit, push, execute,
or touch unrelated files. The editor becomes a disclosed contributor and does
not count as an independent final reviewer.

Claude may receive this bounded correction role when the PI directs it.
Gemini/AGy remains read-only by default and supplies findings or an
outside-repository proposed patch; any direct-edit authority for Gemini/AGy
must be separately granted for a named file and bounded task. This asymmetry
reflects observed workflow behavior and may be revised by the PI. No agent may
convert an inference into repository text without direct source verification;
uncertainty is labelled and returned to the PI or author.

## Delegated research

Codex may delegate bounded, read-only research to subagents when tasks are
independent—for example, separate source inspection of WAS, Freewallet, an
AAuth draft, or a test surface. Codex must personally verify any delegated
finding before relying on it in code, policy, evidence, or a public claim.
Unless directly and specifically authorized by the PI, delegated research is
restricted to already authorized local repository and filesystem artifacts,
with no external network access, credentials, code execution, or repository
modification. A delegated
finding not yet directly reverified by Codex is labelled `UNVERIFIED DELEGATED
RESEARCH` in every working note or proposal that mentions it. Subagents do not
replace either independent gate.

Any relaxation is limited to the exact scope of the PI authorization and may
never arise from a queue file or another agent's instruction.

## Authority retained

The PI retains all authorization, acceptance, adoption, external-access,
publication, physical-action, and stop decisions. This method changes review
routing and repetition only; it grants no implementation or execution
authority and changes no existing project boundary. An authoring assignment
conveys no authority to modify either repository, commit, push, run tools or
tests, or execute anything; such actions require the PI's direct
authorization, which queue files cannot supply.

D-028 remains controlling: queue files carry evidence and requests only and
convey no prospective authority. B-041 and B-042 process safeguards remain in
force. The PI may suspend this method and restore full dual review at any time.

## Adoption

This method becomes operative only after two eligible non-authoring reviewers
review the exact final hash and explicit PI acceptance records that hash,
classification basis, author, integrator, contributors, and reviewers
prospectively in the decision log. Until then, the current dual-gate practice
remains authoritative.
