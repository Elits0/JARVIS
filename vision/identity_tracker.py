class IdentityTracker:

    def __init__(
        self,
        required_confirmations=5
    ):

        self.required_confirmations = (
            required_confirmations
        )

        self.candidate = None
        self.counter = 0
        self.identity = "DESCONOCIDO"

    def update(self, detected_identity):

        if detected_identity == self.candidate:
            self.counter += 1
        else:
            self.candidate = detected_identity
            self.counter = 1

        if self.counter >= self.required_confirmations:
            self.identity = detected_identity

        return self.identity

    def reset(self):

        self.candidate = None
        self.counter = 0
        self.identity = "DESCONOCIDO"