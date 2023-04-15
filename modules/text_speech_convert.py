import pyttsx3
import whisper
import pyaudio
import os
import wave
import time
import speech_recognition as sr
import audioop
import numpy as np

if not os.path.exists("./audio_output"):
    os.makedirs("./audio_output")

engine = pyttsx3.init()
voices = engine.getProperty("voices")
default_voice = voices[0].id


class TextToSpeech:
    engine: pyttsx3.Engine
    global default_voice

    def __init__(self, rate: int, volume: float, voice=default_voice):
        #pyttsx3's settings
        self.engine = pyttsx3.init()
        if voice:
            self.engine.setProperty("voice", voice)
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volumne", volume)

        #whisper's settings
        self.at_model = whisper.load_model("base")
        
        #file path
        self.file_path = os.path.join(os.getcwd(), "audio_output", "my_recording.wav")

    def list_available_voices(self):
        voices: list = [self.engine.getProperty("voices")]

        for i, voice in enumerate(voices[0]):
            print(f"{i+1} {voice.name} {voice.age}: {voice.languages} [{voice.id}] ")

    def text_to_speech(self, text: str, save: bool = False, file_name: str = None):
        # self.engine.say(text)
        print("i am saving mp3...")

        if save:
            self.engine.save_to_file(text, file_name)

        self.engine.runAndWait()

    def dictation(self, body: str, name=None):
        self.engine.say(text=body, name=name)
        self.engine.runAndWait()

    def listen_and_record(self):

        #pyaudio's settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 30

        # check if a stream is already active
        if hasattr(self, "stream") and self.stream.is_active():
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()

        self.p = pyaudio.PyAudio()
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

        frames = []

        print("Recording audio...")
        # time.sleep(1)

        # start recording
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
            rms = audioop.rms(data, 2)  # calculate RMS energy level
            if rms < 700:  # adjust this threshold as necessary
                break  # stop recording if only ambience noise is left
            print(f"Recording: {i+1}/{self.RECORD_SECONDS*self.RATE/self.CHUNK}")
        print("Recording complete.")

        stream.stop_stream()
        stream.close()
        self.p.terminate()

        sound_file = wave.open(self.file_path, "wb")
        sound_file.setnchannels(self.CHANNELS)
        sound_file.setsampwidth(self.p.get_sample_size(self.FORMAT))
        sound_file.setframerate(self.RATE)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

    def transcribe(self):
        r = sr.Recognizer()
        audio_file = sr.AudioFile(self.file_path)
        with audio_file as source:
            audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def audio_to_text(self):
        while True:
            self.listen_and_record()
            time.sleep(2)
            text = self.transcribe()
            if text == None:
                print("I didn't get that. Please try again.")
            else: 
                print("you said: ", text)
                return text
            
     
        
    # def transcribe(self):
    #     result = self.at_model.transcribe(self.file_path, fp16=False)
    #     return result["text"]

    # def listen_and_record(self):
    #     """this function records your voice and saves it to a wav file
    #     """
    #     r = sr.Recognizer()
    #     r.energy_threshold = 700
    #     with sr.Microphone() as source:
    #         print("Say something!")
    #         audio = r.listen(source,timeout=5)
    #         print("Got your voice!!")

    #     with open("./audio_output/my_recording.wav", "wb") as f:
    #         f.write(audio.get_wav_data())
        
    #     print("Recording complete.")

Steris = TextToSpeech(
    rate=150,
    volume=1.0,
    voice="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
)


if __name__ == "__main__":
    text = Steris.audio_to_text()

