from camera import Camera
from gps import Gps

def main():
    camera = Camera()
    gps = Gps()

    while True:
        inp = input("What action do you want to take: ")

        if inp == "p":
            photo = camera.make_photo()
            
        elif inp == "v":
            video = camera.make_video()
        elif inp == "l":
            location = gps.get_location()
            if location == None:
                continue
            
            
        else:
            print("command doesn't exist: " + inp + " commands: [p, v, l]")

if __name__ == "__main__":
    main()