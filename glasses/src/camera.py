import base64
import os
from pathlib import Path
from urllib.parse import urljoin

import requests
from picamzero import Camera as PicamzeroCamera

from .models import FileData


class Camera:
    def __init__(self):
        self.cam = PicamzeroCamera()

    def handle_command(self, cmd: str) -> None:
        url = os.environ.get("BACKEND_URL")

        if not url:
            return

        if "take photo" in cmd:
            photo = self.make_photo()
            requests.post(urljoin(url, "/upload_photo"), json=photo.__dict__)
        elif "take video" in cmd:
            video = self.make_video()
            requests.post(urljoin(url, "/upload_video"), json=video.__dict__)

    def make_photo(self) -> FileData:
        loc = self.cam.take_photo("/home/johanan/Pictures/photo{f}.jpg".format(f=0))
        path = Path(loc)
        filename = path.name

        with open(path, "rb") as file:
            data = base64.b64encode(file.read()).decode("utf-8")

        return FileData(filename, data)

    def make_video(self) -> FileData:
        loc = self.cam.record_video(
            "/home/johanan/Videos/video{f}.mp4".format(f=0), duration=5
        )
        path = Path(loc)
        filename = path.name

        with open(path, "rb") as file:
            data = base64.b64encode(file.read()).decode("utf-8")

        return FileData(filename, data)
