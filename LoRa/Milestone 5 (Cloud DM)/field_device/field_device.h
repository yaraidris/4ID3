//Libraries
#include <Arduino.h>
#include <Wire.h>
#include <AsyncAPDS9306.h>
#include "EBYTE.h"
#include <HardwareSerial.h>
#include "MCP23017.h"

//Pin definitions 
#define PIN_RX 16   
#define PIN_TX 17   
#define PIN_M0 27  
#define PIN_M1 26   
#define PIN_AX 25  
#define Serial_0 Serial2

//Sample frequency
#define POLLING_PERIOD 5000
unsigned long start_time = millis();

//Transceiver setup
#define TRANSCEIVER_CHANNEL 3
EBYTE Transceiver(&Serial2, PIN_M0, PIN_M1, PIN_AX);

//Device information
String group_name = "Group3";
String device_name = "FieldDevice";

//Sensor IIC addresses
#define ADDR (byte)(0x40)
#define TMP_CMD (byte)(0xF3)

//Configure I/O expansion board
#define MCP23017_ADDR 0x20
MCP23017 mcp = MCP23017(MCP23017_ADDR);

//Instantiating sensor object and configuration
AsyncAPDS9306 light_sensor;
const APDS9306_ALS_GAIN_t a_gain = APDS9306_ALS_GAIN_1;
const APDS9306_ALS_MEAS_RES_t a_time = APDS9306_ALS_MEAS_RES_16BIT_25MS;

//Create some global variables
float temp, temp_c, lux;
