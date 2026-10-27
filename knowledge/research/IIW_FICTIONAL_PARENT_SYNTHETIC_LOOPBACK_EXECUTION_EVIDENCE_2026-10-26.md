# IIW Fictional-Parent Synthetic Loopback Execution Evidence

Date: 2026-10-26
Execution decision: D-151
Execution commit: `5b726441629698584826ecee37674c51146342d9`
Result: GATED NEGATIVE — one of 128 tests failed

## Accepted inputs

- execution proposal SHA-256:
  `487d67c3c7b826d29d1048dc88ddc057c2c9783a701bf1018fc4f90d82e93aef`;
- runtime manifest SHA-256:
  `2e84c1e92d7e9e4571c4c16bb642da4b4773ce6e45451cae0a2a6caf63dbb205`;
- controller SHA-256:
  `ed0805e15e7765a3ee7619e711fd0d1d64a5eeadca40fc2a0542e1f3a33d185a`;
- durable provider manifest SHA-256:
  `7d409a9990c2c57623b395d6a74643263f5c4c4e89b750b4a87e38bd680b4c8e`.

The run record preserved the complete 35-entry protected source set. It equals
the runtime manifest's protected set after excluding the separately recorded
fictional-parent controller. The exact hashes are:

- controller chain: demo operator `37bc90282e1cf99226c8ce8086b82644a5c429cb7048f6ff9048778bbd95e112`,
  approval pending `fb76b2135042178a6915ddca03f409e85981ddf40df49937839355540aab0ee7`,
  other-party approval `b0fa483f3ab0ea343de847b8b4acb78096afc81bd81d3f69b0206ef579a3bdc1`,
  localhost gateway `2a3c04506fdfa371f63680a874979421e3288ca07bb421e26e17c2af0c11b32a`;
- fictional-parent files: README `ec58edd4fceafbecf51c7103f25591cb5f686c277a291ef2433b1e18ac3a3a92`,
  `__init__` `98d94e37c9f0a72053e6f51835e464f4b4b8168d5cc69404098346a9aaca0ade`,
  connection `d3cfec526e50d0443372d8b7ee66a269a8f61afdf36b86c33157b83c8a6cc24c`,
  gateway `6bb1c45424adb71008600e0ebf6bd988efe325c5111d557bddf8fba70b1e30f0`,
  session `9e456f08bcc5351c9b47dd6e30809ae1cb16804505bbba77113fa65ec3c68972`;
- QR-session files: README `7d73b5c5dd0490031027059f31ca6ec1e942a628e54141b03e7b69178340e8f8`,
  gateway `9c5824df29ff0909d76e22c65af0ba277cda6d4c9370a720a2613d4256c6e3b8`,
  package `3f079c3bd7c834758a1062926f5083d556497ab8013a2426ea5bef95584495c9`,
  session `2aeeb9bd0e355b2d19521665dbc94569058355e34b365d534282d78f423c7907`;
- AAuth/SOGA sources: `__init__` `c480bf75ecea51a368627cb00dabdd96ed9e48df784497ce9b7efee80f8f58e8`,
  approval pending `18717f7b64007c92f6fb893498f1329b8ed049bb6636eb586a44267588bea47b`,
  demo operator `b65160deffccf80220a0f466384a98ad1c3d21101dc44a1ee3b5d8099bf238a3`,
  exchange `ed82a97873f7c535917dd0ecbecf81e31287015c3dfbc77396cb3dc8675fdf0f`,
  HTTP signatures `f6ae4f4463852b310d09608d4a60084a566733e857098bcd42f2bc1a659cab65`,
  identifiers `54c495785fc5fc26d24e3c406bb334d0022410faff37696d40220e1b83759579`,
  JOSE `cda9b577746116e65c34977706593475a8637a3ec6823375dda7baffa961cdd4`,
  localhost `513f5947582873e741c1e3fbd1a5876805121dd36726745b090b99cdd20d26d7`,
  metadata `c1a473ee3f21ed4832668fadb87e9db72dbade4278f99aa35efff868db225a5a`,
  other-party approval `c5a244da3ef5e6694df663af2ff0fb5cd83cdf928fa49c1ab708b197c35d78b0`,
  profile `fb7b9b51ada64c7e45f61eb24991078cbe5d172cdf781887bf6843c27fb7afbf`,
  SOGA supervision `af1f19eb0710027d7c161e07e060813b9be3f578f252f2a9f3d7f942640dee6a`,
  structured fields `9d774a03dd096577a9ce917b40f4c3693e30758319fa05f455feb3b734c78a71`,
  tokens `34f705123acb83772f9f2428409593233f004384c46b2cf96f0358615cf2dd04`;
- tests: fictional parent `e7bfe9af2b333f591b7f47b203782b5848283479036a99bc684714c5429d826c`,
  QR session `e700137956d85183a474d08ac7d67a2da2d073471acc65616ef31c7d4a113df4`,
  approval pending `b0936449de6a143102ac012f7783ef138a5fe743a56fae41093b53d2eda37c69`,
  demo operator `25abd4b5af7f8eaeaf1585d641bb8e08d024b2cabd09c685c0a319cad5b50f67`,
  Phase 1 `89b71359c6c071453fab289aa85443aa4f7156e4a2d263d8ac12f85bee4deaad`,
  exchange `89dcede33566a1531d9c5630d9598da940ffd7ac99dfb4610a875e3559aad916`,
  localhost `d591d91085107f76e4a9afa46b003197bda0a722460741600594a043d96306bb`,
  other-party approval `a24e5f76832a5b8df7e9ed67409c18b03ce4a2b773103d813285048019e30a66`.

Provider verification covered 190 RECORD entries and preserved these pinned
provider-file hashes: `_cffi_backend.cpython-39-darwin.so`
`c6a40bac9fb5325237fe2ecba85bad7f9a80f6c73d5a79e46e2a9d92884957b0`,
`cryptography/__init__.py`
`9ad86e52b4dde0544e0a9518ad322a863cfab3a4fd763019ad5ee7675a0c9b6a`,
and `cryptography/hazmat/bindings/_rust.abi3.so`
`b172579de53a4f501caff84cfb19539b0fca457843a24c3d593fe6d405dd7494`.

## Pre-start observations

- local `main` and `origin/main` both resolved to execution commit
  `5b726441629698584826ecee37674c51146342d9`;
- source basis `ec93a4bf604f078212ae015a0bec42252bf60032` was an ancestor;
- the complete source-basis diff contained exactly
  `knowledge/proposals/IIW_FICTIONAL_PARENT_SYNTHETIC_LOOPBACK_EXECUTION_PROPOSAL_2026-10-26.md`,
  `tools/iiw_fictional_parent/runtime-manifest.json`,
  `knowledge/strategy/DECISION_LOG.md` and
  `knowledge/working/CURRENT_STATE.md`;
- protected tree IDs matched the source basis exactly: `engines`
  `edb7a6500a34f1b1184adc7d79e96fb4846e75f7`, `input_adapters`
  `8f57ecbb39718327cb93a691d0dd56223489463a`, `verify`
  `db72f46f5d4c2e99292d219dde18f3b73019d9ec` and `advisory`
  `20b61d89ddca8002671a30976dc690f7a80e6653`;
- tracked status was empty; the excluded PI proposal remained the sole untracked
  repository entry and was not opened;
- runtime identity was Darwin arm64, Python 3.9.6 at
  `/Library/Developer/CommandLineTools/usr/bin/python3`;
- the fixed evidence directory was absent, no
  `/private/tmp/iiw-qr-manifest-*` directory existed, and no attributable prior
  controller process or listener was present.

## Invocation

The controller was invoked exactly once, without automatic retry, from
`/Users/debb/dev/soga-clean` as:

`/usr/bin/python3 -I -S -B /Users/debb/dev/soga-clean/tools/iiw_fictional_parent/run_static_and_loopback_tests.py`

The parent environment was exactly:

- `PATH=/usr/bin:/bin:/usr/sbin:/sbin`;
- `LANG=C`;
- `LC_ALL=C`;
- `GIT_OPTIONAL_LOCKS=0`;
- `PYTHONDONTWRITEBYTECODE=1`;
- no `IIW_FICTIONAL_PARENT_TEST_CHILD` variable.

## Preserved evidence

Directory:
`/Users/debb/dev/research-evidence/soga/executions/iiw-fictional-parent-v1`

- `fictional-parent-evidence.json`: SHA-256
  `389882ae10f2df27d86e7600479b6390412c30b816ebf15308433c1e8c34aade`,
  19,145 bytes;
- `fictional-parent-stderr.bin`: SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`,
  0 bytes;
- `run-record.json`: SHA-256
  `9387a4ea73c70fa1caec0e1a92b10dd7ac27d630b267f5d826817a780289e623`,
  5,239 bytes.

The parent started at epoch `1793066720.818645`
(`2026-10-26T22:05:20.818645-04:00`) and ended at epoch
`1793066773.6382909` (`2026-10-26T22:06:13.638291-04:00`), after
52.81964588165283 seconds. The child reported 51.684 seconds. The controller returned `1` and
recorded `IIW_FICTIONAL_PARENT_EXECUTION_NEGATIVE`. There was no timeout,
stdout overflow, stderr overflow, parse error, disallowed stderr or post-run
verification error.

## Test result

The child loaded the exact 128-test composition and recorded:

- tests run: 128;
- failures: 1;
- errors: 0;
- skips: 0;
- expected failures: 0;
- unexpected successes: 0.

The literal-loopback socket audit recorded 149 binds and 422 connects.

The payload recorded 42 `module_origins`: 29 resolved beneath
`/Users/debb/dev/soga-clean` and 13 beneath the pinned provider root
`/Users/debb/dev/research-evidence/soga/runtimes/aauth-fcf656d-provider/site-packages`.
It recorded these ten `package_origins`:

- `iiw_fictional_parent` → `iiw_fictional_parent/__init__.py`;
- `iiw_fictional_parent.connection` → `iiw_fictional_parent/connection.py`;
- `iiw_fictional_parent.gateway` → `iiw_fictional_parent/gateway.py`;
- `iiw_fictional_parent.session` → `iiw_fictional_parent/session.py`;
- `iiw_fictional_parent_tests` → `tests/test_iiw_fictional_parent.py`;
- `iiw_qr_session` → `namespace`;
- `iiw_qr_session.gateway` → `iiw_qr_session/gateway.py`;
- `iiw_qr_session.package` → `iiw_qr_session/package.py`;
- `iiw_qr_session.session` → `iiw_qr_session/session.py`;
- `iiw_qr_session_tests` → `tests/test_iiw_qr_session.py`.

The sole failure was:

`test_05_no_standing_policy_mutation (iiw_fictional_parent_tests.FictionalParentTests)`

At `tests/test_iiw_fictional_parent.py:83`, the assertion expected
`self.base.policy.calls` to remain `0`; the observed value was `1`.

All other 127 tests passed, including the accepted AAuth/SOGA, QR-session and
remaining fictional-parent tests. This report records the observed failure but
does not diagnose its cause or authorize a correction or retry.

## Post-run state

- protected sources, provider, runner and runtime state were unchanged;
- the parent and child ended;
- no attributable listener remained;
- no `/private/tmp/iiw-qr-manifest-*` directory remained;
- the durable evidence directory is preserved unchanged for blind dual review;
- no retry occurred. The single D-151 attempt is consumed.

## Claim boundary

This is a gated negative execution result. It establishes neither the complete
fictional-parent composition nor complete AAuth conformance, verified identity,
a real parent-child relationship, parental or legal authority, legal consent,
a live QR or phone interaction, Beryl/LAN behavior, presentation integration,
wallet/WAS, Misty, physical action, G28 or G29.

No diagnosis, source correction, retry or further execution is authorized by
this evidence report.
