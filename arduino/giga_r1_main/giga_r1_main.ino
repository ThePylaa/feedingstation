#include <ArduinoHttpClient.h>
#include <WiFi.h>
#include <WiFiSSLClient.h>
#include <ArduinoJson.h>

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

//global vars
JsonDocument schedule;
int scheduleSize[10];
String scheduleTime[10];
String scheduleRFID[10];


void setup() {
  Serial.begin(9600);
  Serial3.begin(9600);

  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);                   // print the network name (SSID);

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
}

void loop() {
  Serial.println("Starting routine!");

  Serial.println("Getting schedule from DB");
  if(!getSchedule(scheduleSize, scheduleTime, scheduleRFID)){
    Serial.println("Couldn't get schedule, retrying next loop cicle!");
  }
  Serial.println(scheduleTime[0]);
  Serial.println(String(scheduleSize[0]));
  Serial.println(scheduleRFID[0]);

  delay(10000);
}

void doRoutine(){
  //if(!isValidRFID()){
  //  return;  
  //}
  //if(currenttime >= scheduleTimes){
  // 
  //  if (getWeight() > 5){
  //    delay(5000);
  //    if(getWeight() > 5){
  //      sendNoticicationToUser();
  //      return;
  //    }
  //  }
  //  for(int i = 0; i<schedulePortions; i++){
  //    dispenseFood();
  //  }
  //  delay(9999999);
  //    
  //  dosmthWithGetWeight()!!!  
  //
  //}
}

//this function checks if an rfid chip is scanned and valid for eating time
bool isValidRFID(){
  return true;
}

//this function gets the schedule from the DB
bool getSchedule(int* scheduleSize, String* scheduleTime, String* scheduleRFID) {
  client.get(String("/portion/portions?feedingstation=" + String(uuid)));
  String responseJson = client.responseBody();
  client.stop();

 
  DeserializationError error = deserializeJson(schedule, responseJson);

  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return false;
  }

  int index = 0;
  for (JsonObject item : schedule.as<JsonArray>()) {
    scheduleSize[index] = item["size"].as<int>(); // 20, 60, 60, 60, 60, 60, 60, 60, 60
    scheduleRFID[index] = item["animal_rfid"].as<String>(); // "FAKERFID", "FAKERFID", "FAKERFID", "FAKERFID", ...
    scheduleTime[index] = item["time"].as<String>(); // "16:55:19", "10:32:20.202000", "10:32:20.202000", "10:32:20.202000", ...
    index++;
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
    // Convert String to float
    String responseStr = sendInstruction(4);
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


