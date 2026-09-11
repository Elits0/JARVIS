import os
import cv2
import numpy as np


class FaceRecognizer:

    def __init__(
        self,
        model_path="vision/models/face_recognizer.yml"
    ):

        self.model_path = model_path

        if not hasattr(cv2, "face"):
            raise RuntimeError(
                "OpenCV contrib no está disponible."
            )

        self.recognizer = (
            cv2.face.LBPHFaceRecognizer_create()
        )

    def train(
        self,
        dataset_dir="vision/data/elix"
    ):

        images = []
        labels = []

        for filename in os.listdir(
            dataset_dir
        ):

            if not filename.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):
                continue

            path = os.path.join(
                dataset_dir,
                filename
            )

            image = cv2.imread(
                path,
                cv2.IMREAD_GRAYSCALE
            )

            if image is None:
                continue

            images.append(image)
            labels.append(0)

        if not images:
            raise RuntimeError(
                "No se encontraron imágenes "
                "para entrenar."
            )

        labels = np.array(
            labels,
            dtype=np.int32
        )

        self.recognizer.train(
            images,
            labels
        )

        os.makedirs(
            os.path.dirname(
                self.model_path
            ),
            exist_ok=True
        )

        self.recognizer.write(
            self.model_path
        )

        return len(images)

    def load(self):

        if not os.path.exists(
            self.model_path
        ):
            raise FileNotFoundError(
                "No existe el modelo facial."
            )

        self.recognizer.read(
            self.model_path
        )

    def predict(self, face):

        label, confidence = (
            self.recognizer.predict(face)
        )

        return {
            "label": label,
            "confidence": confidence
        }