import threading
import time

from dotenv import load_dotenv

from .camera import Camera
from .gps import Gps
from .microphone import RazeListener
from .oled import OLEDHandler
from .questions import QuestionHandler

load_dotenv()


def dispatch_loop(
    listener: RazeListener, camera: Camera, question: QuestionHandler, oled: OLEDHandler
):
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
<<<<<<< HEAD
        elif "show menu":
=======
        elif "show menu" in low:
>>>>>>> c2d09b27652a30d8f05a6905ddd438a02cd5ea0d
            oled.handle_command(low)
        else:
            print(f"[dispatch] unrecognised command: {cmd}")


def main():
    listener = RazeListener(model_size="tiny", compute_type="int8")

    camera = Camera()
    gps = Gps()
    question = QuestionHandler()
    oled = OLEDHandler()

    gps_thread = threading.Thread(target=gps.run, daemon=True)

    dispatch_thread = threading.Thread(
<<<<<<< HEAD
        target=dispatch_loop, args=(listener, camera, question), daemon=True
=======
        target=dispatch_loop, args=(listener, camera, question, oled), daemon=True
>>>>>>> c2d09b27652a30d8f05a6905ddd438a02cd5ea0d
    )

    listener.start()
    gps_thread.start()
    dispatch_thread.start()

    print("running")

    try:
        while True:
            time.sleep(1)
    except:
        listener.stop()


if __name__ == "__main__":
    main()
