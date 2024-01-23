
#define DATA_PIN 38

void setup() {
  Serial.begin(9600);

  Serial.println("Startup");

  pinMode(DATA_PIN, INPUT);
}

void loop() {
  Serial.println("Schranke = " + String(digitalRead(DATA_PIN)));

  delay(2000);
}