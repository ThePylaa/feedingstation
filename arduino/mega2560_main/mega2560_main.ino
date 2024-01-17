#include <Stepper.h> 
#include "HX711.h"
#include "DHT.h"

//for HX711
#define DOUT  20
#define CLK  21
HX711 scale;
float calibration_factor = 2180;
//---------
//for DHT11
//ATTENTION: PIN NUMBERs: D5 = 5, not 8 like in pinlayout
#define DHTPIN 53
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
//----------
//for stepper motor
int SPU = 512; // Steps per turn
Stepper Motor(SPU, 37,35,33,31);
//----------------

void setup() {
  Serial.begin(9600);
  
  Motor.setSpeed(20);

  scale.begin(DOUT, CLK);
  scale.tare();
  scale.set_scale(calibration_factor);

  dht.begin();

}

void loop() {
  
  

  Serial.println(getHumidity());

  delay(2000); 
}

//gets weight of the foodbowl in gramms 
int getFoodbowlWeight(){
  return scale.get_units();
}

//turns the stepper x degrees
void turnDegrees(int degree){
  Motor.step(degree * 12);
}

//get humidity of DHT11
float getHumidity(){
  return dht.readHumidity();
}

//get degrees in °C from DHT11
float getCelcius(){
  return dht.readTemperature();
}