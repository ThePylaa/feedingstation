#include <ArduinoHttpClient.h>
#include <WiFi.h>
#include <WiFiSSLClient.h>
#include <ArduinoJson.h>
#include "RTClib.h" 

#include "arduino_secrets.h"

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
/////// WiFi Settings ///////
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
char uuid[] = DEVICE_UUID;

char serverAddress[] = API_HOST;  // server address
int port = 443;

// VERY IMPORTANT FOR HTTPs
WiFiSSLClient wifi;
// -----------------------
HttpClient client = HttpClient(wifi, serverAddress, port);
int status = WL_IDLE_STATUS;

//Real Time Clock 
RTC_DS3231 rtc; 

//global vars
JsonDocument schedule;
int scheduleSize[10][10] ={0};
String scheduleTime[10][10] = {
  {"","","","","","","","","",""},
  {"","","","","","","","","",""},
  {"","","","","","","","","",""},
  {"","","","","","","","","",""},
  {"","","","","","","","","",""},
  {"","","","","","","","","",""},
  {"","","","","","","","","",""},
  {"","","","","","","","","",""},
  {"","","","","","","","","",""},
  {"","","","","","","","","",""}
  };
String scheduleRFID[10] = {"","","","","","","","","",""};

void setup() {
  Serial.begin(9600);
  Serial3.begin(9600);

  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);                   

    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
  }

  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  //start realtime clock 
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }else{
    Serial.println("RTC started!");
  }
}

void loop() {
  Serial.println("Starting routine!");

  Serial.println("Updating DB");
  updateServerData();

  Serial.println("Getting schedule from DB");
  if(!getSchedule()){
    Serial.println("Couldn't get schedule, retrying next loop cicle!");
  }else{
    Serial.println("Fetched schedule!");
  }

  delay(500);

  doMainRoutine();

  Serial.println("Sleeping for 10 seconds...");
  delay(10000);
}

void updateServerData(){
  String humidity = String(getHumidity());
  updateHumidity(humidity);
  bool broke = isBarrierbroken();
  updateFoodlevel(broke);
}

void doMainRoutine(){
  DateTime now = getTime();

  //Check if an RFID is present
  String currRFID = getRFID();
  if(currRFID == ""){
    return;
  }
  Serial.println("Found RFID tag");

  //Check if RFID is known and has an uneaten portion
  int portionSize = isAllowedToEat(currRFID, now); 
  if(portionSize == 0){
    Serial.println("Not allowed to eat right now!");
    return;
  }

  //Check if weight is on the scale
  Serial.println("Checking Foodbowl...");
  int scaleTimer = 0;
  while(getWeight() > 10){
    Serial.println("The foodbowl isn't empty, not dispensing any food!");
    if(scaleTimer >= 10){
      //send animal didnt eat up to server
      return;
    }
    delay(1000);
    scaleTimer++;
  }

  //dispenses food 
  Serial.print("Dispensing ");
  Serial.print(portionSize);
  Serial.println(" portions");

  for(int i = 0; i<portionSize; i++){
    dispenseFood();
    delay(1000);
  }
}

//this function checks if the given RFID is allowed to eat something. Returns 0 if RFID isn't allowed
int isAllowedToEat(String scannedRFID, DateTime currTime){

  int scheduleRFIDLength = sizeof(scheduleRFID) / sizeof(scheduleRFID[0]);
  for (int i = 0; i < scheduleRFIDLength; i++){
    //check if RFID is known in schedule
    if(scheduleRFID[i] != "" && scheduleRFID[i] == scannedRFID){
      Serial.print("RFID known: ");
      Serial.println(scheduleRFID[i]);

      //check if RFID has an uneaten portion
      int scheduleTimeLength = sizeof(scheduleTime[i]) / sizeof(scheduleTime[i][0]);
      for (int j = 0; j < scheduleTimeLength; j++){
        if(scheduleTime[i][j] != "" && scheduleTime[i][j].substring(0, 2).toInt() <= currTime.hour()){
          if(scheduleTime[i][j].substring(0, 2).toInt() == currTime.hour() && scheduleTime[i][j].substring(3, 5).toInt() > currTime.minute()){
            return 0;
          }
          //TODO check if already taken or not
            Serial.print("Is allowed to eat: ");
            Serial.println(scheduleSize[i][j]);
            return scheduleSize[i][j];
        } 
      }
    }
  }
  return 0;
}


//this function checks if an rfid chip is scanned and returns it TODO TODO TODO TODO
String getRFID(){
  //return "NochNeFakeId";
  return "FAKERFID";
  //return "";
}

//this function gets the schedule from the DB
bool getSchedule() {

  client.get(String("/portion/portions?feedingstation=" + String(uuid)));
  String responseJson = client.responseBody();
  client.stop();

  DeserializationError error = deserializeJson(schedule, responseJson);

  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return false;
  }

  //now get the schedule times and sizes of each scheduleRFID
  int animalIndex = 0; 
  for (JsonObject item : schedule.as<JsonArray>()) {
    scheduleRFID[animalIndex] = item["animal_rfid"].as<String>();
    int portionIndex = 0;
    for (JsonObject portion : item["portions"].as<JsonArray>()) {
      scheduleTime[animalIndex][portionIndex] = portion["time"].as<String>();
      scheduleSize[animalIndex][portionIndex] = portion["size"].as<int>();
      portionIndex++;
    }
    animalIndex++;
  }

  return true;
}

//this function registers your Feedingstation in the DB
String registerStation(String name){

  //register Station in the DB
  Serial.println("Register Station in the DB");
  String postData = "{\"feedingstation_id\": \"" + String(uuid) + "\",\"name\": \"" + name + "\"}";
  client.beginRequest();
  client.post("/feedingstation/register");
  client.sendHeader("Content-Type", "application/json");
  client.sendHeader("Content-Length", postData.length());
  client.sendHeader("Host: " + String(serverAddress));
  client.beginBody();
  client.print(postData);
  client.endRequest();

  String response = client.responseBody();
  client.stop();

  return response;
}

//this function updates the the foodlevel in the db
String updateFoodlevel(bool broken){
  String contentType = "application/json";
  String putData =  "{\"feedingstation_id\": \"" + String(uuid) + "\",\"container_foodlevel\": \"" + broken + "\"}";

  Serial.print("Updating foodlevel to: ");
  Serial.println(broken);
  client.put("/feedingstation/update_container_foodlevel", contentType, putData);

  String response = client.responseBody();
  client.stop();

  return response;
}

String updateHumidity(String humidity){
  String contentType = "application/json";
  String putData =  "{\"feedingstation_id\": \"" + String(uuid) + "\",\"humidity\": \"" + humidity + "\"}";

  Serial.print("Updating humidity to: ");
  Serial.println(humidity);
  client.put("/feedingstation/update_humidity", contentType, putData);

  String response = client.responseBody();
  client.stop();

  return response;
}

//sends signal to the other arduino and returns answer
String sendInstruction(int code){
  //Serial.println(code);
  Serial3.print(code);
  delay(1000);
  int index = 0;
  char responseBuffer[10];
  while (Serial3.available() > 0) {  
    char responseChar = Serial3.read(); // Nachricht empfangen
    responseBuffer[index] = responseChar;
    index++;
  }
  
  return String(responseBuffer);
}

//get celcius from other arduino sensor
float getCelcius(){
    // Convert String to float
    String responseStr = sendInstruction(5);
    float response = responseStr.toFloat();
    return response;
}

//get humidity from other arduino sensor
float getHumidity(){ 
    String responseStr = sendInstruction(4);
    // Convert String to float
    float response = responseStr.toFloat();
    return response;
}

//checks if foodlevel barrier from other arduino is broken
int isBarrierbroken(){
  // Convert String to int
  String responseStr = sendInstruction(3);
  int response = responseStr.toInt();
  return response;
}

//get weight of the hx711/foodbowl
int getWeight(){
  // Convert String to int
  String responseStr = sendInstruction(2);
  int response = responseStr.toInt();
  return response;
}

//dispense one portion of food
void dispenseFood(){
  sendInstruction(1);
  return;
}

//get current time
DateTime getTime(){
  return rtc.now();
}

//debug printing
void printSchedule(){
  int scheduleRFIDLength = sizeof(scheduleRFID) / sizeof(scheduleRFID[0]);
  for (int i = 0; i < scheduleRFIDLength; i++)
  {
    //print all RFID's and their portions and times for debugging
    if(scheduleRFID[i] != ""){
        Serial.println(scheduleRFID[i]);
      }
    int scheduleTimeLength = sizeof(scheduleTime[i]) / sizeof(scheduleTime[i][0]);
    for (int j = 0; j < scheduleTimeLength; j++)
    {
      if(scheduleTime[i][j] != ""){
        Serial.println(scheduleTime[i][j]);
      }

      if(scheduleSize[i][j] != 0){
        Serial.println(scheduleSize[i][j]);
      }  
    }
  }
}

