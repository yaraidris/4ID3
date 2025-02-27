import mysql.connector
from mysql.connector import Error
#   Importing our user configurations from Config.py
from Config import HOST_IP, USER, PASSWORD, GROUP_NAME, DEVICE_ID


#   Try/except blocks allow you to handle exceptions when code fails to
#   execute with the expected response
try:
    #   Establishing connection to the MySQL server
    connection = mysql.connector.connect(host=HOST_IP,
                                         user=USER,
                                         password=PASSWORD)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()

        try:
            #   Try to remove the database if one is already there with that name
            cursor.execute(f"DROP DATABASE {GROUP_NAME}")
            print("Database dropped successfully")
            cursor.close() 
                

        except Error as e:
            print(e)

        try:
            cursor = connection.cursor()
            #   Print to the console the databases present in the MySQL server
            cursor.execute("SHOW DATABASES;")
            for x in cursor:
                print(f"   -> {x}")

            cursor.close()
            
            cursor = connection.cursor()
            #   Create a new database using the GROUP_NAME
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS `{GROUP_NAME}` DEFAULT CHARACTER SET utf8;")
            cursor.close() 
            connection.commit()
            print("Created Database")
        except Error as e:
            print(e)

        #   Connecting to that new database 
        connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=GROUP_NAME)
        
        print("Connected to database")

        #cursor.execute(f"USE `{DB_NAME}`;")
        try:
            cursor = connection.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS `{GROUP_NAME}`.`{DEVICE_ID}`;")
            cursor.close() 
            print("Dropped table")
        except Error as e:
            print("Failed to drop table", e)

        try:
            cursor = connection.cursor()
            #   Creating a new table for the device in use
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{GROUP_NAME}`.`{DEVICE_ID}`
                    (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT, 
                    `Timestamp` VARCHAR(45) NOT NULL,
                    `Sensor` VARCHAR(45) NOT NULL,
                    `Reading` VARCHAR(45) NOT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
                    ENGINE = InnoDB;
                    SET SQL_MODE=@OLD_SQL_MODE;
                    SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
                    SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS; """)

            print("Created table")
            print(cursor.fetchall())
            cursor.close() 
            
            
        except Error as e:
            print("Failed to create table", e)

        connection.close()
        connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=GROUP_NAME)

        try:  
            cursor = connection.cursor()  
            #   Inserting a row into that newly created table to ensure that 
            #   the data can be entered correctly without errors
            cursor.execute(f"""INSERT INTO `{GROUP_NAME}`.`{DEVICE_ID}` (`Timestamp`, `Sensor`, `Reading`) 
                    VALUES ('Test', 'Test', 'Test'); """)
            print("Inserted into table")
            res = cursor.fetchall()
            print(res)
            cursor.close() 
            connection.commit()
            
        except:
            print("Failed to insert into table")


        try:
            connection.close()
            connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=GROUP_NAME)
            cursor = connection.cursor()
            #   Retreiveing the entire table from the database
            cursor.execute(f"SELECT * FROM `{GROUP_NAME}`.`{DEVICE_ID}`;")
            table = cursor.fetchall()
            for row in table:
                print(f" [ {row} ] \n")

            print("Selected data from table")
            cursor.close()
            connection.commit()

        except Error as e:
            print("Failed to read table", e)




except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")