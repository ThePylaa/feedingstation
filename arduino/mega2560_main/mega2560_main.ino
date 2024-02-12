#include <Stepper.h> 
#include "HX711.h"
#include "DHT.h"
#include <Rfid134.h>
#include <ArduinoJson.h>


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

//for RFID
#define RFIDRESET 28
//----------------

//global variables
String inputBuffer;
JsonDocument payload;
//-----------------

void setup() {
  //Fake Motor LED
  pinMode(22, OUTPUT);

  //USB communivcation with raspi
  Serial.begin(9600);

  //Serial2 is used for the RFID sensor
  Serial2.begin(9600);

  //Setup for scale
  scale.begin(DOUT, CLK);
  scale.tare();
  scale.set_scale(calibration_factor);

  //Humidity / Celcius sensor
  dht.begin();

  //Lightbarrier
  pinMode(LBP, INPUT);

  //RFID scanner setup
  pinMode(RFIDRESET, OUTPUT);
  resetRFID();

}

void loop() {
  //checks for instructions from the raspi
  while(Serial.available() > 0){
    char inChar = (char)Serial.read();
    inputBuffer += inChar;
  }

  //if instructions were send, process them
  if(inputBuffer != "" && inputBuffer.startsWith("dispense")){
    
    String numStr = inputBuffer.substring(8); // extracts part after "dispense"
    int amount = numStr.toInt(); // convert extracted String to int

    for (int i = 0; i< amount; i++) {
      dispenseFood();
      delay(260);
    }
  }
  
  char rfidRaw[14] = "----NORFID----";
  getRfid(rfidRaw);
  String rfidString;
  for (int i = 0; i < 14; i++) {
    rfidString += rfidRaw[i];
  }

  payload["rfid"]     = rfidString;
  payload["weight"]   = getFoodbowlWeight();
  payload["humidity"] = getHumidity();
  payload["temp"]     = getCelcius();
  payload["broken"]   = isBarrierBroken();
  serializeJson(payload, Serial);
  //!!! It's impoortant that the Serial terminates the data with \n otherwise the
  //raspberry can't recognize the end of the payload -> code freezes
  Serial.print("\n");

  inputBuffer = "";
  
  delay(1000); 
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

void resetRFID(){
  digitalWrite(RFIDRESET, LOW);
  delay(10);
  digitalWrite(RFIDRESET, HIGH);
}

void getRfid(char* getString){
  char asciiRfidCardNum[10];
  char asciiRfidCountry[4];
  int newInt;
  int index = 0;
  int inputBuffer[30];

  //read input from rfid sensor module
  while (Serial2.available()) {
    newInt = Serial2.read();
    inputBuffer[index] = newInt;
    index = index + 1;
  }

  //when there was an input
  if (index > 1 && inputBuffer[0] == 0) {
    
    for (int i = 2; i <= 11; i++) {
      asciiRfidCardNum[i - 2] = decToASCII(inputBuffer[i]);
    }
    for (int i = 12; i <= 15; i++) {
      asciiRfidCountry[i - 12] = decToASCII(inputBuffer[i]);
    }

    //reverse arrays
    reverseArray(asciiRfidCardNum, 10);
    reverseArray(asciiRfidCountry, 4);

    for (int i = 0; i < 14; i++) {
      if (i<10){
        getString[i] = asciiRfidCardNum[i];
      }else{
        getString[i] = asciiRfidCountry[i-10];
      }

    }
  }
  resetRFID();
}

char decToASCII(int dezimal) {
  return static_cast<char>(dezimal);
}

void reverseArray(char arr[], int length) {
  int temp;
  int start = 0;
  int end = length - 1;

  while (start < end) {
    temp = arr[start];
    arr[start] = arr[end];
    arr[end] = temp;
    start++;
    end--;
  }
}


