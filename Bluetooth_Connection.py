import bluetooth
import subprocess

devices = {}

def lookUpNearbyBluetoothDevices():
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        name = str(bluetooth.lookup_name(bdaddr))
        devices[name] = bdaddr
        print(name + " [" +str(bdaddr) + "]")

def startConnection(targetBluetoothMacAddress):
    subprocess.call("kill -9 `pidof bluetoothctl`",shell=True)
    port = 1
    passkey = "1234"
    status = subprocess.call("bluetoothctl" + passkey + "&", shell=True)
    try:
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((targetBluetoothMacAddress, port))
        print("Connected!")
        return s
    except bluetooth.btcommon.BluetoothError as err:
        print("Error occured")
        pass

lookUpNearbyBluetoothDevices()
print(devices)
s = startConnection(devices['HXM034631'])
while True:
    a = s.recv(60)
    print(a)
    
