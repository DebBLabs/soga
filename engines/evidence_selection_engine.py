class EvidenceSelectionEngine:
    """
    Selects the evidence that will be used
    to justify execution of each mission step.

    This is not protocol selection.
    It chooses from evidence already resolved
    as available for the step.
    """

    PREFERENCE_ORDER = [
        "bank_account_authorization",
        "travel_account_authorization",
        "payment_account_authorization",
        "insurance_portal_authorization",
        "change_approval_authorization",
        "research_workspace_authorization",
        "oauth_or_gnap_token",
        "aauth_mission_statement",
        "fiduciary_authorization",
        "travel_delegate_authorization",
        "purchase_delegate_authorization",
        "insurance_delegate_authorization",
        "ucan_capability",
        "zcap_delegation",
        "wallet_credential",
        "human_confirmation",
    ]

    def select(
        self,
        evidence_resolution,
    ):

        selections = []

        for item in evidence_resolution:

            matched = item.get(
                "matched_evidence",
                [],
            )

            if item.get("status") == "PROHIBITED":

                selections.append(
                    {
                        "step_id": item["step_id"],
                        "action": item["action"],
                        "status": "NOT_ALLOWED",
                        "selected_evidence": None,
                        "alternatives": [],
                        "reason": (
                            "Step is prohibited; no evidence "
                            "may authorize execution."
                        ),
                    }
                )

                continue

            selected = None

            for evidence_type in self.PREFERENCE_ORDER:
                if evidence_type in matched:
                    selected = evidence_type
                    break

            if selected is None and matched:
                selected = matched[0]

            alternatives = [
                evidence
                for evidence in matched
                if evidence != selected
            ]

            selections.append(
                {
                    "step_id": item["step_id"],
                    "action": item["action"],
                    "status": (
                        "SELECTED"
                        if selected
                        else "NO_EVIDENCE_AVAILABLE"
                    ),
                    "selected_evidence": selected,
                    "alternatives": alternatives,
                    "reason": (
                        "Selected available evidence that "
                        "satisfies the step requirement."
                        if selected
                        else "No available evidence satisfies "
                        "the step requirement."
                    ),
                }
            )

        return selections
