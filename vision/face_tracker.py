import math


class FaceTracker:

    def analyze(self, face):

        x, y, w, h = face[:4]

        x = float(x)
        y = float(y)
        w = float(w)
        h = float(h)

        # Puntos faciales proporcionados por YuNet
        right_eye = (
            float(face[4]),
            float(face[5])
        )

        left_eye = (
            float(face[6]),
            float(face[7])
        )

        nose = (
            float(face[8]),
            float(face[9])
        )

        mouth_right = (
            float(face[10]),
            float(face[11])
        )

        mouth_left = (
            float(face[12]),
            float(face[13])
        )

        # Centro del rostro
        center_x = x + (w / 2)
        center_y = y + (h / 2)

        # Posición horizontal de la nariz respecto
        # al centro del rostro.
        horizontal_ratio = (
            nose[0] - center_x
        ) / max(w, 1)

        # Posición vertical de la nariz.
        vertical_ratio = (
            nose[1] - center_y
        ) / max(h, 1)

        # Distancia entre los ojos
        eye_distance = math.dist(
            right_eye,
            left_eye
        )

        return {
            "face_center": (
                center_x,
                center_y
            ),
            "face_width": w,
            "face_height": h,
            "nose": nose,
            "right_eye": right_eye,
            "left_eye": left_eye,
            "mouth_right": mouth_right,
            "mouth_left": mouth_left,
            "horizontal_ratio": horizontal_ratio,
            "vertical_ratio": vertical_ratio,
            "eye_distance": eye_distance
        }

    def get_direction(self, analysis):

        ratio = analysis["horizontal_ratio"]

        if ratio < -0.12:
            return "izquierda"

        if ratio > 0.12:
            return "derecha"

        return "frente"