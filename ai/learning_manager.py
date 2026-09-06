from ai.learning import LearningSystem


class LearningManager:

    def __init__(self):

        self.learning = LearningSystem()

    def process_teaching(self, text):

        text = text.strip()

        if not text:
            return {
                "success": False,
                "message": "No recibí ninguna instrucción."
            }

        lower_text = text.lower()

        prefixes = [
            "aprende que ",
            "aprende ",
            "quiero que aprendas que ",
            "quiero enseñarte que "
        ]

        teaching_text = None

        for prefix in prefixes:

            if lower_text.startswith(prefix):
                teaching_text = text[len(prefix):].strip()
                break

        if not teaching_text:

            return {
                "success": False,
                "message": (
                    "No reconocí una orden de aprendizaje."
                )
            }

        if "quiero que abras vs code" in teaching_text.lower():

            return self._create_learning(
                intent="modo_estudio",
                example="modo estudio",
                action={
                    "type": "open_app",
                    "apps": ["code"]
                }
            )

        return {
            "success": False,
            "message": (
                "Entendí que quieres enseñarme algo, "
                "pero todavía no sé convertir esa instrucción "
                "en una acción."
            )
        }

    def _create_learning(
        self,
        intent,
        example,
        action
    ):

        success = self.learning.learn(
            intent=intent,
            example=example,
            action=action
        )

        if not success:

            return {
                "success": False,
                "message": "No pude guardar el aprendizaje."
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