import tkinter as tk
import math


class JarvisWindow:

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("JARVIS")
        self.root.geometry("700x800")
        self.root.minsize(550, 650)
        self.root.configure(bg="#05080d")

        self.current_mode = "IDLE"
        self.current_identity = "DESCONOCIDO"
        self.current_direction = "desconocida"

        self.blink_timer = None
        self.animation_id = None
        self.animation_phase = 0

        self._build_ui()
        self._start_animation()

    # =========================================================
    # INTERFAZ
    # =========================================================

    def _build_ui(self):

        self.canvas = tk.Canvas(
            self.root,
            bg="#05080d",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.root.bind(
            "<Configure>",
            self._on_resize
        )

        # Título
        self.title_text = self.canvas.create_text(
            0,
            0,
            text="J A R V I S",
            fill="#66d9ff",
            font=("Segoe UI", 24, "bold")
        )

        self.subtitle_text = self.canvas.create_text(
            0,
            0,
            text="PERSONAL AI ASSISTANT",
            fill="#3c91b8",
            font=("Segoe UI", 9)
        )

        # Estado
        self.status_text = self.canvas.create_text(
            0,
            0,
            text="LISTO",
            fill="#66d9ff",
            font=("Segoe UI", 12, "bold")
        )

        # Identidad
        self.identity_text = self.canvas.create_text(
            0,
            0,
            text="",
            fill="#56cfff",
            font=("Segoe UI", 10)
        )

        # Línea inferior
        self.footer_text = self.canvas.create_text(
            0,
            0,
            text="SIEMPRE CONTIGO",
            fill="#245c73",
            font=("Segoe UI", 9)
        )

        # Elementos gráficos del rostro
        self.face_parts = []

        # Animación inicial
        self._draw_face()

    # =========================================================
    # ROSTRO
    # =========================================================

    def _draw_face(self):

        self.canvas.delete("face")

        width = self.root.winfo_width()
        height = self.root.winfo_height()

        cx = width // 2
        cy = height // 2 - 20

        # Tamaño adaptativo
        face_radius = min(
            width * 0.29,
            height * 0.29
        )

        # -----------------------------------------------------
        # HALO EXTERIOR
        # -----------------------------------------------------

        for i, alpha_size in enumerate(
            [1.18, 1.12, 1.07]
        ):

            r = face_radius * alpha_size

            self.canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline="#0c3142",
                width=2,
                tags="face"
            )

        # -----------------------------------------------------
        # CÍRCULOS HUD
        # -----------------------------------------------------

        hud_radii = [
            1.00,
            0.94,
            0.87
        ]

        for radius_factor in hud_radii:

            r = face_radius * radius_factor

            self.canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline="#137697",
                width=1,
                tags="face"
            )

        # -----------------------------------------------------
        # CABEZA
        # -----------------------------------------------------

        head_r = face_radius * 0.75

        self.canvas.create_oval(
            cx - head_r,
            cy - head_r,
            cx + head_r,
            cy + head_r,
            fill="#07121a",
            outline="#32c8f4",
            width=3,
            tags="face"
        )

        # Brillo interior
        inner_r = head_r * 0.94

        self.canvas.create_oval(
            cx - inner_r,
            cy - inner_r,
            cx + inner_r,
            cy + inner_r,
            outline="#0d4f67",
            width=1,
            tags="face"
        )

        # -----------------------------------------------------
        # OJOS
        # -----------------------------------------------------

        eye_y = cy - head_r * 0.12
        eye_spacing = head_r * 0.52

        eye_width = head_r * 0.25
        eye_height = head_r * 0.16

        self.left_eye = self._draw_eye(
            cx - eye_spacing,
            eye_y,
            eye_width,
            eye_height
        )

        self.right_eye = self._draw_eye(
            cx + eye_spacing,
            eye_y,
            eye_width,
            eye_height
        )

        # -----------------------------------------------------
        # BOCA
        # -----------------------------------------------------

        mouth_y = cy + head_r * 0.34

        self.mouth = self.canvas.create_arc(
            cx - head_r * 0.23,
            mouth_y - head_r * 0.10,
            cx + head_r * 0.23,
            mouth_y + head_r * 0.10,
            start=200,
            extent=140,
            style=tk.ARC,
            outline="#66d9ff",
            width=5,
            tags="face"
        )

        self.face_center = (cx, cy)
        self.head_radius = head_r

        # -----------------------------------------------------
        # LÍNEAS DE ESCANEO
        # -----------------------------------------------------

        for offset in [-0.65, 0.65]:

            x = cx + head_r * offset

            self.canvas.create_line(
                x,
                cy - head_r * 1.05,
                x,
                cy + head_r * 1.05,
                fill="#0a3445",
                width=1,
                tags="face"
            )

    def _draw_eye(
        self,
        x,
        y,
        width,
        height
    ):

        eye = self.canvas.create_oval(
            x - width,
            y - height,
            x + width,
            y + height,
            fill="#4dd8ff",
            outline="#a9efff",
            width=2,
            tags="face"
        )

        pupil = self.canvas.create_oval(
            x - width * 0.35,
            y - height * 0.55,
            x + width * 0.35,
            y + height * 0.55,
            fill="#051018",
            outline="",
            tags="face"
        )

        return eye, pupil

    # =========================================================
    # ANIMACIÓN
    # =========================================================

    def _start_animation(self):

        self._animate()

    def _animate(self):

        if not self.root.winfo_exists():
            return

        self.animation_phase += 1

        try:
            self._animate_face()
        except Exception:
            pass

        self.animation_id = self.root.after(
            50,
            self._animate
        )

    def _animate_face(self):

        if not hasattr(self, "face_center"):
            return

        cx, cy = self.face_center

        mode = self.current_mode

        # -----------------------------------------------------
        # PARPADEO
        # -----------------------------------------------------

        if self.animation_phase % 180 == 0:
            self._blink()

        # -----------------------------------------------------
        # OJOS
        # -----------------------------------------------------

        eye_offset = 0

        if mode == "THINKING":

            eye_offset = math.sin(
                self.animation_phase * 0.08
            ) * 8

        elif mode == "LISTENING":

            eye_offset = math.sin(
                self.animation_phase * 0.12
            ) * 3

        elif mode == "SPEAKING":

            eye_offset = math.sin(
                self.animation_phase * 0.10
            ) * 2

        # Mover pupilas
        try:

            for eye in [
                self.left_eye,
                self.right_eye
            ]:

                eye_shape, pupil = eye

                coords = self.canvas.coords(
                    eye_shape
                )

                center_x = (
                    coords[0] + coords[2]
                ) / 2

                center_y = (
                    coords[1] + coords[3]
                ) / 2

                pupil_coords = (
                    center_x - 8 + eye_offset,
                    center_y - 5,
                    center_x + 8 + eye_offset,
                    center_y + 5
                )

                self.canvas.coords(
                    pupil,
                    *pupil_coords
                )

        except Exception:
            pass

        # -----------------------------------------------------
        # BOCA
        # -----------------------------------------------------

        if mode == "SPEAKING":

            amount = (
                math.sin(
                    self.animation_phase * 0.5
                ) + 1
            ) / 2

            width = 0.20 + (
                amount * 0.12
            )

            height = 0.06 + (
                amount * 0.14
            )

            self.canvas.coords(
                self.mouth,
                cx - self.head_radius * width,
                cy + self.head_radius * 0.30,
                cx + self.head_radius * width,
                cy + self.head_radius * (
                    0.30 + height
                )
            )

        elif mode == "THINKING":

            self.canvas.itemconfigure(
                self.mouth,
                start=20,
                extent=140
            )

        elif mode == "LISTENING":

            self.canvas.itemconfigure(
                self.mouth,
                start=200,
                extent=140
            )

        else:

            self.canvas.itemconfigure(
                self.mouth,
                start=200,
                extent=140
            )

    # =========================================================
    # PARPADEO
    # =========================================================

    def _blink(self):

        try:

            for eye in [
                self.left_eye,
                self.right_eye
            ]:

                eye_shape, pupil = eye

                coords = self.canvas.coords(
                    eye_shape
                )

                center_x = (
                    coords[0] + coords[2]
                ) / 2

                center_y = (
                    coords[1] + coords[3]
                ) / 2

                self.canvas.coords(
                    eye_shape,
                    center_x - 4,
                    center_y - 2,
                    center_x + 4,
                    center_y + 2
                )

                self.canvas.itemconfigure(
                    pupil,
                    state="hidden"
                )

            self.root.after(
                120,
                self._open_eyes
            )

        except Exception:
            pass

    def _open_eyes(self):

        try:

            width = self.head_radius * 0.25
            height = self.head_radius * 0.16

            cx, cy = self.face_center
            spacing = self.head_radius * 0.52
            eye_y = cy - self.head_radius * 0.12

            positions = [
                cx - spacing,
                cx + spacing
            ]

            for eye, x in zip(
                [self.left_eye, self.right_eye],
                positions
            ):

                eye_shape, pupil = eye

                self.canvas.coords(
                    eye_shape,
                    x - width,
                    eye_y - height,
                    x + width,
                    eye_y + height
                )

                self.canvas.itemconfigure(
                    pupil,
                    state="normal"
                )

        except Exception:
            pass

    # =========================================================
    # ESTADOS
    # =========================================================

    def set_visual_state(
        self,
        mode,
        identity="DESCONOCIDO",
        direction="desconocida"
    ):

        def update():

            self.current_mode = mode
            self.current_identity = identity
            self.current_direction = direction

            status_map = {
                "IDLE": "LISTO",
                "LISTENING": "ESCUCHANDO",
                "THINKING": "PENSANDO",
                "SPEAKING": "HABLANDO",
                "ERROR": "ERROR",
                "SEEING": "VIENDO"
            }

            status = status_map.get(
                mode,
                mode
            )

            self.canvas.itemconfigure(
                self.status_text,
                text=status
            )

            if identity == "ELIX":

                self.canvas.itemconfigure(
                    self.identity_text,
                    text=(
                        f"ELIX DETECTADO · "
                        f"{direction.upper()}"
                    )
                )

            elif identity == "DESCONOCIDO":

                self.canvas.itemconfigure(
                    self.identity_text,
                    text="PERSONA NO IDENTIFICADA"
                )

            else:

                self.canvas.itemconfigure(
                    self.identity_text,
                    text=""
                )

        self.root.after(
            0,
            update
        )

    # =========================================================
    # TEXTO
    # =========================================================

    def set_status(self, text):

        self.root.after(
            0,
            lambda: self.canvas.itemconfigure(
                self.status_text,
                text=text
            )
        )

    def set_input(self, text):

        # Lo mantenemos compatible con assistant.py.
        # La cara es ahora el elemento principal.
        pass

    def set_response(self, text):

        # Compatible con assistant.py.
        pass

    def set_identity(
        self,
        identity,
        direction="desconocida"
    ):

        self.set_visual_state(
            self.current_mode,
            identity,
            direction
        )

    # =========================================================
    # REDIMENSIONADO
    # =========================================================

    def _on_resize(self, event):

        if event.widget != self.root:
            return

        width = event.width
        height = event.height

        self.canvas.coords(
            self.title_text,
            width // 2,
            35
        )

        self.canvas.coords(
            self.subtitle_text,
            width // 2,
            65
        )

        self.canvas.coords(
            self.status_text,
            width // 2,
            height - 80
        )

        self.canvas.coords(
            self.identity_text,
            width // 2,
            height - 52
        )

        self.canvas.coords(
            self.footer_text,
            width // 2,
            height - 25
        )

        self._draw_face()

    # =========================================================
    # CERRAR
    # =========================================================

    def close(self):

        try:

            if self.animation_id:
                self.root.after_cancel(
                    self.animation_id
                )

        except Exception:
            pass

        self.root.destroy()

    def run(self):

        self.root.mainloop()