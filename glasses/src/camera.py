from picamzero import Camera as PicamzeroCamera
from pathlib import Path
from models import FileData
import base64

class Camera:
    def __init__(self):
        self.cam = PicamzeroCamera()

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