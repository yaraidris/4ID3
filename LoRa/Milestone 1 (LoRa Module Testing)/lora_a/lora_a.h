//Libraries
#include "EBYTE.h"
#include <HardwareSerial.h>

#define PIN_RX 16   // Serial2 RX -> EBYTE TX
#define PIN_TX 17   // Serial2 TX pin -> EBYTE RX
#define PIN_M0 27 
#define PIN_M1 26
#define PIN_AX 25
#define Serial_1 Serial2

#define TIME_PER_SEND_MS 5000
unsigned long startTime = millis();

//Transceiver frequency
#define TRANSCEIVER_CHANNEL 3 // Channel must be 0 - 64
EBYTE Transceiver(&Serial2, PIN_M0, PIN_M1, PIN_AX);

//Device details
String group_name = "Group3";
String device_name = "Device3B";
