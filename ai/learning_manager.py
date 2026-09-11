from ai.action_schema import validate_action
from ai.learning import LearningSystem
from ai.learning_session import LearningSession
from ai.teaching_parser import TeachingParser


class LearningManager:

    def __init__(self):

        self.learning = LearningSystem()
        self.parser = TeachingParser()
        self.session = LearningSession()

    def prepare_learning(self, text: str):

        parsed = self.parser.parse(text)

        if not parsed.get("success"):
            return parsed

        intent = parsed["intent"]
        example = parsed["example"]
        action = parsed["action"]

        if not validate_action(action):
            return {
                "success": False,
                "message": "La acción no está permitida."
            }

        existing = self.learning.get_intent(
            intent
        )

        if existing:

            proposal = {
                "operation": "add_example",
                "intent": existing["intent"],
                "example": example,
                "action": action
            }

        else:

            proposal = {
                "operation": "create_intent",
                "intent": intent,
                "example": example,
                "action": action
            }

        self.session.set_pending(
            proposal
        )

        return {
            "success": True,
            "pending": True,
            **proposal
        }

    def confirm_learning(self):

        if not self.session.has_pending():

            return {
                "success": False,
                "message": (
                    "No hay ningún aprendizaje pendiente."
                )
            }

        proposal = self.session.get_pending()

        intent = proposal["intent"]
        example = proposal["example"]
        action = proposal["action"]
        operation = proposal["operation"]

        if operation == "add_example":

            saved = self.learning.add_example(
                intent,
                example
            )

        else:

            saved = self.learning.create_intent(
                intent=intent,
                example=example,
                action=action
            )

        if not saved:

            return {
                "success": False,
                "message": (
                    "No pude guardar el aprendizaje."
                )
            }

        self.session.clear()

        return {
            "success": True,
            "message": (
                f"He aprendido '{example}'."
            ),
            "intent": intent,
            "example": example,
            "action": action
        }

    def cancel_learning(self):

        if not self.session.has_pending():

            return {
                "success": False,
                "message": (
                    "No hay ningún aprendizaje pendiente."
                )
            }

        self.session.clear()

        return {
            "success": True,
            "message": "He descartado el aprendizaje."
        }

    def teach_from_text(self, text: str):

        prepared = self.prepare_learning(text)

        if not prepared.get("success"):
            return prepared

        return self.confirm_learning()

    def process_learning(
        self,
        intent: str,
        example: str,
        action: dict
    ):

        if not intent or not example:

            return {
                "success": False,
                "message": "Faltan datos para aprender."
            }

        if not validate_action(action):

            return {
                "success": False,
                "message": "La acción no está permitida."
            }

        existing = self.learning.get_intent(
            intent
        )

        if existing:

            saved = self.learning.add_example(
                intent,
                example
            )

        else:

            saved = self.learning.create_intent(
                intent=intent,
                example=example,
                action=action
            )

        if not saved:

            return {
                "success": False,
                "message": (
                    "No pude guardar el aprendizaje."
                )
            }

        return {
            "success": True,
            "intent": intent,
            "example": example,
            "action": action,
            "message": (
                f"He aprendido la intención "
                f"'{intent}'."
            )
        }

    def get_learned_intent(
        self,
        intent: str
    ):

        return self.learning.get_intent(intent)

    def get_learned_action(
        self,
        intent: str
    ):

        return self.learning.get_action(intent)

    def get_all_learning(self):

        return self.learning.get_all()