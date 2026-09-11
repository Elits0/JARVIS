import os
import cv2


class FaceDataset:

    def __init__(
        self,
        output_dir="vision/data/elix"
    ):

        self.output_dir = output_dir

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    def save_face(
        self,
        frame,
        face,
        index
    ):

        x, y, w, h = face[:4]

        x = max(0, int(x))
        y = max(0, int(y))
        w = int(w)
        h = int(h)

        crop = frame[
            y:y + h,
            x:x + w
        ]

        if crop.size == 0:
            return False

        filename = os.path.join(
            self.output_dir,
            f"elix_{index:04d}.jpg"
        )

        return cv2.imwrite(
            filename,
            crop
        )