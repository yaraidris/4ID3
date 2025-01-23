#   Importing libraries
import serial
import json
import time
import pymongo

#   Setting the COM and MongoDB targets
db_address = "mongodb://localhost:27017/"
bluetooth_com_port = None
bluetooth_com_port = input("Bluetooth COM (e.g. COM4): ")
if(bluetooth_com_port == None or bluetooth_com_port  == ''): bluetooth_com_port = 'COM4'
print(f'\n-------\nCONFIGURATION\n-------\nBT COM: { bluetooth_com_port }\nMongoDB: {db_address}')

#   Connecting to bluetooth
print("Connecting to serial: " + bluetooth_com_port)
time.sleep(1)
ser = serial.Serial(bluetooth_com_port, 9600)
print("Bluetooth COM opened")

#   Instantiating the MongoDB client
mongo_client = pymongo.MongoClient(db_address)

while True:
    serial_json_string=str(ser.readline())
    firstSplitIndex = serial_json_string.find('{')
    secondSplitIndex = serial_json_string.rfind('}')
    serial_json_string = serial_json_string[firstSplitIndex: secondSplitIndex+1]
   
    try:
        json_data = json.loads(serial_json_string)
        print(f"Received: {json_data} ")
        group_name = list(json_data.keys())[0]
        device_id = list(json_data[group_name])[0]
    
        database = mongo_client[group_name]
        collection = database[device_id]

        db_response = collection.insert_one(json_data[group_name][device_id])
        print(f"Inserted document, response code: {db_response}")
            
    except Exception as e:
        print(f"Failed to decode: \n    : {serial_json_string} \n    : {e}")
   

ser.close()
