"""
three_api_calls.py: Chechi, a Malayalam + English (Manglish) voice agent, stripped bare.

This is the three Smallest APIs in a row, one turn at a time:
  1. speech to text   Pulse STT (language=ml)
  2. LLM              Electron, OpenAI-compatible chat completions
  3. text to speech   Lightning v3.1 Pro, a Malayalam voice

No streaming, no voice activity detection, no barge-in. Each step waits for the one before it,
so you can see every piece and the time it takes. It's for learning only. It is NOT how you ship
a voice agent. For the real thing (streaming, VAD, interruptions) see chechi_pipecat.py.

Run it:
  pip install -r requirements.txt
  export SMALLEST_API_KEY="your-key"     # Windows PowerShell: $env:SMALLEST_API_KEY="your-key"
  python three_api_calls.py                       # push-to-talk with your mic
  python three_api_calls.py --file samples/user_question_ml.wav   # no mic? feed it a wav
  python three_api_calls.py --type                # no mic at all? type your line instead
  Ctrl+C or q quits.

Tip: --voice vishnu (male) or --voice parvathy (female). Other Malayalam voices: lakshmi, sreenath, unni, aravindan.
"""
import argparse, io, os, sys, time, wave

import requests

API = "https://api.smallest.ai/waves/v1"
KEY = os.environ.get("SMALLEST_API_KEY")
if not KEY:
    sys.exit("Set SMALLEST_API_KEY first (see .env.example).")
HEADERS = {"Authorization": f"Bearer {KEY}"}
MIC_RATE, SECONDS = 16000, 5

PERSONA = (
    "You are Chechi, a warm, funny voice assistant from Kochi, talking to students at BUILD Day Cochin "
    "on Kerala Piravi (1 November 2026, the 70th anniversary of Kerala state being formed on 1 November 1956). Never make up facts or numbers. "
    "Talk the way young people in Kerala actually talk: Malayalam written in Malayalam script, "
    "with English words mixed in naturally (code-switching), like 'ഇന്ന് നമ്മൾ ഒരു voice agent build ചെയ്യാം'. "
    "Reply in 1 or 2 short spoken sentences. No markdown, no emojis, no lists."
)
history = [{"role": "system", "content": PERSONA}]


def record_wav(seconds=SECONDS) -> bytes:
    import numpy as np, sounddevice as sd  # only needed in mic mode
    print(f"\n🎙  Speak now ({seconds}s)...")
    audio = sd.rec(int(seconds * MIC_RATE), samplerate=MIC_RATE, channels=1, dtype="int16")
    sd.wait()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(MIC_RATE)
        w.writeframes(audio.tobytes())
    return buf.getvalue()


def speech_to_text(wav_bytes: bytes, language="ml") -> str:
    """Pulse STT, pre-recorded. language=ml handles Malayalam with English words mixed in."""
    r = requests.post(f"{API}/stt/", params={"model": "pulse", "language": language},
                      headers={**HEADERS, "Content-Type": "application/octet-stream"},
                      data=wav_bytes, timeout=60)
    r.raise_for_status()
    return r.json().get("transcription", "").strip()


def think(user_text: str) -> str:
    history.append({"role": "user", "content": user_text})
    r = requests.post(f"{API}/chat/completions", headers={**HEADERS, "Content-Type": "application/json"},
                      json={"model": "electron", "messages": history}, timeout=60)
    r.raise_for_status()
    reply = r.json()["choices"][0]["message"]["content"].strip()
    history.append({"role": "assistant", "content": reply})
    return reply


def tts(text: str, voice: str) -> bytes:
    r = requests.post(f"{API}/tts", headers={**HEADERS, "Content-Type": "application/json", "Accept": "audio/wav"},
                      json={"text": text, "voice_id": voice, "model": "lightning_v3.1_pro", "language": "ml",
                            "sample_rate": 24000, "output_format": "wav"}, timeout=60)
    r.raise_for_status()
    return r.content


def play(wav_bytes: bytes, save_to=None):
    if save_to:
        open(save_to, "wb").write(wav_bytes); print(f"(saved {save_to})")
    try:
        import numpy as np, sounddevice as sd
        with wave.open(io.BytesIO(wav_bytes), "rb") as w:
            pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
            sd.play(pcm, samplerate=w.getframerate()); sd.wait()
    except Exception as e:  # no speaker / no sounddevice: just keep the file
        print(f"(could not play audio here: {e.__class__.__name__}; open the saved wav instead)")


def turn(get_text, voice, n):
    t0 = time.time(); heard = get_text(); t1 = time.time()
    if not heard:
        print("(didn't catch that, try again)"); return
    print(f"you   : {heard}")
    reply = think(heard); t2 = time.time()
    print(f"chechi: {reply}")
    audio = tts(reply, voice); t3 = time.time()
    play(audio, save_to=f"reply_{n}.wav")
    print(f"⏱  STT {t1 - t0:.2f}s | LLM {t2 - t1:.2f}s | TTS {t3 - t2:.2f}s")


def bye():
    """Stop any audio and leave right away, on the first Ctrl+C."""
    try:
        import sounddevice as sd
        sd.stop()
    except Exception:
        pass
    print("\nbye! നന്ദി 👋", flush=True)
    os._exit(0)  # don't wait on audio threads or a hanging HTTP call


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="use this wav as what you said (no mic needed)")
    ap.add_argument("--type", action="store_true", help="type instead of talking")
    ap.add_argument("--voice", default="parvathy")
    a = ap.parse_args()
    print("Chechi is live. കേരളപ്പിറവി ആശംസകൾ! (Ctrl+C or q to quit)")
    if a.file:
        turn(lambda: speech_to_text(open(a.file, "rb").read()), a.voice, 1)
        return
    n = 0
    while True:
        cmd = input("\nEnter to talk (or type a line), q to quit > ").strip()
        if cmd.lower() == "q":
            break
        n += 1
        if a.type or cmd:
            line = cmd or input("you > ")
            turn(lambda: line, a.voice, n)
        else:
            wav = record_wav()
            turn(lambda: speech_to_text(wav), a.voice, n)
    print("bye! നന്ദി 👋")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        bye()
