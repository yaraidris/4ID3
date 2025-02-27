//Yara Idris 400393007
//Luc Suzuki 400332170
//Shehab Ahmed 400359237
//Erin Ng 400360728

#include "field_device.h"
void setup() {
  lora_serial.begin(57600);
  debug_serial.println("-- JOIN");
  ttn.join(app_eui, app_key);

  debug_serial.begin(9600);
  while (!debug_serial) {}
  
  debug_serial.println("-- STATUS");
  ttn.showStatus();
  
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);
  dht.begin();
  
  Serial.println("\n\n--------------------------------------\n\n      The Things Uno\n      "
              + String(GROUP_NAME) + " - " + String(DEVICE_NAME) 
              + "\n\n--------------------------------------\n\n");

}

void loop() {
  if(millis() - start_time > POLLING_PERIOD){
    sensors_event_t temp_event, hum_event;
    dht.temperature().getEvent(&temp_event);
    float temp = round(temp_event.temperature * 100) / 100.0;
    dht.humidity().getEvent(&hum_event);
    float hum = round(hum_event.relative_humidity * 100) / 100.0;
    delay(200);
    if((100 > temp > -100) && (100 > hum > -100)){
      String msg = "{ \"" + String(GROUP_NAME) +  "\": { \"" + String(DEVICE_NAME) 
                  + "\": { \"Temperature\": " + String(temp) 
                  + " , \"Humidity\": " + String(hum) + " } } }";
      debug_serial.println(msg);
      
      char msg_data[msg.length()];
      for(int i = 0; i < msg.length(); i++){
        msg_data[i] = msg[i];
      }
      ttn.sendBytes(msg_data, sizeof(msg_data));
    }
    else{
      debug_serial.println("Unable to read sensor data...");
    }

    start_time = millis();  
  }
}
