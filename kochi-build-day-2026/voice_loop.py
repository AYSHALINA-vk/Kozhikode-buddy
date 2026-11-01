"""
voice_loop.py: a push-to-talk voice agent in ~60 lines.
STT (Pulse) -> LLM (Electron) -> TTS (Lightning), all on Smallest AI.

Docs used (every endpoint/parameter below comes from these pages):
  STT  https://docs.smallest.ai/models/speech-to-text/pre-recorded/quickstart
  LLM  https://docs.smallest.ai/models/llm/quickstart
  TTS  https://docs.smallest.ai/models/text-to-speech/quickstart

Setup:
  pip install requests sounddevice numpy
  export SMALLEST_API_KEY="your-key"      # Windows PowerShell: $env:SMALLEST_API_KEY="your-key"
  python voice_loop.py
"""
import io, os, sys, time, wave

import numpy as np
import requests
import sounddevice as sd

API = "https://api.smallest.ai/waves/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['SMALLEST_API_KEY']}"}
MIC_RATE = 16000          # 16 kHz mono is plenty for speech
SECONDS = 5               # how long each push-to-talk turn records

PERSONA = (
    "You are Kochi Buddy, a cheerful voice assistant for students at BUILD Day Cochin. "
    "Reply in 1-2 short spoken sentences. No markdown, no emojis, no lists."
)
history = [{"role": "system", "content": PERSONA}]


def record_wav(seconds=SECONDS) -> bytes:
    """Record from the default mic and return WAV bytes."""
    print(f"\n🎙  Speak now ({seconds}s)...")
    audio = sd.rec(int(seconds * MIC_RATE), samplerate=MIC_RATE, channels=1, dtype="int16")
    sd.wait()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(MIC_RATE)
        w.writeframes(audio.tobytes())
    return buf.getvalue()


def speech_to_text(wav_bytes: bytes) -> str:
    """Pulse STT, pre-recorded: POST raw bytes to /stt/?model=pulse-pro"""
    r = requests.post(
        f"{API}/stt/",
        params={"model": "pulse-pro", "language": "en"},
        headers={**HEADERS, "Content-Type": "application/octet-stream"},
        data=wav_bytes, timeout=60,
    )
    r.raise_for_status()
    return r.json().get("transcription", "").strip()


def think(user_text: str) -> str:
    """Electron LLM, OpenAI-compatible chat completions."""
    history.append({"role": "user", "content": user_text})
    r = requests.post(
        f"{API}/chat/completions",
        headers={**HEADERS, "Content-Type": "application/json"},
        json={"model": "electron", "messages": history}, timeout=60,
    )
    r.raise_for_status()
    reply = r.json()["choices"][0]["message"]["content"].strip()
    history.append({"role": "assistant", "content": reply})
    return reply


def speak(text: str, voice_id="meher"):
    """Lightning TTS: returns a WAV, which we play through the speakers."""
    r = requests.post(
        f"{API}/tts",
        headers={**HEADERS, "Content-Type": "application/json", "Accept": "audio/wav"},
        json={"text": text, "voice_id": voice_id, "model": "lightning_v3.1_pro",
              "sample_rate": 24000, "output_format": "wav"},
        timeout=60,
    )
    r.raise_for_status()
    with wave.open(io.BytesIO(r.content), "rb") as w:
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        sd.play(pcm, samplerate=w.getframerate()); sd.wait()


def main():
    print("Kochi Buddy is live. Press Enter to talk, type q + Enter to quit.")
    while input("> ").strip().lower() != "q":
        t0 = time.time()
        heard = speech_to_text(record_wav())
        t1 = time.time()
        if not heard:
            print("(didn't catch that, try again)"); continue
        print(f"you   : {heard}")
        reply = think(heard)
        t2 = time.time()
        print(f"agent : {reply}")
        speak(reply)
        t3 = time.time()
        # The latency lesson: where did the time go?
        print(f"⏱  STT {t1 - t0 - SECONDS:.2f}s | LLM {t2 - t1:.2f}s | TTS+play {t3 - t2:.2f}s")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        sd.stop()
        print("\nbye 👋", flush=True)
        os._exit(0)  # first Ctrl+C always wins, even mid-recording or mid-request
