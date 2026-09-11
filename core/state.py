import time


class JarvisState:

    def __init__(self):

        self.mode = "IDLE"

        self.person_detected = False
        self.identity = "DESCONOCIDO"
        self.direction = "desconocida"

        self.vision_timestamp = 0.0

        self.last_user_text = ""
        self.last_response = ""

    def set_mode(self, mode):

        self.mode = mode

    def update_vision(
        self,
        person_detected,
        identity,
        direction
    ):

        self.person_detected = person_detected
        self.identity = identity
        self.direction = direction

        self.vision_timestamp = time.time()

    def update_conversation(
        self,
        user_text,
        response
    ):

        self.last_user_text = user_text
        self.last_response = response

    def get_state(self):

        return {
            "mode": self.mode,
            "person_detected": self.person_detected,
            "identity": self.identity,
            "direction": self.direction,
            "vision_timestamp": self.vision_timestamp,
            "last_user_text": self.last_user_text,
            "last_response": self.last_response
        }