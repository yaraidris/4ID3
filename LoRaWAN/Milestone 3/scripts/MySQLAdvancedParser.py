#
#   Advanced SQL Database Parser
#   Adam Sokacz
#   2023 - 02 - 17
#

#   Libraries
import socketserver
import http.server
import logging
import time
import json
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse, parse_qs
import cgi
from Config import HOST_IP, USER, PASSWORD, GROUP_NAME, DEVICE_ID

#   HTTP Server
HTTP_IP = '0.0.0.0'
PORT = 3000


class ServerHandler(http.server.SimpleHTTPRequestHandler):
    #   Serve get requests
    def do_GET(self):
        logging.error(self.headers)
        #   If base route, serve this page
        if self.path.endswith(''):
            #   Error code of 200 means that it was processed correctly
            self.send_response(200)
            #   Finished settings, now go to the HTML document
            self.end_headers()
        
            #   Start concatenating together an HTML/CSS document
            out = """
                <style rel="stylesheet" type="text/css" media="screen">
                html {
                    background-color: #DCDCDC;
                    margin: 0px 0px;
                    padding: 0px 0px;
                }
                ul { 
                    list-style-type: none; 
                }
                li {
                    font-size: 18pt;
                }
                fieldset {
                    background-color: white;
                    border: solid 3px #9c9c9c;
                    width: 400px;
                }
                legend {
                    font-size: 20pt;
                    font-weight: bold;
                }
                </style>"""

            out += """
                <form method="POST" action="/data">
                    <label for="dbip">What is the IP for the Database:</label>
                    <input type="text" id="dbip" name="dbip" value = "localhost"></input>
                    <br />
                    <br />
                    <label for="dbuser">Database Username:</label>
                    <input type="text" id="dbuser" name="dbuser" value = "root"></input>
                    <br />
                    <br />
                    <label for="dbpass">Database Password:</label>
                    <input type="password" id="dbpass" name="dbpass" value = "9055259140"></input>
                    <br />
                    <br />
                    <label for="dbname">Database Name:</label>
                    <input type="text" id="dbname" name="dbname" value = "GroupA"></input>
                    <br />
                    <br />
                    <label for="dbtable">Database Table:</label>
                    <input type="text" id="dbtable" name="dbtable" value = "DeviceA"></input>
                    <br />
                    <br />
                    <label for="filters">Choose a Filter:</label>
                    <select name="filters" id="filters">
                        <option value="id">id</option>
                        <option value="Timestamp">Timestamp</option>
                        <option value="Sensor">Sensor</option>
                        <option value="Reading">Reading</option>
                    </select>
                    <br />
                    <br />
                    <label for="comparison">Choose a Comparison:</label>
                    <select name="comparison" id="comparison">
                        <option value="<">LES</option>
                        <option value=">">GRT</option>
                        <option value="=">EQL</option>
                    </select>
                    <br />
                    <br />
                    <input type="text" id="val" name="val" value = "5"></input> 
                    <br />
                    <br />
                    <label for="order">Order by:</label>
                    <select name="order" id="order">
                        <option value="ASC">ASC</option>
                        <option value="DESC">DESC</option>

                    </select>
                    <br />
                    <br />
                    <button type="submit">Query Database</button>
                </form>
            """
       

            self.wfile.write(f"""
                    <html>
                    <body style="padding-left: 100px;">
                    <br />
                        <h1>MySQL Database Parser</h1>
                        <br/>
                        {out}
                    </body>
                    </html>
                    """.encode())


    def do_POST(self):
        #logging.error(self.headers)
        if self.path.endswith('/data'):
            self.send_response(200)
            self.end_headers()
            #   Parse all the data that was submitted by the HTML form
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })
            #   Convert the submitted data to a python dictionary
            postVals = dict()            
            for key in form.keys():
                postVals[key] =  form.getvalue(str(key))             
            
            postVals["comparison"] = postVals["comparison"][0]

            def ifExists(val):
                
                if postVals[val] != None:
                    print(f'{val} exits :)')
                    return postVals[val]
                else:
                    print(f'{val} does not exist!')
                    return "NONE"

            out = str()
            table = dict()

            try:
                connection = mysql.connector.connect(host=postVals["dbip"],
                                            user=postVals["dbuser"],
                                            password=postVals["dbpass"],
                                            database=postVals["dbname"])
                print("Conn")
                #   Concatenate together a MySQL query
                cursor = connection.cursor()  
                print('cursor')
                query = str(f"SELECT * FROM `{ifExists('dbname')}`.`{ifExists('dbtable')}` WHERE `{ifExists('dbtable')}`.`{ifExists('filters')}` {ifExists('comparison')} {ifExists('val')} ORDER BY `id` {ifExists('order')};") # ORDER BY `{ifExists('tbtable')}`.`iddata` {ifExists('order')} ; ")
                
                print("Q:")
                print(query)
                cursor.execute(query)
                table = cursor.fetchall()
                print(table)
                cursor.close()
                connection.close()
                #   Format the HTML document to serve back to the user
                out += "<table style='border: 1px solid black;'> "
                for row in table:
                    out += "<tr> "
                    for col in row:
                        out += f"<td style='width: 150px; border: 1px solid black;'>{col}</td>"

                    out += " </tr>"

                out += " </table>" 

            except:
                logging.error(form.keys())
                print("ERROR")
                out += "<h1>ERROR</h1>"
            
            
            
            #   Serve your HTML/CSS document to the user
            self.wfile.write(f"""
                    <html>
                    <body style="padding-left: 100px;">
                    <br />
                        <h1>MySQL Database Parser</h1>
                        <br />
                        <a href="/"><button>Back</button></a>
                        <br />
                        <br />
                        <b>HTML Form Debug:</b> {str(postVals)} <br />
                        <b>Generated MySQL Query:</b> {str(query)} <br /> <br />
                        <br/>
                        {out}
                        <br />

                    </body>
                    </html>
                    """.encode())

Handler = ServerHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()

