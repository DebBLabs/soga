# M02 Stage 3-Lib — Exact Environment Restoration Evidence

Date: 2026-09-14
Status: ACCEPTED GATED NEGATIVE RESULT UNDER D-061
Proposal checkpoint: `a77d86d1170762bed707011735e1464d4b9403e1`
Authorization record: D-061, recorded retrospectively after the PI's explicit
pre-execution chat authorization
Selected path: Option A, `/private/tmp/m02-stage3lib-20260910`

## Result

Exact-source reacquisition and the single frozen installation succeeded. The
single upstream build exited nonzero at the final `write-build-info` stage
because `tsx` attempted to listen on a local IPC pipe and the environment
returned `EPERM`. The no-retry rule was honored. Phase 1 harnesses and tests
were not executed, WAS was not started or imported, and no listener was opened
by SOGA or WAS.

This is a negative restoration result, not a completed restoration and not
Phase 2 evidence.

## Provenance

The content was newly reacquired on 2026-09-14. It is not the original
2026-09-10 environment. The 2026-09-10 directory name is retained solely as
the accepted harness identifier.

Observed values:

- SOGA HEAD: `a77d86d1170762bed707011735e1464d4b9403e1`
- origin: `https://github.com/interop-alliance/was-teaching-server.git`
- detached commit: `2090a606f2723e4d57ef0090db55fd1bdab9427e`
- tree: `540d85cea6cc7ab50ee6f00b0dead2084c1d65de`
- package version: `0.27.0`
- license declaration: `AGPL-3.0-or-later`
- lockfile SHA-256: `edda1bc47d02a673e0994e2b184886e02f581f00c85958879b15225e4c7b7884`
- LICENSE SHA-256: `8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef`
- Node: `v26.7.0`, identical to the Phase 0 value
- pnpm: `11.20.0`, invoked from the exact reviewed cache path

All exact source values matched before dependency work and remained matching
after the failed build. Tracked Git status remained clean. The sole untracked
path was the permitted checkout-local `.npm-cache/`.

## Operation chronology and captured timing

The command runner captured aggregate wall times for command groups rather than
individual timings for every setup command. That instrumentation gap is stated
instead of reconstructed. The three time-limited operations have captured
upper bounds sufficient to verify the proposal's limits:

- exact fetch: exit 0; no more than 31 seconds observed; limit 10 minutes;
  output identified the requested commit as `FETCH_HEAD`;
- frozen install: exit 0; no more than 35 seconds observed (pnpm itself
  reported 2 seconds); limit 20 minutes; output reported 595 resolved, 595
  reused, zero downloaded, and pnpm 11.20.0;
- upstream build: exit 1; 2.7 seconds observed; limit 10 minutes; output showed
  successful clear, TypeScript compilation, and asset copy followed by
  `listen EPERM` at `tsx` pipe
  `/var/folders/z4/hjztf4vx5pbfx8fc3z_6fsj40000gn/T/tsx-501/7252.pipe`.

The target-absence/version/status group completed with exit 0 in 0.4 seconds
aggregate. The mkdir/init/remote-add group completed with exit 0 in 0.1 seconds
aggregate. The checkout and complete pre-install identity-verification group
completed with exit 0 in 0.2 seconds aggregate. Individual elapsed times inside
those groups were not captured.

The acquisition, installation, and build commands executed were exactly the
proposal's Option A command block, in its stated order:

```text
test ! -e /private/tmp/m02-stage3lib-20260910
mkdir -p /private/tmp/m02-stage3lib-20260910/was-teaching-server
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server init
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server remote add origin https://github.com/interop-alliance/was-teaching-server.git
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server fetch --depth=1 --no-tags origin 2090a606f2723e4d57ef0090db55fd1bdab9427e
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server checkout --detach FETCH_HEAD
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server status --porcelain
npx --yes --cache /private/tmp/m02-stage3lib-20260910/was-teaching-server/.npm-cache pnpm@11.20.0 install --frozen-lockfile
node /private/tmp/m02-stage3lib-20260910/was-teaching-server/.npm-cache/_npx/90ee57dca4845993/node_modules/pnpm/bin/pnpm.cjs run build
```

The verification commands actually run before dependency work and after the
failed build were:

```text
git rev-parse HEAD
git status --short
node --version
npx --version
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server remote get-url origin
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server rev-parse HEAD
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server rev-parse 'HEAD^{tree}'
node -p "require('/private/tmp/m02-stage3lib-20260910/was-teaching-server/package.json').version"
node -p "require('/private/tmp/m02-stage3lib-20260910/was-teaching-server/package.json').license"
shasum -a 256 /private/tmp/m02-stage3lib-20260910/was-teaching-server/pnpm-lock.yaml /private/tmp/m02-stage3lib-20260910/was-teaching-server/LICENSE
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server status --porcelain
```

1. Confirmed exact SOGA HEAD, target absence, Node version, and repository
   status. The unrelated PI routine-tool proposal remained untracked and was
   not read or modified.
2. Initialized the empty fixed checkout, added only the recorded origin,
   fetched the exact commit once with `--depth=1 --no-tags`, and checked out
   detached `FETCH_HEAD`.
3. Verified every source identity value and clean tracked status.
4. Ran the one authorized frozen installation through the checkout-local npx
   cache. Result: exit 0; 595 packages resolved, 595 reused, zero downloaded.
   The content-addressable store was
   `/Users/debb/Library/pnpm/store/v11`; the virtual store was
   `node_modules/.pnpm`.
5. Verified the exact cached executable at
   `.npm-cache/_npx/90ee57dca4845993/node_modules/pnpm/bin/pnpm.cjs`.
6. Ran the single authorized upstream build. `clear`, TypeScript compilation,
   and `copy-assets` completed. `write-build-info` invoked `tsx`, which
   attempted `listen` on
   `/var/folders/z4/hjztf4vx5pbfx8fc3z_6fsj40000gn/T/tsx-501/7252.pipe`
   and received `EPERM`. The command exited 1.
7. Stopped. No retry, substitution, diagnosis, source change, harness
   execution, or additional dependency operation occurred.

## Network-bearing operations

- one Git fetch from the recorded GitHub origin for the exact commit;
- npm GET of `https://registry.npmjs.org/npm` for its update check;
- two npm GET requests for pnpm package metadata;
- one npm POST to `/-/npm/v1/security/advisories/bulk`, carrying the pnpm
  package identifier;
- one GET of the pnpm 11.20.0 tarball; and
- pnpm's frozen dependency operation, which reported 595 packages reused from
  the host store and zero dependency-package downloads.

The npm update-check marker was written under the checkout-local cache. The
update check and advisory POST are not package downloads and were not
specifically enumerated in the proposal; their authorization-boundary
classification remains unresolved for PI disposition. The equivalent Phase 0
npx traffic was not recorded in its evidence. pnpm's own registry requests, if
any, were not separately captured; only pnpm's reported counts are claimed.

PI disposition: the update-check GET and security-advisory POST are an
unanticipated network-boundary variance. They do not invalidate the source or
failure evidence. Future dependency authorizations must address or suppress
them explicitly. The recorded `npx --version` check produced no observed
network record.

Inference only: because pnpm reported zero dependency downloads, no new content
was expected to be added to `/Users/debb/Library/pnpm/store/v11`. Whether the
host store was written was not independently measured.

## Partial-build and IPC classification

`dist/` contains compiled output including `dist/index.js`, but
`dist/build-info.json` is absent. This is not an accepted build and the Phase
1 harness may not rely on the partial output.

The failed endpoint was an upstream-build-tool local IPC pipe, not a network
socket under the feasibility proposal's classification. The accepted Stage 3A
evidence records the same first-build `tsx` IPC denial and an identical build
succeeding when local-process permission was available. Phase 0 surfaced no
such event in command output. The `tsx-501` directory is now empty. Any
inference that the difference is execution-context dependent remains an
inference, not a diagnosis.

## Preserved state

The exact checkout, dependency tree, runner cache, and partial build output
remain at the Option A path pending review and PI disposition. The environment
is non-durable and must be identity/integrity checked immediately before any
future dependence. No claim is made that it will survive shutdown or cleanup.

## Boundaries

This evidence does not authorize or establish a successful restoration, Phase
2, a harness/test result, WAS application operation, Fastify injection,
network containment, wallet integration, Person Server integration, external
service use, personal data, payment, Misty access, actuation, G28, or G29.
