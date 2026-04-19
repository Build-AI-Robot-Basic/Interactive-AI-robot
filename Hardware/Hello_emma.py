from cvzone.SerialModule import SerialObject
from time import sleep

# ------------------- Arduino Setup -------------------
# Set your correct COM port here
arduino = SerialObject(portNo="COM3", digits=3)

# ------------------- Wave Function -------------------
def wave_once():
    """
    Single wave motion
    """

    # Move arm up
    arduino.sendData([60, 90, 70])
    sleep(0.5)

    # Return to neutral
    arduino.sendData([90, 90, 70])
    sleep(0.5)


def wave_three_times():
    """
    Wave 3 times then return to neutral
    """

    # Initial position (neutral)
    arduino.sendData([90, 90, 70])
    sleep(1)

    # Repeat wave 3 times
    for i in range(3):
        print(f"Waving cycle {i + 1}")
        wave_once()

    # Final reset position
    arduino.sendData([90, 90, 70])


# ------------------- Run Program -------------------
if __name__ == "__main__":
    wave_three_times()