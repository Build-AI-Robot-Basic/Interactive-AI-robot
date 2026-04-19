#include <cvzone.h>
#include <Servo.h>

Servo LServo;
Servo RServo;
Servo HServo;

SerialData serialData(3, 3);
int valsRec[3];

void setup() {
  serialData.begin();

  LServo.attach(8);
  RServo.attach(9);
  HServo.attach(10);

  LServo.write(90);
  RServo.write(90);
  HServo.write(90);
}

void loop() {

  serialData.Get(valsRec);

  int leftArm = constrain(valsRec[0], 0, 180);
  int rightArm = constrain(valsRec[1], 0, 180);
  int head = constrain(valsRec[2], 60, 120);

  LServo.write(leftArm);

  // 🔄 عكس اتجاه اليمين
  RServo.write(180 - rightArm);

  HServo.write(head);
}
