import time

import numpy as np
import sounddevice as sd

from core.config import (
    MICROPHONE_DEVICE,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS
)

from voice.vad import VoiceActivityDetector


class SmartListener:

    def __init__(self):

        self.sample_rate = AUDIO_SAMPLE_RATE
        self.channels = AUDIO_CHANNELS
        self.device = MICROPHONE_DEVICE

        self.vad = VoiceActivityDetector(
            aggressiveness=2
        )

        # Tamaño de cada bloque de audio.
        # 30 ms es compatible con WebRTC VAD.
        self.frame_duration = 0.03

        self.frame_samples = int(
            self.sample_rate * self.frame_duration
        )

        # Tiempo máximo de una intervención
        self.max_duration = 20

        # Cuánto silencio esperamos después de hablar
        self.silence_duration = 0.9

    def listen(self):

        print("🎤 Esperando voz...")

        frames = []

        speech_detected = False
        silence_start = None

        start_time = time.time()

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            device=self.device,
            blocksize=self.frame_samples
        ) as stream:

            while True:

                audio, overflowed = stream.read(
                    self.frame_samples
                )

                if overflowed:
                    continue

                frame = audio[:, 0].tobytes()

                is_speech = self.vad.is_speech(
                    frame,
                    self.sample_rate
                )

                if is_speech:

                    speech_detected = True
                    silence_start = None

                    frames.append(
                        audio.copy()
                    )

                elif speech_detected:

                    frames.append(
                        audio.copy()
                    )

                    if silence_start is None:

                        silence_start = time.time()

                    elif (
                        time.time() - silence_start
                        >= self.silence_duration
                    ):

                        break

                if (
                    time.time() - start_time
                    >= self.max_duration
                ):

                    break

        if not frames:

            return None

        audio_data = np.concatenate(
            frames,
            axis=0
        )

        return audio_data