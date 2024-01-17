#include "DHT.h"

//ATTENTION: PIN NUMBERs: D5 = 5, not 8 like in pinlayout
#define DHTPIN 50
///
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

char arduinoPayload[5]; // Char-Array für die Daten, inklusive Null-Terminator

void setup() {
  // Begin the Serial at 9600 Baud
  Serial.begin(9600);

  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  dtostrf(humidity, 4, 2, arduinoPayload); // Konvertiere die Float-Zahl in ein char-Array

  Serial.write(arduinoPayload, 5); //Write the serial data
  delay(1000);
}