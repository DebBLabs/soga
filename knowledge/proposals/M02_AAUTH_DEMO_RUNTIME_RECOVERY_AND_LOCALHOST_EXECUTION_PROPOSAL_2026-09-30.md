# M02 AAuth Demo Runtime Recovery and Localhost Execution Proposal

Date: 2026-09-30  
Status: DRAFT — NOT AUTHORIZED FOR IMPLEMENTATION OR EXECUTION  
Repository basis: `main @ c48ed175fddb3e41e126615a292160f477bbea22`  
Author/integrator: Codex  
Review class: mandatory blind dual review, batched by claim

## Purpose

Recover the exact runtime inputs lost from `/private/tmp`, remove personal and
temporary absolute paths from the bounded AAuth demonstration, and perform the
already-planned localhost gateway proof without changing its protocol claim.

This is a recovery and portability plan. It does not advance the implementation
to the current published AAuth draft, add parent or visitor authority, create a
QR flow, or connect a robot.

## Current verified state

- Local and remote `main` match at `c48ed175fddb3e41e126615a292160f477bbea22`.
- D-113 accepted the 35-test transport-free exchange.
- D-116 accepted the static localhost transport, SOGA supervision adapter and
  18-test localhost package.
- D-117 accepted the localhost execution controller at SHA-256
  `87b17c9a28313ae8399364d59f038377a792987857e202f4a89a71c38a307950`,
  but authorized commit and push only. It has never been executed.
- The reboot removed the accepted wheel, provider-installation, normative-source
  and AAuth-source trees formerly under `/private/tmp`.
- Read-only post-reboot inspection established that the 2026-09-30 07:52 reboot
  cleared `/private/tmp` completely. Missing material includes the 59-file
  `fcf656d` editor's copy, four normative sources, four D-091 wheels, the
  192-file provider installation, all accepted AAuth execution-evidence
  directories and the prior review queue. This is a recurrence of B-043's
  non-durable-input failure mode.
- The committed source, tests, controllers, decisions and evidence reports
  survived. The four exact wheel URLs, sizes and SHA-256 values are recorded in
  the repository.
- The D-082 WAS backup under `/Users/debb/dev/research-evidence` survived and
  was reverified read-only at commit
  `2090a606f2723e4d57ef0090db55fd1bdab9427e`, tree
  `540d85cea6cc7ab50ee6f00b0dead2084c1d65de`, 298 `dist/` files and
  dist-manifest SHA-256
  `7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586`.
  It remains preservation evidence, not an active runtime, and this proposal
  does not restore, modify or use it.
- The unrelated PI routine-tool proposal remains excluded and untouched.

## Claim to be established

On the same Apple-silicon macOS/Python 3.9 environment previously evidenced,
the exact pinned provider can be restored into a durable ignored runtime and
the committed localhost package can complete its 53 bounded tests using only
literal-loopback listeners.

Success would establish only the bounded `fcf656d` localhost exchange. It would
not establish current-draft conformance, a browser or wallet exchange, parent
authorization, QR admission, public deployment or physical-robot execution.

## Recovery selection

Do not recreate every lost temporary tree. The localhost proof requires only
the four exact wheels and their verified provider installation. Recover those
into the durable shared store below.

Do not restore WAS: its durable backup is intact and WAS is outside this proof.
Do not reacquire the historical AAuth editor's copy or normative documents in
this recovery: they are not runtime inputs to the localhost test. A later
published-`-11` repin is a separate claim. If that work needs the historical
baseline, restore only commit `fcf656de1926535f5bd6fc0538147ead6646e727`
and require protocol SHA-256
`295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`;
never substitute upstream `HEAD`.

## Durable shared-store layout

Derive the repository root from each controller's resolved path and derive its
sibling durable evidence root as:

`<repository-parent>/research-evidence/soga/`

On the present machine that resolves to
`/Users/debb/dev/research-evidence/soga/`. All local agents may inspect this
stable location. Use owner-only permissions and these children:

- `inputs/aauth/fcf656d/wheels/` — the four exact wheel replacements;
- `runtimes/aauth-fcf656d-provider/site-packages/` — the verified provider;
- `runtimes/aauth-fcf656d-provider/scratch/` — bounded install scratch;
- `executions/localhost-gateway/` — bounded run evidence; and
- `manifests/` — machine-readable inventories for independent checking.

Runtime bytes remain outside the repository and must never be staged or
committed. Add a small committed
`knowledge/working/EXTERNAL_INPUT_MANIFEST.md` that records each dependency's
purpose, durable path, version/commit, byte identity, authorizing decision,
preservation-versus-runtime status and last verification date. This committed
index is the common discovery point for every agent.

The sibling-derived layout removes personal and `/private/tmp` assumptions
while giving this checkout one deterministic shared store. Cross-platform
portability is not claimed because the wheels and interpreter are
platform-specific.

## Phase 1 — create-only recovery and portability package

Create or modify only:

- `knowledge/working/EXTERNAL_INPUT_MANIFEST.md`;
- `tools/m02_aauth_fcf656d/restore_demo_runtime.py`;
- `tools/m02_aauth_fcf656d/run_localhost_gateway_tests.py`; and
- focused static tests for path derivation, manifests, stop rules and evidence
  boundaries.

The recovery controller must:

1. accept no dynamic URL, digest, filename, version or target;
2. derive the repository and runtime roots without a personal absolute path;
3. require the runtime target not to exist before acquisition;
4. retrieve exactly the four repository-recorded wheel URLs, sequentially,
   over HTTPS with zero redirects, finite time and byte limits and no retry;
5. require the exact recorded size and SHA-256 for every wheel before use;
6. install with `/usr/bin/python3` and the exact locally verified pip version,
   `--no-index`, `--no-deps`, `--only-binary=:all:`, `--no-cache-dir` and
   `--no-compile`, with update checks, advisory access and user packages
   disabled; before acquisition, require and record as explicit controller
   constants the pinned environment identity — interpreter version `3.9.6`,
   `sys.platform` `darwin`, `platform.machine()` `arm64` and pip version
   `21.2.4` — and stop on any mismatch; record the same four values in
   `EXTERNAL_INPUT_MANIFEST.md` as the committed comparison baseline;
7. make all network access impossible after acquisition;
8. verify the exact four-distribution identity, every wheel `RECORD`, absence
   of symlinks and absence of unaccounted installed files;
9. treat a residual Darwin `xcrun_db` scratch artifact under an exact rule that
   accepts zero or one such entry, requires regular-file type, mode `0600`,
   absence of symlink and a size not exceeding 4096 bytes, records its observed
   size and SHA-256 in evidence without comparison against a value carried from
   the lost 2026-09-21 installation, and rejects every other residual scratch
   artifact;
10. preserve complete redacted evidence, source/controller hashes and pre/post
    repository state in the durable shared store; and
11. refuse to create, modify, rename or delete any path beneath
    `<repository-parent>/research-evidence/` that is not inside
    `<repository-parent>/research-evidence/soga/`, protecting the accepted
    D-082 preservation evidence; and
12. fail closed without deleting diagnostic evidence or making a retry.

The corrected localhost controller must:

- retain every D-117 source hash, test count, socket-audit rule, timeout,
  output bound, redaction rule and permitted-stderr rule;
- derive `REPO`, provider root and evidence root from its own resolved path;
- refuse a provider outside the exact durable runtime root;
- verify the recovered provider tree before import;
- require clean exact committed protected sources; and
- retain literal `127.0.0.1`, ephemeral-port and default-deny socket controls.

Acceptance of the Phase 1 instrument will supersede the D-117 controller hash.
No execution authority is inherited from D-117; Phase 3 requires a new
prospective decision identifying the exact corrected controller.

No created or modified source may be imported, compiled, linted, tested or
executed during Phase 1. Both blind gates must review every complete file.

## Phase 2 — one recovery execution

After blind dual static PASS and a separate prospective PI authorization,
commit the exact reviewed Phase 1 package and execute the exact recovery
controller once. Network authority is limited to the four exact wheel requests.
No source-repository clone is required for the localhost run.

The recovery evidence requires blind dual review and PI acceptance before the
runtime may be used.

## Phase 3 — one localhost execution

After accepted Phase 2 evidence and a separate prospective PI authorization,
execute the exact committed localhost controller once. It may bind only
ephemeral literal-loopback listeners and run exactly the committed 53-test
suite. No automatic retry is permitted. Preserve bounded redacted evidence in
the durable shared store and produce a standalone repository evidence report
for blind dual review.

## Review batching

The gates review three claims, not each individual file operation:

1. **Plan:** this complete proposal once;
2. **Instrument:** the entire Phase 1 recovery/portability package once; and
3. **Evidence:** Phase 2 and Phase 3 evidence once per executed claim.

Gate 1 reviews protocol/profile fidelity and implementation detail. Gate 2
reviews network confinement, filesystem containment, negative cases, cleanup
and test completeness. Each first pass must separate all blockers from optional
improvements. Mechanical corrections may receive a diff-only recheck under the
adopted risk-based review method.

Because the `fcf656d` editor's copy and the four normative sources were lost and
are deliberately not reacquired here, no review under this proposal may rest on
a primary-specification citation. For Claims 1 through 3 the protocol/profile
claim is unchanged; fidelity is discharged by exact SHA-256 identity of the
fourteen protected sources to the set accepted under D-116 and D-117. Any
finding requiring a fresh normative-source citation is outside this recovery
claim and defers to the separate published-`-11` repin, which must first restore
commit `fcf656de1926535f5bd6fc0538147ead6646e727` and verify protocol SHA-256
`295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953`.

## Stop rules

Stop before use on any source/hash mismatch, platform/interpreter/pip mismatch,
redirect, extra request, unexpected wheel, dependency resolution, index query,
update/advisory access, install escape, symlink, unaccounted file, unexpected
scratch artifact, dirty protected source, non-loopback socket event, timeout,
overflow, redaction failure or incomplete evidence.

## Exclusions

This proposal authorizes nothing by itself. Until separate prospective PI
decisions are recorded, it authorizes no file implementation, download,
installation, import, native-code execution, test, listener or evidence run.

It does not authorize current-draft repinning, AAuth design changes, parent or
visitor authority, QR/session admission, Freewallet or WAS work, external
runtime services, personal data, payment, Misty access, physical actuation,
public deployment, G28 or G29. The unrelated PI routine-tool proposal remains
excluded and untouched.
