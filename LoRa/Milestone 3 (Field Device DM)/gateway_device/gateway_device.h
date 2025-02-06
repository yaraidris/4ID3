//Libraries
#include "EBYTE.h"
#include <HardwareSerial.h>
#include <WiFi.h>
#include <WebServer.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "MCP23017.h"
#include <Wire.h>

//Pin definitions
#define PIN_RX 16  
#define PIN_TX 17 
#define PIN_M0 27  
#define PIN_M1 26 
#define PIN_AX 25 
#define Serial_0 Serial2  

#define TIME_PER_SEND_MS 5000
unsigned long startTime = millis();

//Transceiver setup
#define TRANSCEIVER_CHANNEL 3
EBYTE Transceiver(&Serial2, PIN_M0, PIN_M1, PIN_AX);

const char* group_name = "Group3";
const char* gateway_device_name = "GatewayDevice";
const char* field_device_name = "FieldDevice";

//WiFi login credentials
const char* ssid = "SEPT SmartLAB 537";
const char* pass = "Factory1";
const char* mqtt_server = "broker.hivemq.com"; //mqtt server

WiFiClient espClient;
PubSubClient client(espClient);

#define MCP23017_ADDR 0x20
MCP23017 mcp = MCP23017(MCP23017_ADDR);
