from camera import Camera
from gps import Gps
from microphone import RazeListener
import threading
import time


def main():
    listener = RazeListener(model_size="base", compute_type="int8")
    
    camera = Camera(listener)
    gps = Gps()

    camera_thread = threading.Thread(
        target=camera.run,
        daemon=True
    )

    gps_thread = threading.Thread(
        target=gps.run,
        daemon=True
    )
    
    listener.start()
    camera_thread.start()
    gps_thread.start()    
    
    try:
        while True:
            time.sleep(1)
    except:
        listener.stop()

if __name__ == "__main__":
    main()