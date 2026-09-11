from core import perception_manager
from voice.smart_listener import SmartListener
from voice.speaker import Speaker
from voice.transcriber import Transcriber

from core.brain import Brain
from core.state import JarvisState

from ai.learning_manager import LearningManager
import time


class JarvisAssistant:

    def __init__(
        self,
        state=None,
        window=None
    ):

        self.listener = SmartListener()
        self.transcriber = Transcriber()
        self.speaker = Speaker()
        self.brain = Brain()
        self.learning_manager = LearningManager()

        self.state = state or JarvisState()
        self.window = window

        self.running = True
        self.learning_confirmation = False

    def start(self):

        self.set_mode("IDLE")

        self.speaker.speak(
            "Sistemas iniciados. JARVIS está listo."
        )

        while self.running:

            try:

                # Esperando al usuario
                self.set_mode("LISTENING")

                audio = self.listener.listen()

                if audio is None:
                    continue

                # Transcripción
                text = self.transcriber.transcribe(
                    audio
                )

                if not text:
                    continue

                text = text.strip()

                self.state.last_user_text = text

                if self.window:

                    self.window.set_input(
                        text
                    )

                # --------------------------------
                # CONFIRMACIÓN DE APRENDIZAJE
                # --------------------------------

                if self.learning_confirmation:

                    self.handle_learning_confirmation(
                        text
                    )

                    continue

                # --------------------------------
                # APAGADO
                # --------------------------------

                if self.should_exit(text):

                    self.speaker.speak(
                        "Entendido. Cerrando sistemas."
                    )

                    self.running = False

                    continue

                # --------------------------------
                # MODO APRENDIZAJE
                # --------------------------------

                if self.is_learning_command(text):

                    self.handle_learning_command(
                        text
                    )

                    continue

                # --------------------------------
                # PENSAMIENTO
                # --------------------------------

                self.set_mode("THINKING")

                vision_age = (
                    time.time() - self.state.vision_timestamp
                    if self.state.vision_timestamp > 0
                    else None
                )

                vision_context = {
                    "person_detected": (
                        self.state.person_detected
                    ),
                    "identity": (
                        self.state.identity
                    ),
                    "direction": (
                        self.state.direction
                    ),
                    "vision_data_age_seconds": (
                        vision_age
                    )
                }

                response = self.brain.think(
                    text,
                    vision_context=vision_context
                )

                self.state.update_conversation(
                    text,
                    response
                )

                if self.window:

                    self.window.set_response(
                        response
                    )

                # --------------------------------
                # RESPUESTA DE VOZ
                # --------------------------------

                self.set_mode("SPEAKING")

                self.speaker.speak(
                    response
                )

            except KeyboardInterrupt:

                self.running = False

            except Exception as error:

                print(
                    f"Error interno: {error}"
                )

                self.set_mode("ERROR")

                self.speaker.speak(
                    "Lo siento. Encontré un problema "
                    "al procesar tu solicitud."
                )

        self.set_mode("IDLE")

    def set_mode(self, mode):

        self.state.set_mode(
            mode
        )

        if self.window:

            self.window.set_visual_state(
                mode,
                self.state.identity,
                self.state.direction
            )

    def is_learning_command(
        self,
        text: str
    ):

        text = text.lower().strip()

        commands = [
            "aprende ",
            "aprende que ",
            "quiero enseñarte ",
            "quiero enseñarte que "
        ]

        return any(
            text.startswith(command)
            for command in commands
        )

    def handle_learning_command(
        self,
        text: str
    ):

        result = (
            self.learning_manager.prepare_learning(
                text
            )
        )

        if not result.get("success"):

            self.speaker.speak(
                result.get(
                    "message",
                    "No pude interpretar "
                    "lo que quieres enseñarme."
                )
            )

            return

        self.learning_confirmation = True

        example = result["example"]
        action = result["action"]

        apps = action.get(
            "apps",
            []
        )

        action_type = action["type"]

        if action_type == "open_app":

            action_description = (
                "abrir "
                + ", ".join(apps)
            )

        elif action_type == "close_app":

            action_description = (
                "cerrar "
                + ", ".join(apps)
            )

        elif action_type == "volume_up":

            action_description = (
                "subir el volumen"
            )

        elif action_type == "volume_down":

            action_description = (
                "bajar el volumen"
            )

        elif action_type == "mute":

            action_description = (
                "silenciar el volumen"
            )

        else:

            action_description = (
                "realizar esa acción"
            )

        response = (
            f"Entendí que cuando digas "
            f"{example}, debo {action_description}. "
            f"¿Quieres que lo aprenda?"
        )

        if self.window:

            self.window.set_response(
                response
            )

        self.set_mode("SPEAKING")

        self.speaker.speak(
            response
        )

    def handle_learning_confirmation(
        self,
        text: str
    ):

        text = text.lower().strip()

        yes_words = [
            "sí",
            "si",
            "correcto",
            "afirmativo",
            "aprende",
            "hazlo",
            "guárdalo",
            "guardalo"
        ]

        no_words = [
            "no",
            "cancelar",
            "cancela",
            "olvídalo",
            "olvidalo",
            "no quiero"
        ]

        if any(
            word in text
            for word in yes_words
        ):

            result = (
                self.learning_manager.confirm_learning()
            )

            self.learning_confirmation = False

            self.set_mode("SPEAKING")

            self.speaker.speak(
                result.get(
                    "message",
                    "Aprendizaje guardado."
                )
            )

            return

        if any(
            word in text
            for word in no_words
        ):

            result = (
                self.learning_manager.cancel_learning()
            )

            self.learning_confirmation = False

            self.set_mode("SPEAKING")

            self.speaker.speak(
                result.get(
                    "message",
                    "He descartado el aprendizaje."
                )
            )

            return

        self.set_mode("SPEAKING")

        self.speaker.speak(
            "Necesito que me respondas sí o no."
        )

    def should_exit(
        self,
        text: str
    ):

        exit_commands = [
            "apágate",
            "apagate",
            "apaga sistemas",
            "apagar sistemas",
            "cierra jarvis",
            "cierra",
            "cerrate",
            "salir",
            "termina",
            "terminar",
            "finaliza",
            "finalizar",
            "hasta luego",
            "adiós",
            "adios"
        ]

        text = text.lower().strip()

        return any(
            command in text
            for command in exit_commands
        )