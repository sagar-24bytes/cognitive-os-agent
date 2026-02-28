import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

print("Loading Whisper model...")
model = WhisperModel("small", device="cpu", compute_type="int8")
print("Whisper loaded.")

def record(seconds=5, filename="recorded.wav"):
    fs = 16000
    print("Speak now...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)

def listen(seconds=5):
    record(seconds)
    segments, info = model.transcribe("recorded.wav", language="en")
    text = " ".join([seg.text for seg in segments])
    return text.strip()
