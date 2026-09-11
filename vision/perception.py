from vision.camera import Camera
from vision.face_detector_yunet import YuNetFaceDetector
from vision.face_recognizer import FaceRecognizer
from vision.face_tracker import FaceTracker
from vision.identity_tracker import IdentityTracker
from vision.presence import PresenceState


class Perception:

    def __init__(self):

        self.camera = Camera()
        self.detector = YuNetFaceDetector()
        self.recognizer = FaceRecognizer()

        self.tracker = FaceTracker()

        self.identity_tracker = IdentityTracker(
            required_confirmations=5
        )

        self.presence = PresenceState()

        self.recognizer.load()

    def start(self):

        self.camera.start()

    def process_frame(self, frame):

        faces = self.detector.detect(frame)

        if len(faces) == 0:

            self.identity_tracker.reset()

            self.presence.reset()

            return self.presence.get_state()

        # Utilizar el rostro más grande
        face = max(
            faces,
            key=lambda item: item[2] * item[3]
        )

        x, y, w, h = face[:4]

        x = max(0, int(x))
        y = max(0, int(y))
        w = int(w)
        h = int(h)

        face_crop = frame[
            y:y + h,
            x:x + w
        ]

        if face_crop.size == 0:

            self.presence.reset()

            return self.presence.get_state()

        gray = self._to_gray(
            face_crop
        )

        prediction = self.recognizer.predict(
            gray
        )

        confidence = prediction[
            "confidence"
        ]

        if confidence < 45:

            detected_identity = "ELIX"

        else:

            detected_identity = "DESCONOCIDO"

        identity = self.identity_tracker.update(
            detected_identity
        )

        analysis = self.tracker.analyze(
            face
        )

        direction = self.tracker.get_direction(
            analysis
        )

        self.presence.update(
            person_detected=True,
            identity=identity,
            direction=direction
        )

        state = self.presence.get_state()

        state["face"] = {
            "x": x,
            "y": y,
            "width": w,
            "height": h
        }

        state["confidence"] = confidence

        return state

    def _to_gray(self, frame):

        import cv2

        return cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

    def stop(self):

        self.camera.stop()