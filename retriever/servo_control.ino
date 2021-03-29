#include <Servo.h>

// This is just a simple example, to confirm that we can rotate the servo to the designated angle
Servo servo_test; // initialize servo object
int angle = 0;

void setup() {
  // put your setup code here, to run once:
  servo_test.attach(9); // pin 9 connected to servo
}

void loop() {
  // put your main code here, to run repeatedly:
//  for (angle = 0; angle <= 180; angle += 20) {
//    servo_test.write(angle);
//    delay(1000);
//  }
  angle = 180;
  servo_test.write(angle);
  //delay(5000);

//  angle = 20;
//  servo_test.write(angle);
//  for (angle = 0; angle <= 180; angle += 20) {
//    servo_test.write(angle);
//    delay(1000);
//  }
  //delay(5000);

}
