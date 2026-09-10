# M02 Stage 3-Lib Phase 0 — Exact-Source Acquisition and Build Evidence

Date: 2026-09-10
Status: ACCEPTED UNDER D-059
Authorization: D-058
Authorization checkpoint: `main @ 58f45b8875fb7382c43b415bce61b38347ffaeba`

## Boundary

This report records only the authorized reacquisition, frozen-lockfile
installation, exact build, integrity checks, and preservation of one WAS
teaching-server checkout. No WAS module was imported by SOGA, no application or
candidate runtime was started, no listener was opened, and no route, storage,
wallet, Person Server, governance, or execution behavior was exercised.

Phase 1 harness or test creation and Phase 2 execution remain unauthorized.
Freewallet, Docker, personal data, payment, Misty, G28, and G29 remained outside
this phase.

## Fixed location and exact source

Temporary root fixed by D-058:

`/private/tmp/m02-stage3lib-20260910`

Checkout:

`/private/tmp/m02-stage3lib-20260910/was-teaching-server`

The root was confirmed absent before creation. The checkout was created as an
empty Git repository, assigned only the recorded origin, fetched at the exact
full commit without tags, and checked out detached. No submodule or LFS command
was used.

Verified values:

| Property | Observed value |
|---|---|
| Origin | `https://github.com/interop-alliance/was-teaching-server.git` |
| Detached HEAD | `2090a606f2723e4d57ef0090db55fd1bdab9427e` |
| Git tree | `540d85cea6cc7ab50ee6f00b0dead2084c1d65de` |
| Package version | `0.27.0` |
| Package manager | `pnpm@11.20.0` |
| Node requirement | `>=24.0` |
| Observed Node | `v26.7.0` |
| Lockfile SHA-256 | `edda1bc47d02a673e0994e2b184886e02f581f00c85958879b15225e4c7b7884` |
| License declaration | `AGPL-3.0-or-later` |
| LICENSE SHA-256 | `8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef` |

These values match the accepted Stage 3A evidence.

## Commands executed

Acquisition:

```text
mkdir -p /private/tmp/m02-stage3lib-20260910/was-teaching-server
git init /private/tmp/m02-stage3lib-20260910/was-teaching-server
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server remote add origin https://github.com/interop-alliance/was-teaching-server.git
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server fetch --depth=1 --no-tags origin 2090a606f2723e4d57ef0090db55fd1bdab9427e
git -C /private/tmp/m02-stage3lib-20260910/was-teaching-server checkout --detach FETCH_HEAD
```

The fetch obtained only the requested commit and reported detached HEAD
`2090a60`, release `v0.27.0`.

Frozen installation:

```text
npx --yes --cache /private/tmp/m02-stage3lib-20260910/was-teaching-server/.npm-cache pnpm@11.20.0 install --frozen-lockfile
```

The command reported the lockfile current, resolved 595 packages, reused all
595 from the existing content-addressed store, downloaded zero, and completed
with pnpm `11.20.0`. The package runner cache is inside the checkout at
`.npm-cache/`. As in accepted Stage 3A evidence, pnpm used the host's existing
content-addressed store at `/Users/debb/Library/pnpm/store/v11` and the
checkout-local virtual store at `node_modules/.pnpm`.

Build:

```text
node /private/tmp/m02-stage3lib-20260910/was-teaching-server/.npm-cache/_npx/90ee57dca4845993/node_modules/pnpm/bin/pnpm.cjs run build
```

The cached exact package-manager executable was invoked directly so the build
did not require another registry-capable package-runner call. The build
completed successfully through `clear`, TypeScript compilation, asset copy,
and `tsx scripts/write-build-info.ts`. `dist/index.js` exists.

No `tsx` IPC denial or other IPC event appeared in command output. This is only
an observation about surfaced output; it is not evidence that `tsx` opened no
local IPC pipe. No network-listener claim is made from the absence of an error.

## Source and build integrity

Before installation the checkout had no tracked or untracked status output.
After installation and build:

- `git status --porcelain --untracked-files=no` returned empty;
- `git diff --check` returned clean;
- the only reported untracked path family was the authorized `.npm-cache/`;
- tracked source remained unchanged; and
- built output remained ignored by the candidate repository.

The candidate-generated `dist/build-info.json` records
`2090a606f2723e4d57ef0090db55fd1bdab9427e-dirty`. The `-dirty` suffix reflects
the authorized untracked `.npm-cache/` present inside the checkout when the
build-information script inspected Git status. It does not establish a tracked
source modification; the separate tracked-only status and diff checks above
were empty. The evidence preserves both observations rather than rewriting the
candidate's stamp.

## Exact library-surface re-verification

The reacquired exact revision confirms:

- `src/index.ts:14-19` exports `fastifyWas`, `createApp`, `defaultBackend`,
  `FileSystemBackend`, `PostgresBackend`, and `onboardingTokenAuthorizer` from
  the package root;
- `src/server.ts:29-77` constructs and returns a Fastify instance without
  calling `listen`;
- `src/server.ts:64-72` supplies the unauthenticated health route;
- `docs/consuming-server-as-library.md:19-21` states that only the ESM package
  root is importable and deep `dist` paths are not exposed; and
- `docs/consuming-server-as-library.md:23-39` documents the relevant public
  exports.

These facts are now verified at the selected revision rather than inferred
from the older reference clone.

## Preservation and stop

The checkout, dependency tree, `.npm-cache`, and build output remain unchanged
at the fixed temporary location, as D-058 requires, pending both independent
reviews and PI disposition. They are not adopted repository content.

Phase 0 stops here. No Phase 1 file was created, no package was imported into a
SOGA harness, no Fastify instance was constructed, and no candidate code was
executed as an application runtime.
