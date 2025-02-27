//Yara Idris 400393007
//Luc Suzuki 400332170
//Shehab Ahmed 400359237
//Erin Ng 400360728

#include <TheThingsNetwork.h>

#define lora_serial Serial1
#define debug_serial Serial
#define frequency_plan TTN_FP_US915

TheThingsNetwork ttn(lora_serial, debug_serial, frequency_plan);

void setup(){
  lora_serial.begin(57600);
  debug_serial.begin(9600);
  
  while (!debug_serial) {}
  debug_serial.println("-- CONFIGURATION");
  debug_serial.println("Please note down your APP EUI and DEV EUI.");
  ttn.showStatus();
}
void loop()
{
}
