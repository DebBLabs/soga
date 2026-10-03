# External Input Manifest

Last updated: 2026-10-02  
Authority: D-118 and D-121
Repository-relative derivation: the durable root is the repository parent's
`research-evidence/soga/` directory.

This is the common discovery point for non-repository inputs used by SOGA.
The paths below are derived by the reviewed controllers; they are not personal
home-directory constants. Runtime and evidence bytes remain outside Git.

## Mockin interoperability assessment inputs

| Field | Value |
|---|---|
| Purpose | Source-only AAuth interoperability comparison; supplemental reference only |
| Durable source path | `<repository-parent>/research-evidence/soga/inputs/mockin/06bb4e7cae491beaf143395a8040659a1196c4b8/source/` |
| Official origin | `https://github.com/hellocoop/mockin.git` |
| Commit | `06bb4e7cae491beaf143395a8040659a1196c4b8` |
| Tree | `281a3aa737200ec66ca98caddb20b1dfd0a98687` |
| Package identity | `@hellocoop/mockin==3.2.1`; Node `>=22`; MIT |
| `package.json` SHA-256 | `8cc1abe2fa9a8c4d440ea3cae0c24c2d1068b428ea1ef1ff51d2662a4e73dc1f` |
| `package-lock.json` SHA-256 | `4873cc09e8ed5dedca286cfa5834e98d6d805688f42008ffb7ef36e1c5bbc5f8` |
| Classification | Pinned source evidence; not installed, built, executed or approved as the core PS |
| Authorizing decisions | D-120 acquisition; D-121 evidence acceptance |
| Last verified | 2026-10-02, detached and clean |

## AAuth `fcf656d` editor source

| Field | Value |
|---|---|
| Purpose | Governing editor-source baseline for the bounded AAuth profile and Mockin comparison |
| Durable source path | `<repository-parent>/research-evidence/soga/inputs/aauth/fcf656d/source/` |
| Official origin | `https://github.com/dickhardt/AAuth.git` |
| Commit | `fcf656de1926535f5bd6fc0538147ead6646e727` |
| Tree | `fe5a02d4a965557c0d31620c5bbb8f725fdccb94` |
| Protocol file | `draft-hardt-oauth-aauth-protocol.md` |
| Protocol SHA-256 | `295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953` |
| Classification | Pinned source evidence; upstream `HEAD` is not a substitute |
| Authorizing decisions | D-120 restoration; D-121 evidence acceptance |
| Last verified | 2026-10-02, detached and clean |

## AAuth `fcf656d` provider runtime

| Field | Value |
|---|---|
| Purpose | Exact Ed25519 provider for the bounded `fcf656d` localhost AAuth proof |
| Durable wheel path | `<repository-parent>/research-evidence/soga/inputs/aauth/fcf656d/wheels/` |
| Durable runtime path | `<repository-parent>/research-evidence/soga/runtimes/aauth-fcf656d-provider/site-packages/` |
| Durable scratch path | `<repository-parent>/research-evidence/soga/runtimes/aauth-fcf656d-provider/scratch/` |
| Durable execution path | `<repository-parent>/research-evidence/soga/executions/localhost-gateway/` |
| Manifest path | `<repository-parent>/research-evidence/soga/manifests/aauth-fcf656d-provider.json` |
| Authorizing decision | D-118/D-119 instrument; D-122 execution; D-123 evidence acceptance |
| Status | Durable runtime recovered and accepted; use requires separately authorized bounded localhost execution |
| Preservation/runtime classification | Reproducible pinned runtime, not preservation evidence |
| Platform baseline | CPython `3.9.6`; resolved interpreter `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`; `sys.platform=darwin`; `platform.machine()=arm64`; pip `21.2.4` |
| Last verified | 2026-10-02 under D-122; manifest SHA-256 `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e` |

### Exact wheel identities

| Distribution | Filename | Bytes | SHA-256 |
|---|---|---:|---|
| `cryptography==50.0.1` | `cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl` | 4,035,307 | `ca83d00d9e69cd5eb63f2e69c3a5a59e0cecae5ae14c6ae0b35830fe3b37bad0` |
| `cffi==2.0.0` | `cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl` | 180,509 | `de8dad4425a6ca6e4e5e297b27b5c824ecc7581910bf9aee86cb6835e6812aa7` |
| `pycparser==2.23` | `pycparser-2.23-py3-none-any.whl` | 118,140 | `e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934` |
| `typing-extensions==4.15.0` | `typing_extensions-4.15.0-py3-none-any.whl` | 44,614 | `f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548` |

## WAS teaching-server preservation evidence

| Field | Value |
|---|---|
| Purpose | Accepted socket-free WAS research environment preservation |
| Durable path | `<repository-parent>/research-evidence/` (existing D-082 material outside the SOGA runtime subtree) |
| Version | commit `2090a606f2723e4d57ef0090db55fd1bdab9427e`; tree `540d85cea6cc7ab50ee6f00b0dead2084c1d65de` |
| Byte identity | 298 `dist/` files; dist manifest SHA-256 `7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586` |
| Authorizing decisions | D-082 and D-083 |
| Preservation/runtime classification | Preservation evidence only; not an active runtime |
| Last verified | 2026-09-30 read-only after reboot |

The D-118 recovery controller must refuse to write anywhere beneath the
repository parent's `research-evidence/` directory except its dedicated
`research-evidence/soga/` subtree.
