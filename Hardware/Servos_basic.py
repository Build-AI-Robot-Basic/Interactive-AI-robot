from cvzone.SerialModule import SerialObject
from time import sleep

# ------------------- Arduino Connection -------------------
arduino = SerialObject(portNo="COM3", digits=3)

# ------------------- Servo Move Function -------------------
def move_servo(position, delay=1.0):
    arduino.sendData(position)
    sleep(delay)

# ------------------- BIG MOTION POSITIONS -------------------
# [Left Arm, Right Arm, Head]

NEUTRAL = [90, 90, 90]

POSITION_A = [170, 10, 110]   # big movement (arms wide + head up)
POSITION_B = [60, 150, 70]    # opposite movement (mirrored pose)

# ------------------- MAIN LOOP (LIMITED CYCLES) -------------------
for i in range(5):

    print(f"Cycle {i + 1}: Moving to Position A")
    move_servo(POSITION_A)

    print("Holding...")
    sleep(1)

    print("Moving to Position B")
    move_servo(POSITION_B)

    print("Back to Neutral")
    move_servo(NEUTRAL)

    sleep(1)

print("Motion Test Finished ✔")