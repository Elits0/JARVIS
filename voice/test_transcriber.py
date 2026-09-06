from voice.smart_listener import SmartListener
from voice.transcriber import Transcriber


print("================================")
print("    PRUEBA DE TRANSCRIPCIÓN")
print("================================")
print()

listener = SmartListener()
transcriber = Transcriber()

audio = listener.listen()

if audio is None:

    print("No se detectó voz.")

else:

    print()
    print("📝 Transcribiendo...")

    text = transcriber.transcribe(audio)

    print()
    print("================================")
    print("TEXTO DETECTADO:")
    print(text)
    print("================================")