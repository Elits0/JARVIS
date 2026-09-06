from voice.audio_recorder import AudioRecorder


recorder = AudioRecorder()

audio = recorder.record(duration=5)

recorder.save_wav(
    audio,
    "test_audio.wav"
)

print("Audio guardado correctamente.")