import sounddevice as sd


DEVICE = 1
DURATION = 5
SAMPLE_RATE = 16000


print("Dispositivo seleccionado:")
print(sd.query_devices(DEVICE))

print("\n🎤 Habla durante 5 segundos...\n")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16",
    device=DEVICE
)

sd.wait()

print("\n✅ Grabación terminada.")
print(f"Muestras capturadas: {len(audio)}")