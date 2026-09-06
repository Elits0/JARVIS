import sounddevice as sd
import wave

from core.config import (
    MICROPHONE_DEVICE,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS
)


class AudioRecorder:

    def __init__(
        self,
        sample_rate=AUDIO_SAMPLE_RATE,
        channels=AUDIO_CHANNELS,
        device=MICROPHONE_DEVICE
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.device = device

    def record(self, duration=5):

        print("🎤 Grabando...")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            device=self.device
        )

        sd.wait()

        print("🎤 Grabación terminada.")

        return audio

    def save_wav(self, audio, filename):

        with wave.open(filename, "wb") as wav_file:

            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)

            wav_file.writeframes(audio.tobytes())