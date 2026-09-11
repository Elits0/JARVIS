class PresenceState:

    def __init__(self):

        self.person_detected = False
        self.identity = "DESCONOCIDO"
        self.direction = "desconocida"

    def update(
        self,
        person_detected,
        identity="DESCONOCIDO",
        direction="desconocida"
    ):

        self.person_detected = person_detected
        self.identity = identity
        self.direction = direction

    def get_state(self):

        return {
            "person_detected": self.person_detected,
            "identity": self.identity,
            "direction": self.direction
        }

    def reset(self):

        self.person_detected = False
        self.identity = "DESCONOCIDO"
        self.direction = "desconocida"