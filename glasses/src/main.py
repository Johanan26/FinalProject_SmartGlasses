from camera import Camera
from gps import Gps
from db import DB

def main():
    camera = Camera()
    db = DB()
    gps = Gps()

    while True:
        inp = input("What action do you want to take: ")

        if inp == "p":
            collection = camera.make_photo()
            db.write_collection(collection)
        elif inp == "v":
            collection = camera.make_video()
            db.write_collection(collection)
        elif inp == "l":
            collection = gps.get_location()
            db.write_collection(collection)
        else:
            print("command doesn't exist: " + inp + " commands: [p, v, l]")


if __name__ == "__main__":
    main()