from __future__ import annotations

import html
from pathlib import Path

from tools.cdp_regression import USE_CASES
from tools.run_use_case import execute_use_case, load_use_case


OUTPUT = Path("web/governance_workbench.html")


def safe(value):
    return html.escape(str(value))


def execution_outcome(determination):

    if determination == "ALLOW":
        return "EXECUTING"

    if determination == "RESTRICT":
        return "HOLDING"

    if determination == "DENY":
        return "ABORTED"

    return "UNKNOWN"


def package_to_view(use_case_id, use_case, package):
    mission = package.get("mission", {})
    dimensions = package.get("dimension_results", {})
    receipt = package.get("execution_receipt")

    outcome = execution_outcome(
        package.get("governance_determination")
    )

    rows = "\n".join(
        f"<tr><td>{safe(k)}</td><td>{safe(v)}</td></tr>"
        for k, v in dimensions.items()
    )

    return f"""
    <section class="package">
      <h3>{safe(package.get("governance_determination"))}</h3>
      <p><strong>Mission:</strong> {safe(mission.get("title"))}</p>
      <p><strong>Request:</strong> {safe(use_case.get("request"))}</p>
      <p><strong>Subject Agency State:</strong> {safe(package.get("subject_agency_state"))}</p>
      <p><strong>Execution Outcome:</strong> {safe(outcome)}</p>
      <p><strong>Execution Receipt:</strong> {safe(receipt)}</p>
      <table>
        <thead><tr><th>Dimension</th><th>Result</th></tr></thead>
        <tbody>{rows}</tbody>
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
            package_to_view(use_case_id, use_case, package)
            for package in packages
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

        sections.append(
            f"""
            <div class="use-case" id="{safe(use_case_id)}">
              <h2>{safe(use_case.get("title"))}</h2>
              <p class="id">Use case: {safe(use_case_id)}</p>
              {notes_html}
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
  </style>
</head>
<body>

  <h1>SOGA Governance Workbench</h1>

  <div class="note">
    <p>
      <strong>
        SOGA Governance Laboratory —
        Demonstration environment.
      </strong>
    </p>

    <p>
      Governance determinations influence
      execution outcomes.
    </p>

    <p>
      This workbench is not a production
      execution environment, workflow
      engine, orchestration runtime,
      or agent framework.
    </p>
  </div>

  <div class="note">
    <p><strong>One governance model. Many mission types. Same lifecycle visible across all of them.</strong></p>
    <p>This page is generated from existing SOGA regression use cases. It does not introduce new governance logic.</p>
  </div>

  <label for="selector"><strong>Select mission type:</strong></label>
  <select id="selector">
    {options}
  </select>

  {''.join(sections)}

  <script>
    const selector = document.getElementById("selector");
    const cases = document.querySelectorAll(".use-case");

    function showSelected() {{
      cases.forEach(el => el.classList.remove("active"));
      const selected = document.getElementById(selector.value);
      if (selected) selected.classList.add("active");
    }}

    selector.addEventListener("change", showSelected);
    showSelected();
  </script>

</body>
</html>
"""

    OUTPUT.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
