import os
import cv2


class YuNetFaceDetector:

    def __init__(
        self,
        model_path="vision/models/face_detection_yunet_2023mar.onnx"
    ):

        if not os.path.exists(model_path):

            raise FileNotFoundError(
                f"No se encontró el modelo: {model_path}"
            )

        self.detector = cv2.FaceDetectorYN.create(
            model_path,
            "",
            (320, 320),
            score_threshold=0.6,
            nms_threshold=0.3,
            top_k=5000
        )

    def detect(self, frame):

        height, width = frame.shape[:2]

        self.detector.setInputSize(
            (width, height)
        )

        _, faces = self.detector.detect(
            frame
        )

        if faces is None:
            return []

        return faces