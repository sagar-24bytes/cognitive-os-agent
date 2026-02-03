import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

print("Loading speech model...")
model = Model("voice/models/vosk-model-en-us-0.22")
print("Speech model loaded.")

def find_best_input_device():
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d['max_input_channels'] > 0 and "Microphone" in d['name']:
            return i, d
    raise RuntimeError("No microphone found")

DEVICE_ID, device_info = find_best_input_device()
CHANNELS = device_info['max_input_channels']
SAMPLE_RATE = int(device_info['default_samplerate'])

print(f"Using device: {device_info['name']}")
print(f"Channels: {CHANNELS}")
print(f"Sample rate: {SAMPLE_RATE}")

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen(seconds=8):
    print("Listening...")
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    with sd.RawInputStream(
        device=DEVICE_ID,
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=CHANNELS,
        callback=callback
    ):
        for _ in range(int(seconds * SAMPLE_RATE / 8000)):
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                return result.get("text", "")
        
        final_result = json.loads(recognizer.FinalResult())
        return final_result.get("text", "")
