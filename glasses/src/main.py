from dotenv import load_dotenv
from camera import Camera
from gps import Gps
from microphone import RazeListener
from questions import QuestionHandler
import threading
import time

load_dotenv()

def main():
    listener = RazeListener(model_size="base", compute_type="int8")
    
    camera = Camera(listener)
    gps = Gps()
    question = QuestionHandler(listener)

    camera_thread = threading.Thread(
        target=camera.run,
        daemon=True
    )

    gps_thread = threading.Thread(
        target=gps.run,
        daemon=True
    )
    
    question_thread = threading.Thread(
        target=question.run,
        daemon=True
    )
    
    listener.start()
    camera_thread.start()
    gps_thread.start()    
    question_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except:
        listener.stop()

if __name__ == "__main__":
    main()