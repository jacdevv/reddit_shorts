import whisper_timestamped as whisper
import os

def transcribe_audio(audio_file):
    print("Whisper loading audio...")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    audio_file_path = os.path.join(dir_path, audio_file)
    audio = whisper.load_audio(audio_file_path)
    model = whisper.load_model("small", device="cpu")
    print("Whisper transcribing audio...")
    result = whisper.transcribe(model, audio, language="en")
    print("Whisper done.")
    return result
