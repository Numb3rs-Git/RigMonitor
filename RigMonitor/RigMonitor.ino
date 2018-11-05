#include "DHT.h"

#define TIMEOUT_MS 5000
#define RST_PIN    7
#define DHT_PIN    10
#define DHTTYPE    DHT11

DHT dht(DHT_PIN, DHTTYPE);
uint32_t lastPing, now, timeElapsed;
uint8_t inByte;
uint32_t nCycles;
float tmp, hum;
boolean started;

void setup(){
  Serial.begin(9600);
  started = false;
  inByte = 0;
  lastPing = 0;
  timeElapsed = 0;
  now = 0;
  nCycles = 0;
  pinMode(RST_PIN, OUTPUT);
  digitalWrite(RST_PIN, 0);
}

void loop(){

  if(Serial.available()){
    inByte = Serial.read();
    lastPing = millis();
    started = inByte == '*' ? false : true;
  }

  if(started){

    now = millis();
    
    if (lastPing > now)
      timeElapsed = (0xFFFFFFFF - lastPing) + now + 1;
    else
      timeElapsed = now - lastPing;

    if(timeElapsed > TIMEOUT_MS){
      reset();
      started = false;
    }
  }
  
  if(nCycles++ % 10 == 0){
    tmp = dht.readTemperature();
    hum = dht.readHumidity();
    if(!isnan(tmp) && !isnan(hum)){
      Serial.print("Temperature=");
      Serial.print(tmp);
      Serial.print(";Humidity=");
      Serial.print(hum);
      Serial.print("\n");
    }
  }    
  
  delay(100);
}

void reset(){
  digitalWrite(RST_PIN, 1);
  delay(500);
  digitalWrite(RST_PIN, 0);
}
