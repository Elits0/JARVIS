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
                    "JARVIS dispone de un sistema visual local "
                    "que proporciona información en tiempo real "
                    "sobre las personas detectadas.\n\n"
                    "El sistema visual puede indicar:\n"
                    "- si hay una persona detectada;\n"
                    "- si una persona ha sido identificada como ELIX "
                    "o como DESCONOCIDO;\n"
                    "- la dirección aproximada de la persona.\n\n"
                    "Cuando el estado visual indique que ELIX está "
                    "detectado, puedes decir que ves y reconoces a ELIX.\n"
                    "Cuando no haya ninguna persona detectada, indica "
                    "que actualmente no detectas a ninguna persona.\n"
                    "No inventes detalles visuales que el sistema no "
                    "proporcione, como ropa, color de ojos, apariencia "
                    "física o elementos del entorno.\n"
                    "No digas que no tienes acceso a la cámara si el "
                    "estado visual indica que la cámara está activa y "
                    "proporcionando información."
                )
            }
        ]

    def think(
        self,
        user_message,
        vision_context=None
    ):

        # Guardar mensaje del usuario
        self.memory.remember(
            "user",
            user_message
        )

        # Añadir contexto visual actual
        if vision_context:

            visual_context_text = (
                "Estado visual actual de JARVIS:\n\n"
                f"Persona detectada: "
                f"{vision_context.get('person_detected', False)}\n"
                f"Identidad: "
                f"{vision_context.get('identity', 'DESCONOCIDO')}\n"
                f"Dirección: "
                f"{vision_context.get('direction', 'desconocida')}\n"
            )

            self.conversation.append(
                {
                    "role": "developer",
                    "content": visual_context_text
                }
            )

        # Buscar recuerdos relacionados
        memories = self.memory.search(
            user_message
        )

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

        # Mensaje actual
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

        self.conversation.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer