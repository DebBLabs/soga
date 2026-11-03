# Misty-first shared robot gateway

This additive package implements only the reviewed D-194 source boundary.

- The accepted public Flow A presentation remains robot-free and cannot import
  or construct this package.
- Misty B is the only implemented physical adapter target, but physical access
  remains unauthorized.
- mBot2 is represented only by the zero-I/O unavailable identifier
  `urn:debblabs:mbot2-iiw:unavailable`.
- A successful HTTP response is not a physical-outcome claim.
- The exact utterance-complete event starts the five-second response window.
- Missing completion and ambiguous delivery fail closed and require a bounded
  stop attempt; physical outcome remains unknown.
- No participant secret, token, lease, browser identifier or fictional-parent
  receipt crosses the robot boundary.
- Until the separately reviewed dual-network phase, participant devices never share Beryl with a robot; the public launcher remains robot-free.
- A dispatch/stop race permits exactly one bounded stop command. If Speak remains outstanding or its delivery is ambiguous, the target locks for operator reset and requires the independent local stop; no compensating second robot command is sent.

The transport is pinned to the two literal Misty B TTS URLs and disables proxy
use, redirect following, retry, discovery and fallback. Nothing in this package
authorizes import, tests, network access, robot contact, speech or movement.
