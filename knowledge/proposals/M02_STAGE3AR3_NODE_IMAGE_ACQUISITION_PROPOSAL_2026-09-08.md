# M02 Stage 3A-R3 Proposal — Digest-Pinned Node Image Acquisition

Date: 2026-09-08
Status: AUTHORIZED UNDER D-045 — ACQUISITION NOT YET STARTED
Prepared from checkpoint: `main @ 4aaca2b`

## Purpose

Resolve the Phase 0 stop recorded in
`knowledge/research/M02_STAGE3AR3_DOCKER_CONTAINMENT_EVIDENCE_2026-09-08.md`
by acquiring exactly one Docker Official Image needed for the already-reviewed
Stage 3A-R3 synthetic containment preflight. This is a narrow supply operation,
not containment execution, candidate startup, or Stage 3B.

## Selected image

| Property | Selected value |
|---|---|
| Registry repository | Docker Official Image `docker.io/library/node` |
| Human-readable tag used only for source cross-check | `24.20.0-bookworm-slim` |
| Required platform | `linux/arm64` |
| Required manifest digest | `sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb` |
| Expected Node runtime | `v24.20.0` |
| Reported compressed size | approximately 76.85 MB |

The executable image reference must be the repository plus digest, not the
mutable tag:

```text
docker.io/library/node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb
```

Docker Hub currently identifies that arm64 digest with the official
`24.20.0-bookworm-slim` image. The Node Docker project identifies
`bookworm-slim` as a supported Node 24 arm64 variant and its Dockerfile declares
Node `24.20.0`. Sources checked:

- <https://hub.docker.com/_/node/tags?name=-bookworm-slim&page=1>
- <https://hub.docker.com/layers/library/node/24.20.0-slim/images/sha256-e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb>
- <https://github.com/nodejs/docker-node/blob/main/24/bookworm-slim/Dockerfile>
- <https://github.com/nodejs/docker-node/blob/main/versions.json>

These public references support selection; the post-pull local inspection is
the controlling evidence for what was actually acquired.

## Permitted acquisition

After independent review and explicit PI authorization, run exactly one
digest-pinned pull for `linux/arm64` from `docker.io/library/node`. Docker may
perform the registry authentication-token exchange and content-layer downloads
intrinsic to that one pull. No Docker login, account credential, subscription,
private registry, other repository, tag-only pull, mirror substitution, build,
load, import, tag, push, or package-manager operation is permitted.

The complete pull command must be recorded before execution and must include:

- `--platform linux/arm64`;
- the full `docker.io/library/node@sha256:...` reference above; and
- no other image reference.

If Docker requests a login, license, subscription, privileged helper, update,
mirror choice, credential-store change, or other interactive decision, stop for
the PI. If the registry reports a different platform, digest, or source, stop.

## Mandatory post-pull verification

Before creating any R3 network, published port, preflight script, or candidate
container:

1. Inspect the locally stored image and record its immutable image ID,
   repository digest, OS, architecture, creation time, entrypoint, command,
   declared environment, and labels.
2. Require `linux/arm64` and a repository digest matching the exact selected
   manifest digest.
3. Run only `node --version` in one disposable verification container using
   the digest reference, `--pull=never`, `--network none`, read-only root
   filesystem, all capabilities dropped, `no-new-privileges`, finite memory,
   CPU, and PID limits, and no mounts or published ports.
4. Require exact output `v24.20.0` and exit status zero.
5. Verify the disposable verification container is removed and that no new
   Docker network, listener, or fixed-name R3 resource exists.

Any deviation is a stop condition. Do not attempt repair, a second pull, tag
substitution, platform emulation, or candidate execution.

## Image lifecycle

The verified digest-pinned image may remain cached only as the selected input
to the already-authorized Stage 3A-R3 tooling review and containment preflight.
It grants no permission to execute that preflight before its scripts pass both
independent reviews. Remove the image after the R3 disposition unless the PI
explicitly adopts its continued retention. Do not remove either legacy
A2A/GNAP image.

## Evidence and holdpoint

Create a standalone acquisition record containing the exact command, observed
registry reference, pull result, immutable local metadata, isolated runtime
version check, cleanup checks, and any prompt or deviation. Both independent
gates must review the acquisition evidence before the image is treated as an
eligible R3 input.

## Explicit nonauthorization

This proposal authorizes nothing. It permits no pull or registry access until
both gates pass and the PI authorizes it. It permits no Docker build, image
modification, dependency installation, source modification, network or
container preflight, port publication, candidate startup, Stage 3B code or
tests, wallet interaction, Person Server integration, external exposure,
personal data, payment, Misty access, physical actuation, R3 protocol work,
G28, or G29.
