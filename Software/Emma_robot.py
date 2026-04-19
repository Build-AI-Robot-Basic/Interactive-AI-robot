
# ------------------- Imports -------------------
import vosk
import pyaudio
import json
import pygame
import asyncio
import edge_tts
from google import genai
from cvzone.SerialModule import SerialObject
from time import sleep

# ------------------- Arduino -------------------
arduino = SerialObject(digits=3)
last_positions = [180, 0, 90]

# ------------------- Audio -------------------
pygame.mixer.init()

# ------------------- VOSK -------------------
model = vosk.Model("../Resources/vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)

# ------------------- Gemini -------------------
client = genai.Client(api_key="AQ.Ab8RN6IfQpXA4IMFuXkLnPIjXvigkNu8JpfEiKGxU-lNuntEHA")

VOICE = "en-US-AriaNeural"

# ------------------- Helpers -------------------
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

# ------------------- STT -------------------
def listen_with_vosk():
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=16000,
                      input=True,
                      frames_per_buffer=8192)

    stream.start_stream()
    print("Listening...")

    while True:
        data = stream.read(8192)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result["text"]
            print("You said:", text)
            return text

# ------------------- Gemini -------------------
def gemini_api(text):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=text
    )
    return response.text

# ------------------- TTS (FIXED) -------------------
async def speak(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("speech.mp3")

    pygame.mixer.music.load("speech.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# ------------------- Servo Gesture -------------------
def move_servo(target):
    arduino.sendData(target)
    sleep(0.2)

def hello_gesture():
    move_servo([180, 180, 90])
    for _ in range(3):
        move_servo([180, 150, 90])
        move_servo([180, 180, 90])
    move_servo([180, 0, 90])

# ------------------- MAIN LOOP -------------------
while True:
    move_servo([180, 0, 90])

    text = listen_with_vosk()

    if "hello" in text.lower() or "emma" in text.lower():
        hello_gesture()
        response = "Hello! How can I help you?"
    else:
        response = gemini_api(text)

    asyncio.run(speak(response))