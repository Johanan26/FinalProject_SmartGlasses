import subprocess
import time
import pexpect

def wait_for_bnep():
    print("Waiting for network interface (bnep0)...")
    while True:
        result = subprocess.run(
            ["ip", "link", "show", "bnep0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return
        time.sleep(2)
        
def start_pan(mac):
    subprocess.Popen(
        ["sudo", "bt-network", "-c", mac, "nap",],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def setup_bluetooth_pan():
    """Make Pi discoverable and wait for phone to connect via Bluetooth PAN"""
    
    child = pexpect.spawn("bluetoothctl", encoding="utf-8")
    
    child.sendline("power on")
    child.sendline("discoverable on")
    child.sendline("pairable on")
    child.sendline("agent NoInputNoOutput")
    child.sendline("default-agent")
    
    print("Waiting for connection...")
    
    phone_mac = None
    
    while True:
        try:
            child.expect(r"Device ([0-9A-F:]{17})", timeout=600)
            phone_mac = child.match.group(1)
            child.expect(r'\[agent\] Confirm passkey \d+ \(yes/no\):', timeout=30)
        except pexpect.TIMEOUT:
            print("waiting to pair...")
            continue
        break
    
    child.sendline("yes")
    
    start_pan(phone_mac)
    
    print("Internet connected! Ready to use.\n")

if __name__ == "__main__":
    setup_bluetooth_pan()
