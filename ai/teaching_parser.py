import json

from openai import OpenAI

from ai.action_schema import validate_action


class TeachingParser:

    def __init__(self):

        self.client = OpenAI()
        self.model = "gpt-5.6-luna"

    def parse(self, text: str):

        prompt = f"""
Analiza la siguiente instrucción de aprendizaje para JARVIS.

INSTRUCCIÓN:
{text}

Devuelve EXCLUSIVAMENTE un JSON válido con esta estructura:

{{
    "intent": "nombre_de_la_intencion",
    "example": "frase_que_debe_reconocerse",
    "action": {{
        "type": "tipo_de_accion",
        "apps": ["aplicacion"]
    }}
}}

Las únicas acciones permitidas son:

- open_app
- close_app
- volume_up
- volume_down
- mute

Reglas:

1. No inventes acciones.
2. El intent debe estar escrito en minúsculas y usar guiones bajos.
3. El example debe ser una frase corta que represente el comando aprendido.
4. Para open_app y close_app utiliza "apps".
5. Para acciones de volumen no necesitas "apps".
6. Si no puedes determinar una acción válida, devuelve:
{{
    "intent": "",
    "example": "",
    "action": {{}}
}}
"""

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "developer",
                    "content": (
                        "Eres un parser de comandos para un "
                        "asistente virtual. Devuelve únicamente "
                        "JSON válido."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        raw = response.output_text.strip()

        try:

            data = json.loads(raw)

        except json.JSONDecodeError:

            return {
                "success": False,
                "message": "No pude interpretar la instrucción."
            }

        intent = data.get("intent", "").strip()
        example = data.get("example", "").strip()
        action = data.get("action", {})

        if not intent or not example:

            return {
                "success": False,
                "message": "La instrucción no contiene suficientes datos."
            }

        if not validate_action(action):

            return {
                "success": False,
                "message": "La acción propuesta no está permitida."
            }

        return {
            "success": True,
            "intent": intent,
            "example": example,
            "action": action
        }