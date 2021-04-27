#include <Servo.h>
Servo servo_test; // initialize servo object
int angle = 0;

void setup() {
  // put your setup code here, to run once:
  servo_test.attach(9); // pin 9 connected to servo
  servo_test.write(0);
}

void loop() {
  delay(30000);
  // put your main code here, to run repeatedly:
  for (angle = 0; angle <= 180; angle += 3) {
    servo_test.write(angle);
    delay(200);
  }

  for (angle = 180; angle >= 0; angle -= 3) {
    servo_test.write(angle);
    delay(200);
  }

  delay (5000);
//  angle = 180;
//  servo_test.write(angle);
  //delay(5000);

//  angle = 20;
//  servo_test.write(angle);
//  for (angle = 0; angle <= 180; angle += 20) {
//    servo_test.write(angle);
//    delay(1000);
//  }
  //delay(5000);

}
