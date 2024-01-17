#include <ArduinoHttpClient.h>
#include <WiFi.h>
#include <WiFiSSLClient.h>


#include "arduino_secrets.h"

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
/////// WiFi Settings ///////
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;

char serverAddress[] = API_HOST;  // server address
int port = 443;

String uuid;

// VERY IMPORTANT FOR HTTPs
WiFiSSLClient wifi;
// -----------------------
HttpClient client = HttpClient(wifi, serverAddress, port);
int status = WL_IDLE_STATUS;

void setup() {
  Serial.begin(9600);
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
  // Getting the UUID from the API. Neccessary for possible duplicants
  Serial.println("Getting UUID from API");
  client.get("/feedingstation/get_station_uuid");

  // read the status code and body of the response
  int statusCode = client.responseStatusCode();
  uuid = client.responseBody();
  client.stop();

  //register Station in the DB
  Serial.println("Register Station in the DB");
  String postData = "{\"feedingstation_id\": " + uuid + ",\"name\": \"string\"}";
  Serial.println(postData);
  client.beginRequest();
  client.post("/feedingstation/register");
  client.sendHeader("Content-Type", "application/json");
  client.sendHeader("Content-Length", postData.length());
  client.sendHeader("Host: " + String(serverAddress));
  client.beginBody();
  client.print(postData);
  client.endRequest();

  statusCode = client.responseStatusCode();
  String response = client.responseBody();

  while(true){
    Serial.print("Status code: ");
    Serial.println(statusCode);
    Serial.print("Response: ");
    Serial.println(response);
    Serial.println("Wait ten seconds");
    delay(10000);
  }
  
}