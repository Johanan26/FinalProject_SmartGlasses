from .models import FileData
from picamzero import Camera as PicamzeroCamera
from pathlib import Path
import base64
import requests
import os
from urllib.parse import urljoin


class Camera:
    def __init__(self):
        self.cam = PicamzeroCamera()

    def handle_command(self, cmd: str) -> None:
        url = os.environ.get("BACKEND_URL")
        if "take photo" in cmd:
            photo = self.make_photo()
            requests.post(urljoin(url, "/upload_photo"), photo.__dict__)
        elif "take video" in cmd:
            video = self.make_video()
            requests.post(urljoin(url, "/upload_video"), video.__dict__)

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