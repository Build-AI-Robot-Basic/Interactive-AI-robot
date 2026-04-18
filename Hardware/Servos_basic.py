from cvzone.SerialModule import SerialObject
from time import sleep

arduino = SerialObject(digits=3)

arduino.sendData([90, 90, 70])
sleep(2)

for _ in range(3):

    arduino.sendData([90, 60, 70])  # رفع الدراع اليمين
    sleep(0.7)

    arduino.sendData([90, 90, 70])  # رجوع
    sleep(0.7)

arduino.sendData([90, 90, 100])
sleep(1)

arduino.sendData([90, 90, 60])
sleep(1)

arduino.sendData([90, 90, 70])