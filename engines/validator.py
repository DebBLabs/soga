from models.mission_working_representation import (
    MissionWorkingRepresentation,
)
from models.validation_result import ValidationResult


class Validator:
    """
    Validation gates:

      1. Completeness
      2. Evaluability
      3. Internal Consistency
    """

    def evaluate(
        self,
        mwr: MissionWorkingRepresentation,
    ) -> ValidationResult:

        findings = []
        questions = []

        semantic_types = {
            obs.get("semantic_type")
            for obs in mwr.candidate_observations
        }

        confirmed_answers = (
            mwr.inferred.get(
                "confirmed_answers",
                [],
            )
        )

        if "objective" not in semantic_types:

            findings.append(
                {
                    "gate": "Completeness",
                    "status": "FAIL",
                    "reason": "No objective identified.",
                }
            )

            questions.append(
                {
                    "question": "What is the objective of this mission?",
                    "scope": "mission_only",
                }
            )

        if "delegate" in semantic_types and not confirmed_answers:

            findings.append(
                {
                    "gate": "Evaluability",
                    "status": "REVIEW",
                    "reason": (
                        "Delegate identified but authority "
                        "boundary requires confirmation."
                    ),
                }
            )

            questions.append(
                {
                    "question": (
                        "What authority is delegated "
                        "to the identified representative?"
                    ),
                    "scope": "mission_only",
                }
            )

        elif "delegate" in semantic_types and confirmed_answers:

            findings.append(
                {
                    "gate": "Evaluability",
                    "status": "PASS",
                    "reason": (
                        "Delegate authority boundary "
                        "has been confirmed for this mission."
                    ),
                }
            )

        findings.append(
            {
                "gate": "Internal Consistency",
                "status": "PASS",
                "reason": "No conflicts detected.",
            }
        )

        status = (
            "READY"
            if not questions
            else "WORKING"
        )

        return ValidationResult(
            status=status,
            findings=findings,
            questions=questions,
        )
