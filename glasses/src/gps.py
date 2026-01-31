from models import Location
import sys
import serial #read GPS from UART
import pynmea2 #parse NMEA GPS messages
import time

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
    
    def get_location(self, timeout=30):
        end_time = time.time() + timeout #stop trying after X seconds

        while time.time() < end_time:
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
                    print("Waiting for gps fix!")
                    break   # break inner for, read another line

                lat = msg.latitude
                lng = msg.longitude
                return Location(lat, lng)

        print(f"Warining: No GPS fix after {timeout} seconds.")
        return None
    