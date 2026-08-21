from voice.listener import Listener
from voice.speaker import Speaker
from core.commands import CommandHandler


class JarvisAssistant:

    def __init__(self):
        self.listener = Listener()
        self.speaker = Speaker()

        # El CommandHandler necesita acceso al Speaker
        self.commands = CommandHandler(self.speaker)

    def start(self):

        self.speaker.speak(
            "Sistemas iniciados. JARVIS está listo."
        )

        while self.commands.running:

            command = self.listener.listen()

            if not command:
                continue

            response = self.commands.execute(command)

            # Si execute devuelve una respuesta, JARVIS la dice
            if response:
                self.speaker.speak(response)

        self.speaker.speak("Hasta luego.")