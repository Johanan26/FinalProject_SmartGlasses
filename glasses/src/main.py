from picamzero import Camera
from time import sleep
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
import base64
import time

uri = os.environ.get("DB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    exit()
  
db = client["brain"]
photo_collection = db["photos"]
video_collection = db["videos"]

#Camera
#Photo
# cam = Camera()
# cam.start_preview()

# sleep(2)

# loc = cam.take_photo("/home/johanan/Pictures/test{f}.jpg".format(f=0))

# with open(loc, "rb") as file:
#     data = file.read()

#     photo = {
#         "user_id": 0,
#         "created_at": time.time(),
#         "data": base64.b64encode(data).decode("utf-8") # we are base64 encoding the data so we can make sure there is no dataloss when sinding it over htttp
#     }

#     photo_collection.insert_one(photo)

#Video
cam = Camera()
cam.start_preview()

loc = cam.record_video("/home/johanan/Videos/test{f}.mp4".format(f=0), duration = 5)

with open(loc, "rb") as file:
    data = file.read()

    video = {
        "user_id": 0,
        "created_at": time.time(),
        "data": base64.b64encode(data).decode("utf-8") # we are base64 encoding the data so we can make sure there is no dataloss when sinding it over htttp
    }

    video_collection.insert_one(video)