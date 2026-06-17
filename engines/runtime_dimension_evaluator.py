class RuntimeDimensionEvaluator:
    """
    Evaluates the six locked SOGA governance dimensions.

    Each dimension returns one of:

        PASS
        REVIEW
        FAIL

    The evaluator does not produce the final
    governance decision. It produces dimension
    evaluations for the PDP.
    """

    VALID_SUBJECT_STATES = {
        "Independent",
        "Supervised",
        "Managed",
        "Delegated",
        "Lapsed",
    }

    VALID_REACHABILITY = {
        "Reachable",
        "Unreachable",
        "Unknown",
    }

    def evaluate(
        self,
        step,
        runtime,
        review_signals=None,
    ):

        runtime = runtime or {}
        review_signals = review_signals or set()

        dimensions = {
            "mission":
                self._mission(step),
            "authority":
                self._authority(step, runtime),
            "subject_agency_state":
                self._subject(runtime),
            "reachability":
                self._reachability(runtime),
            "execution_context":
                self._context(runtime),
            "policy":
                self._policy(step, runtime),
        }

        for dimension in review_signals:
            if dimensions.get(dimension) == "PASS":
                dimensions[dimension] = "REVIEW"

        return dimensions

    def _mission(
        self,
        step,
    ):

        if step.get("status") in {
            "NOT_ALLOWED",
            "PROHIBITED",
        }:
            return "FAIL"

        if step.get("status") in {
            "NO_EVIDENCE_AVAILABLE",
            "ACQUIRE_EVIDENCE",
        }:
            return "REVIEW"

        return "PASS"

    def _authority(
        self,
        step,
        runtime,
    ):

        selected = step.get(
            "selected_evidence"
        )

        if selected is None:
            return "FAIL"

        authority = runtime.get(
            "authority",
            {},
        )

        if authority.get(
            "revoked",
            False,
        ):
            return "FAIL"

        if authority.get(
            "expired",
            False,
        ):
            return "FAIL"

        if authority.get(
            "delegation_hops",
            0,
        ) > authority.get(
            "max_delegation_hops",
            3,
        ):
            return "REVIEW"

        if authority.get(
            "elapsed_seconds",
            0,
        ) > authority.get(
            "max_elapsed_seconds",
            86400,
        ):
            return "REVIEW"

        if authority.get(
            "attenuated",
            False,
        ):
            return "REVIEW"

        return "PASS"

    def _subject(
        self,
        runtime,
    ):

        state = runtime.get(
            "subject_agency_state",
            "Independent",
        )

        if state not in self.VALID_SUBJECT_STATES:
            return "REVIEW"

        if state == "Lapsed":
            return "FAIL"

        if state in {
            "Supervised",
            "Managed",
            "Delegated",
        }:
            return "REVIEW"

        return "PASS"

    def _reachability(
        self,
        runtime,
    ):

        reachability = runtime.get(
            "reachability",
            "Reachable",
        )

        if reachability not in self.VALID_REACHABILITY:
            return "REVIEW"

        if reachability == "Unknown":
            return "REVIEW"

        if reachability == "Unreachable":
            if runtime.get(
                "bounded_continuation_allowed",
                False,
            ):
                return "REVIEW"

            return "FAIL"

        return "PASS"

    def _context(
        self,
        runtime,
    ):

        if runtime.get(
            "execution_context_valid",
            True,
        ):
            if runtime.get(
                "context_requires_supervision",
                False,
            ):
                return "REVIEW"

            return "PASS"

        if runtime.get(
            "context_allows_bounded_continuation",
            False,
        ):
            return "REVIEW"

        return "FAIL"

    def _policy(
        self,
        step,
        runtime,
    ):

        if step.get("status") == "NOT_ALLOWED":
            return "FAIL"

        policy = runtime.get(
            "policy",
            {},
        )

        if policy.get(
            "prohibited",
            False,
        ):
            return "FAIL"

        if policy.get(
            "requires_supervision",
            False,
        ):
            return "REVIEW"

        if policy.get(
            "requires_escalation",
            False,
        ):
            return "REVIEW"

        return "PASS"
