# G27 prototype implementation gaps

- Grant consumption and the one-live-session policy are atomic only among
  threads sharing one `SessionGrantService` instance. Multi-process,
  multi-host, restart, and durable-store concurrency are unaddressed.
- Grant integrity, QR encoding, authentication, durable storage, and service
  ownership remain uninstantiated because the adopted contract leaves them
  open.
- Fake surfaces record receipt only. They cannot establish dispatch to a real
  robot, physical start, completion, interruption, neutral state, or safety.
- The versioned primitive/composition catalog, interruption classifications,
  safe boundaries, and claimed receipt states are not instantiated in the
  adopted artifacts. Per-primitive acceptance cases cannot be generated until
  those inputs are supplied; this prototype does not invent them.
- Runtime event history is process-local, memory-only, and unbounded. The
  interactive terminal is an acceptance surface over that same state; it is not
  a durable audit service or a participant application.
- The package contains no network transport, Misty address, robot discovery,
  hardware adapter, or actuation mechanism.
