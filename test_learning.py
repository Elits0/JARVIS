from ai.learning import LearningSystem


learning = LearningSystem()

learning.learn(
    "modo_estudio",
    "activa el modo estudio",
    {
        "type": "open_app",
        "apps": [
            "code"
        ]
    }
)

learning.learn(
    "modo_estudio",
    "ponme en modo estudio"
)

learning.learn(
    "modo_estudio",
    "vamos a estudiar"
)

print("================================")
print("   PRUEBA DE APRENDIZAJE V2")
print("================================")

print()

print("Todos los conocimientos:")

for item in learning.get_all():
    print(item)

print()
print("Acción de modo_estudio:")

print(
    learning.get_action(
        "modo_estudio"
    )
)