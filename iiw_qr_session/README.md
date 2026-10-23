# IIW QR participant-session fixture

This source-only package defines a bounded adult-participant QR session. It is
not an AAuth authorization flow and does not call any AAuth/SOGA production
seam. In particular, it does not characterize the participant as a parent,
guardian, representative or local operator.

The two fixed choices are `ALLOW_DIRECTED_RESPONSE` and
`DECLINE_DIRECTED_RESPONSE`, bound to fixture mission
`iiw-adult-participant-fixture-v1`, action `address_participant` and participant
`adult-demo-participant`. The callback used by the synthetic tests records only
that fixture event.

The participant may choose nothing and leave. A recorded choice is explicitly
unverified demo input; it establishes no identity, consent for another person,
parental authority or legal authority.

## Execution boundary

This package has not been imported, compiled, linted, tested or executed by its
creation. Do not start it directly. Its controller is also create-only and
requires blind static review, commit and separate prospective authorization
before any loopback test. The later execution request must provide the exact
bundle root and an independently reviewed runtime manifest matching the host
system, architecture, Python version and complete runtime file hashes. A
non-loopback Beryl/phone test requires another
reviewed instrument and authorization. Public-event use requires a separate
G29 and privacy disposition.

The eventual operator must supply an exact private IPv4 address and complete
the reviewed interface, route, port and Beryl-isolation preflight before any
non-loopback bind. Shared venue Wi-Fi is prohibited. Stop by cancelling the
single session, shutting down the server and verifying that no listener or live
capability remains. A failed start or test is terminal; do not retry without
new authority.
