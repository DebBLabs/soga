# Affected Files — Stage Gate 2

## Added

- project/backlog.md
- project/actors.md
- project/roles.md
- project/states.md
- project/scenario_template.md
- sprints/gate-2/STAGE_GATE_2.md
- sprints/gate-2/affected_files.md
- canonical_caregiver_scenario.md
- tools/canonical_caregiver_scenario.py
- docs/repository_inventory_v0_1.md

## Modified

- tools/restrict_visibility_demo.py

## Validation

- python3 -m tools.canonical_caregiver_scenario
- python3 -m tools.cdp_regression

Result:

- CDP REGRESSION PASS: 10 use cases, 38 canonical decision packages
