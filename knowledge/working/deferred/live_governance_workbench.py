"""
SOGA Live Governance Workbench
Flask server — thin bridge only.
No governance logic. No policy logic.
Calls real GovernedExecutionLoop.
"""
from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, jsonify, request, render_template_string

from builders.mission_builder import build_governed_mission, load_mission_file
from engines.capability_registry import CapabilityRegistry
from engines.governed_execution_loop import GovernedExecutionLoop
from verify.runtime_envelope_model import SubjectGovernanceState

app = Flask(__name__)

CAPABILITY_FIXTURES = Path("tests/fixtures/capabilities")
MISSION_FIXTURE = Path("tests/fixtures/missions/caregiver_discharge_followup.json")

SCENARIOS = {
    "caregiver_supervised": {
        "label": "Caregiver — Supervised Subject (RESTRICT → Clearance → ALLOW)",
        "subject_state": SubjectGovernanceState.SUPERVISED,
        "clearance": True,
        "description": (
            "Supervision required. Stage Gate fires. "
            "Clearance provided. Resubmission produces ALLOW."
        ),
    },
    "caregiver_independent": {
        "label": "Caregiver — Independent Subject (ALLOW)",
        "subject_state": SubjectGovernanceState.INDEPENDENT,
        "clearance": False,
        "description": (
            "No supervision constraint active. "
            "Stage Gate clears immediately. Execution proceeds."
        ),
    },
    "caregiver_lapsed": {
        "label": "Caregiver — Lapsed Authority (DENY)",
        "subject_state": SubjectGovernanceState.LAPSED,
        "clearance": False,
        "description": (
            "Subject authority has lapsed. "
            "Governance denies execution."
        ),
    },
}


def load_registry() -> CapabilityRegistry:
    registry = CapabilityRegistry()
    for fixture_path in sorted(CAPABILITY_FIXTURES.glob("*.json")):
        with fixture_path.open("r", encoding="utf-8") as f:
            capability = json.load(f)
        registry.register(
            canonical_name=capability["canonical_name"],
            implementations=capability["implementations"],
            required_authority_scope=capability["required_authority_scope"],
            governance_dimensions_affected=capability["governance_dimensions_affected"],
        )
    return registry


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>SOGA Live Governance Workbench</title>
<style>
  body { font-family: monospace; max-width: 900px; margin: 40px auto; padding: 20px; background: #f8f8f8; }
  h1 { color: #222; }
  .subtitle { color: #666; font-size: 0.9em; margin-bottom: 30px; }
  select, button { font-size: 1em; padding: 8px 12px; margin: 8px 4px; }
  button { background: #2c5f2e; color: white; border: none; cursor: pointer; border-radius: 4px; }
  button:hover { background: #1a3d1c; }
  #description { color: #555; font-style: italic; margin: 10px 0; min-height: 40px; }
  #results { margin-top: 20px; }
  .panel { background: white; border: 1px solid #ddd; border-radius: 4px; padding: 20px; margin: 10px 0; }
  .panel h3 { margin-top: 0; color: #333; }
  .ALLOW { color: #2c5f2e; font-weight: bold; font-size: 1.2em; }
  .RESTRICT { color: #b8860b; font-weight: bold; font-size: 1.2em; }
  .DENY { color: #8b0000; font-weight: bold; font-size: 1.2em; }
  .field { margin: 6px 0; }
  .label { color: #666; }
  .impl { margin: 4px 0 4px 20px; color: #444; }
  .boundary { border-top: 1px solid #eee; margin-top: 15px; padding-top: 10px; color: #888; font-size: 0.85em; }
  .loading { color: #888; }
</style>
</head>
<body>
<h1>SOGA Live Governance Workbench</h1>
<div class="subtitle">
  Live execution-time governance demonstration.<br>
  Real GovernancePDP. Real Stage Gates. Real Canonical Decision Package.
</div>

<div>
  <label><strong>Select scenario:</strong></label><br>
  <select id="scenario">
    {% for key, s in scenarios.items() %}
    <option value="{{ key }}">{{ s.label }}</option>
    {% endfor %}
  </select>
  <button onclick="runScenario()">Run Governance</button>
</div>

<div id="description"></div>
<div id="results"></div>

<script>
const scenarios = {{ scenarios_json | safe }};

document.getElementById('scenario').addEventListener('change', function() {
  const key = this.value;
  document.getElementById('description').textContent = scenarios[key].description;
  document.getElementById('results').innerHTML = '';
});

// Set initial description
window.onload = function() {
  const key = document.getElementById('scenario').value;
  document.getElementById('description').textContent = scenarios[key].description;
};

async function runScenario() {
  const scenario = document.getElementById('scenario').value;
  document.getElementById('results').innerHTML = '<p class="loading">Running governance evaluation...</p>';

  try {
    const response = await fetch('/api/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario })
    });
    const data = await response.json();
    renderResults(data);
  } catch (err) {
    document.getElementById('results').innerHTML = '<p style="color:red">Error: ' + err + '</p>';
  }
}

function renderResults(data) {
  let html = '';

  if (data.mission_context) {
    html += '<div class="panel">';
    html += '<h3>Mission Context</h3>';
    html += '<div class="field"><span class="label">Mission: </span>' + data.mission_context.objective + '</div>';
    html += '<div class="field"><span class="label">Subject: </span>' + data.mission_context.subject_id + '</div>';
    html += '<div class="field"><span class="label">Authority: </span>' + data.mission_context.authority_id + '</div>';
    html += '<div class="field"><span class="label">Constraint: </span>' + data.mission_context.constraint + '</div>';
    html += '<div class="field"><span class="label">Capability: </span>' + data.mission_context.capability + '</div>';
    html += '</div>';
  }

  for (const phase of data.phases) {
    html += '<div class="panel">';
    html += '<h3>' + phase.label + '</h3>';
    html += '<div class="field"><span class="label">Stage Gate State: </span>' + phase.stage_gate_state + '</div>';
    html += '<div class="field"><span class="label">Route: </span>' + phase.route + '</div>';

    if (phase.decision) {
      html += '<div class="field"><span class="label">CDP Decision: </span>';
      html += '<span class="' + phase.decision + '">' + phase.decision + '</span></div>';
    }
    if (phase.token) {
      html += '<div class="field"><span class="label">Governance Reasoning Token: </span>' + phase.token + '</div>';
    }
    if (phase.interruption) {
      html += '<div class="field"><span class="label">Interruption: </span>' + phase.interruption + '</div>';
    }
    if (phase.capability) {
      html += '<div class="field"><span class="label">Capability: </span>' + phase.capability + '</div>';
      if (phase.implementations) {
        html += '<div class="field"><span class="label">Available Implementations:</span>';
        for (const impl of phase.implementations) {
          html += '<div class="impl">&#8227; ' + impl.type + ': ' + impl.stub_endpoint + '</div>';
        }
        html += '</div>';
      }
    }

    html += '<div class="boundary">GovernancePDP: UNCHANGED &nbsp;|&nbsp; RuntimeEnvelope: UNCHANGED</div>';
    html += '</div>';
  }

  document.getElementById('results').innerHTML = html;
}
</script>
</body>
</html>
"""


@app.route("/")
def index():
    scenarios_json = json.dumps({
        k: {"label": v["label"], "description": v["description"]}
        for k, v in SCENARIOS.items()
    })
    return render_template_string(
        HTML,
        scenarios=SCENARIOS,
        scenarios_json=scenarios_json,
    )


@app.route("/api/run", methods=["POST"])
def run_governance():
    data = request.get_json()
    scenario_key = data.get("scenario", "caregiver_supervised")
    scenario = SCENARIOS.get(scenario_key, SCENARIOS["caregiver_supervised"])

    source = load_mission_file(MISSION_FIXTURE)
    mission = build_governed_mission(source)
    steps = source["steps"]
    registry = load_registry()
    loop = GovernedExecutionLoop(capability_registry=registry)

    phases = []

    # Phase 1 — initial governance evaluation
    result1 = loop.run(mission, steps, scenario["subject_state"], {})
    record1 = result1["records"][0] if result1["records"] else {}

    phase1 = {
        "label": "Phase 1 — Governance Evaluation",
        "stage_gate_state": record1.get("stage_gate_state", ""),
        "route": record1.get("route", ""),
        "decision": record1.get("governance_decision"),
        "token": "supervision_required" if record1.get("governance_decision") == "RESTRICT" else None,
    }

    if record1.get("interruption"):
        phase1["interruption"] = (
            f"step_id={record1['interruption'].get('step_id')} — "
            f"{record1['interruption'].get('reason')}"
        )

    phases.append(phase1)

    # Phase 2 — clearance and resubmission if applicable
    if scenario["clearance"] and record1.get("route") in ("INTERRUPTED", "RESTRICTED"):
        clearance_evidence = {
            "supervisor_confirmation": True,
            "governance_reasoning_token": "supervision_required",
        }
        result2 = loop.run(
            mission, steps,
            SubjectGovernanceState.INDEPENDENT,
            clearance_evidence,
        )
        record2 = result2["records"][0] if result2["records"] else {}

        phase2 = {
            "label": "Phase 2 — Clearance Provided / Resubmission",
            "stage_gate_state": record2.get("stage_gate_state", ""),
            "route": record2.get("route", ""),
            "decision": record2.get("governance_decision"),
            "token": "supervision_required" if record2.get("governance_decision") == "RESTRICT" else None,
        }

        if record2.get("capability_resolution"):
            res = record2["capability_resolution"]
            phase2["capability"] = res.get("canonical_name")
            phase2["implementations"] = res.get("implementations", [])

        phases.append(phase2)

    elif record1.get("capability_resolution"):
        res = record1["capability_resolution"]
        phase1["capability"] = res.get("canonical_name")
        phase1["implementations"] = res.get("implementations", [])

    return jsonify({
        "scenario": scenario_key,
        "mission_context": {
            "mission_id": mission["mission_id"],
            "objective": mission["objective"],
            "subject_id": mission["subject_id"],
            "authority_id": mission["authority_id"],
            "constraint": "supervision_required = true",
            "capability": steps[0]["required_capability"],
        },
        "phases": phases,
    })


if __name__ == "__main__":
    print("SOGA Live Governance Workbench")
    print("Open http://localhost:5001 in your browser")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5001)
