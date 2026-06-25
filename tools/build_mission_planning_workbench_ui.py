from pathlib import Path
import html


OUTPUT = Path("web/mission_planning_workbench.html")


def safe(value):
    return html.escape(str(value))


SCENARIOS = {
    "banking": {
        "title": "Bounded Banking Support",
        "mission_id": "mission-bounded-banking-support",
        "intent": "My attorney may pay household bills while I am unavailable.",
        "objective": "Support routine household banking without expanding authority.",
        "tasks": [
            ["Review unpaid household bills", "banking / bill review", "no", "capability invocation"],
            ["Check account balance", "banking read access", "no", "capability invocation"],
            ["Pay electric bill", "bill payment", "yes", "delegated capability invocation"],
            ["Pay water bill", "bill payment", "yes", "delegated capability invocation"],
            ["Change beneficiary", "account administration", "not permitted", "blocked before governance"],
            ["Transfer assets", "asset transfer", "not permitted", "blocked before governance"],
        ],
    },
    "caregiver": {
        "title": "Caregiver Recovery Support",
        "mission_id": "mission-caregiver-recovery-support",
        "intent": "My caregiver may coordinate my daily care while I recover from surgery.",
        "objective": "Coordinate daily recovery support within bounded caregiver authority.",
        "tasks": [
            ["Check clinic hours", "public directory lookup", "no", "capability invocation"],
            ["Schedule follow-up appointment", "calendar / scheduling", "yes", "delegated capability invocation"],
            ["Coordinate transportation", "transportation service", "yes", "delegated capability invocation"],
            ["Purchase approved supplies", "shopping / payment", "yes", "delegated capability invocation"],
            ["Authorize treatment", "clinical authorization", "not permitted", "blocked before governance"],
        ],
    },
    "emergency": {
        "title": "Emergency Response Support",
        "mission_id": "mission-emergency-response-support",
        "intent": "If I am in an emergency, help coordinate immediate support.",
        "objective": "Support emergency response while preserving authority boundaries.",
        "tasks": [
            ["Locate nearest emergency facility", "maps / directory lookup", "no", "capability invocation"],
            ["Notify emergency contact", "messaging", "yes", "delegated capability invocation"],
            ["Share emergency information", "health information exchange", "yes", "delegated capability invocation"],
            ["Unlock home access for responder", "smart lock / device", "yes", "delegated capability invocation"],
            ["Make non-emergency financial decision", "financial system", "not permitted", "blocked before governance"],
        ],
    },
    "enterprise": {
        "title": "Enterprise Operations Support",
        "mission_id": "mission-enterprise-operations-support",
        "intent": "Help respond to an operational incident using approved enterprise procedures.",
        "objective": "Support incident response while respecting enterprise authority boundaries.",
        "tasks": [
            ["Review incident summary", "ticketing system read access", "no", "capability invocation"],
            ["Collect system logs", "observability platform", "no", "capability invocation"],
            ["Restart service", "operations control", "yes", "delegated capability invocation"],
            ["Deploy approved patch", "deployment system", "yes", "delegated capability invocation"],
            ["Bypass change control", "administrative override", "not permitted", "blocked before governance"],
        ],
    },
    "guardianship": {
        "title": "Guardianship Support",
        "mission_id": "mission-guardianship-support",
        "intent": "My guardian may help manage approved care and support tasks.",
        "objective": "Support guardianship actions within delegated and legal authority.",
        "tasks": [
            ["Review appointment calendar", "calendar read access", "no", "capability invocation"],
            ["Schedule appointment", "calendar / scheduling", "yes", "delegated capability invocation"],
            ["Pay approved provider invoice", "payment system", "yes", "delegated capability invocation"],
            ["Submit required form", "government / provider portal", "yes", "delegated capability invocation"],
            ["Authorize major surgery", "clinical authorization", "not permitted", "blocked before governance"],
        ],
    },
    "insurance": {
        "title": "Insurance Claim Support",
        "mission_id": "mission-insurance-claim-support",
        "intent": "Help me prepare and submit an insurance claim.",
        "objective": "Support insurance claim preparation and bounded submission.",
        "tasks": [
            ["Review policy coverage", "policy lookup", "no", "capability invocation"],
            ["Collect claim documents", "document management", "no", "capability invocation"],
            ["Submit claim", "insurance portal", "yes", "delegated capability invocation"],
            ["Upload supporting evidence", "insurance portal", "yes", "delegated capability invocation"],
            ["Accept settlement offer", "insurance portal", "yes", "delegated capability invocation"],
        ],
    },
    "medical_appointments": {
        "title": "Medical Appointment Scheduling",
        "mission_id": "mission-medical-appointment-scheduling",
        "intent": "Schedule my medical appointment according to my preferences.",
        "objective": "Find and schedule an appointment without exceeding scheduling authority.",
        "tasks": [
            ["Find available appointment slots", "scheduling availability lookup", "no", "capability invocation"],
            ["Check provider location", "directory / maps", "no", "capability invocation"],
            ["Book appointment", "scheduling system", "yes", "delegated capability invocation"],
            ["Notify patient", "messaging", "context dependent", "possible delegated capability invocation"],
            ["Authorize treatment", "clinical authorization", "not permitted", "blocked before governance"],
        ],
    },
    "multi_hop": {
        "title": "Multi-Hop Appointment Delegation",
        "mission_id": "mission-multi-hop-appointment-delegation",
        "intent": "Alice delegates appointment coordination to Beth. Beth delegates scheduling execution to a care agent.",
        "objective": "Schedule a cardiology appointment through a delegated chain.",
        "tasks": [
            ["Find cardiology availability", "scheduling availability lookup", "no", "capability invocation"],
            ["Compare appointment windows", "calendar / scheduling lookup", "no", "capability invocation"],
            ["Schedule cardiology appointment", "scheduling system", "yes", "delegated capability invocation"],
            ["Notify Alice and Beth", "messaging", "context dependent", "possible delegated capability invocation"],
            ["Change medication", "medication management", "not permitted", "blocked before governance"],
        ],
    },
    "research": {
        "title": "Research Support",
        "mission_id": "mission-research-support",
        "intent": "Help conduct research and prepare outputs without exceeding delegated authority.",
        "objective": "Support bounded research work and identify authority-bearing actions.",
        "tasks": [
            ["Search literature", "academic search", "no", "capability invocation"],
            ["Summarize papers", "document analysis", "no", "local execution"],
            ["Draft report", "document generation", "no", "local execution"],
            ["Submit dataset", "research repository", "yes", "delegated capability invocation"],
            ["Submit publication", "publication system", "yes", "delegated capability invocation"],
        ],
    },
    "shopping": {
        "title": "Bounded Shopping Support",
        "mission_id": "mission-bounded-shopping-support",
        "intent": "Help purchase approved items within my limits.",
        "objective": "Support shopping while separating search from purchase authority.",
        "tasks": [
            ["Search products", "product search", "no", "capability invocation"],
            ["Compare prices", "product search", "no", "capability invocation"],
            ["Read reviews", "public web lookup", "no", "capability invocation"],
            ["Add approved item to cart", "commerce site", "context dependent", "possible delegated capability invocation"],
            ["Place order", "commerce / payment", "yes", "delegated capability invocation"],
            ["Purchase prohibited item", "commerce / payment", "not permitted", "blocked before governance"],
        ],
    },
    "travel": {
        "title": "Travel Displacement Support",
        "mission_id": "mission-travel-displacement-support",
        "intent": "Help me recover from travel disruption and get home safely.",
        "objective": "Support travel recovery while identifying authority-bearing actions.",
        "tasks": [
            ["Check flight status", "airline status lookup", "no", "capability invocation"],
            ["Search alternate flights", "travel search", "no", "capability invocation"],
            ["Search hotels", "hotel search", "no", "capability invocation"],
            ["Book replacement flight", "travel booking / payment", "yes", "delegated capability invocation"],
            ["Book hotel", "hotel booking / payment", "yes", "delegated capability invocation"],
            ["Submit reimbursement request", "expense system", "yes", "delegated capability invocation"],
        ],
    },
}


def route_counts(tasks):
    total = len(tasks)
    authority = sum(1 for task in tasks if task[2] == "yes")
    no_authority = sum(1 for task in tasks if task[2] == "no")
    conditional = sum(1 for task in tasks if task[2] == "context dependent")
    blocked = sum(1 for task in tasks if task[2] == "not permitted")

    return {
        "total": total,
        "authority": authority,
        "no_authority": no_authority,
        "conditional": conditional,
        "blocked": blocked,
    }


def task_rows(tasks):
    return "\n".join(
        f"""
        <tr>
          <td>{safe(task)}</td>
          <td>{safe(capability)}</td>
          <td>{safe(authority)}</td>
          <td>{safe(route)}</td>
        </tr>
        """
        for task, capability, authority, route in tasks
    )


def scenario_section(scenario_id, scenario):
    counts = route_counts(scenario["tasks"])

    return f"""
    <section class="scenario" id="{safe(scenario_id)}">
      <h2>{safe(scenario["title"])}</h2>

      <div class="panel">
        <h3>Mission Identity</h3>
        <p><strong>Mission ID:</strong> {safe(scenario["mission_id"])}</p>
        <p>
        This is a notional mission planning view.
        It demonstrates task classification only.
        It is not yet integrated with a runtime agent implementation.
        </p>
      </div>

      <div class="panel">
        <h3>Human Intent</h3>
        <p>{safe(scenario["intent"])}</p>
      </div>

      <div class="panel">
        <h3>Mission Construction</h3>
        <p><strong>Objective:</strong> {safe(scenario["objective"])}</p>
        <p>
        Mission construction turns human intent into a task plan.
        It identifies capabilities and authority-bearing tasks.
        It does not approve, deny, restrict, evaluate Subject Agency State,
        or produce a governance determination.
        </p>
      </div>

      <div class="panel">
        <h3>Mission Plan / Task Classification</h3>
        <table>
          <thead>
            <tr>
              <th>Task</th>
              <th>Capability Needed</th>
              <th>Authority Needed</th>
              <th>Route</th>
            </tr>
          </thead>
          <tbody>
            {task_rows(scenario["tasks"])}
          </tbody>
        </table>
      </div>

      <div class="panel">
        <h3>Mission Planning Summary</h3>
        <ul>
          <li>Total mission tasks: {counts["total"]}</li>
          <li>Tasks with no authority needed: {counts["no_authority"]}</li>
          <li>Authority-bearing tasks: {counts["authority"]}</li>
          <li>Context-dependent authority tasks: {counts["conditional"]}</li>
          <li>Not permitted tasks: {counts["blocked"]}</li>
        </ul>
      </div>

      <div class="boundary">
        Mission planning ends here. Governance is separate.
        SOGA sees only authority-bearing execution requests when they reach
        the execution boundary.
      </div>
    </section>
    """


def main():
    options = "\n".join(
        f'<option value="{safe(key)}">{safe(value["title"])}</option>'
        for key, value in SCENARIOS.items()
    )

    sections = "\n".join(
        scenario_section(key, value)
        for key, value in SCENARIOS.items()
    )

    doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>SOGA Mission Planning Workbench</title>

  <style>
    body {{
      font-family: system-ui, sans-serif;
      margin: 2rem;
      max-width: 1100px;
    }}

    select {{
      font-size: 1rem;
      padding: 0.4rem;
      margin-bottom: 1.5rem;
    }}

    .scenario {{
      display: none;
      border-top: 2px solid #333;
      padding-top: 1rem;
    }}

    .scenario.active {{
      display: block;
    }}

    .panel {{
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 1rem;
      margin: 1rem 0;
      background: #fff;
    }}

    .note {{
      background: #f8f8f8;
      padding: 1rem;
      border-left: 4px solid #444;
      margin-bottom: 1rem;
    }}

    .boundary {{
      background: #f8f8f8;
      border: 2px dashed #444;
      padding: 1rem;
      margin: 1rem 0;
      font-weight: bold;
    }}

    table {{
      border-collapse: collapse;
      width: 100%;
    }}

    th, td {{
      border: 1px solid #ddd;
      padding: 0.5rem;
      text-align: left;
      vertical-align: top;
    }}

    th {{
      background: #f4f4f4;
    }}
  </style>
</head>

<body>
  <h1>SOGA Mission Planning Workbench</h1>

  <div class="note">
    <p><strong>Mission planning demonstration.</strong></p>
    <p>
    This page shows notional mission construction and task classification.
    It does not perform governance evaluation.
    </p>
    <p>
    The mission side identifies which tasks need authority.
    SOGA governance is a separate execution-time function.
    </p>
  </div>

  <label for="selector"><strong>Select mission:</strong></label>

  <select id="selector">
    {options}
  </select>

  {sections}

  <script>
    const selector = document.getElementById("selector");
    const scenarios = document.querySelectorAll(".scenario");

    function showSelected() {{
      scenarios.forEach(
        el => el.classList.remove("active")
      );

      const selected =
        document.getElementById(selector.value);

      if (selected) {{
        selected.classList.add("active");
      }}
    }}

    selector.addEventListener(
      "change",
      showSelected
    );

    showSelected();
  </script>
</body>
</html>
"""

    OUTPUT.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
