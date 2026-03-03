import whisper
import sounddevice as sd
from scipy.io.wavfile import write

fs = 16000
seconds = 5

print("Recording...")
audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()

write("recorded.wav", fs, audio)
print("Recording finished")

model = whisper.load_model("base")

result = model.transcribe("recorded.wav")

print("You said:")
print(result["text"])