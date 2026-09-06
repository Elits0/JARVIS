import sounddevice as sd


devices = sd.query_devices()

print("\n=== MICRÓFONOS DISPONIBLES ===\n")

for i, device in enumerate(devices):

    if device["max_input_channels"] > 0:

        print(f"{i}: {device['name']}")

print("\n==============================")