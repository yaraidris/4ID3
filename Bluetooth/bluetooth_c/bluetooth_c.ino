//Yara Idris 400393007
//Luc Suzuki 400332170
//Shehab Ahmed 400359237
//Erin Ng 400360728
#include "bluetooth_c.h"

void setup() {
    Serial.begin(9600);
    Serial.print("\n\n------------------------\n"
      + group_name + " : " + device_name + "\n------------------------\n\n"); 

    bluetooth_serial.begin(group_name + " : " + device_name); 
    bluetooth_serial.flush();
    Serial.println("Ready for bluetooth connection!");

    Wire.begin();
    //  Initializing IO port for MCP23017 IO expansion bus
    mcp.init();
    mcp.portMode(MCP23017Port::A, 0); // Configuring port A as OUTPUT
    mcp.writeRegister(MCP23017Register::GPIO_A, 0x00);  //Resetting port A 
}


void loop() {
    String command = "";
    bool ret = 0;
    char char_byte = ' ';
    while (bluetooth_serial.available()){
      command = "";
      ret = 0;
      char_byte = ' '; 
      while(char_byte != '\n'){
        char_byte= bluetooth_serial.read();
        command += String(char_byte);
     }
     bluetooth_serial.flush();
     Serial.println(command);
     
     if(command == "LED_ON\n"){
        Serial.println("Value of 1 written to LED's 1 - 7");   
        mcp.digitalWrite(0, 1);
     }
     else if(command == "LED_OFF\n"){
        Serial.println("Value of 0 written to LED's 1 - 7");
        mcp.digitalWrite(0, 0);
    }
  }
}
