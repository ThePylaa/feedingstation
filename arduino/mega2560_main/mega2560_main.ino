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
#define DHTPIN 53
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
//----------

//for stepper motor
int SPU = 512; // Steps per turn
Stepper Motor(SPU, 37,35,33,31);
//----------------

//for lightbarrier
#define LBP 23
//----------------

//global variables
char serialInstruction[1];
//-----------------

void setup() {
  Serial.begin(9600);
  //for communication with other arduino, SERIAL2 = TX2/RX2
  Serial2.begin(9600);

  Motor.setSpeed(20);

  scale.begin(DOUT, CLK);
  scale.tare();
  scale.set_scale(calibration_factor);

  dht.begin();

  pinMode(LBP, INPUT);
}

void loop() {
  //checks for instructions from the other arduino
  serialInstruction[0] = 0;
  if (Serial2.available() > 0) {  
    serialInstruction[0] = Serial2.read(); 
  }
  //recieved char has to be convertet to an int
  manageArduinoInput(atoi(serialInstruction)); 

  delay(5000); 
}

void manageArduinoInput(int code){
  Serial.println(code);
  if (code == 0){
    Serial.println("Doing nothing");
    return;
  }else if(code == 1){
    //dispense 1 time 
    Serial.println("Dispensing food");
    dispenseFood();
    return;
  }else if(code == 2){
    //get weight of scale
    Serial.println("Returning scalevalue");
    int weight = getFoodbowlWeight();
    Serial2.print(weight);
    Serial.print("Weight: ");
    Serial.println(weight);
    return;
  }else if(code == 3){
    //returning foodlevelstatus barrier
    bool broken = isBarrierBroken();
    Serial.print("Barrier is broken: ");
    Serial.println(broken);
    Serial2.print(broken);
    return;
  }else if(code == 4){
    //return humidity
    float msg = getHumidity();
    Serial2.print(msg);
    return;
  }else if(code == 5){
    //return degrees in celcius
    Serial2.print(getCelcius());
    return;
  }else{
    Serial.println("False signal from arduino");
    return;
  }
}

void dispenseFood(){
  turnDegrees(60);
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