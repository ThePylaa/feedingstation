#include <Stepper.h> // Hinzufügen der Programmbibliothek.
int SPU = 512; // Schritte pro Umdrehung.
Stepper Motor(SPU, 37,35,33,31); // Der Schrittmotor erhält die Bezeichnung "Motor" und es wird angegeben an welchen Pins der Motor angeschlossen ist.

void setup() //Hier beginnt das Setup.
{
Motor.setSpeed(20); // Angabe der Geschwindigkeit in Umdrehungen pro Minute.
}

void loop() {
Motor.step(4096); // Der Motor macht 2048 Schritte, das entspricht einer Umdrehung.
delay(1000); // Durch diese Pause bleibt der Motor nach der Drehung für eine Sekunde stehen.

}