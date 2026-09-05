# M01 Misty Neutral Correction — Gate 1 Review

Date: 2026-09-05  
Reviewer: Claude, constitutional Gate 1  
Checkpoint: `37d02271b7f6db89e7b978bbec394e0509b09ba1`  
Ruling: PASS WITH CONDITIONS — advisory only

Claude independently reproduced 9 of 9 focused and 81 of 81 full-suite tests. It verified the ordered signal → bounded wait → neutral calls, truthful separate API acknowledgment and unknown physical/neutral outcome fields, candidate labeling, and the absence of network code or physical access.

## Condition discovered

The signal/wait/neutral sequence lacked exception safety. A response timeout after possible signal delivery could skip neutral, leave no cached receipt, and allow a retry to send a second signal. Gate 1 required neutral to remain attempted under uncertainty and an incomplete receipt to prevent redispatch. It also advised directly recording signal acknowledgment and testing duration boundaries.

No physical access or authorization occurred during review.
