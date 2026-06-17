from datetime import datetime, timezone


class AuthorityComputationEngine:
    """
    Computes live authority state for the
    Authority governance dimension.

    This engine computes runtime facts.

    It does not make governance decisions.
    """

    def compute(
        self,
        authority,
    ):

        authority = authority or {}

        delegation_time = authority.get(
            "delegation_time",
        )

        execution_time = authority.get(
            "execution_time",
        )

        if execution_time is None:
            execution_time = datetime.now(
                timezone.utc
            )

        elapsed_seconds = 0

        if delegation_time is not None:

            elapsed_seconds = int(
                (
                    execution_time
                    - delegation_time
                ).total_seconds()
            )

        delegation_chain = authority.get(
            "delegation_chain",
            [],
        )

        delegation_hops = max(
            len(delegation_chain) - 1,
            0,
        )

        max_elapsed_seconds = authority.get(
            "max_elapsed_seconds",
            86400,
        )

        max_delegation_hops = authority.get(
            "max_delegation_hops",
            3,
        )

        attenuated = (
            elapsed_seconds >
            max_elapsed_seconds
            or
            delegation_hops >
            max_delegation_hops
        )

        return {
            "elapsed_seconds":
                elapsed_seconds,
            "delegation_hops":
                delegation_hops,
            "max_elapsed_seconds":
                max_elapsed_seconds,
            "max_delegation_hops":
                max_delegation_hops,
            "attenuated":
                attenuated,
            "expired":
                authority.get(
                    "expired",
                    False,
                ),
            "revoked":
                authority.get(
                    "revoked",
                    False,
                ),
        }
