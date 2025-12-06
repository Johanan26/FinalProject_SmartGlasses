from picamzero import Camera as PicamzeroCamera
from dbcollections import PhotoCollection, VideoCollection

import base64

# TODO: we are using 0 as a user_id for now, in the future we should get the future_id instead
# we could do something like connect to the app with the glasses and get the user from there

class Camera:
    def __init__(self):
        self.cam = PicamzeroCamera()

    def make_photo(self) -> PhotoCollection:
        loc = self.cam.take_photo("/home/johanan/Pictures/test{f}.jpg".format(f=0))
        file = open(loc, "rb")
        data = base64.b64encode(file.read()).decode("utf-8")
        file.close()

        return PhotoCollection(0, data)
    
    def make_video(self) -> VideoCollection:
        loc = self.cam.record_video("/home/johanan/Videos/test{f}.mp4".format(f=0), duration = 5)
        file = open(loc, "rb")
        data = base64.b64encode(file.read()).decode("utf-8")
        file.close()

        return VideoCollection(0, data)