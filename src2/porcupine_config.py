import pvporcupine
import pyaudio
import pvporcupine
import struct
import sys

def listen_for_wake_word(ACCESS_KEY, wake_word_file, callback):
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[wake_word_file]
    )

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                # Wake word detected
                callback()  # Call the callback function when the wake word is detected

    except KeyboardInterrupt:
     sys.exit()
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()



