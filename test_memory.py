from core.memory import Memory


memory = Memory()

print("=== PRUEBA DE MEMORIA ===")

memory.remember(
    "user",
    "Mi proyecto se llama JARVIS."
)

print("Recuerdo guardado.")

print()
print("Último recuerdo:")
print(memory.get_last_interaction())