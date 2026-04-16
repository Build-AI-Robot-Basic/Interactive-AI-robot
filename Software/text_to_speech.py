"""
Step 3: Text to Speech model (Google TTS)
"""

import io
import pygame
from gtts import gTTS

# Function to play audio using pygame
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def google_text_to_speech(text, lang="en"):
    # Generate speech using Google TTS
    tts = gTTS(text=text, lang=lang)

    filename = "speech.mp3"
    tts.save(filename)

    return filename


# Play the audio
text = "Hi, I'm Google text to speech model"

audio_file = google_text_to_speech(text)
play_audio(audio_file)
