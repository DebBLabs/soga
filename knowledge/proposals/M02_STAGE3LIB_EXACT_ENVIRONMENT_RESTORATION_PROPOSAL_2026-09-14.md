# M02 Stage 3-Lib — Exact Environment Restoration Proposal

Date: 2026-09-14
Status: PROPOSED — NOT AUTHORIZED
Prepared from checkpoint: `main @ a3a8a87d6d49052f75093b0ae3d380102f73ab10`

## Purpose and durability boundary

Restore the exact Phase 0 WAS input found absent after shutdown. This is prerequisite restoration only. `/private/tmp` is intentionally non-durable and is not expected to survive reboot, unplanned shutdown, or operating-system cleanup. Any accepted restoration is usable only while present and after complete identity and integrity checks immediately before Phase 2. Loss requires a new reviewed restoration.

## Path decision requiring PI selection

- **Option A — original root (recommended):** `/private/tmp/m02-stage3lib-20260910/was-teaching-server`. This satisfies both hard-coded Phase 1 values, `EXPECTED_CHECKOUT` and `COMPLETION_FILE`.
- **Option B — new dated root:** not executable under this proposal. Selecting
  it requires a revised proposal that fixes the exact root and command sequence;
  both hard-coded values would then require separately reviewed harness changes.

No symlink substitution is permitted. PI authorization must select A or B. The sequence below implements Option A only.

## Exact target

- origin `https://github.com/interop-alliance/was-teaching-server.git`
- detached commit `2090a606f2723e4d57ef0090db55fd1bdab9427e`
- tree `540d85cea6cc7ab50ee6f00b0dead2084c1d65de`
- package version `0.27.0`
- lockfile SHA-256 `edda1bc47d02a673e0994e2b184886e02f581f00c85958879b15225e4c7b7884`
- license `AGPL-3.0-or-later`; LICENSE SHA-256 `8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef`
- `pnpm@11.20.0` with `--frozen-lockfile`
- Node 24 or later

## Exact Option A sequence

Run each command separately from `/Users/debb/dev/soga-clean`; record command, status, elapsed time, and output. Stop on every nonzero result.

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

The recorded cached pnpm path must exist exactly; otherwise stop without discovering or substituting another executable. No lockfile modification is permitted. Tracked status must be clean before installation and after build. Only the preregistered checkout-local `.npm-cache` may be untracked; every other untracked or modified path is a stop.

Evidence must record the actual reacquisition date and state explicitly that the
content is newly reacquired, not the original 2026-09-10 environment; the dated
directory name is retained solely because it is the accepted harness identifier.

## Network, storage, timing, and version controls

Network access is limited to the exact Git fetch and npm/pnpm registry token, metadata, and package downloads intrinsic to the single frozen installation. Downloads are permitted and must be enumerated. No alternate origin, registry, mirror, retry, or dependency operation is permitted. pnpm may read or write its host store at `/Users/debb/Library/pnpm/store/v11`; this out-of-root effect must be recorded.

Operator-enforced limits are 10 minutes for fetch, 20 minutes for install, and 10 minutes for build. Exceeding a limit requires interruption and consumes the attempt; no retry follows. Node below 24 is a stop. Node 24 or later but different from Phase 0 `v26.7.0` is a recorded nonblocking environment difference unless an exact check or build fails.

Do not fetch submodules or LFS, modify source, import WAS, construct `createApp`, create a symlink, execute the Phase 1 harness/tests, or open a listener.

## Verification, evidence, and closure

Before dependency work and after build, verify origin, commit, tree, package version, license declaration/hash, lockfile hash, tracked-clean status, and Node version. Record build stages, reused/downloaded counts, and any `tsx` IPC event; silence is not proof of no IPC. Verify expected build output and the bounded cache condition. Produce standalone evidence and preserve the environment unchanged for both gates.

Immediately before later Phase 2 dependence, reverify presence and every identity/integrity value. Restoration closes only when both gates verify evidence and the PI accepts it; it creates no Phase 2 authority.

## Explicit exclusions

This proposal authorizes nothing by itself. It excludes Phase 2, harness changes or execution, WAS startup, Fastify injection, listeners, Freewallet, `did-cli-typescript`, wallet interaction, Person Server integration, Docker, external runtime services, personal data, payment, Misty access, actuation, G28, and G29. It excludes reading or adopting the unrelated PI routine-tool proposal.
