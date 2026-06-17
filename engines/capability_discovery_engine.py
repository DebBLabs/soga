class CapabilityDiscoveryEngine:
    """
    Discovers whether planned execution steps
    are supported by standing Subject capabilities.

    This does not select protocols.
    It identifies capabilities needed by a step
    and finds available capability evidence.
    """

    ACTION_CAPABILITY_REQUIREMENTS = {
        "schedule_appointment": {
            "required_capability": "create_calendar_event",
            "capability_category": "calendar_or_provider_scheduling",
        },
        "authorize_treatment": {
            "required_capability": "medical_treatment_authorization",
            "capability_category": "clinical_authorization",
        },
        "pay_bill": {
            "required_capability": "pay_bill",
            "capability_category": "banking",
        },
        "change_beneficiary": {
            "required_capability": "change_beneficiary",
            "capability_category": "banking",
        },
        "transfer_assets": {
            "required_capability": "transfer_assets",
            "capability_category": "banking",
        },
        "rebook_travel": {
            "required_capability": "rebook_travel",
            "capability_category": "travel",
        },
        "approve_unnecessary_upgrade": {
            "required_capability": "approve_unnecessary_upgrade",
            "capability_category": "travel",
        },
        "book_unrelated_travel": {
            "required_capability": "book_unrelated_travel",
            "capability_category": "travel",
        },
        "purchase_gift": {
            "required_capability": "purchase_gift",
            "capability_category": "commerce",
        },
        "buy_age_restricted_item": {
            "required_capability": "buy_age_restricted_item",
            "capability_category": "commerce",
        },
        "create_recurring_commitment": {
            "required_capability": "create_recurring_commitment",
            "capability_category": "commerce",
        },
        "submit_claim_documents": {
            "required_capability": "submit_claim_documents",
            "capability_category": "insurance",
        },
        "check_claim_status": {
            "required_capability": "check_claim_status",
            "capability_category": "insurance",
        },
        "settle_claim": {
            "required_capability": "settle_claim",
            "capability_category": "insurance",
        },
        "accept_payment_terms": {
            "required_capability": "accept_payment_terms",
            "capability_category": "insurance",
        },
        "deploy_release": {
            "required_capability": "deploy_release",
            "capability_category": "enterprise_deployment",
        },
        "bypass_change_control": {
            "required_capability": "bypass_change_control",
            "capability_category": "enterprise_deployment",
        },
        "grant_admin_access": {
            "required_capability": "grant_admin_access",
            "capability_category": "enterprise_identity",
        },
        "disable_security_monitoring": {
            "required_capability": "disable_security_monitoring",
            "capability_category": "enterprise_security",
        },
        "collect_references": {
            "required_capability": "collect_references",
            "capability_category": "research_workspace",
        },
        "submit_publication": {
            "required_capability": "submit_publication",
            "capability_category": "research_publication",
        },
        "commit_funding": {
            "required_capability": "commit_funding",
            "capability_category": "research_funding",
        },
        "accept_authorship": {
            "required_capability": "accept_authorship",
            "capability_category": "research_authorship",
        },
    }

    def discover(
        self,
        execution_plan,
        standing_capabilities,
    ):

        discoveries = []

        for step in execution_plan.get("steps", []):

            action = step.get("action")

            requirement = self.ACTION_CAPABILITY_REQUIREMENTS.get(
                action,
                {
                    "required_capability": action,
                    "capability_category": "unknown",
                },
            )

            matches = [
                capability
                for capability in standing_capabilities
                if capability.get("capability")
                == requirement["required_capability"]
                and capability.get("status") == "active"
            ]

            if step.get("status") == "PROHIBITED":

                discoveries.append(
                    {
                        "step_id": step["step_id"],
                        "action": action,
                        "required_capability":
                            requirement["required_capability"],
                        "capability_status": "PROHIBITED",
                        "matched_capabilities": [],
                    }
                )

                continue

            discoveries.append(
                {
                    "step_id": step["step_id"],
                    "action": action,
                    "required_capability":
                        requirement["required_capability"],
                    "capability_category":
                        requirement["capability_category"],
                    "capability_status": (
                        "FOUND" if matches else "MISSING"
                    ),
                    "matched_capabilities": matches,
                }
            )

        return discoveries
