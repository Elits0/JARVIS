from openai import OpenAI
import io
import wave


class Transcriber:

    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-4o-mini-transcribe"

    def transcribe(
        self,
        audio,
        sample_rate=16000,
        channels=1
    ):

        wav_buffer = io.BytesIO()

        with wave.open(wav_buffer, "wb") as wav_file:

            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            wav_file.writeframes(
                audio.tobytes()
            )

        wav_buffer.seek(0)
        wav_buffer.name = "audio.wav"

        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=wav_buffer,
            language="es"
        )

        return transcription.text