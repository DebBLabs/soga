# M02 AAuth Demo Runtime Recovery Evidence

Date: 2026-10-02  
Status: EXECUTED EVIDENCE — AWAITING BLIND DUAL REVIEW AND PI ACCEPTANCE  
Authority: D-118, D-119 and D-122  
Execution HEAD: `59865f08d969f2ff0fe648acb7927437ef166738`

## Result

The single D-122 recovery execution completed with exit code `0`. The durable
manifest reports `VERIFIED_DURABLE_RUNTIME`. All four exact wheels were
retrieved once over HTTPS with HTTP 200, zero redirects and exact size/hash
matches. The pinned provider was installed offline and its complete static
filesystem identity passed the controller's checks.

This is recovery evidence only. The runtime has not been accepted for use. No
provider behavior was invoked outside the controller's bounded static
installation verification, no localhost gateway was executed and no listener
was opened by the controller.

## Exact instrument and durable evidence

- Controller:
  `tools/m02_aauth_fcf656d/restore_demo_runtime.py`
- Controller SHA-256:
  `07f3d1e8a5d42811d2945358b3ff5a8ee157ed88c27586b02f2009e4750621bb`
- Durable manifest:
  `/Users/debb/dev/research-evidence/soga/manifests/aauth-fcf656d-provider.json`
- Manifest bytes: `7470`
- Manifest SHA-256:
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`
- Started: `2026-10-03T02:51:11Z`
- Finished: `2026-10-03T02:51:12Z`
- Result: `VERIFIED_DURABLE_RUNTIME`

## Environment holdpoints

All exact controller holdpoints passed:

| Field | Required and observed |
|---|---|
| Python | `3.9.6` |
| Resolved interpreter | `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9` |
| Platform | `darwin` |
| Machine | `arm64` |
| pip | `21.2.4` |

## Wheel acquisition evidence

| Distribution | Bytes | SHA-256 | HTTP | Redirects |
|---|---:|---|---:|---:|
| `cryptography==50.0.1` | 4035307 | `ca83d00d9e69cd5eb63f2e69c3a5a59e0cecae5ae14c6ae0b35830fe3b37bad0` | 200 | 0 |
| `cffi==2.0.0` | 180509 | `de8dad4425a6ca6e4e5e297b27b5c824ecc7581910bf9aee86cb6835e6812aa7` | 200 | 0 |
| `pycparser==2.23` | 118140 | `e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934` | 200 | 0 |
| `typing-extensions==4.15.0` | 44614 | `f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548` | 200 | 0 |

Every retrieved wheel was stored mode `0400`. No dynamic URL, mirror,
redirect, index resolution or retry was used.

## Offline installation and static verification

- pip return code: `0`
- stdout: `655` bytes, SHA-256
  `4ac7b0c17eecca0f9f94beda51ac11d0dd5f020572853bfa034d69becbdf603b`
- stderr: `0` bytes, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Distribution identities:
  `cryptography==50.0.1`, `cffi==2.0.0`, `pycparser==2.23`,
  `typing-extensions==4.15.0`
- Regular files verified and accounted for through wheel `RECORD` files: `190`
- `RECORD` entries verified: cryptography `123`, cffi `33`, pycparser `26`,
  typing-extensions `8`
- Symlinks observed in installed tree: `0`
- Scratch inventory after installation: `0`

The controller wrapped pip with a Python audit hook that rejects `socket.*`
events after acquisition and used `--no-index`, `--no-deps`,
`--only-binary=:all:`, `--no-cache-dir` and `--no-compile`.

## Repository and cleanup evidence

The controller's before/after repository records are byte-identical:

- HEAD before and after:
  `59865f08d969f2ff0fe648acb7927437ef166738`
- status before and after included the pre-existing untracked `.claude/` and
  unrelated PI routine-tool proposal; neither was modified by the controller.
- the current repository status retains only the unrelated untracked PI
  routine-tool proposal.

Independent post-run filesystem inspection found exactly `190` regular files,
zero symlinks in the installed target and an empty scratch directory. Process
enumeration was unavailable to the inspecting sandbox (`ps`/`pgrep` denied by
the host), so this report does not claim independent OS-process enumeration.
The controller was a finite foreground process and returned exit code `0`; no
controller or pip process remained attached to its completed execution call.
Independent listener inspection found no Python, pip or AAuth TCP listener.

## Claim boundary

Established, subject to evidence acceptance:

- the four exact pinned wheel bytes are durably present;
- the pinned platform-specific provider tree was installed without index or
  dependency resolution;
- distribution identities and every installed file are statically accounted
  for; and
- the repository was unchanged by recovery.

Not established:

- provider import or cryptographic behavior in this recovered tree;
- localhost gateway behavior or the 53-test result;
- complete AAuth conformance;
- Mockin interoperability;
- wallet, WAS, QR, parent-authority or Misty integration; or
- G28/G29 readiness.

The recovered runtime must remain unused until this evidence receives blind
dual review and explicit PI acceptance. The D-122 attempt is consumed; no retry
is authorized.

