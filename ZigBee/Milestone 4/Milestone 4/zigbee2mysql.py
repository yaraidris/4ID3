#------------------------------------
#       LIBRARIES
#------------------------------------

from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
from datetime import datetime


#------------------------------------
#       CONFIGURATIONS
#------------------------------------

#   Database Connection
HOST_IP = "localhost"
USER = "root"
PASSWORD = "Y3414071i!"

#   Device Connection
PORT = "COM5"
BAUD_RATE = 9600
REMOTE_NODE_ID = "END_DEVICE"
IO_SAMPLING_RATE = 5  # 5 seconds.
GROUP_NAME = "Group3"
DEVICE_ID = "DeviceA"


def reset_database():
    print("---\nDatabase reset:")
    connection = mysql.connector.connect(host=HOST_IP,
                                         user=USER,
                                         password=PASSWORD)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("    > Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE `{GROUP_NAME}`")
        print("    > Database dropped successfully")
        cursor.close() 
        connection.commit()
        cursor = connection.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS `{GROUP_NAME}` DEFAULT CHARACTER SET utf8;")
        cursor.close() 
        connection.commit()
        print("     > Created Database")
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS `{GROUP_NAME}`.`{DEVICE_ID}`;")
        cursor.close()
        connection.commit() 
        print(f"    > Dropped table {DEVICE_ID}")
        cursor = connection.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{GROUP_NAME}`.`{DEVICE_ID}`
                    (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                    `Time` VARCHAR(45) NOT NULL,
                    `Sensor` VARCHAR(45) NOT NULL,
                    `Value` VARCHAR(45) NOT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
                    ENGINE = InnoDB;
                    SET SQL_MODE=@OLD_SQL_MODE;
                    SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
                    SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS; """)

        print("     > Created table")
        print(cursor.fetchall())
        cursor.close() 
        #connection.commit()
        connection.close()
        print("Database reset successful\n---\n\n")



#------------------------------------
#       MAIN METHOD
#------------------------------------

def main():
    print(" +----------------------------------------------+")
    print(" | XBee Python Library Handle IO Samples Sample |")
    print(" +----------------------------------------------+\n")

    try:
        reset_database()

    except Exception as e:
        print(f"Failed to reset db {e}")
    
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
            t = datetime.now()
            print(f"{t}")
            for s in sample:
                d = s.split(":")
                data[d[0]] = d[1]
            
            for key, val in data.items():
                print(f"    : {GROUP_NAME}/{DEVICE_ID}/{key} -> {val}")
                try:
                    connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=GROUP_NAME)
                    cursor = connection.cursor()
                    query = f"INSERT INTO `{GROUP_NAME}`.`{DEVICE_ID}` (`Time`, `Sensor`, `Value`) VALUES ('{str(t.strftime('%d/%m/%Y %H:%M:%S'))}', '{str(key)}', '{str(val)}'); "
                    print(query)
                    cursor.execute(query)
                    cursor.close()
                    connection.commit()
                    connection.close()
                except:
                    print("Failed to send to MySQL")

            print("\n")
        
        device.add_io_sample_received_callback(io_samples_callback)

        while True: 
            pass

    finally:
        if device is not None and device.is_open():
            device.close()



if __name__ == '__main__':
    main()
