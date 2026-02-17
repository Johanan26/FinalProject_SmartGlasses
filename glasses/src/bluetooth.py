import subprocess
import time

def setup_bluetooth_pan():
    """Make Pi discoverable and wait for phone to connect via Bluetooth PAN"""
    
    print("\n" + "="*50)
    print("BLUETOOTH PAIRING")
    print("="*50)
    print("\n1. On your phone, go to Bluetooth settings")
    print("2. Enable 'Bluetooth tethering' in hotspot settings")
    print("3. Scan and pair with this device")
    print("\nPIN CODE: 0000")
    print("\n" + "="*50 + "\n")
    
    subprocess.run(["bluetoothctl", "discoverable", "on"])
    subprocess.run(["bluetoothctl", "pairable", "on"])
    subprocess.run(["bluetoothctl", "agent", "on"])
    subprocess.run(["bluetoothctl", "default-agent"])
    
    print("Waiting for connection...")
    
    while True:
        result = subprocess.run(["ip", "link", "show", "bnep0"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("\nPhone connected!")
            break
        time.sleep(2)
    
    subprocess.run(["sudo", "dhclient", "bnep0"])
    
    print("Internet connected! Ready to use.\n")

if __name__ == "__main__":
    setup_bluetooth_pan()
