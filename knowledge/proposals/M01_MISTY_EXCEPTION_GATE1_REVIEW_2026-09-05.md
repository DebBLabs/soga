# M01 Exception-Safe Neutral Return — Gate 1 Review

Date: 2026-09-05  
Reviewer: Claude, constitutional Gate 1  
Checkpoint: `6e530ff41f783f866459dd38a337532372812ea7`  
Ruling: PASS — advisory only

## Independent verification

Claude independently reproduced 11 of 11 focused tests and 83 of 83 full-suite tests. It verified that:

- signal uncertainty does not prevent the neutral attempt;
- incomplete receipts remain truthful;
- signal, wait, and neutral status are directly recorded;
- first-attempt receipts seal the request against redispatch;
- invalid duration bounds are rejected; and
- no network code, hardcoded target, discovery, query, or physical test exists.

The earlier exception-safety condition is resolved. A minor non-blocking observation recommends dedicated tests for wait-error and neutral-error branches before physical configuration.

## Remaining prerequisites outside code preparation

1. Adopt the canonical Misty A platform identity and verified address.
2. Establish isolated network placement.
3. Inspect hardware and battery.
4. Verify an independent physical safety halt and operator-stop procedure.
5. Adopt and physically verify pink, yellow, and the one-second interval.
6. Keep the local Person Server correctly labeled as a test fixture.
7. Independently review the exact physical-run checkpoint.

No physical access or authorization occurred during review.
