# M02 AAuth `fcf656d` Phase A Exact-Wheel Acquisition Request

Date: 2026-09-21
Status: DRAFT REQUEST — NOT AUTHORIZED FOR EXECUTION
Prepared at: `main @ 1694e9a`
Authority to create: D-088
Author/integrator: Codex
Review class: mandatory blind dual review

## Requested action

Authorize one bounded acquisition attempt that retrieves exactly four selected
wheel files into:

`/private/tmp/m02-aauth-fcf656d-phase1-20260921/wheels`

The target root must not exist before the run. Create it with owner-only access.
No package manager, resolver, installer, importer, build tool or Python package
code may consume the retrieved files.

## Exact acquisition manifest

| Filename | Bytes | SHA-256 | Exact URL |
|---|---:|---|---|
| `cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl` | 4,035,307 | `ca83d00d9e69cd5eb63f2e69c3a5a59e0cecae5ae14c6ae0b35830fe3b37bad0` | `https://files.pythonhosted.org/packages/84/a9/ee16a903f13755e914d1eecc482fe64d1f10761c3960e5d8fa6837377aff/cryptography-50.0.1-cp39-abi3-macosx_11_0_arm64.whl` |
| `cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl` | 180,509 | `de8dad4425a6ca6e4e5e297b27b5c824ecc7581910bf9aee86cb6835e6812aa7` | `https://files.pythonhosted.org/packages/3d/de/38d9726324e127f727b4ecc376bc85e505bfe61ef130eaf3f290c6847dd4/cffi-2.0.0-cp39-cp39-macosx_11_0_arm64.whl` |
| `pycparser-2.23-py3-none-any.whl` | 118,140 | `e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934` | `https://files.pythonhosted.org/packages/a0/e3/59cd50310fc9b59512193629e1984c1f95e5c8ae6e5d8c69532ccc65a7fe/pycparser-2.23-py3-none-any.whl` |
| `typing_extensions-4.15.0-py3-none-any.whl` | 44,614 | `f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548` | `https://files.pythonhosted.org/packages/18/67/36e9267722cc04a6b9f15c7f3441c2363321a3ea07da7ae0c0707beb2a9c/typing_extensions-4.15.0-py3-none-any.whl` |

## Controller and network controls

Before execution, create and independently review a bounded controller that:

- accepts no dynamic URL, filename, expected size or digest input;
- permits HTTPS only and requests the four exact URLs once each, sequentially;
- refuses every redirect, including same-host redirects, and records affirmative
  no-redirect evidence for each response;
- uses a 15-second connection timeout, 120-second total timeout per artifact,
  and a response-body cap equal to the pinned size plus 65,536 bytes;
- refuses a declared content length that differs from the pinned size; an absent
  content length is permitted only when the bounded received-length check below
  yields the exact pinned size; and refuses any received length that differs;
- writes each response first to an owner-only `.partial` file, fsyncs it, then
  computes its SHA-256 before any final naming;
- renames a size-and-hash-matching file to its exact manifest filename;
- quarantines a complete size-correct but hash-mismatched file as
  `<filename>.UNVERIFIED`, records the observed hash and stops;
- removes an incomplete or truncated `.partial` file and stops;
- makes no retry, substitution, index query, resolver call, mirror request,
  authentication request, update check or advisory request; and
- stops on the first unexpected status, host, redirect, TLS/network failure,
  timeout, size mismatch, hash mismatch, filesystem anomaly or extra file.

The controller source itself requires both blind reviews before commit or use.
The controller may use only standard operating-system/Python networking and
hashing facilities already present; a new dependency is a stop condition.

## Evidence and cleanup

Evidence must record the exact SOGA HEAD and tree state; controller hash;
timestamps; request URL and host; HTTP status; TLS result available from the
client; redirect count/chain; declared and received sizes; expected and observed
hashes; filesystem modes; command/action; exit status; stop rule; and before and
after directory inventories.

On complete success, preserve the four files owner-read-only with the controller
and standalone evidence report pending both blind reviews and PI disposition.
On failure, preserve the diagnostic record and any quarantined complete file;
remove only incomplete/truncated partial bytes. Do not retry automatically.

## Claim boundary and exclusions

Success would establish only acquisition of four exact bytestrings matching the
accepted manifest. It would not establish safe installation, importability,
runtime behavior, absence of vulnerabilities, or AAuth conformance.

This request does not authorize itself. It requests no installation, extraction,
import, compilation, test, implementation, listener, external runtime service,
Phase B work, Steps 4–9, wallet/WAS work, personal data, payment, Misty access,
physical actuation, G28 or G29. The unrelated PI routine-tool proposal remains
excluded and untouched.
