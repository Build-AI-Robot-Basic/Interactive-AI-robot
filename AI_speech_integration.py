"""
AI-Speech Integration (VOSK + Gemini + Edge-TTS)
"""

# ------------------- Imports -------------------
import vosk
import pyaudio
import json
import pygame
import asyncio
import edge_tts
from google import genai

# ------------------- Initializations -------------------

pygame.mixer.init()

# VOSK small English model
model_path = r"C:\Users\hp\PycharmProjects\PythonProject\Resources\vosk-model-small-en-us-0.15"
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Gemini Client
client = genai.Client(api_key="AIzaSyDZK2n3x2MRXPPZRfKOKqULibKEaFYFmJc")

# Edge TTS voice
VOICE = "en-US-AriaNeural"

# ------------------- Utility -------------------
def play_sound(file_path):
    """Play a sound file using pygame"""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

# ------------------- Speech-to-Text -------------------
def listen_with_vosk():
    """Capture audio from microphone and convert to text"""
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
    play_sound("../Resources/listen.mp3")  # optional listening sound

    while True:
        data = stream.read(8192)

        if recognizer.AcceptWaveform(data):
            play_sound("../Resources/convert.mp3")  # optional conversion sound
            result = recognizer.Result()
            text = json.loads(result)["text"]
            print("You said:", text)
            return text

# ------------------- Gemini AI -------------------
def gemini_api(text):
    """Generate AI response using Gemini API"""
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=text
    )
    ai_text = response.text
    print("AI:", ai_text)
    return ai_text

# ------------------- Edge TTS -------------------
async def text_to_speech(text):
    """Convert text to speech using Edge-TTS"""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("../Resources/speech.mp3")

    pygame.mixer.music.load("../Resources/speech.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# ------------------- Main Loop -------------------
while True:
    # 1) Speech-to-Text
    text = listen_with_vosk()

    # 2) Gemini AI Response
    ai_response = gemini_api(text)

    # 3) Text-to-Speech
    asyncio.run(text_to_speech(ai_response))