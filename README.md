<div alt style="text-align: center; transform: scale(.5);">
	<picture>
		<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/tylerbryy/shadow/main/public/shadow-logo.png" />
		<img alt="shadow" src="https://raw.githubusercontent.com/tylerbryy/shadow/main/public/shadow-logo.png" />
	</picture>
</div>

# Shadow 

## Description

Shadow is an innovative voice assistant designed to provide users with a seamless and intuitive way to interact with their devices using voice commands. It leverages state-of-the-art machine learning models to understand and execute a wide range of tasks. Whether you need to transcribe speech, control smart home devices, or simply get answers to your questions, Shadow is here to help. It's useful for hands-free operation and accessibility, enhancing productivity and user experience.

## Getting Started

### Dependencies

* Python 3.6 or higher
* Whisper (OpenAI's speech-to-text model)
* ElevenLabs API for text-to-speech functionality
* Porcupine Wake Word engine for voice activation
* SoundDevice and SoundFile for audio processing
* dotenv for environment variable management

Ensure you have the above dependencies installed, or install them using the provided requirements file.

### Installing

To set up Shadow on your local machine, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/Tylerbryy/shadow.git
   ```
2. Navigate to the project directory:
   ```
   cd shadow
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables by copying the `.env.example` file to `.env` and put your api keys in. 

   For macOS/Linux:
   ```
   cp .env.example .env
   ```

   For Windows:
   ```
   copy .env.example .env
   ```
   - Edit the `.env` file with your actual values.
   - Follow the instructions [here](https://platform.openai.com/api-keys) to get your OpenAI API key.

### Executing program

To run Shadow, execute the following command in the project's root directory:
```
python run.py
```
Make sure to activate the virtual environment if you are using one. You can also pass additional command line arguments as needed for different modes of operation.