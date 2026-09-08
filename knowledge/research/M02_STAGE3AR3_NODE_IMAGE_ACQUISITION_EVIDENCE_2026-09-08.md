# M02 Stage 3A-R3 — Digest-Pinned Node Image Acquisition Evidence

Date: 2026-09-08
Status: ACCEPTED AS A GATED POSITIVE RESULT UNDER D-046
Authorization: D-045
Authorization checkpoint: `main @ f106030`

## Boundary

D-045 authorized exactly one `linux/arm64` pull of the Docker Official Node
image identified by full digest in the independently reviewed acquisition
proposal, local immutable-metadata inspection, and one disposable
network-disabled `node --version` verification container. It authorized no
containment preflight, port publication, candidate execution, Stage 3B, or
other excluded activity.

Selected reference:

```text
docker.io/library/node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb
```

## Exact acquisition

The complete executed command was:

```text
docker pull --platform linux/arm64 docker.io/library/node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb
```

It ran once. Docker reported five content layers downloaded and completed, then:

```text
Digest: sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb
Status: Downloaded newer image for node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb
```

No login, interactive prompt, alternate image, mutable-tag pull, mirror
selection, build, load, import, tag, push, package operation, or second pull
occurred.

## Immutable local metadata

Local inspection by the same full-digest reference returned:

```text
id=sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb
repo_digests=["node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb"]
os=linux
architecture=arm64
created=2026-08-27T17:03:19.405438408Z
entrypoint=["docker-entrypoint.sh"]
cmd=["node"]
env=["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","NODE_VERSION=24.20.0","YARN_VERSION=1.22.22"]
labels=null
```

The local immutable image ID and repository digest equal the selected arm64
manifest digest. The OS, architecture, and declared Node version match the
reviewed selection.

## Isolated runtime verification

The complete executed verification command was:

```text
docker run --rm --pull=never --platform linux/arm64 --network none --read-only --cap-drop ALL --security-opt no-new-privileges:true --memory 128m --cpus 0.5 --pids-limit 32 --name soga-m02-r3-node-verify docker.io/library/node@sha256:e9b5516b06baeaea9a8e65a7aec6a85fbb960a30b52b66968f2c8092b3e2a3eb node --version
```

The container had no mounts or published ports. It returned exactly:

```text
v24.20.0
```

and exited successfully.

## Cleanup and retained state

Post-run inspection found:

- no container bearing the `soga-m02-r3` prefix;
- no Docker network bearing the `soga-m02-r3` prefix;
- no listener on TCP port `46321`;
- no listener on TCP port `46322`; and
- the selected image retained under only the expected repository digest, with
  immutable local image ID equal to that digest.

The two legacy A2A/GNAP images remain untouched. Docker Desktop remains open;
no R3 workload is running.

## Finding and holdpoint

The selected Docker Official Node image was acquired and verified exactly as
authorized. This establishes the identity, platform, and Node version of the
locally cached R3 input. It establishes no container-network containment,
candidate reachability, wallet behavior, WAS conformance, Person Server
composition, or Stage 3B result.

The retained image may not be used for the synthetic containment preflight
until that preflight and every startup script receive full independent review.
Claude Gate 1 and Gemini/AGy Gate 2 independently returned PASS. D-046 accepts
this acquisition evidence and treats the retained full-digest image as an
eligible input for creation—but not execution—of the Stage 3A-R3 scripts.
Stage 3B remains unauthorized.
