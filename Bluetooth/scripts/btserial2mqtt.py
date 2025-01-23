#   Imported libraries
import serial
import json
import paho.mqtt.client as mqtt
import time

#   Configuring MQTT server and COM
mqtt_ip = None
mqtt_port = None
bluetooth_com_port = None

mqtt_ip = input("MQTT Broker IP: ")
if(mqtt_ip == None or mqtt_ip == ''): mqtt_ip = 'broker.hivemq.com'

mqtt_port = input("MQTT Broker Port: ")
if(mqtt_port == None or mqtt_port== ''): mqtt_port = 1883

bluetooth_com_port = input("Bluetooth COM (e.g. COM4): ")
if(bluetooth_com_port == None or bluetooth_com_port  == ''): bluetooth_com_port  = 'COM4'

print(f'\n-------\nCONFIGURATION\n-------\nIP: {mqtt_ip}\nPORT: {mqtt_port}\nBT COM: {bluetooth_com_port}')


#   MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected, status = {str(rc)}")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#   Connecting to serial
print("Connecting to serial: " + bluetooth_com_port)
time.sleep(1)
ser = serial.Serial(bluetooth_com_port, 9600)
print("Bluetooth COM opened")


while True:
    #   Refreshing the client connection
    if(client.is_connected() == False):
        client.connect(mqtt_ip, mqtt_port, 60)

    client.loop()   
    serial_json_string=str(ser.readline())  #   Reading serial to newline character '\n'
    first_split_index = serial_json_string.find('{')    #   Start of message
    second_split_index = serial_json_string.rfind('}')  #   End of message
    serial_json_string = serial_json_string[first_split_index: second_split_index+1]

    try:
        sensor_data = json.loads(serial_json_string)
        print(f"Received from Bluetooth: {sensor_data}")
        group_name = list(sensor_data.keys())[0]    #   Getting first key in JSON
        device_id = list(sensor_data[group_name])[0]    #   Getting value of first key from JSON
        for key, val in sensor_data[group_name][device_id].items():  
            success = client.publish(f'{group_name}/{device_id}/{key}', val.encode("UTF-8"))
            print(f'MQTT Publish {group_name}/{device_id}/{key} -> {val}\n    : send status = {success.is_published()}')
            
            
    except Exception as e:
        print("Failed to decode: ", e)
        print(serial_json_string)

ser.close()

