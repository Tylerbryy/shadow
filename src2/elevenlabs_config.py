from elevenlabs import generate, play, set_api_key
import time 
import os 
from dotenv import load_dotenv
load_dotenv()

set_api_key(os.getenv('ELEVEN_LABS_API_KEY'))

import io
from pydub import AudioSegment

def get_audio_length(audio_bytes):
  # Create a BytesIO object from the byte array
  byte_io = io.BytesIO(audio_bytes)

  # Load the audio data with PyDub
  audio = AudioSegment.from_mp3(byte_io)

  # Get the length of the audio in milliseconds
  length_ms = len(audio)

  # Optionally convert to seconds
  length_s = length_ms / 1000.0

  return length_s

def speak(text):
  speaking = True
  audio = generate(
      text=text,
      voice="waklyZ1q0J2sqLGmTYSo"
  )
  play(audio)

  audio_length = get_audio_length(audio)
  time.sleep(audio_length)