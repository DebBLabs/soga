# External Input Manifest

Last updated: 2026-10-02  
Authority: D-118  
Repository-relative derivation: the durable root is the repository parent's
`research-evidence/soga/` directory.

This is the common discovery point for non-repository inputs used by SOGA.
The paths below are derived by the reviewed controllers; they are not personal
home-directory constants. Runtime and evidence bytes remain outside Git.

## AAuth `fcf656d` provider runtime

| Field | Value |
|---|---|
| Purpose | Exact Ed25519 provider for the bounded `fcf656d` localhost AAuth proof |
| Durable wheel path | `<repository-parent>/research-evidence/soga/inputs/aauth/fcf656d/wheels/` |
| Durable runtime path | `<repository-parent>/research-evidence/soga/runtimes/aauth-fcf656d-provider/site-packages/` |
| Durable scratch path | `<repository-parent>/research-evidence/soga/runtimes/aauth-fcf656d-provider/scratch/` |
| Durable execution path | `<repository-parent>/research-evidence/soga/executions/localhost-gateway/` |
| Manifest path | `<repository-parent>/research-evidence/soga/manifests/aauth-fcf656d-provider.json` |
| Authorizing decision | D-118 Phase 1 create-only; recovery execution requires separate authority |
| Status | Runtime absent after reboot; recovery instrument awaiting blind dual review |
| Preservation/runtime classification | Reproducible pinned runtime, not preservation evidence |
| Platform baseline | CPython `3.9.6`; resolved interpreter `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`; `sys.platform=darwin`; `platform.machine()=arm64`; pip `21.2.4` |
| Last verified | 2026-09-24 before temporary input loss; durable recovery not yet executed |

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
