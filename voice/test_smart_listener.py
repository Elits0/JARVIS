from voice.smart_listener import SmartListener


listener = SmartListener()

print("================================")
print("   PRUEBA SMART LISTENER")
print("================================")
print()

audio = listener.listen()

if audio is None:

    print("No se detectó voz.")

else:

    print()
    print("✅ Audio capturado correctamente.")
    print(f"Muestras: {len(audio)}")
    print(
        f"Duración aproximada: "
        f"{len(audio) / listener.sample_rate:.2f} segundos"
    )