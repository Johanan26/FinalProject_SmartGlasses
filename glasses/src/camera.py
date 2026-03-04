from picamzero import Camera as PicamzeroCamera
from pathlib import Path
from models import FileData
from typing import TYPE_CHECKING
import base64

if TYPE_CHECKING:
    from microphone import RazeListener

class Camera:
    def __init__(self, listener: RazeListener):
        self.cam = PicamzeroCamera()
        self.listener = listener
        
    def run(self):
        while True:
            cmd = self.listener.get_command()
            
            if cmd:
                print(f"cmd: {cmd}")
                
                if "take photo" in cmd.lower():
                    self.make_photo()
                elif "take video" in cmd.lower():
                    self.make_video()

    def make_photo(self) -> FileData:
        loc = self.cam.take_photo("/home/johanan/Pictures/video{f}.jpg".format(f=0))
        path = Path(loc)
        filename = path.name

        with open(path, "rb") as file:
            data = base64.b64encode(file.read()).decode("utf-8")
        
        return FileData(filename, data)
    
    def make_video(self) -> FileData:
        loc = self.cam.record_video("/home/johanan/Videos/video{f}.mp4".format(f=0), duration = 5)
        path = Path(loc)
        filename = path.name

        with open(path, "rb") as file:
            data = base64.b64encode(file.read()).decode("utf-8")
        
        return FileData(filename, data)