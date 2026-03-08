from .camera import Camera
from .gps import Gps
from .microphone import RazeListener
from .questions import QuestionHandler
from dotenv import load_dotenv

import threading
import time

load_dotenv()


def dispatch_loop(listener: RazeListener, camera: Camera, question: QuestionHandler):
    """Single consumer that reads every command once and routes it."""
    while True:
        cmd = listener.get_command(timeout=1.0)
        if cmd is None:
            continue

        low = cmd.lower()
        print(f"[dispatch] received: {cmd}")

        if "question" in low:
            question.handle_command(low)
        elif "take photo" in low or "take video" in low:
            camera.handle_command(low)
        else:
            print(f"[dispatch] unrecognised command: {cmd}")


def main():
    listener = RazeListener(model_size="tiny", compute_type="int8")

    camera = Camera()
    gps = Gps()
    question = QuestionHandler()

    gps_thread = threading.Thread(
        target=gps.run,
        daemon=True
    )

    dispatch_thread = threading.Thread(
        target=dispatch_loop,
        args=(listener, camera, question),
        daemon=True
    )

    listener.start()
    gps_thread.start()
    dispatch_thread.start()

    try:
        while True:
            time.sleep(1)
    except:
        listener.stop()

if __name__ == "__main__":
    main()