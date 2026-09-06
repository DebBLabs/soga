# M01 Exit Reconciliation Proposal

Date: 2026-09-06
Status: ADOPTED — M01 accepted under D-034
Prepared by: Codex/CG
Review target: `main @ ddcdabb7939c3c3e94bab0db95431d88fcbe416d`

## Purpose

Reconcile the two M01 exit recommendations without representing the dedicated
Beryl network boundary as already complete and without delaying unrelated,
non-robot AAuth and Person Server work.

This proposal changes no authorization. D-032 remains exhausted. It authorizes
no robot power, connection, query, configuration, discovery, or actuation and
does not activate G28 or a successor mission.

## Verified completion evidence

- D-028 through D-033 preserve the staged mission, implementation, preparation,
  connection, single-action, and outcome decisions.
- The authorized `m01.signal_light` sequence was dispatched once. Pink was
  directly observed; the neutral appearance was recorded as consistent with
  yellow by PI observation and inference rather than independently measured.
- The post-authorization stale test was repaired at `0b1e922`; the recorded
  suite passed 88 of 88 tests.
- D-032 is exhausted and D-033 authorizes no additional physical action.

## Exit-review difference requiring disposition

Gate 1 recommended `ACCEPT` only after the stale test was repaired and Misty A
was secured behind the Beryl router. Gate 2 recommended `ACCEPT` and treated
Beryl placement as a prerequisite to a future run rather than to recognition
of the completed bounded experiment.

Misty A is not behind the Beryl router. This proposal does not conceal or waive
that fact. The G3100 use was a one-time accepted exception and creates no
precedent. It proposes that the PI classify the dedicated Beryl boundary as a
hard prerequisite to every future Misty power-on, connection, query,
configuration, demonstration, or actuation, rather than as evidence needed to
determine whether the already-completed M01 experiment achieved its bounded
objective. No further Misty A network exposure under any router is authorized
until that placement is confirmed through a later decision.

That classification is prospective. It does not rewrite D-032's temporary
G3100 exception or claim that its anticipated immediate follow-up occurred.

## Additional facts requiring correction at closure

1. `CURRENT_STATE.md` still describes the active authorization boundary as
   Mission Formation only under D-028 even though D-029 through D-033 occurred.
2. Gate 2 described the runner's decision-log presence check as
   “unforgeable.” The check establishes that a matching durable repository
   record exists; it is not a cryptographic or unforgeable authorization proof.
3. Gate 2 stated that G28 requires separate hardware procurement. The
   repository does not establish procurement as a requirement. Deb states from
   her own knowledge as PI and physical-asset owner that Misty B is already
   owned; this is PI testimony rather than repository-derived evidence. Unit
   qualification, network isolation, and explicit PI authorization remain
   required.
4. On 2026-09-06, Deb directly confirmed that Misty A is physically powered
   off and on the shelf. This is PI-observed physical-state evidence, not a
   software query or network verification. It authorizes no subsequent power,
   connection, query, configuration, discovery, or actuation.
5. `CURRENT_STATE.md` also still instructs the program to obtain the two exit
   recommendations even though both reviews are committed and the stale test
   has been repaired. The Current Program Phase and Immediate Next Action
   sections must be refreshed together at closure.

## Proposed closure rule

M01 may receive `ACCEPT` only if:

- the exit record preserves the PI's 2026-09-06 observation that Misty A is
  physically powered off and on the shelf;
- Gate 1 and Gate 2 confirm that reclassifying Beryl placement as a hard
  pre-next-connection prerequisite preserves the adopted safety and isolation
  boundaries;
- the documentary corrections above are incorporated in the canonical
  exit record; and
- the exit record states that M01 closure does not activate G28 or authorize
  any subsequent robot access.

If either reviewer concludes that Beryl placement remains a necessary M01 exit
criterion, present that disagreement to the PI as `REWORK`; do not infer a
waiver.

## Requested reviews

- **Claude / Gate 1:** determine whether the proposed prospective
  reclassification preserves the constitutional, safety, evidence, and
  authorization record; verify every completion claim at the stated HEAD.
- **AGy/Gemini / Gate 2:** independently attempt to falsify the proposed exit
  rule, documentary corrections, and separation between M01 closure and future
  network readiness.

Both reviews are advisory. Only the PI may select `ACCEPT`, `REWORK`, or `FAIL`.
