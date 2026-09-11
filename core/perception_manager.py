from core.state import JarvisState
from vision.perception import Perception


class PerceptionManager:

    def __init__(self, state: JarvisState):

        self.state = state
        self.perception = Perception()

    def start(self):

        self.perception.start()

    def update(self, frame):

        vision = self.perception.process_frame(
            frame
        )

        self.state.update_vision(
            person_detected=vision[
                "person_detected"
            ],
            identity=vision[
                "identity"
            ],
            direction=vision[
                "direction"
            ]
        )

        return vision

    def stop(self):

        self.perception.stop()