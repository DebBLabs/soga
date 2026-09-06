# M01 Physical Execution Evidence

Date: 2026-09-05  
Authorization: D-032  
Reviewed execution code: `2afcc6fa21ed956e0bc2c0f82b2d31900dac498f`  
D-032 record: `9978f6aea08856a0881173bc53d76a6dc72c3c5b`  
PI/operator: Deb Bucci

## Authorized binding and action

- Platform: `urn:debblabs:misty-a:20221304273`
- MAC: `00:d0:ca:01:a2:61`
- DHCP target: `http://192.168.1.183/api`
- Action: `m01.signal_light`
- Sequence: pink `(255,105,180)` → 1.0 second → yellow `(255,255,0)`
- Cardinality: one governed action; no retry

## Terminal evidence

The first runner invocation ended before dispatch because its confirmation did
not match. The second used `EXECUTE m01.signal_light` and reported:

```text
Governance: granted
Adapter: robot_api_acknowledged
Signal API: robot_api_acknowledged
Neutral API: robot_api_acknowledged
Physical outcome: unknown
Neutral outcome: unknown
```

Successful grant reference: `m01-grant:m01-physical-8d01843221fb7711`.

## PI observation

Deb directly observed Misty A turn pink. Deb initially described the final
color as yellow or green, then concluded it was yellow given the commanded
payload and API acknowledgment. Record:

- signal: **pink directly observed**;
- neutral API: **yellow command acknowledged**;
- neutral physical state: **consistent with yellow by PI observation and
  inference; not independently measured**.

No retry or additional LED, query, or action command was sent. The historical
API catalog exposes no read-only endpoint for current LED color.

This was one Dazza/HOPE acceptance run, not a production deployment. The PI
accepted the temporary G3100 exception and directed that Misty be secured
behind the Beryl router immediately afterward. G28 remains inactive pending
M01 exit review and a separate PI decision.
