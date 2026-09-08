# M02 Stage 3A-R2 — Fixed-Port Containment Evidence

Date: 2026-09-08
Status: INDEPENDENTLY GATED NEGATIVE RESULT — NOT YET PI-ACCEPTED
Authorization: D-042
Authorization checkpoint: `main @ d77f7cf`

## Boundary

D-042 authorized only the reviewed fixed-port containment preflight and, if
every pre-start control passed, bounded reachability of the existing exact
Freewallet `8e806c0` and WAS `2090a60` build outputs. Stage 3B and every other
excluded activity remained unauthorized.

The following temporary SOGA research files were created:

- `tools/m02_stage3ar2/network.sb`;
- `tools/m02_stage3ar2/preflight.mjs`; and
- `tools/m02_stage3ar2/launcher.mjs`.

Both JavaScript files passed `node --check`; `git diff --check` passed. The
launcher was never executed.

Independent Gate 1 and Gate 2 review confirmed the negative result and found
that retaining the disproven profile and unexecuted launcher would create an
attractive nuisance. All three temporary research files were therefore removed
before PI acceptance. This standalone evidence record preserves the complete
executed profile and preflight output; no R2 launcher, sandbox profile, or
preflight program is adopted.

## Preliminary tool correction

The first port-availability command used an invalid combined `lsof` form and
printed both an `lsof` usage error and `FIXED_PORTS_FREE`. That output is not
treated as port evidence. No preflight or candidate ran as a result of that
invalid check because the following `sandbox-exec` invocation was independently
blocked by the outer Codex sandbox with `sandbox_apply: Operation not
permitted`.

The port check was then corrected to query `46321` and `46322` separately. Both
returned no listener and the command recorded `FIXED_PORTS_FREE` before the
authorized preflight was rerun with permission for the nested local sandbox.

## Exact sandbox profile

The executed profile contained:

```scheme
(version 1)
(allow default)

; Deny the complete network class, then admit TCP operations only at the two
; fixed candidate endpoints. The preflight must empirically verify rule
; precedence and all expected allow/deny outcomes before candidates start.
(deny network*)
(allow network-bind
  (local ip "localhost:46321" "localhost:46322"))
(allow network-inbound
  (local ip "localhost:46321" "localhost:46322"))
(allow network-outbound
  (remote ip "localhost:46321" "localhost:46322"))
```

The profile parsed and the Node preflight ran.

## Preflight result

The preflight produced:

```json
{"control":"literal_ipv4_nonce_exchange","result":"PASS","address":{"address":"127.0.0.1","family":"IPv4","port":46321},"echoed":true}
{"control":"wildcard_bind_denial","result":"FAIL"}
{"control":"ipv6_loopback_characterization","result":"ALLOWED","address":{"address":"::1","family":"IPv6","port":46321}}
{"control":"other_loopback_port_denial","result":"PASS","error":{"code":"EPERM","syscall":"connect","address":"127.0.0.1","port":46323,"message":"connect EPERM 127.0.0.1:46323 - Local (0.0.0.0:0)"}}
{"control":"test_net_denial","result":"PASS","error":{"code":"EPERM","syscall":"connect","address":"192.0.2.1","port":46321,"message":"connect EPERM 192.0.2.1:46321 - Local (0.0.0.0:0)"}}
{"control":"containment_preflight","result":"FAIL"}
```

The process exited `1`. The wildcard-control implementation reports `FAIL`
without an error object when the forbidden bind succeeds, then closes that
synthetic listener. Thus the fixed-port symbolic-`localhost` rule admitted a
wildcard bind on an otherwise permitted port. It also admitted IPv6 loopback on
that port, as the proposal anticipated and required the preflight to
characterize. Connections to a different literal-loopback port and to
TEST-NET-1 were denied locally with `EPERM`.

## Required stop and candidate state

The proposal required every pre-start control to pass. The wildcard-bind
control failed, so the launcher was not executed and neither candidate was
imported, served, or started. No upstream source changed, no dependency or
registry command ran, no candidate runtime network activity occurred, and no
candidate shutdown was needed.

A final external listener and process check must accompany gate review. The
preflight closed every synthetic listener before exit.

## Finding and holdpoint

Stage 3A-R2 ends as a gated-candidate negative result. The profile successfully
restricts outbound connections by port, but its symbolic-localhost bind rule
does not enforce the required distinction between literal-loopback and wildcard
binding on an allowed port. It therefore cannot serve as the reviewed
containment mechanism.

This result does not establish that no macOS containment option exists. It
establishes only that the exact fixed-port profile and controls tested here fail
the adopted wildcard-bind requirement. Do not remove that requirement or rely
on the application binding alone without a separately reviewed PI decision.

Independent Gate 1 and Gate 2 review confirmed this negative result and the
required removal of the temporary research machinery. PI acceptance remains
pending. Stage 3B remains unauthorized.
