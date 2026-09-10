# M02 Stage 3-Lib Phase 1 harness

Status: create-only source under D-059. Do not run this package until a
separate Phase 2 decision authorizes one bounded execution.

The harness is designed to exercise the exact WAS teaching-server revision
`2090a606f2723e4d57ef0090db55fd1bdab9427e` through its documented package-root
library exports and Fastify injection. It does not start the WAS executable or
call `listen`.

Whole-source inspection of that exact revision found one `.listen(` call under
`src/`: `src/start.ts:66`. The package-root `createApp` composition does not
invoke it; the call belongs to the standalone startup module.

At execution time only, the harness will create a temporary package-resolution
link beneath this directory, dynamically import the bare
`was-teaching-server` package after installing network-attempt guards, use a
fresh filesystem data directory outside both repositories, and remove every
harness-created path in `finally`.

The first proposed operation is an injected `GET /health`. The bounded write is
an injected onboarding-token Space provision using locally generated material.
The harness verifies that write directly through the injected
`FileSystemBackend`. It deliberately does not attempt a resource read or
conditional resource write: no Resource exists to read, and creating one uses
a non-safe method requiring authorization headers and zcap verification that
this phase does not supply. Phase 1 authorizes neither a verification bypass
nor remote DID resolution.

The in-process guards cover the harness process only. The harness contains no
child-process or worker-thread creation; the separately authorized Phase 2
observer remains responsible for process and host socket evidence. Checkout
identity is checked in the harness, while the preserved clean tree and recorded
tree hash `540d85cea6cc7ab50ee6f00b0dead2084c1d65de` remain external preflight
checks.
