"""
Speech to Text using Google SpeechRecognition API
"""

import speech_recognition as sr
import pygame

# Initialize pygame mixer
pygame.mixer.init()

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

def listen_with_google():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise (important!)
        recognizer.adjust_for_ambient_noise(source, duration=1)

        play_sound("../Resources/listen.mp3")

        # Capture audio
        audio = recognizer.listen(source)

        play_sound("../Resources/convert.mp3")

        try:
            # Recognize speech (English)
            text = recognizer.recognize_google(audio, language="en-US")
            print("You said: " + text)
            return text

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""

        except sr.RequestError:
            print("Could not request results from Google (check your internet).")
            return ""

# -------- MAIN --------
if __name__ == "__main__":
    listen_with_google()
