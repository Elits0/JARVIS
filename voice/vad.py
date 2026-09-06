import webrtcvad


class VoiceActivityDetector:

    def __init__(self, aggressiveness=2):
        self.vad = webrtcvad.Vad(aggressiveness)

    def is_speech(self, audio_frame, sample_rate):
        return self.vad.is_speech(
            audio_frame,
            sample_rate
        )