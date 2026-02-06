import dbus
import dbus.service
import dbus.mainloop.glib 
from gi.repository import GLib

class Agent(dbus.service.Object):
    
    def __init__(self, bus, path):
        super().__init__(bus, path)
        
    @dbus.service.method("org.bluez.Agent1", in_signature="os", out_signature="")
    def DisplayPasskey(self, device, passkey):
        print(f"\n{'='*50}")
        print(f"Pairing Code: {passkey:06d}")
        print(f"Device: {device}")
        print(f"Cofirm this code on your phone!")
        print(f"\n{'='*50}")
        
    @dbus.service.method("org.bluez.Agent1", in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        print(f"Authorizing {device}")
        return
    
    @dbus.service.method("org.bluez.Agent1", in_signature="", out_signature="")
    def Cancel(self):
        print("Pairing cancelled")