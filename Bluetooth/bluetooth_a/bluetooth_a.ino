//Yara Idris 400393007
//Luc Suzuki 400332170
//Shehab Ahmed 400359237
//Erin Ng 400360728

#include "bluetooth_a.h"

void setup() {
  Serial.begin(9600);
  Serial.print("\n\n------------------------\n"
    + group_name + " : " + device_name + "\n------------------------\n\n"); 

  Wire.begin();
  Wire.beginTransmission(ADDR);
  Wire.endTransmission();
  delay(300);
  
  light_sensor.begin(apds_gain, apds_time);
  
}

void loop() {
  Wire.beginTransmission(ADDR);
  Wire.write(TMP_CMD);
  Wire.endTransmission();
  delay(100);

  Wire.requestFrom(ADDR, 2);

  char data[2];
  if(Wire.available() == 2){
    data[0] = Wire.read();
    data[1] = Wire.read();
  }

  float temp = ((data[0] * 256.0) + data[1]);
  float temp_c = ((175.72 * temp) / 65536.0) - 46.85;

  AsyncAPDS9306Data light_data = light_sensor.syncLuminosityMeasurement();
  float lux = light_data.calculateLux();

  String formatted_data = 
    "{ \"" + group_name + "\": { \"" 
    + device_name + "\": { \"Temp\": \"" 
    + String(temp_c) + "\", \"Luminosity\": \"" 
    + String(lux) + "\" } } }" + '\n';
      
  Serial.println(formatted_data);
  
  delay(DELAY_BETWEEN_SAMPLES_MS);

}
