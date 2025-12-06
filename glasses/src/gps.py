import sys
import serial
import pynmea2
import time
from dbcollections import LocationCollection

class Gps:
    def __init__(self, port="/dev/serial0", baudrate=9600, timeout=0.5):
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        except PermissionError:
            print(f"[ERROR] No permission to open {port}.")
            print("Fix: add your user to the 'dialout' group:")
            print("  sudo usermod -a -G dialout $USER")
            print("then reboot and run the script again.")
            sys.exit(1)
        except serial.SerialException as e:
            print(f"[ERROR] Could not open {port}: {e}")
            sys.exit(1)
    
    def get_location(self, timeout=30):
        end_time = time.time() + timeout

        while time.time() < end_time:
            raw = self.ser.readline().decode(errors="ignore")

            # Split in case multiple sentences come in one read
            for chunk in raw.split('$'):
                if not chunk.startswith('GPRMC'):
                    continue

                sentence = '$' + chunk.strip()

                try:
                    msg = pynmea2.parse(sentence)
                except pynmea2.ParseError:
                    # malformed sentence, just skip
                    continue

                # A = valid fix, V = no fix
                if getattr(msg, "status", "V") != "A":
                    break   # break inner for, read another line

                lat = msg.latitude
                lng = msg.longitude
                return LocationCollection(0, lat, lng)  

        print(f"Warining: No GPS fix after {timeout} seconds.")
        return None