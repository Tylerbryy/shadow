import os
import sys
from src2.whisper_config import transcribe
from src2.elevenlabs_config import speak, set_api_key
import interpreter
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
import whisper
import random
from src2.porcupine_config import listen_for_wake_word

load_dotenv()
# Load the Whisper model
model = whisper.load_model("tiny")

# Set the API keys
PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY')
WAKEWORD_FILE = os.getenv('WAKEWORD_FILE')
set_api_key(os.getenv('ELEVEN_LABS_API_KEY'))
interpreter.api_key = os.getenv('OPENAI_API_KEY')
interpreter.system_message += """\nYou're named Shadow, you're designed to assist users with a wide range of tasks, spanning from general inquiries to specific requests. you're equipped to handle a variety of topics, including but not limited to technology, daily life, entertainment, and educational content. you're is programmed to approach interactions with a humorous personality, often incorporating jokes and light-hearted comments to make the conversation more engaging and enjoyable. However, you maintains a balance, ensuring that humor does not overshadow the accuracy and relevance of the information provided. Shadow is also capable of adapting to the user's tone and requirements, shifting between being purely informative and engagingly humorous as the context demands. It avoids sensitive topics and refrains from using humor in serious discussions. you're designed to be user-friendly, encouraging users to ask questions freely and providing clear, concise, and helpful responses."""
interpreter.auto_run = True

# Function to record audio from the microphone
def record_audio(duration=8, sample_rate=16000):
    print("Please speak now...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return audio

# Function to save the recorded audio to a file
def save_audio(audio, filename='input.wav', sample_rate=16000):
    sf.write(filename, audio, sample_rate)

# Function to transcribe audio to text
def transcribe(audio_path):
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text

# Function to add user message and transcribe
def add_user_message(audio_path, history):
    user_message = transcribe(audio_path)
    return history + [[user_message, None]]

# Function to process bot response
def bot(history):
    last_sentence = ""
    user_message = history[-1][0]
    history[-1][1] = ""
    active_block_type = ""
    language = ""
    for chunk in interpreter.chat(user_message, stream=True, display=True):

        # Assuming interpreter.chat() yields similar chunks as in your snippet
        if "message" in chunk:
            if active_block_type != "message":
                active_block_type = "message"
            history[-1][1] += chunk["message"]

            last_sentence += chunk["message"]
            if any(punct in last_sentence for punct in ".?!\n"):
                speak(last_sentence)
                last_sentence = ""
            # No else part, as we want to speak only when a sentence ends.

        if "language" in chunk:
            language = chunk["language"]
        if "code" in chunk:
            if active_block_type != "code":
                active_block_type = "code"
                history[-1][1] += f"\n```{language}\n"
            history[-1][1] += chunk["code"]

        if "executing" in chunk:
            history[-1][1] += "\n```\n\n```text\n"

        if "output" in chunk:
            if chunk["output"] != "KeyboardInterrupt":
                history[-1][1] += chunk["output"] + "\n"

        if "active_line" in chunk and chunk["active_line"] is None:
            history[-1][1] = history[-1][1].strip()
            history[-1][1] += "\n```\n"

    if last_sentence:
        speak(last_sentence)

# Main loop for the interactive chatbot
def interactive_chatbot():
    greetings = [
        "Good evening, Tyler. It's Shadow, your personal assistant. How may I assist you today?",
        "Hello, Tyler. Shadow here, at your service. What can I do for you this fine day?",
        "Hi Tyler, I'm Shadow, your aide in the digital realm. What's on your agenda today?",
        "Greetings, Tyler. This is Shadow, your virtual helper. How can I make your day easier?"
    ]

    history = []
    try:
        # Audible greeting to the user, picked randomly from the list
        speak(random.choice(greetings))

        while True:
            # Record the user's voice
            audio = record_audio()
            save_audio(audio, 'input.wav')

            # Add user message and transcribe
            history = add_user_message('input.wav', history)

            # Process bot response
            bot(history)

    except KeyboardInterrupt:
        speak("Goodbye now")
        
        sys.exit()

def start_chatbot():
    interactive_chatbot()

# Modify the main part of the script to listen for the wake word
if __name__ == "__main__":
    listen_for_wake_word(PORCUPINE_ACCESS_KEY, WAKEWORD_FILE, start_chatbot)