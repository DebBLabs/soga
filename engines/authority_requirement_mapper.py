class AuthorityRequirementMapper:
    """
    Maps a compiled mission into step-level
    authority requirements.

    This does not select a protocol.
    It identifies what evidence is required
    for each execution step.
    """

    ACTION_EVIDENCE = {
        "schedule_appointment": [
            "aauth_mission_statement",
            "ucan_capability",
            "zcap_delegation",
            "oauth_or_gnap_token",
            "wallet_credential",
            "human_confirmation",
        ],
        "pay_bill": [
            "fiduciary_authorization",
            "bank_account_authorization",
            "human_confirmation",
        ],
        "rebook_travel": [
            "travel_account_authorization",
            "travel_delegate_authorization",
            "human_confirmation",
        ],
        "purchase_gift": [
            "payment_account_authorization",
            "purchase_delegate_authorization",
            "human_confirmation",
        ],
        "submit_claim_documents": [
            "insurance_portal_authorization",
            "insurance_delegate_authorization",
            "human_confirmation",
        ],
        "check_claim_status": [
            "insurance_portal_authorization",
            "insurance_delegate_authorization",
            "human_confirmation",
        ],
        "deploy_release": [
            "change_approval_authorization",
            "deployment_delegate_authorization",
            "human_confirmation",
        ],
        "collect_references": [
            "research_workspace_authorization",
            "research_delegate_authorization",
            "human_confirmation",
        ],
    }

    def map(
        self,
        cmr,
    ):

        requirements = []

        for action in cmr.get("allowed_actions", []):

            requirements.append(
                {
                    "step_id":
                        f"step-{action}",
                    "action":
                        action,
                    "required_authority":
                        "delegated_representative_authority",
                    "acceptable_evidence":
                        self.ACTION_EVIDENCE.get(
                            action,
                            [
                                "human_confirmation",
                            ],
                        ),
                    "status":
                        "REQUIRES_EVIDENCE",
                }
            )

        for action in cmr.get("forbidden_actions", []):

            requirements.append(
                {
                    "step_id":
                        f"step-{action}",
                    "action":
                        action,
                    "required_authority":
                        "prohibited_by_mission_constraint",
                    "acceptable_evidence":
                        [],
                    "status":
                        "PROHIBITED",
                }
            )

        return requirements
