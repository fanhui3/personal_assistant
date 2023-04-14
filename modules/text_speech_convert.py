import pyttsx3
import whisper
import pyaudio
import ffmpeg
import os
import wave

if not os.path.exists("./audio_output"):
    os.makedirs("./audio_output")

engine = pyttsx3.init()
voices = engine.getProperty("voices")
default_voice = voices[0].id


class TextToSpeech:
    engine: pyttsx3.Engine
    global default_voice

    def __init__(self, rate: int, volume: float, voice=default_voice):
        self.engine = pyttsx3.init()
        if voice:
            self.engine.setProperty("voice", voice)
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volumne", volume)
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.p = pyaudio.PyAudio()

    def list_available_voices(self):
        voices: list = [self.engine.getProperty("voices")]

        for i, voice in enumerate(voices[0]):
            print(f"{i+1} {voice.name} {voice.age}: {voice.languages} [{voice.id}] ")

    def text_to_speech(self, text: str, save: bool = False, file_name="output.mp3"):
        # self.engine.say(text)
        print("i am saving mp3...")

        if save:
            self.engine.save_to_file(text, file_name)

        self.engine.runAndWait()

    def dictation(self, body: str, name=None):
        self.engine.say(text=body, name=name)
        self.engine.runAndWait()

    def listen_and_record(self):
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

        frames = []

        print("Recording audio...")
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print("Recording complete.")

        stream.stop_stream()
        stream.close()
        self.p.terminate()

        sound_file = wave.open("./audio_output/my_recording.wav", "wb")
        sound_file.setnchannels(self.CHANNELS)
        sound_file.setsampwidth(self.p.get_sample_size(self.FORMAT))
        sound_file.setframerate(self.RATE)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()


Steris = TextToSpeech(
    rate=150,
    volume=1.0,
    voice="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
)
Steris.listen_and_record()
