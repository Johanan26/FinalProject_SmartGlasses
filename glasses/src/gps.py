from urllib.parse import urljoin
from models import Location
import requests
import sys
import serial #read GPS from UART
import pynmea2 #parse NMEA GPS messages
import time
import os

class Gps:
    def __init__(self, port="/dev/serial0", baudrate=9600, timeout=0.5):
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout) #open serial port
        except PermissionError:
            print(f"[ERROR] No permission to open {port}.") #common Pi permission issue
            print("Fix: add your user to the 'dialout' group:")
            print("  sudo usermod -a -G dialout $USER")
            print("then reboot and run the script again.")
            sys.exit(1)
        except serial.SerialException as e:
            print(f"[ERROR] Could not open {port}: {e}")
            sys.exit(1)
            
    def run(self):
        url = os.environ.get("BACKEND_URL")
        
        while True:
            raw = self.ser.readline().decode(errors="ignore") #read one line from GPS
                
            for chunk in raw.split('$'):  #Split in case multiple sentences come in one read
                if not chunk.startswith('GPRMC'):
                    continue

                sentence = '$' + chunk.strip()

                try:
                    msg = pynmea2.parse(sentence)
                except pynmea2.ParseError:  # parse sentence
                    continue #malformed sentence, just skip

                
                if getattr(msg, "status", "V") != "A": #A = valid fix, V = no fix
                    # we are waiting for a valid gps fix
                    continue   # break inner for, read another line
                
                #TODO: upon receiving the location we will need to send it to the backend
                lat = msg.latitude
                lng = msg.longitude
                # return Location(lng, lat)
                url = urljoin(os.environ.get("BACKEND_URL"), "/upload_location")
                requests.post(url, {"lat": lat, "long": lng})
                