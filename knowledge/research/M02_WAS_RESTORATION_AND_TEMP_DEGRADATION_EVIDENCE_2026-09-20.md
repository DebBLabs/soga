# M02 WAS Restoration and Temporary-Path Degradation Evidence

Date: 2026-09-20
Accepted repository checkpoint: `b89b5de02686586e1877e747b2d07db60fc8e5c3`
Classification: accepted bounded restoration result and subsequent durability finding

## Result

The PI prospectively authorized one execution of the reviewed offline restoration utility, SHA-256 `1529980ad1b1e4c893c6aa29968434b1b985b132ecafd8a80d4d0a7df30e304b`. It ran once on 2026-09-18, exited zero in 8,347 ms, and was not retried.

Immediately after execution, the utility verified exact logical equality across the accepted durable backup, its 29,235-row manifest, and `/private/tmp/m02-stage3lib-20260910`. It also verified candidate commit `2090a606f2723e4d57ef0090db55fd1bdab9427e`, tree `540d85cea6cc7ab50ee6f00b0dead2084c1d65de`, clean tracked status, 298-file `dist/` manifest `7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586`, and expected absence of `dist/build-info.json`.

Retained primary records:

- `restore-attempt.json`: SHA-256 `d9214614eef174cc4879d06f0ce08320c8022d0f7e540aa50e3acf346c499a56`
- `restore-verification.json`: SHA-256 `ad6156860fb92cf2949d320a4eb0dc1b1959fd34fd153fe535cd3598ecaf09fa`
- accepted backup manifest: SHA-256 `ceef625d8b233b55d8f7494347c6273301603fb7c9a208d4ff31115496e83f0c`

Claude independently recomputed the immediate restored/backup/recorded three-way equality and candidate identity and found the execution evidence factually accurate. Claude disclosed that it authored the proposal and utility and therefore supplied corroboration rather than an eligible final gate.

On 2026-09-20, AGy independently confirmed the retained historical evidence but found that the live temporary tree now contained 29,230 entries. Five empty directories were absent: `.git/objects/info`, `.git/refs`, `.git/refs/heads`, `.git/refs/tags`, and `.npm-cache/_cacache/tmp`. Local Git no longer recognized the temporary candidate. The accepted durable backup still contained all 29,235 entries and remained unchanged. The timing and filesystem evidence make macOS periodic temporary-directory maintenance the probable cause; this record does not claim the deletion mechanism was directly observed.

## Disposition and review basis

The PI read the two reports, formally accepted them and the coordinator's conclusion, and accepted this disclosed basis: AGy independent eligible review plus Claude technically independent recomputation disclosed as ineligible corroboration. This is a package-specific PI deviation, not a change to the standing review method and not a representation that Claude was an eligible gate.

Accept the 2026-09-18 restoration as an historically verified positive result. Do not accept the 2026-09-20 temporary tree as an intact runtime input. The durable backup and restoration mechanism remain valid; the hardcoded `/private/tmp` runtime strategy does not support multi-day reliance.

## Claim boundary

Equality was logical path/type/mode/size/content/symlink-target equality. It does not establish owner, timestamp, inode, hard-link or xattr fidelity, dependency executability, a completed upstream build, live Person Server integration, Freewallet integration, AAuth conformance, or governed mission execution. No candidate, harness, wallet, Person Server, Misty, listener or external service ran during restoration or review.

B-043 remains open. Before further WAS-dependent execution, use a separately reviewed durable/configurable runtime path or perform a separately authorized restoration followed by immediate identity verification and same-session use. No repeat restoration, source change, candidate execution, integration, commit/push, Misty access, G28 or G29 is authorized by this evidence.

## Process follow-up

Define a reviewer-capacity fallback that does not automatically treat a subagent reviewing its parent or related authoring agent as independent. Independence must be assessed from actual authorship, context exposure and package-specific contribution, with PI-visible disclosure and no backdating.
