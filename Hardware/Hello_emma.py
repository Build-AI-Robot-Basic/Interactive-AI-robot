from cvzone.SerialModule import SerialObject
from time import sleep

arduino = SerialObject(digits=3)

def wave_once():

    arduino.sendData([60, 90, 70])
    sleep(0.5)

    arduino.sendData([90, 90, 70])
    sleep(0.5)


def wave_3_times():


    arduino.sendData([90, 90, 70])
    sleep(1)

    for _ in range(3):
        wave_once()

    arduino.sendData([90, 90, 70])


wave_3_times()