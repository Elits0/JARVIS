import threading
import time

from core.assistant import JarvisAssistant
from core.state import JarvisState
from core.perception_manager import PerceptionManager

from interface.jarvis_window import JarvisWindow


def vision_loop(
    manager,
    window,
    state,
    assistant
):

    manager.start()

    last_update = 0

    while assistant.running:

        frame = manager.perception.camera.read()

        if frame is None:
            continue

        vision = manager.update(
            frame
        )

        now = time.time()

        # No actualizar la interfaz en cada frame.
        if now - last_update >= 0.15:

            window.set_visual_state(
                state.mode,
                state.identity,
                state.direction
            )

            last_update = now

    manager.stop()


def main():

    state = JarvisState()

    window = JarvisWindow()

    assistant = JarvisAssistant(
        state=state,
        window=window
    )

    perception_manager = PerceptionManager(
        state
    )

    assistant_thread = threading.Thread(
        target=assistant.start,
        daemon=True
    )

    vision_thread = threading.Thread(
        target=vision_loop,
        args=(
            perception_manager,
            window,
            state,
            assistant
        ),
        daemon=True
    )

    assistant_thread.start()
    vision_thread.start()

    window.run()

    assistant.running = False

    perception_manager.stop()


if __name__ == "__main__":
    main()