from vision.face_recognizer import FaceRecognizer


recognizer = FaceRecognizer()

print("================================")
print("   ENTRENAMIENTO FACIAL JARVIS")
print("================================")
print()

count = recognizer.train()

print(
    f"Imágenes utilizadas: {count}"
)

print(
    "Modelo guardado correctamente."
)

print(
    "vision/models/face_recognizer.yml"
)
