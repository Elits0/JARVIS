from voice.smart_listener import SmartListener
from voice.speaker import Speaker
from voice.transcriber import Transcriber
from core.brain import Brain


class JarvisAssistant:

    def __init__(self):

        self.listener = SmartListener()
        self.transcriber = Transcriber()
        self.speaker = Speaker()
        self.brain = Brain()

        self.running = True

    def start(self):

        self.speaker.speak(
            "Sistemas iniciados. JARVIS está listo."
        )

        while self.running:

            try:

                audio = self.listener.listen()

                if audio is None:
                    continue

                text = self.transcriber.transcribe(
                    audio
                )

                if not text:
                    continue

                if self.should_exit(text):

                    self.speaker.speak(
                        "Entendido. Cerrando sistemas."
                    )

                    self.running = False
                    continue

                response = self.brain.think(
                    text
                )

                self.speaker.speak(
                    response
                )

            except KeyboardInterrupt:

                self.running = False

            except Exception as error:

                print(
                    f"Error interno: {error}"
                )

                self.speaker.speak(
                    "Lo siento. Encontré un problema "
                    "al procesar tu solicitud."
                )

    def should_exit(self, text):

        exit_commands = [
            "apágate",
            "apagate",
            "cierra jarvis",
            "cerrate",
            "salir"
        ]

        text = text.lower()

        return any(
            command in text
            for command in exit_commands
        )