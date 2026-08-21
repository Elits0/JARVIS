import sys
from core.assistant import JarvisAssistant


def main():
    print("=" * 40)
    print("         🤖 J.A.R.V.I.S. ASISTENTE       ")
    print("=" * 40)
    
    assistant = JarvisAssistant()
    assistant.start()


if __name__ == "__main__":
    main()
