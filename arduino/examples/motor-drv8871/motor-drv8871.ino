// Basic sketch for trying out the Adafruit DRV8871 Breakout

#define MOTOR_IN1 22

void setup() {
  Serial.begin(9600);

  Serial.println("DRV8871 test");
  
  pinMode(MOTOR_IN1, OUTPUT);
}

void loop() {
  if(Serial.available() != 0){
    delay(100);
    Serial.read();
  }

  // ramp up forward
  Serial.println("Start");
  for (int i=127; i<132; i++) {
    analogWrite(MOTOR_IN1, i);
    delay(6);
  }
  

  // forward full speed for one second
  digitalWrite(MOTOR_IN1, LOW);
  delay(1000);
  byte n = Serial.available(); //check if charctaer(s)has been accumulated in buffer
  /*while ( n == 0){
    Serial.println("Wait for input");
    delay(100);
    n = Serial.available();
  }*/
}