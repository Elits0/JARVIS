import os

import cv2


class FaceDetector:

    def __init__(self):

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        cascade_path = os.path.join(
            base_dir,
            "models",
            "haarcascade_frontalface_default.xml"
        )

        if not os.path.exists(cascade_path):

            raise FileNotFoundError(
                "No se encontró el clasificador facial en: "
                f"{cascade_path}"
            )

        self.detector = cv2.CascadeClassifier(
            cascade_path
        )

        if self.detector.empty():

            raise RuntimeError(
                "No se pudo cargar el clasificador facial."
            )

    def detect(self, frame):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        return faces