import vosk
import pyaudio
import json
import pygame
import asyncio
import edge_tts
from google import genai
from cvzone.SerialModule import SerialObject
from time import sleep
import os
import time

# ------------------- Arduino Setup -------------------
arduino = SerialObject(portNo="COM3", digits=3)

# [Left Arm, Right Arm, Head]
last_positions = [180, 0, 90]

# ------------------- Audio Setup -------------------
pygame.mixer.init()

# ------------------- VOSK Setup -------------------
model_path = "../Resources/vosk-model-en-us-0.22"

model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# ------------------- Gemini Setup (NEW API FIX) -------------------
client = genai.Client(api_key="AIzaSyCKTzb2ssRplrWe8ZZ0D-PuvXddeRRtArU")

VOICE = "en-US-AriaNeural"

# ------------------- Servo Movement -------------------
def move_servo(target_positions, delay=0.01):
    global last_positions

    max_steps = max(
        abs(target_positions[i] - last_positions[i]) for i in range(3)
    )

    if max_steps == 0:
        return

    for step in range(max_steps):
        current_positions = [
            last_positions[i]
            + (step + 1) * (target_positions[i] - last_positions[i]) // max_steps
            for i in range(3)
        ]

        arduino.sendData(current_positions)
        sleep(delay)

    last_positions = target_positions[:]

# ------------------- TTS -------------------
async def speak_free(text):
    filename = f"speech_{int(time.time())}.mp3"

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()

    try:
        os.remove(filename)
    except:
        pass

# ------------------- STT -------------------
def listen_with_vosk():
    mic = pyaudio.PyAudio()

    stream = mic.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192
    )

    stream.start_stream()
    print("Listening...")

    while True:
        data = stream.read(8192)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")

            if text:
                print("You said:", text)
                return text

# ------------------- Gesture -------------------
def hello_gesture():
    print("Hello Gesture...")

    move_servo([180, 180, 90])

    for _ in range(3):
        move_servo([180, 150, 90])
        move_servo([180, 180, 90])

    move_servo([180, 0, 90])

# ------------------- Main Program -------------------
if __name__ == "__main__":
    print("Robot System Started...")

    while True:

        move_servo([180, 0, 90])  # neutral

        user_input = listen_with_vosk()

        # ------------------- Greeting -------------------
        if "hello" in user_input.lower() or "emma" in user_input.lower():

            response_text = "Hello! I am Emma, how can I help you today?"

            hello_gesture()
            asyncio.run(speak_free(response_text))

        # ------------------- AI Response -------------------
        else:
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=user_input
                )

                ai_response = response.text
                print("Emma says:", ai_response)

                move_servo([180, 0, 110])  # thinking pose
                asyncio.run(speak_free(ai_response))
                move_servo([180, 0, 90])

            except Exception as e:
                print("Gemini Error:", e)