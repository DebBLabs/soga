from engines.cmr_compiler import CMRCompiler
from engines.conversation_engine import ConversationEngine
from engines.glean_engine import GleanEngine
from engines.mwr_updater import MWRUpdater
from engines.observation_extractor import ObservationExtractor
from engines.persistence_router import PersistenceRouter
from engines.validator import Validator


class MissionIntakeEngine:
    """
    Public contract:

        request + answers -> CMR

    Internal path:

        request -> observations -> MWR -> validation loop -> CMR
    """

    def __init__(self):

        self.observation_extractor = ObservationExtractor()
        self.glean_engine = GleanEngine()
        self.validator = Validator()
        self.conversation = ConversationEngine()
        self.persistence_router = PersistenceRouter()
        self.mwr_updater = MWRUpdater()
        self.cmr_compiler = CMRCompiler()

    def build_mwr(
        self,
        request,
    ):

        observations = self.observation_extractor.extract(
            request
        )

        return self.glean_engine.glean(
            candidate_observations=observations,
            subject_representation={},
            mission_context={
                "request": request,
            },
            sector_knowledge=[],
        )

    def run_diagnostics(
        self,
        request,
        answers,
    ):

        mwr = self.build_mwr(
            request
        )

        answer_index = 0

        while True:

            validation = self.validator.evaluate(
                mwr
            )

            if validation.status == "READY":

                mwr.intake_status = "ready"

                return {
                    "status": "READY",
                    "mwr": mwr,
                    "validation": validation,
                }

            question = self.conversation.next_question(
                validation.questions
            )

            if question is None:

                return {
                    "status": "STOPPED_NO_QUESTION",
                    "mwr": mwr,
                    "validation": validation,
                }

            if answer_index >= len(answers):

                return {
                    "status": "WAITING_FOR_ANSWER",
                    "mwr": mwr,
                    "validation": validation,
                    "next_question": question,
                }

            answer = answers[answer_index]
            answer_index += 1

            routed = self.persistence_router.route(
                question,
                answer,
            )

            mwr = self.mwr_updater.apply(
                mwr,
                routed,
            )

    def run(
        self,
        request,
        answers,
    ):

        result = self.run_diagnostics(
            request,
            answers,
        )

        if result["status"] != "READY":

            raise RuntimeError(
                "Mission intake did not reach READY state."
            )

        return self.cmr_compiler.compile(
            result["mwr"]
        )
