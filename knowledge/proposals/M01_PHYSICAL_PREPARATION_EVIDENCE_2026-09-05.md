# M01 Physical Preparation and Read-Only Connection Evidence

Date: 2026-09-05  
PI: Deb Bucci  
Scope: preparation and read-only verification only

## Adopted run-specific binding

| Field | Adopted value | Evidence |
|---|---|---|
| Platform | Misty A | PI adoption after case, router, historical, power-on, and service corroboration |
| Serial | `20221304273` | PI-verified case label; physical underside label was not re-read while powered |
| MAC | `00:d0:ca:01:a2:61` | Verizon G3100 device record |
| IPv4 | `192.168.1.183` | Current Verizon G3100 DHCP lease; matches historical Misty address |
| Allocation | Dynamic DHCP | Router record; recheck required immediately before run |
| Service | Misty Studio | Read-only root GET returned HTTP 200 and redirected to `/sdk/dashboard/index.html` |
| Battery | 100% | Visible Misty Studio dashboard |

## Read-only observation

The root response identified Misty Studio. The visible dashboard automatically
initialized Live Data, including camera preview and distance telemetry, without
any action-control click. Codex closed the tab upon observing the camera because
the authorization prohibited camera use. The PI observed the same page and
classified the behavior as normal website API initialization. No LED, speech,
movement, configuration, mapping, skill, or other actuation control was used.

## Still unresolved before Physical Execution Authorization

- The G3100 home Wi-Fi shown by the router is not yet evidenced as the dedicated
  isolated network/VLAN required by G27.
- Physical stability/clearance inspection and a specific independent operator
  stop have not yet been attested and recorded.
- Pink `(255,105,180)`, one second, and yellow `(255,255,0)` remain candidates
  rather than PI-adopted physical run parameters.
- A production Person Server is absent; the local implementation remains a
  clearly labeled test fixture.
- A strict-timeout live HTTP transport has not been instantiated or reviewed at
  the exact run checkpoint.

No physical execution is authorized by this evidence.
