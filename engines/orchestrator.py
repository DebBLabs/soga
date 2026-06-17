from engines.observation_extractor import ObservationExtractor
from engines.glean_engine import GleanEngine
from engines.validator import Validator

from models.intake_result import IntakeResult


class MissionIntakeOrchestrator:

    def __init__(self):

        self.observation_extractor = ObservationExtractor()
        self.glean_engine = GleanEngine()
        self.validator = Validator()

    def run(
        self,
        request: str,
    ) -> IntakeResult:

        observations = self.observation_extractor.extract(
            request
        )

        mwr = self.glean_engine.glean(
            candidate_observations=observations,
            subject_representation={},
            mission_context={
                "request": request,
            },
            sector_knowledge=[],
        )

        validation = self.validator.evaluate(
            mwr
        )

        return IntakeResult(
            request=request,
            candidate_observations=observations,
            mission_working_representation=mwr,
            validation=validation,
            questions=validation.questions,
        )
