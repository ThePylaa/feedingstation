#include <SharpDistSensor.h>

// Analog pin to which the sensor is connected
#define LIGHTBARRIERPIN A0

// Window size of the median filter (odd number, 1 = no filtering)
#define MEDIANFILTERWINDOWSIZE 5

// Create an object instance of the SharpDistSensor class
SharpDistSensor sensor(LIGHTBARRIERPIN, MEDIANFILTERWINDOWSIZE);

void setup() {
  Serial.begin(9600);

  // Set sensor model
  sensor.setModel(SharpDistSensor::GP2Y0A41SK0F_5V_DS);
}

void loop() {
  // Get distance from sensor
  unsigned int distance = sensor.getDist();

  // Print distance to Serial
  Serial.println(distance);

  if(distance < 200){
    Serial.println("Close");
  }

  // Wait some time
  delay(200);
}