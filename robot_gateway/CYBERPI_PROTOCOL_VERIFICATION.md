# CyberPi F3/F4 offline candidate verification

This draft models only candidate bytes and response grammar. The source is the G handoff
dated 2026-11-03, SHA-256
`169e866c5e079406538e51df7708fd04df4acc5cdcedb09398c8e55a91434c93`.
The handoff is engineering input. Its firmware and wire claims remain unverified.

| Fixture | Provenance and assumption | Bytes (hex) |
|---|---|---|
| Reported script | G readiness, TYPE_SCRIPT, reported checksum | `f30a1700280101001100637962657270692e6765745f627269282959f4` |
| Additive script | G readiness, TYPE_SCRIPT, stated additive rule | `f30a1700280101001100637962657270692e6765745f627269282984f4` |
| Reported online | G driver constant, TYPE_ONLINE, reported bytes | `f3f603000d00010ef4` |
| Reported offline | G driver constant, TYPE_ONLINE class, reported bytes | `f3f603000d00000ef4` |

The stated rule gives 0x84. The closed comparison also considers data-only
and script-only sums, their one's and two's complements, and XOR over each.
The data-only XOR is 0x18 and the script-only XOR is 0x09. No rule
in the named set yields 0x59. For the mode
vectors the additive comparison yields 0x0e online and 0x0d offline.
The reported offline checksum remains 0x0e. The ambient brightness expression
is sensor-related inert fixture data, excluded as a default first physical probe.

The response model uses a four-byte header, a bounded declared body of up to
256 bytes, a body checksum and an F4 footer. It accepts only the TYPE_SCRIPT,
mode 1 response candidate. The body contains an exact little-endian payload
length and a strictly decoded UTF-8 payload. JSON uses exact ret or err
envelopes, rejects duplicate keys and separates null from return and error.
The Python comparison accepts only explicit literal None fixtures. Every
stream has a 4096-byte lifetime budget. Retired indexes cannot be reused.

The manifest describes the staging snapshot. A later execution request must
pin the committed HEAD, hashes, exact command and interpreter, status and
absent evidence path. A changed protected snapshot requires repinning and
blind review. The runner records bounded combined child output, the exact
command, before/after hashes and the terminal result. The parent reads and hashes the exact bytes embedded in the isolated
child bootstrap. The controller has no child CLI entry point. Only the
bounded parent invocation can produce reviewable execution evidence.
The child denies every open after its audit hook is installed. The audit
self-tests use synthetic events without opening devices or creating sockets
or processes. The durable evidence destination is an absent child directory
of the canonical SOGA evidence directory.

Synthetic evidence can establish internal consistency for these candidates.
Hardware behavior, supported control and a gateway endpoint require separate
review and accepted physical evidence.
