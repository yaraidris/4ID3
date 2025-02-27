import mysql.connector
from mysql.connector import Error
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime
#   Importing our configurations from Config.py
from Config import HOST_IP, USER, PASSWORD, GROUP_NAME, DEVICE_ID, MQTT_HOSTNAME, MQTT_API_KEY, MQTT_PORT, MQTT_TOPIC, MQTT_USERNAME



print(f'\n-------\nCONFIGURATION\n-------\nIP: {MQTT_HOSTNAME}\nPORT: {MQTT_PORT}\nTOPIC: {MQTT_TOPIC}\n')

def on_connect(client, userdata, flags, rc):
    print("MQTT connection code: "+str(rc))

#   Message handler callback function
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    #   Parse the message as a JSON formatted data object
    payload = json.loads(str(msg.payload.decode('utf-8')))
    #print(payload)
    try:
        deviceId  = payload["end_device_ids"]["device_id"]
        #   Parse out the information that we need and store it as a python dictionary
        data = dict(payload["uplink_message"]["decoded_payload"][GROUP_NAME][DEVICE_ID])
        #   Retrieve the time at this instant
        now = datetime.now()

        #   Iterate over the number of sensors in the parse JSON object
        for sensor, reading in data.items():
            #   For each sensor, connect to the database and insert the data
            #   as a new row in your devices table
            connection = mysql.connector.connect(host=HOST_IP,
                                                user=USER,
                                                password=PASSWORD,
                                                database=GROUP_NAME)
            cursor = connection.cursor()  
            cursor.execute(f"""INSERT INTO `{GROUP_NAME}`.`{DEVICE_ID}` (`Timestamp`, `Sensor`, `Reading`) VALUES ('{now.strftime("%Y-%m-%d %H:%M:%S")}', '{sensor}', '{str(reading)}'); """)
            print(f"['{now.strftime('%Y-%m-%d %H:%M:%S')}', '{sensor}', '{str(reading)}' ] MQTT -> MySQL ( `{GROUP_NAME}`.`{DEVICE_ID}` )")
            res = cursor.fetchall()
            print(f"Response from MySQL: {res}\n\n")
            cursor.close() 
            connection.commit()
            connection.close()


    except Error as e:
        print(f"ERROR: MQTT - / - > `{GROUP_NAME}`.`{DEVICE_ID}`", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
print("Connecting to MQTT")

#   Connect to an MQTT server that uses basic username/password security over TCP
client.username_pw_set(MQTT_USERNAME, MQTT_API_KEY)
client.connect(MQTT_HOSTNAME, port=MQTT_PORT)
client.subscribe("#")

client.loop_forever() 