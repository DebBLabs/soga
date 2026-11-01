# IIW Flow A Beryl/iPad Stopped-Attempt Recovery

Date: 2026-11-01  
Status: CREATE-ONLY — NOT AUTHORIZED FOR EXECUTION  
Authority: PI direction after the stopped D-186 invocation

## Observed result

The first D-186 invocation is consumed as a stopped attempt. The launcher
created the reviewed `iiw-flow-a-beryl-ipad-rehearsal-v1` directory but exited
before writing its three evidence files. The bridge child remained active on
literal `192.168.8.247:4317`; no launcher parent remained. The integrator
terminated that exact orphaned bridge process and verified that ports 4317 and
4318 were unused. The empty v1 directory remains preserved.

The operator reported that she did not understand that `/flow-a` was a
display-only laptop surface while all choices occurred on the iPad. This
explains why the intended rehearsal was not completed, but it does not by
itself prove which signal or terminal action ended the launcher. The absence of
durable launcher evidence prevents a stronger causal claim.

## Exact recovery correction

Modify only `run_beryl_ipad_rehearsal.py`:

1. preserve and verify the empty v1 directory before and after any R2 attempt;
2. write only to a new, initially absent
   `iiw-flow-a-beryl-ipad-rehearsal-v2` directory;
3. handle `SIGHUP` and `SIGQUIT` through the same bounded cleanup path as
   `SIGINT` and `SIGTERM`, so ordinary Terminal loss or Ctrl-\\ requests child
   shutdown and evidence preservation;
4. update the presentation and SOGA source bases and allow-lists to the accepted
   D-186 commits; and
5. preserve every other request-096-reviewed control and all visitor-visible
   Flow A files byte-identical.

Create a separate R2 execution request pinning the corrected launcher. Before
any R2 execution, both gates must statically review the complete corrected
launcher and request, and the PI must prospectively authorize one attempt.
The R2 request must also require read-only post-exit listener/process checks
and narrowly bound cleanup of an exact orphaned reviewed bridge if present;
`SIGKILL`, forced application termination and power loss cannot be handled by
the launcher itself.

## Boundaries

This correction does not authorize execution, Beryl access, a listener, QR
generation or scan, iPad/device contact, robot activity, deletion or mutation
of v1, or a retry. The unrelated PI routine-tool proposal remains excluded,
unread and untouched.
