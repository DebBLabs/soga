# M02 Stage 3A-R3 — Docker Containment Readiness Evidence

Date: 2026-09-08
Status: INDEPENDENTLY GATED PHASE 0 STOP — INCORPORATED UNDER D-045
Authorization: D-044
Authorization checkpoint: `main @ 4aaca2b`

## Boundary

D-044 authorized Docker Desktop startup, daemon readiness and immutable
local-image inventory before any synthetic containment tooling or candidate
execution. The independently reviewed proposal required `--pull=never` and a
locally cached arm64 image containing Node 24 or later. Absence of such an image
was a mandatory stop condition.

No image pull, build, load, import, tag, registry access, dependency operation,
source modification, Stage 3B work, wallet interaction, Person Server
integration, external exposure, personal data, payment, Misty access, physical
actuation, R3 protocol work, G28, or G29 was authorized.

## Docker readiness

The installed CLI reported Docker `28.5.2`, build `ecc6942`. The first daemon
readiness query confirmed that Docker Desktop was not running. Docker Desktop
was then opened under D-044. No password, privileged-helper, license,
subscription, update, network-access, or security prompt appeared.

The ready daemon reported:

```text
server=28.5.2 os=linux arch=aarch64 name=docker-desktop
context=desktop-linux
```

The daemon version satisfies the proposal's minimum 28.0.0 threshold. This
readiness result does not establish containment.

## Fixed resources and ports

Read-only inventory found:

- no existing container bearing the `soga-m02-r3` prefix;
- no existing network bearing the `soga-m02-r3` prefix;
- no listener on TCP port `46321`; and
- no listener on TCP port `46322`.

No R3 container or network was created.

## Immutable local-image inventory

Only two locally cached images were present:

| Immutable image ID | Repository:tag | Platform | Entrypoint/command basis |
|---|---|---|---|
| `sha256:de16a326b90ff2dad32c8679cdcee2b88cc69b8bc3b9897058bef1b7355a64c9` | `a2a-gateway-verify:latest` | linux/arm64 | `python -m verify.verify_server`; metadata declares Python 3.11.15 |
| `sha256:321521bce9cacd311d99e45ac0bc41bd27e81fc2538d30105e84d5ff6536b38a` | `a2a-gateway-gnap:latest` | linux/arm64 | `python -m gnap.gnap_server`; metadata declares Python 3.11.15 |

Both images are legacy A2A/GNAP research images. Neither image metadata
establishes Node 24 or later, and their declared Python entry points make them
inappropriate substitutes for the reviewed Node-image requirement. Neither
image was run, modified, tagged, or otherwise repurposed.

## Required stop

No suitable locally cached arm64 Node 24+ image was available by immutable ID.
The R3 proposal required an immediate stop at that condition and prohibited
pulling, building, loading, or importing a replacement image. Therefore:

- no synthetic preflight or candidate-startup script was created;
- no container or Docker network was created;
- no image was executed;
- neither exact candidate checkout was mounted, imported, served, or started;
- no registry or dependency command ran; and
- no application runtime network activity occurred.

Docker Desktop remains running pending explicit PI direction; no R3 workload is
running within it.

## Finding and holdpoint

Stage 3A-R3 ends at Phase 0 as a candidate gated negative result. Docker Desktop
and its daemon meet the reviewed version and architecture prerequisites, but
the host lacks the required already-local Node 24+ image. The authorized
no-acquisition boundary worked as intended by preventing an implicit registry
request or reuse of unrelated A2A/GNAP images.

This result establishes no Docker containment property because the synthetic
preflight did not run. It does not establish that a Docker approach is
unsuitable. Any acquisition of a pinned Node image would require a separately
reviewed PI decision covering source, digest, platform, registry access, and
post-acquisition verification. Stage 3B remains unauthorized.

Claude Gate 1 and Gemini/AGy Gate 2 independently confirmed this Phase 0 stop
before the PI authorized the separately reviewed digest-pinned image
acquisition under D-045.
