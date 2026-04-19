#include "cvzone.h"

SerialData myData(2, 2);   // هنستقبل 2 values

int sendVals[2] = {10, 20};
int receiveVals[2];

void setup() {
  myData.begin(9600);
}

void loop() {

  // إرسال بيانات
  myData.Send(sendVals);

  // استقبال بيانات
  myData.Get(receiveVals);

  // عرض البيانات على Serial Monitor
  Serial.print("Received: ");
  Serial.print(receiveVals[0]);
  Serial.print(" , ");
  Serial.println(receiveVals[1]);

  delay(1000);
}