#
#   Simple SQL Database Parser
#   Adam Sokacz
#   2023 - 02 - 15
#

#   Libraries
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import json
import mysql.connector
from mysql.connector import Error
from Config import HOST_IP, USER, PASSWORD, GROUP_NAME, DEVICE_ID

#   HTTP Server
HTTP_IP = '0.0.0.0'
HTTP_PORT = 3000


#   Handles when a device makes a POST or GET request to HTTP server
class requestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global uiDict
        if self.path.endswith('/'):
            self.send_response(200)
            self.end_headers()
            connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=GROUP_NAME)
            try:
                cursor = connection.cursor()  
                #   Query data from the database, based on your database and table name
                cursor.execute(f"""SELECT * FROM `{GROUP_NAME}`.`{DEVICE_ID}` WHERE `{DEVICE_ID}`.`id` < 40 ORDER BY `{DEVICE_ID}`.`id` DESC; """)
                table = cursor.fetchall()
                #   Concatenate together an HTML/CSS document
                out = """
                    <style rel="stylesheet" type="text/css" media="screen">
                    html {
                        background-color: white;
                        margin: 0px 0px;
                        padding: 0px 0px;
                    }
                    ul { 
                        list-style-type: none; 
                    }
                    li {
                        font-size: 14pt;
                    }
                    fieldset {
                        background-color: white;
                        border: solid 3px #9c9c9c;
                        width: 400px;
                    }
                    legend {
                        font-size: 14pt;
                        font-weight: bold;
                    }
                    </style>"""

                for row in table:
                    out += f"""
                        <fieldset>
                            <legend>{row[2]}</legend>
                            <ul>
                                <li>Timestamp: {row[1]}</li>
                                <li>Reading: {row[3]}</li>
                            </ul>
                        </fieldset><br />"""

    
                cursor.close() 
                connection.commit()
                connection.close()


                
            except Error as e:
                print(f"DB Query Error", e)

            #   Serve the document to the user
            self.wfile.write(f"""
                    <html>
                    <body style="padding-left: 100px;">
                    <br />
                        <h2>MySQL Database Parser</h2>
                        <br/>
                        {out}
                    </body>
                    </html>
                    """.encode())
            


def main():
    #Tuple that stores the HTTP server data
    serverAddress = (HTTP_IP, HTTP_PORT)
    #Instantiate the server object
    server = HTTPServer(serverAddress, requestHandler)
    #Print useful data to the terminal
    print("\nSimple HTTP Server\n")
    print(f'HTTP server running on {HTTP_IP} port {HTTP_PORT}')
    print("\n\nServer Ready\n")
    #Serve the page until the thread exits
    server.serve_forever()

if __name__ == '__main__':
    main()




