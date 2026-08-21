import speech_recognition as sr
import numpy as np

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False


class Listener:
    def __init__(self, language: str = "es-ES"):
        self.language = language
        self.recognizer = sr.Recognizer()
        self.use_pyaudio = HAS_PYAUDIO
        
        if self.use_pyaudio:
            try:
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            except Exception:
                self.use_pyaudio = False

    def listen(self, duration: int = 5) -> str:
        """
        Escucha el micrófono del usuario y devuelve el texto reconocido.
        """
        if self.use_pyaudio:
            return self._listen_pyaudio()
        elif HAS_SOUNDDEVICE:
            return self._listen_sounddevice(duration=duration)
        else:
            print("⚠️ No hay backend de audio disponible (PyAudio o sounddevice).")
            return ""

    def _listen_pyaudio(self) -> str:
        try:
            with self.microphone as source:
                print("🎤 Escuchando...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
            
            print("🧠 Procesando...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"👤 Usuario: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"⚠️ Error en el servicio de voz: {e}")
            return ""
        except Exception as e:
            print(f"⚠️ Error inesperado al escuchar: {e}")
            return ""

    def _listen_sounddevice(self, duration: int = 5, sample_rate: int = 16000) -> str:
        try:
            print("🎤 Escuchando (grabando audio)...")
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16"
            )
            sd.wait()

            audio_data = sr.AudioData(
                recording.tobytes(),
                sample_rate=sample_rate,
                sample_width=2
            )

            print("🧠 Procesando audio...")
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            print(f"👤 Usuario: {text}")
            return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"⚠️ Error de conexión en reconocimiento: {e}")
            return ""
        except Exception as e:
            print(f"⚠️ Error de captura de audio: {e}")
            return ""
