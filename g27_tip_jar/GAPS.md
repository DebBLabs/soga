# G27 prototype implementation gaps

- Grant consumption and the one-live-session policy are atomic only among
  threads sharing one `SessionGrantService` instance. Multi-process,
  multi-host, restart, and durable-store concurrency are unaddressed.
- Grant integrity, QR encoding, authentication, durable storage, and service
  ownership remain uninstantiated because the adopted contract leaves them
  open.
- Fake surfaces record receipt only. They cannot establish dispatch to a real
  robot, physical start, completion, interruption, neutral state, or safety.
- `OperatingStateMachine.action_finished(observed=True)` can represent the
  adopted model's future independently observed completion state, but this
  prototype has no observation source or evidence binding. The active runtime
  always calls it with `observed=False`; the bare Boolean branch is not a
  completion-verification mechanism and must not be exposed as one.
- The versioned primitive/composition catalog, interruption classifications,
  safe boundaries, and claimed receipt states are not instantiated in the
  adopted artifacts. Per-primitive acceptance cases cannot be generated until
  those inputs are supplied; this prototype does not invent them.
- D-023 specifies per-action cardinality for the first mission (including
  greeting once, bounded choice changes, one dance, a bounded conversation turn
  count, and close once), but this prototype does not enforce those counters.
  Single-use grants and request idempotency do not substitute for per-action or
  per-session turn limits.
- Runtime event history is process-local, memory-only, and unbounded. The
  interactive terminal is an acceptance surface over that same state; it is not
  a durable audit service or a participant application.
- Grant and session state are also process-local and memory-only; stopping the
  process loses them.
- The D-025 localhost services are threads in one process. They do not establish
  process-crash isolation, multi-process authority, restart recovery, or
  distributed atomicity.
- The governance relay transports a separately supplied decision; it is not a
  governance evaluator and does not decide whether an action should be allowed.
- The localhost transport has no TLS, service identity, authentication, durable
  store, or production deployment model. It binds only to loopback and uses
  ephemeral ports for acceptance testing.
- The package makes no MCP implementation or conformance claim. It contains no
  external-network transport, Misty address or credential, robot discovery,
  status query, hardware adapter, or actuation mechanism.
