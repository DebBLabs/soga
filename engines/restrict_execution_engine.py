class RestrictExecutionEngine:
    """
    Implements operational RESTRICT execution modes.

    The PDP selects the restrict mode.

    This execution engine implements the selected
    mode as an execution-layer behavior.
    """

    def execute(
        self,
        step,
        restrict_mode,
    ):

        mode = restrict_mode.get("mode")

        if mode == "bounded_continuation":
            return self._bounded_continuation(step, restrict_mode)

        if mode == "supervised_execution":
            return self._supervised_execution(step, restrict_mode)

        if mode == "delayed_execution":
            return self._delayed_execution(step, restrict_mode)

        if mode == "reduced_authority":
            return self._reduced_authority(step, restrict_mode)

        if mode == "partial_execution":
            return self._partial_execution(step, restrict_mode)

        if mode == "escalation":
            return self._escalation(step, restrict_mode)

        return {
            "execution_status": "RESTRICTED_UNKNOWN_MODE",
            "mode": mode,
            "reason": "Unknown RESTRICT mode.",
        }

    def _bounded_continuation(self, step, restrict_mode):
        return {
            "execution_status": "BOUNDED_CONTINUATION",
            "mode": "bounded_continuation",
            "reason": restrict_mode["reason"],
            "allowed_scope": "limited mission-safe continuation",
        }

    def _supervised_execution(self, step, restrict_mode):
        return {
            "execution_status": "SUPERVISED_EXECUTION",
            "mode": "supervised_execution",
            "reason": restrict_mode["reason"],
            "supervision_required": True,
        }

    def _delayed_execution(self, step, restrict_mode):
        return {
            "execution_status": "DELAYED_EXECUTION",
            "mode": "delayed_execution",
            "reason": restrict_mode["reason"],
            "resume_condition": "subject reachable or escalation completed",
        }

    def _reduced_authority(self, step, restrict_mode):
        return {
            "execution_status": "REDUCED_AUTHORITY",
            "mode": "reduced_authority",
            "reason": restrict_mode["reason"],
            "authority_scope": "reduced to lowest safe scope",
        }

    def _partial_execution(self, step, restrict_mode):
        return {
            "execution_status": "PARTIAL_EXECUTION",
            "mode": "partial_execution",
            "reason": restrict_mode["reason"],
            "partial": True,
        }

    def _escalation(self, step, restrict_mode):
        return {
            "execution_status": "ESCALATION_REQUIRED",
            "mode": "escalation",
            "reason": restrict_mode["reason"],
            "escalation_required": True,
        }
