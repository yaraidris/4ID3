import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
from Config import HOST_IP, USER, PASSWORD, GROUP_NAME, DEVICE_ID


#   Connect to the MySQL server and a specific databse
connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=GROUP_NAME)
try:
    #   Retrieve all database records
    cursor = connection.cursor()  
    cursor.execute(f"""SELECT * FROM `{GROUP_NAME}`.`{DEVICE_ID}`; """)
    table = cursor.fetchall()
    now = datetime.now()
    #   Open a text file
    f = open(f'{GROUP_NAME}_{DEVICE_ID}_{now.strftime("%Y-%m-%d_%H-%M-%S")}.csv', 'w')
    #   Iterate over all database records and reformat them as CSV. Write them to the text file
    for row in table:
        print(f"{row[1]}, {row[2]}, {row[3]}", file=f)

    f.close()
    cursor.close() 
    connection.commit()
    connection.close()

except Error as e:
    print(f"ERROR: MQTT - / - > `{GROUP_NAME}`.`{DEVICE_ID}`", e)