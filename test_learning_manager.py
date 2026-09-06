from ai.learning_manager import LearningManager


manager = LearningManager()


print("================================")
print("   PRUEBA DE MODO APRENDIZAJE")
print("================================")

text = (
    "Aprende que cuando diga modo estudio "
    "quiero que abras VS Code"
)

result = manager.process_teaching(text)

print()
print("Resultado:")
print(result)