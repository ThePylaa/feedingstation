#define MAGNETSWITCHPIN 35

#define MOTOR_IN1 22

void setup() {
  Serial.begin(9600);

  Serial.println("DRV8871 test");
  
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MAGNETSWITCHPIN, INPUT);
}

void loop() {
  if(Serial.available() != 0){
    delay(100);
    Serial.read();
  }

  // go away from current magnet
  while(digitalRead(MAGNETSWITCHPIN) == 0){
    for (int i=128; i<130; i++) {
      analogWrite(MOTOR_IN1, i);
      delay(4);
    }
    digitalWrite(MOTOR_IN1, LOW);
    delay(1000);
  }
  digitalWrite(MOTOR_IN1, LOW);

  delay(1000);
  
  //got to next magnet
  while(digitalRead(MAGNETSWITCHPIN) == 1){
    for (int i=128; i<130; i++) {
      analogWrite(MOTOR_IN1, i);
      delay(4);
    }
    digitalWrite(MOTOR_IN1, LOW);
    delay(1000);
  }
  digitalWrite(MOTOR_IN1, LOW);
  
  delay(1000);
  byte n = Serial.available(); //check if charctaer(s)has been accumulated in buffer
  while ( n == 0){
    Serial.println("Wait for input");
    delay(100);
    n = Serial.available();
  }
  serialFlush();
  Serial.println("Next round");

}

void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}