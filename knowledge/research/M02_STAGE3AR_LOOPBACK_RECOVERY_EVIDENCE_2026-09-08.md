# M02 Stage 3A-R — Loopback Recovery Evidence

Date: 2026-09-08
Status: ACCEPTED AS A GATED NEGATIVE RESULT UNDER D-041
Authorization: D-040
Authorization checkpoint: `main @ 66e27c9`

## Boundary and attempted work

D-040 authorized a SOGA-owned research launcher, an OS-level containment
preflight, and candidate startup only after that preflight passed. It authorized
no Stage 3B behavior, dependency installation, package-registry access,
upstream modification, wallet interaction, Person Server integration, external
access, personal data, payment, Misty access, physical actuation, R3, G28, or
G29.

The following uncommitted SOGA research files were created under D-040 and
reviewed after the stop:

- `tools/m02_stage3ar/network.sb` — proposed macOS sandbox profile;
- `tools/m02_stage3ar/preflight.mjs` — positive loopback and negative wildcard
  / TEST-NET controls; and
- `tools/m02_stage3ar/launcher.mjs` — bounded WAS library composition and
  zero-dependency Freewallet static server, written but never executed.

Both JavaScript files passed `node --check`. `git diff --check` passed. Gate 1
then identified that the proposed profile's `allow default` posture did not
implement the authorized deny-network-by-default design, and identified two
dormant launcher defects: an asset URL was not independently constrained to the
wallet's loopback origin, and the holdpoint had no maximum timeout. None of
these defects affected runtime because profile parsing stopped before Node ran.

Rather than retain unsafe or unexecutable research machinery, all three files
were removed before adoption. They are not part of the accepted repository
package and must not be reused as a starting point. This report retains the
exact command, diagnostic, and material profile expression needed to establish
the observed negative result.

## Required preflight result

The exact reviewed profile attempted to restrict `network-outbound` remote IP
and `network-bind` local IP to `127.0.0.1:*`. Before importing or starting either
candidate, the command was invoked:

```text
/usr/bin/sandbox-exec -f tools/m02_stage3ar/network.sb node tools/m02_stage3ar/preflight.mjs
```

It exited `65` during profile parsing, before Node or the synthetic controls
ran:

```text
sandbox-exec: host must be * or localhost in network address
```

The diagnostic points to the profile's `(remote ip "127.0.0.1:*")` expression.
On this host, the deprecated sandbox profile language will not accept the
literal IPv4 address required by the reviewed proposal; it accepts `localhost`
or `*`. Substituting `localhost` could also admit IPv6 loopback and would no
longer be the exact literal-`127.0.0.1` containment reviewed and authorized.

For archival verification, the removed `network.sb` contained exactly:

```scheme
(version 1)
(allow default)

; Preserve literal IPv4 loopback only. Deny every outbound connection whose
; remote endpoint is not 127.0.0.1, and every bind whose local endpoint is not
; 127.0.0.1. The synthetic preflight must prove these rules before candidates
; are imported or served.
(deny network-outbound
  (require-not (remote ip "127.0.0.1:*")))
(deny network-bind
  (require-not (local ip "127.0.0.1:*")))
```

This quoted block is evidence, not an executable profile. It shows both the
literal-IP predicate that failed parsing and Gate 1's independent retained-code
finding: the profile began with `allow default`, did not implement the stated
deny-network-by-default posture, and contained no `network-inbound` restriction.

Under the proposal's stop condition, failure to establish the exact containment
profile requires stopping before candidate startup. No alternative profile,
programmatic hook, firewall rule, or relaxed address interpretation was tried.

## Candidate and process state

- The preflight never reached its synthetic listener or connection controls.
- The launcher was never executed and was removed after review.
- WAS and Freewallet were never imported, served, or started during Stage 3A-R.
- No upstream source was modified.
- No dependency or package command ran.
- No application runtime network activity occurred.

A final listener check must accompany gate review, but no candidate shutdown was
needed because no candidate process started.

## Finding and holdpoint

Stage 3A-R ends as a second bounded negative result. The public WAS library seam
remains source-supported, but the selected macOS `sandbox-exec` mechanism cannot
express the exact reviewed literal-IPv4 containment rule on this host.

No Stage 3B inference follows. A further proposal would need to choose and gate
a different OS-level containment mechanism or explicitly justify a broader
`localhost` sandbox rule combined with literal-address application binding and
external socket verification. Neither choice is made or authorized here.

This report requires independent Gate 1 and Gate 2 recheck followed by PI
disposition. No launcher or sandbox profile is proposed for retention.
