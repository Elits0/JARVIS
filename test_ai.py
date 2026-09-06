from ai.classifier import IntentClassifier


classifier = IntentClassifier()

test_phrases = [
    "Oye, dime quién eres",
    "¿Te acuerdas de mi proyecto?",
    "Necesito que cierres todo",
    "Buenas, JARVIS",
    "Muchas gracias por ayudarme",
    "¿Qué cosas puedes hacer?",
    "Todo bien contigo",
    "Me voy, hablamos después"
]


print("================================")
print("     PRUEBA DE INTELIGENCIA")
print("================================")

for phrase in test_phrases:

    result = classifier.predict(phrase)

    print()
    print(f"Frase: {phrase}")
    print(f"Intención: {result['intent']}")
    print(
        f"Confianza: {result['confidence']:.2f}"
    )