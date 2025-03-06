#------------------------------------
#       LIBRARIES
#------------------------------------

from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import paho.mqtt.client as mqtt
from mysql.connector import Error
from datetime import datetime
from digi import xbee
from datetime import datetime

#------------------------------------
#       CONFIGURATIONS
#------------------------------------

#   MQTT Connection
MQTT_IP = 'broker.hivemq.com'
MQTT_PORT = 1883
GROUP_NAME = "Group3"
DEVICE_ID = "DeviceA"

#   Device Connection
PORT = "COM5"
BAUD_RATE = 9600
REMOTE_NODE_ID = "END_DEVICE"
IO_SAMPLING_RATE = 5  # 5 seconds.


#------------------------------------
#       CONNECTIONS
#------------------------------------

#   Instantiating MQTT and callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to  "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = str(msg.payload.decode('utf-8'))


client = mqtt.Client() 
#If newer python version: client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) 
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_IP, MQTT_PORT, 60)

#------------------------------------
#       MAIN METHOD
#------------------------------------

def main():
    print(" +----------------------------------------------+")
    print(" | XBee Python Library Handle IO Samples Sample |")
    print(" +----------------------------------------------+\n")
    device = XBeeDevice(PORT, BAUD_RATE)
    try:
        device.open()
        
        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        # Set the local device as destination address of the remote.
        remote_device.set_dest_address(device.get_64bit_addr())
        # Enable periodic sampling every IO_SAMPLING_RATE seconds in the remote device.
        remote_device.set_io_sampling_rate(IO_SAMPLING_RATE)
        #   User Button
        remote_device.set_io_configuration(IOLine.DIO4_AD4, IOMode.DIGITAL_IN)
        remote_device.set_dio_change_detection({IOLine.DIO4_AD4})

        #   Potentiometer
        remote_device.set_io_configuration(IOLine.DIO2_AD2, IOMode.ADC)
        
        #   Photo Resistor
        remote_device.set_io_configuration(IOLine.DIO3_AD3, IOMode.ADC)
        
        # Register a listener to handle the samples received by the local device.
        def io_samples_callback(sample, remote, time):
            #print("New sample received from %s - %s" % (remote.get_64bit_addr(), sample))
            sample = str(sample).replace(" ", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("IOLine.", "").replace("IOValue.", "")
            sample = list(sample.split(','))
            data = dict()
            print(f"{datetime.now()}")
            for s in sample:
                d = s.split(":")
                data[d[0]] = d[1]
            
            for key, val in data.items():
                 print(f"    : {GROUP_NAME}/{DEVICE_ID}/{key} -> {val}")
                 try:
                     client.publish(f'{GROUP_NAME}/{DEVICE_ID}/{key}', val.encode('utf-8'))
                 except:
                     print("Failed to send to MQTT")
            print("\n")
        
        device.add_io_sample_received_callback(io_samples_callback)

        while True: 
            pass

    finally:
        if device is not None and device.is_open():
            device.close()



if __name__ == '__main__':
    main()
