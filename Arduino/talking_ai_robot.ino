#include <cvzone.h>
#include <Servo.h>

Servo LServo;
Servo RServo;
Servo HServo;

SerialData serialData(3, 3);
int valsRec[3];

bool started = false;

void setup() {
  serialData.begin();

  LServo.attach(8);
  RServo.attach(9);
  HServo.attach(10);

  // وضع آمن (مفيش حركة)
  LServo.write(90);
  RServo.write(90);
  HServo.write(70);
}

void loop() {

  serialData.Get(valsRec);

  //
  int arm = constrain(valsRec[0], 0, 180);

  // 🤖 الإيدين
  LServo.write( 180-arm);
  RServo.write(arm);

  // 🤖 الرأس (مع الميل اليمين)
 int head = valsRec[2];

// ميل خفيف لليمين دائم + حركة الإشارة
HServo.write(constrain(head + 20, 60, 120));
}