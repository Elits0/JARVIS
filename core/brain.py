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
                    "y más detallado cuando sea necesario.\n\n"
                    "Puedes utilizar recuerdos de conversaciones "
                    "anteriores cuando sean relevantes."
                )
            }
        ]

    def think(self, user_message):

        # Guardar mensaje del usuario
        self.memory.remember(
            "user",
            user_message
        )

        # Buscar recuerdos relacionados
        memories = self.memory.search(user_message)

        # Añadir recuerdos relevantes
        if memories:

            memory_context = "\n".join(
                [
                    f"- {memory['role']}: {memory['message']}"
                    for memory in memories[-10:]
                ]
            )

            self.conversation.append(
                {
                    "role": "developer",
                    "content": (
                        "Estos son recuerdos relevantes de "
                        "conversaciones anteriores:\n\n"
                        f"{memory_context}\n\n"
                        "Utilízalos únicamente si son relevantes "
                        "para responder al usuario."
                    )
                }
            )

        # Añadir mensaje actual
        self.conversation.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        # Generar respuesta
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