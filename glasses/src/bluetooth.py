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
    
def make_discoverable():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    
    # Get Bluetooth adapter
    adapter_path = '/org/bluez/hci0'
    adapter = dbus.Interface(bus.get_object('org.bluez', adapter_path),
                            'org.bluez.Adapter1')
    
    # Power on and make discoverable
    adapter.Set('org.bluez.Adapter1', 'Powered', dbus.Boolean(True))
    adapter.Set('org.bluez.Adapter1', 'Discoverable', dbus.Boolean(True))
    adapter.Set('org.bluez.Adapter1', 'Pairable', dbus.Boolean(True))
    adapter.Set('org.bluez.Adapter1', 'DiscoverableTimeout', dbus.UInt32(0))  # 0 = always discoverable
    
    print("Raspberry Pi is now discoverable!")
    print("Look for it on your Android phone's Bluetooth settings")
    
    # Register pairing agent
    agent_path = "/test/agent"
    agent = Agent(bus, agent_path)
    
    agent_manager = dbus.Interface(bus.get_object('org.bluez', '/org/bluez'),
                                   'org.bluez.AgentManager1')
    agent_manager.RegisterAgent(agent_path, "DisplayOnly")
    agent_manager.RequestDefaultAgent(agent_path)
    
    print("Pairing agent registered. Waiting for connections...")
    
    # Run the main loop
    mainloop = GLib.MainLoop()
    try:
        mainloop.run()
    except KeyboardInterrupt:
        print("\nStopping...")
        adapter.Set('org.bluez.Adapter1', 'Discoverable', dbus.Boolean(False))

if __name__ == "__main__":
    make_discoverable()