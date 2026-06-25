from __future__ import annotations

import html
from pathlib import Path

from tools.cdp_regression import USE_CASES
from tools.run_use_case import execute_use_case, load_use_case


OUTPUT = Path("web/governance_workbench.html")


def safe(value):
    return html.escape(str(value))


def display_value(value):
    text = str(value)

    if "." in text:
        return text.split(".")[-1]

    return text


def determination_key(value):
    return display_value(value).upper()


def execution_outcome(determination):
    decision = determination_key(determination)

    if decision == "ALLOW":
        return "EXECUTING"

    if decision == "RESTRICT":
        return "HOLDING"

    if decision == "DENY":
        return "ABORTED"

    return "UNKNOWN"


def caregiver_restrict_lifecycle():
    return """
    <div class="note">
      <strong>Reference RESTRICT Lifecycle</strong>

      <p>Subject Agency State: SUPERVISED</p>
      <p>Governance Determination: RESTRICT</p>
      <p>Execution Outcome: HOLDING</p>
      <p>Approval Event: Scenario Demonstration</p>
      <p>Governance Re-Evaluation</p>
      <p>Governance Determination: ALLOW</p>
      <p>Execution Outcome: EXECUTING</p>

      <p>
      Source: Canonical Caregiver Scenario.
      Reference execution layer only.
      Not a production approval service.
      </p>
    </div>
    """


def delegation_boundary_panel():
    return """
    <div class="note">
      <strong>Delegation Evidence Boundary</strong>

      <pre>
Alice
  |
  v
Beth
  |
  v
Care Agent
  |
  v
Execution Request

  |
  v

Single Governance Evaluation

  |
  v

Governance Determination
      </pre>

      <p>
      Delegation chains arrive as authority evidence.
      </p>

      <p>
      SOGA performs one governance evaluation
      at execution time.
      </p>

      <p>
      Current implementation does not perform
      per-hop governance evaluation.
      </p>

      <p>
      Current implementation does not produce
      per-hop governance receipts.
      </p>

      <p>
      Future Architecture: B-020
      </p>
    </div>
    """


def mission_builder_panel(use_case_id):
    if use_case_id == "caregiver":
        human_intent = (
            "My caregiver may coordinate my daily care "
            "while I recover from surgery."
        )

        mission_items = [
            ("Objective", "Coordinate daily care during recovery"),
            ("Subject", "Patient"),
            ("Delegate", "Caregiver"),
            (
                "Allowed actions",
                "Schedule appointments; coordinate transportation; "
                "purchase approved items",
            ),
            (
                "Prohibited actions",
                "Authorize treatment; transfer assets; change beneficiaries",
            ),
            ("Governance requirement", "Evaluate at execution time"),
        ]

        peer_items = [
            "Canonical Mission Representation",
            "Delegation Evidence",
            "Subject Agency State",
            "Other governance-relevant inputs",
        ]

    elif use_case_id == "multi_hop":
        human_intent = (
            "Alice delegates appointment coordination to Beth. "
            "Beth delegates scheduling execution to a Care Agent."
        )

        mission_items = [
            ("Objective", "Schedule cardiology appointment"),
            ("Subject", "Alice"),
            ("Delegates", "Beth; Care Agent"),
            ("Allowed actions", "Schedule appointment"),
            (
                "Prohibited actions",
                "Authorize treatment; change medication; "
                "access unrelated records",
            ),
            ("Governance requirement", "Evaluate at execution time"),
        ]

        peer_items = [
            "Canonical Mission Representation",
            "Delegation Evidence",
            "Subject Agency State",
            "Other governance-relevant inputs",
        ]

    else:
        return ""

    mission_rows = "\n".join(
        f"<tr><td>{safe(name)}</td><td>{safe(value)}</td></tr>"
        for name, value in mission_items
    )

    peer_list = "\n".join(
        f"<li>{safe(item)}</li>"
        for item in peer_items
    )

    return f"""
    <div class="note mission-builder-panel">
      <strong>Notional Mission Builder</strong>

      <p>
      Mission Builder - independent adjacent contribution.
      Produces mission context consumed by the Governance Server
      alongside delegation evidence, authorization context, policy
      inputs, capability context, Subject Agency State, runtime
      conditions, and the execution request.
      </p>

      <div class="mission-grid">
        <div class="mission-box">
          <h4>Human Intent</h4>
          <p>{safe(human_intent)}</p>
        </div>

        <div class="mission-box">
          <h4>Canonical Mission Representation</h4>
          <table>
            <tbody>
              {mission_rows}
            </tbody>
          </table>
        </div>

        <div class="mission-box">
          <h4>Representative Peer Inputs</h4>
          <ul>
            {peer_list}
          </ul>
        </div>
      </div>

      <div class="convergence">
        <strong>Convergence Point</strong>
        <p>
        The CMR is one contributor among several. These inputs
        converge as Governance-Relevant Information before the
        SOGA Governance Server evaluates execution-time legitimacy.
        </p>
      </div>
    </div>
    """


def package_to_view(use_case_id, use_case, package, entry_number):
    mission = package.get("mission", {})
    dimensions = package.get("dimension_results", {})
    receipt = package.get("execution_receipt")
    execution_context = package.get("execution_context", {})
    step_id = execution_context.get("step_id")
    action = execution_context.get("action")

    decision = display_value(
        package.get("governance_determination")
    )

    subject_state = display_value(
        package.get("subject_agency_state")
    )

    outcome = execution_outcome(
        package.get("governance_determination")
    )

    rows = "\n".join(
        f"<tr><td>{safe(k)}</td><td>{safe(display_value(v))}</td></tr>"
        for k, v in dimensions.items()
    )

    return f"""
    <section class="package">
      <h3>Runtime Log Entry {entry_number}</h3>
      <p><strong>Decision:</strong> {safe(decision)}</p>
      <p><strong>Mission Context:</strong> {safe(mission.get("title"))}</p>
      <p><strong>Mission ID:</strong> {safe(mission.get("mission_id"))}</p>
      <p><strong>Task Action:</strong> {safe(action)}</p>
      <p><strong>Task Step ID:</strong> {safe(step_id)}</p>
      <p><strong>Subject Agency State at Decision Time:</strong> {safe(subject_state)}</p>
      <p><strong>Execution Outcome:</strong> {safe(outcome)}</p>
      <p><strong>Execution Receipt:</strong> {safe(receipt)}</p>
      <table>
        <thead>
          <tr>
            <th>Dimension</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </section>
    """


def main():
    sections = []

    for use_case_id in USE_CASES:
        use_case = load_use_case(use_case_id)
        result = execute_use_case(use_case)

        packages = [
            package.to_dict()
            for package in result["canonical_decision_packages"]
        ]

        rendered = "\n".join(
            package_to_view(
                use_case_id,
                use_case,
                package,
                index,
            )
            for index, package in enumerate(packages, start=1)
        )

        notes = use_case.get("notes", [])

        notes_html = ""

        if notes:
            note_items = "\n".join(
                f"<li>{safe(note)}</li>"
                for note in notes
            )

            notes_html = f"""
              <div class="note">
                <strong>Scenario Notes</strong>
                <ul>{note_items}</ul>
              </div>
            """

        mission_html = ""

        if use_case_id in {"caregiver", "multi_hop"}:
            mission_html = mission_builder_panel(use_case_id)

        lifecycle_html = ""

        if use_case_id == "caregiver":
            lifecycle_html = caregiver_restrict_lifecycle()

        delegation_html = ""

        if use_case_id == "multi_hop":
            delegation_html = delegation_boundary_panel()

        sections.append(
            f"""
            <div class="use-case" id="{safe(use_case_id)}">
              <h2>{safe(use_case.get("title"))}</h2>
              <p class="id">Use case: {safe(use_case_id)}</p>
              {notes_html}
              {mission_html}
              {lifecycle_html}
              {delegation_html}
              {rendered}
            </div>
            """
        )

    options = "\n".join(
        f'<option value="{safe(use_case_id)}">{safe(use_case_id)}</option>'
        for use_case_id in USE_CASES
    )

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>SOGA Governance Workbench</title>

  <style>
    body {{
      font-family: system-ui, sans-serif;
      margin: 2rem;
      max-width: 1000px;
    }}

    select {{
      font-size: 1rem;
      padding: 0.4rem;
      margin-bottom: 1.5rem;
    }}

    .use-case {{
      display: none;
      border-top: 2px solid #333;
      padding-top: 1rem;
    }}

    .use-case.active {{
      display: block;
    }}

    .package {{
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 1rem;
      margin: 1rem 0;
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

    .note {{
      background: #f8f8f8;
      padding: 1rem;
      border-left: 4px solid #444;
      margin-bottom: 1rem;
    }}

    .mission-builder-panel {{
      background: #fafafa;
      border-left: 4px solid #222;
    }}

    .mission-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 1rem;
      margin-top: 1rem;
    }}

    .mission-box {{
      background: #fff;
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 1rem;
    }}

    .mission-box h4 {{
      margin-top: 0;
    }}

    .convergence {{
      background: #fff;
      border: 1px dashed #777;
      border-radius: 8px;
      padding: 1rem;
      margin-top: 1rem;
    }}

    pre {{
      white-space: pre-wrap;
    }}
  </style>
</head>

<body>

  <h1>SOGA Governance Decision Workbench</h1>

  <div class="note">
    <p>
      <strong>
        SOGA Governance Decision Log -
        Demonstration environment.
      </strong>
    </p>

    <p>
      This page shows governance decisions for authority-bearing
      execution requests.
    </p>

    <p>
      This workbench is not a mission planner,
      mission builder, execution environment,
      workflow engine, orchestration runtime,
      or agent framework.
    </p>
  </div>

  <div class="note">
    <p>
      <strong>
      One governance model. Many authority-bearing
      execution requests. Same decision lifecycle
      visible across all of them.
      </strong>
    </p>

    <p>
      This page is generated from existing SOGA
      regression use cases. It shows only the tasks
      that reached governance evaluation. It does not
      introduce new governance logic.
    </p>
  </div>

  <label for="selector"><strong>Select governance scenario:</strong></label>

  <select id="selector">
    {options}
  </select>

  {''.join(sections)}

  <script>
    const selector = document.getElementById("selector");
    const cases = document.querySelectorAll(".use-case");

    function showSelected() {{
      cases.forEach(
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

    OUTPUT.write_text(
        html_doc,
        encoding="utf-8",
    )

    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
