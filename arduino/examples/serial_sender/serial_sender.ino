void setup() {
  Serial.begin(9600);   // Serial Monitor
  Serial3.begin(9600);  // Hardware-Serial auf TX3/RX3 Pins
}

void loop() {
  Serial3.print("5"); // Nachricht senden
  delay(5000);
  while (Serial3.available() > 0) {  
    char msg = Serial3.read(); // Nachricht empfangen
    Serial.print(msg);
  }
  Serial.println();
}
