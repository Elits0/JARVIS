from datetime import datetime
import webbrowser


class CommandHandler:

    def __init__(self, speaker):
        self.speaker = speaker
        self.running = True

    def execute(self, command):

        if not command:
            return None

        # =========================
        # SALUDOS
        # =========================

        if "hola" in command:
            return "Hola. ¿En qué puedo ayudarte?"

        if "buenos días" in command:
            return "Buenos días. Estoy listo para ayudarte."

        if "buenas tardes" in command:
            return "Buenas tardes. ¿Qué necesitas?"

        if "buenas noches" in command:
            return "Buenas noches. ¿En qué puedo ayudarte?"

        # =========================
        # IDENTIDAD
        # =========================

        if "quién eres" in command or "quien eres" in command:
            return "Soy JARVIS, tu asistente virtual."

        if "cómo te llamas" in command or "como te llamas" in command:
            return "Mi nombre es JARVIS."

        # =========================
        # HORA
        # =========================

        if "qué hora es" in command or "que hora es" in command:
            hora = datetime.now().strftime("%H:%M")
            return f"Son las {hora}."

        # =========================
        # FECHA
        # =========================

        if "qué fecha es" in command or "que fecha es" in command:
            fecha = datetime.now().strftime("%d/%m/%Y")
            return f"Hoy es {fecha}."

        if "qué día es" in command or "que dia es" in command:
            fecha = datetime.now().strftime("%d/%m/%Y")
            return f"Hoy es {fecha}."

        # =========================
        # NAVEGADOR
        # =========================

        if "abre google" in command:
            webbrowser.open("https://www.google.com")
            return "Abriendo Google."

        if "abre youtube" in command:
            webbrowser.open("https://www.youtube.com")
            return "Abriendo YouTube."

        if "abre chatgpt" in command:
            webbrowser.open("https://chatgpt.com")
            return "Abriendo ChatGPT."

        # =========================
        # SALIR
        # =========================

        if (
            "apágate" in command
            or "apagate" in command
            or "adiós" in command
            or "adios" in command
            or "cerrate" in command
        ):
            self.running = False
            return "Entendido. Cerrando JARVIS."

        # =========================
        # COMANDO DESCONOCIDO
        # =========================

        return "Todavía no conozco ese comando."