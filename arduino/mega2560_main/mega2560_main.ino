#include <Stepper.h> 
#include "HX711.h"
#include "DHT.h"

//for HX711
#define DOUT  36
#define CLK  34
HX711 scale;
float calibration_factor = 2180;
//---------

//for DHT11
#define DHTPIN 30
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
//----------

//for stepper motor
int SPU = 512; // Steps per turn
Stepper Motor(SPU, 37,35,33,31);
//----------------

//for lightbarrier
#define LBP 40
//----------------

//global variables
int inputInt = 0;
//-----------------

void setup() {
  //Fake Motor LED
  pinMode(22, OUTPUT);

  //USB communivcation with raspi
  Serial.begin(9600);

  //Setup for scale
  scale.begin(DOUT, CLK);
  scale.tare();
  scale.set_scale(calibration_factor);

  //Humidity / Celcius sensor
  dht.begin();

  //Lightbarrier
  pinMode(LBP, INPUT);
}

void loop() {
  //checks for instructions from the raspi
  //Needs to be -48 bc of ASCII-Byte-Int conversion
  if(Serial.available() > 0) inputInt = Serial.read() - 48; 

  if(inputInt > 0){
    //recieved char has to be convertet to an int
    manageArduinoInput(inputInt);
  }
  
  inputInt = 0;

  delay(100); 
}

//!!! It's impoortant that the Serial terminates the data with \n otherwise the
//raspberry can
void manageArduinoInput(int code){
  if(code == 1){
    //dispense 1 time 
    dispenseFood();
    return;
  }else if(code == 2){
    //get weight of scale
    int weight = getFoodbowlWeight();
    Serial.println(weight);
    return;
  }else if(code == 3){
    //returning foodlevelstatus barrier
    bool broken = isBarrierBroken();
    Serial.println(broken);
    return;
  }else if(code == 4){
    //return humidity
    float msg = getHumidity();
    Serial.println(msg);
    return;
  }else if(code == 5){
    //return degrees in celcius
    Serial.println(getCelcius());
    return;
  }else{
    Serial.println("False command");
    return;
  }
}

void dispenseFood(){
  digitalWrite(22, HIGH);
  delay(250);
  digitalWrite(22, LOW);

}

//gets weight of the foodbowl in gramms 
int getFoodbowlWeight(){
  return scale.get_units();
}

//turns the stepper x degrees
void turnDegrees(int degree){
  Motor.step(degree * 12);
  return;
}

//get humidity of DHT11
float getHumidity(){
  return dht.readHumidity();
}

//get degrees in °C from DHT11
float getCelcius(){
  return dht.readTemperature();
}

//checks if light barrier is broken
bool isBarrierBroken(){
  if (digitalRead(LBP)){
    return false;
  }
  return true;
}