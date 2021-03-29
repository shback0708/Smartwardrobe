#include <Servo.h>
char serial_data;
int pin=9;
Servo servo_test;
int default_angle = 90;
String inBytes;

void setup() {
  servo_test.attach(3);
  Serial.begin(9600);
  while (!Serial); // wait until Serial is ready
  delay(100);
  servo_test.write(default_angle);
  //Serial.println("setup complete");
}

void loop() {
  if (Serial.available() > 0) {
    inBytes = Serial.readStringUntil('\n');
    // angle = inBytes.toInt()
    if (inBytes == "open") {
      servo_test.write(180);
      Serial.println("open grip");
    }
    else if (inBytes == "close") {
      servo_test.write(0);
      Serial.println("close grip");
    }
    else {
      Serial.println("invalid input");
    }
  }

}
