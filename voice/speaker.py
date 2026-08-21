
import pyttsx3


class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

        self._configure_voice()

    def _configure_voice(self):
        voices = self.engine.getProperty("voices")

        for voice in voices:
            voice_data = voice.name.lower()

            if "spanish" in voice_data or "es_" in voice.id.lower():
                self.engine.setProperty("voice", voice.id)
                break

    def speak(self, text):
        print(f"🤖 JARVIS: {text}")

        self.engine.say(text)
        self.engine.runAndWait()