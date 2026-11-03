# IIW Misty Gateway Synthetic Execution Authority

Date: 2026-11-02 (America/New_York)
Status: AUTHORIZED — EXACTLY ONE BOUNDED SYNTHETIC EXECUTION

## Authority

Deb's direct authorization recorded in D-196 conditionally authorizes exactly
one bounded synthetic execution after blind dual PASS on the exact final
external execution request. Both gates returned PASS with no blockers.

- SOGA HEAD: `9ddd1e5ac4b9310e746e640175f02872f5518560`
- Execution request SHA-256: `dc4cad264b497970da8408bc6930e9b92eaa327544dc4a8a21739aa98441481d`
- Proposal SHA-256: `81d2d32848cc97b246cf112f5d0ca686e89fe19955f196e70d4fb1424c3d0b86`
- Controller SHA-256: `a5e17e25d61dfb089ccdd8447b73337dcc60a7c7eff5c5f211a8990b2c46063e`
- Runtime manifest SHA-256: `27c0758984fa0653652d52cd8d47c45276fe357a6888f0f9b232c5037bd45aa6`
- Claude Gate 1 response SHA-256: `f80fc8eab3ff211fbf57125d8c05c030ef406387177083f7ce564e27f1c493e5` — PASS, no blockers
- AGy Gate 2 response SHA-256: `9808f58e4c6ab5940b9f72932c947278b64c8f71672dc6264e03d1ed8d8114f4` — PASS, no blockers

## Exact invocation

`/usr/bin/python3 -B /Users/debb/dev/soga-clean/tools/robot_gateway/run_static_and_synthetic_tests.py`

The invocation is permitted exactly once, with no wrapper, alternate
interpreter, additional argument, repository change, or automatic retry.

## Boundary

This authority permits synthetic execution only. It permits no listener,
network request, Beryl access, Misty or mBot2 contact, robot command, speech,
light, sensor read, movement, or other physical execution. The resulting
evidence requires blind dual review and PI acceptance before use.
