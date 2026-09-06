from openai import OpenAI
from core.memory import Memory


class Brain:

    def __init__(self):

        self.client = OpenAI()

        self.model = "gpt-5.6-luna"

        self.memory = Memory()

        self.conversation = [
            {
                "role": "developer",
                "content": (
                    "Eres JARVIS, un asistente virtual avanzado "
                    "de escritorio.\n\n"
                    "Responde siempre en español.\n"
                    "Tu personalidad es elegante, tranquila, "
                    "precisa y natural.\n"
                    "Habla de forma humana y conversacional.\n"
                    "Mantén el contexto de la conversación.\n"
                    "Sé conciso cuando la pregunta sea sencilla "
                    "y más detallado cuando sea necesario."
                )
            }
        ]

    def think(self, user_message):

        # Guardar mensaje del usuario
        self.memory.remember(
            "user",
            user_message
        )

        # Añadir a contexto temporal
        self.conversation.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        # Pensamiento de JARVIS
        response = self.client.responses.create(
            model=self.model,
            input=self.conversation
        )

        answer = response.output_text

        # Guardar respuesta
        self.memory.remember(
            "assistant",
            answer
        )

        # Añadir respuesta al contexto temporal
        self.conversation.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer