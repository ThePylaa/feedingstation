#include "DHT.h"

//ATTENTION: PIN NUMBERs: D5 = 5, not 8 like in pinlayout
#define DHTPIN 50
///


#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);

  dht.begin();
}

void loop() {
  Serial.println("Temperature = " + String(dht.readTemperature()) + " °C");
  Serial.println("Humidite = " + String(dht.readHumidity()) + " %");

  delay(3000);
}