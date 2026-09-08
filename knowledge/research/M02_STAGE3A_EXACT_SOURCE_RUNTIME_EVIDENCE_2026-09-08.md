# M02 Stage 3A — Exact-Source Runtime Reproduction Evidence

Date: 2026-09-08
Status: ACCEPTED AS A GATED NEGATIVE RESULT UNDER D-039
Authorization: D-038
Authorization checkpoint: `main @ 83a0d4e`

## Boundary

This report records exact-source acquisition, lockfile-pinned dependency
installation, literal-loopback runtime reproduction, interface inspection, and
shutdown evidence only. It contains no Stage 3B adapter code or tests and makes
no AAuth-conformance, integration, identity, authority, consent, payment,
execution, or physical-outcome claim. Application runtime external-network
access is prohibited. Misty, G28, and G29 remain outside scope.

## Exact sources acquired

Temporary root: `/private/tmp/m02-stage3a-20260908`

| Candidate | Origin | Detached HEAD | Version | Lockfile SHA-256 |
|---|---|---|---|---|
| Freewallet | `https://github.com/interop-alliance/freewallet.git` | `8e806c049b1134e36e72ab243ea3fbeb93153c37` | `0.42.0` | `0bfe8e1dcd5d977b49292d35d0966d10840dee85c9cccbfe958055f7d104a700` |
| WAS teaching server | `https://github.com/interop-alliance/was-teaching-server.git` | `2090a606f2723e4d57ef0090db55fd1bdab9427e` | `0.27.0` | `edda1bc47d02a673e0994e2b184886e02f581f00c85958879b15225e4c7b7884` |

Both checkouts were clean immediately after detached checkout. Freewallet is
AGPL-3.0; the WAS teaching server is AGPL-3.0-or-later. Each checkout's
`LICENSE` file has SHA-256
`8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef`.
Neither source is copied into or represented as part of SOGA.

## Pre-install inspection

Observed host runtime: Node `v26.7.0`. The bundled `pnpm` is `11.19.0`; no
`corepack` executable is available. Both selected sources declare Node 24 or
later and `packageManager: pnpm@11.20.0`.

WAS documents that an unset `DATABASE_URL` selects its filesystem backend.
Postgres tests are opt-in. Therefore Postgres and Docker are not required for
the bounded reproduction.

Freewallet is a static browser application. Its README documents passphrase as
an available fallback when WebAuthn PRF is unavailable, and an unset
`VITE_WAS_SERVER_URL` as local-only browser storage. Stage 3A will build and
serve its static interface on literal loopback, but will not install a browser,
run Playwright, perform a WebAuthn ceremony, or claim that a wallet interaction
was completed.

## Dependency commands recorded before execution

The following are the only approved dependency-install commands. Each invokes
the source-declared pnpm `11.20.0`, uses the committed lockfile without update,
and confines the npm package-runner cache to the corresponding detached
checkout rather than changing the global package-manager selection.

```text
npx --yes --cache /private/tmp/m02-stage3a-20260908/freewallet/.npm-cache pnpm@11.20.0 install --frozen-lockfile
npx --yes --cache /private/tmp/m02-stage3a-20260908/was-teaching-server/.npm-cache pnpm@11.20.0 install --frozen-lockfile
```

Package-registry access is authorized only while these two commands execute.
Application runtime external-network access remains prohibited.

## Installation, runtime, interfaces, and shutdown

Both recorded install commands completed successfully using pnpm `11.20.0` and
the committed lockfiles. Freewallet installed 752 packages and WAS installed
595 packages. The npm runner caches were confined to `.npm-cache/` inside each
temporary checkout. pnpm nevertheless used its normal shared content-addressed
store at `/Users/debb/Library/pnpm/store/v11`; each checkout's virtual store is
local at `node_modules/.pnpm`. No global package-manager selection was changed.
The `.npm-cache/` directories are untracked temporary artifacts; tracked source
diffs remain empty in both checkouts.

Freewallet built successfully from the exact selected source with TypeScript
and Vite. The output is a static SPA in `dist/`. No graphical browser,
Playwright flow, WebAuthn ceremony, wallet account, camera, microphone, remote
WAS, or external application runtime was used. Because the phase stopped on the
WAS boundary below, the Freewallet server was not started and no wallet
interaction is claimed.

The first WAS build compiled TypeScript and copied assets, then the `tsx`
build-metadata step failed because the execution sandbox denied its temporary
local IPC pipe with `listen EPERM`. The identical build was rerun with local
process permission and completed successfully. This was an environmental
restriction, not a source defect or a Postgres/Docker dependency.

Before starting WAS, direct source inspection found that the selected
executable calls:

```text
await fastify.listen({ port: config.port, host: '0.0.0.0' })
```

at `src/start.ts:66`. The host is not configurable through the documented
environment surface. Running this executable would create a wildcard listener,
contrary to D-038's literal-loopback boundary and the proposal's explicit
wildcard-bind rejection. Changing the source or adding a SOGA wrapper would
exceed Stage 3A authority. The runtime was therefore not started.

No Freewallet or WAS application service was started during Stage 3A. A final
listening-socket check found no Node, tsx, Vite, or serve listener. Thus there
was no application runtime external-network activity and no service required
shutdown.

## Findings and holdpoint

Stage 3A stops with a reproducible negative result:

- both exact source revisions and lockfiles were acquired and verified;
- both lockfile-pinned dependency installations completed;
- both exact sources built, after distinguishing one sandbox-only IPC denial;
- WAS documents and supplies a non-Postgres filesystem backend, so neither
  Postgres nor Docker is intrinsically required for this bounded run;
- the selected WAS executable cannot be run inside the authorized
  literal-loopback boundary because it hardcodes a wildcard bind; and
- Freewallet was not served after the WAS stop condition, so no selected
  runtime interface or cross-runtime handoff was claimed reachable.

This evidence does not justify Stage 3B. The next step is independent Gate 1 and
Gate 2 review followed by PI disposition. A later proposal could evaluate an
upstream configuration change, a separately authorized process wrapper, or a
different exact source revision; none is authorized or selected here.
