# Single-owner two-robot switching revision

Static integration draft. The gateway is constructed privately by RobotSwitcher
with an identity capability required on all mutating gateway calls. Retained
legacy coordinator references have no capability and their reserve/release calls
are refused. The gateway rejects unselected targets. The registry is immutable.

The operator service calls select, allow_open, completed, finish, neutral,
recover and tick through the same owner. The authorize callback must verify an
issued allow decision and return the exact selected platform/session/decision
Invocation. Session, decision and request reuse are refused. This callback and
the observation verifiers are trusted runtime components, not participant inputs.

Startup selection requires a fresh neutral observation for that robot bound to
a unique run_id. The service must generate a new run_id per process incarnation.
Observation verifiers receive the active Invocation, including Misty utterance
derivation inputs, session and decision. A verifier must check fresh, authenticated
robot facts and return literal True. Neutral covers speech stopped on Misty, or
cleared display and LEDs and cancelled pending output on mBot2. Transport
acknowledgement alone is insufficient. The unchanged unavailable placeholder
is explicitly handled as a zero-I/O terminal result.

Reservation precedes dispatch publication. Stop and dispatch receipts remain
separate. Every termination records terminal_event, completion_verified and
neutral_verified. These fields map explicitly to coordinator lifecycle facts;
the execution surface is this owner rather than a claim of speech completion.
Missing completion or an uncertain dispatch produces one stop and a lock.
Stop during dispatch locks. Neutral waits and stop waits have three-second
deadlines. Recovery requires fresh neutral proof and no in-flight dispatch;
only then are reservation and operator lock cleared. No repeated stop is sent.

The service must drive tick at a bounded interval and prevent dispatch when
that driver is unhealthy. Concrete driver implementation, robot-specific event
verifiers, the issued-decision authorizer, mBot2 wire transport and live runtime
wiring remain pending. Runtime use is barred until these are reviewed and wired.
Injected callbacks and adapter calls must be independently bounded. Proof and
authorization sets persist for the bounded operator session lifetime.

Tests use the real staged gateway with the committed Misty adapter under fake
transport and the real zero-I/O mBot2 placeholder. They are authored for future
execution against a staged package containing the committed dependency modules.
They have not been imported, compiled, linted or run.

## Revision 3 disposition and concurrency correction
The owner-capability gateway is now a new module, owned_gateway.py, with class
OwnedRobotGateway. The committed gateway.py, coordinator and accepted suites
are preserved byte-for-byte. Runtime wiring must choose this separate owner
path explicitly. It is not a replacement for the accepted coordinator path.
No switching commit may precede acceptance of the current CyberPi synthetic
evidence without a separately reviewed repin of HEAD and protected artifacts.

Switcher-owned operations remain counted through dispatch and stop receipt
postprocessing. Recovery, neutral release and selection cannot overtake those
operations. Returning callbacks bind the exact Invocation before updating state.
Concurrent callers wait at most three seconds for STOPPING; if still pending,
the returned phase remains explicitly STOPPING with no claim of completed stop.
Gateway reservation flight is cleared in finally even if receipt conversion
fails. Terminal records persist by request, and zero-I/O neutrality inference
is labeled separately from verified observation and requires the placeholder
platform and registered adapter identity. This capability is an in-process
ownership guard, not a security boundary against arbitrary Python introspection.
