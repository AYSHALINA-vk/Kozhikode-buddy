"""
three_api_calls.py: Kozhikode Buddy, a Malayalam + English (Manglish) voice agent, stripped bare.

This is the three Smallest APIs in a row, one turn at a time:
  1. speech to text   Pulse STT (language=ml)
  2. LLM              Electron, OpenAI-compatible chat completions
  3. text to speech   Lightning v3.1 Pro, a Malayalam voice

No streaming, no voice activity detection, no barge-in. Each step waits for the one before it,
so you can see every piece and the time it takes. It's for learning only. It is NOT how you ship
a voice agent. For the real thing (streaming, VAD, interruptions) see chechi_pipecat.py.

Run it (PowerShell):
  cd C:\\Users\\ACER\\workshops\\kochi-build-day-2026
  .\\.venv\\Scripts\\Activate.ps1
  $env:SMALLEST_API_KEY="your-key"
  python three_api_calls.py                                      # push-to-talk with your mic
  python three_api_calls.py --file samples\\user_question_ml.wav  # no mic? feed it a wav
  python three_api_calls.py --type                               # no mic at all? type your line
  Ctrl+C or q quits.

Tip: --voice vishnu (male) or --voice parvathy (female). Other Malayalam voices: lakshmi, sreenath, unni, aravindan.
"""
import argparse, io, os, re, sys, time, wave

import requests

API = "https://api.smallest.ai/waves/v1"
KEY = os.environ.get("SMALLEST_API_KEY")
if not KEY:
    sys.exit("Set SMALLEST_API_KEY first (see .env.example).")
HEADERS = {"Authorization": f"Bearer {KEY}"}
MIC_RATE, SECONDS = 16000, 5

PERSONA = (
    "You are Kozhikode Buddy, a warm, funny local guide from Kozhikode (Calicut). "
    "Help the user plan a fun evening or outing in Kozhikode. "
    "LANGUAGE RULE (most important): you speak Manglish, the way young Keralites talk. "
    "Write every Malayalam word in Malayalam script (മലയാളം), and write English words (like beach, sunset, traffic, "
    "biriyani, humidity, hotel) in English letters. NEVER write Malayalam words in English letters (no 'ente', 'aanu', "
    "'pattum'). Do this even if the user types in English or in English-letter Malayalam. "
    "Examples of the exact style: "
    "'ബീച്ചിൽ പോകാം, sunset കാണാൻ Kappad ആണ് best.' "
    "'Biriyani ആണെങ്കിൽ Malabar style തന്നെ try ചെയ്യണം, പക്ഷേ ഏത് hotel ആണ് best എന്ന് ചോദിച്ചാൽ വഴക്കാകും.' "
    "Use simple everyday spoken Malayalam, not formal or bookish words. "
    "Keep every reply under 25 words, 1 or 2 short sentences. No markdown, no emojis, no lists. "
    "Suggest only ONE idea at a time. "
    "Things you know about: Malabar biriyani (people love arguing about which place is best, so never crown one), "
    "Kozhikode halwa on S.M. Street (Sweet Meat Street), pathiri and curry, kallummakkaya, banana chips, "
    "Kozhikode Beach in the evening, Kappad Beach at sunset (where Vasco da Gama landed in 1498), "
    "Beypore Beach, Mishkal Mosque, Tali Temple, Mananchira Square, Kozhippara Falls, Kadalundi Bird Sanctuary, "
    "Sargaalaya arts and crafts village. "
    "Joke gently about food, humidity and traffic. Never joke about religion, communities or politics. "
    "Never make up facts, prices, opening hours or entry fees. If you are not sure, say so honestly."
)
history = [{"role": "system", "content": PERSONA}]


def check(r, name):
    """Print the server's explanation when a call fails, then raise as usual."""
    if not r.ok:
        print(f"\n{name} failed: HTTP {r.status_code}\n{r.text}\n")
    r.raise_for_status()


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
    check(r, "STT")
    return r.json().get("transcription", "").strip()


def _llm(messages):
    """One chat call to any OpenAI-compatible API, with retries when the provider is busy."""
    url = os.environ.get("LLM_URL", "https://api.openai.com/v1/chat/completions")
    key = os.environ.get("LLM_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("Set LLM_KEY (and LLM_URL, LLM_MODEL) first, e.g. your Gemini key.")
    body = {"model": os.environ.get("LLM_MODEL", "gpt-4.1-mini"), "messages": messages}
    if os.environ.get("LLM_REASONING"):  # only for thinking models, e.g. "low"
        body["reasoning_effort"] = os.environ["LLM_REASONING"]
    r = None
    for attempt in range(4):  # busy (429/5xx) or timed out: wait a bit and retry
        try:
            r = requests.post(url, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                              json=body, timeout=30)
            if r.status_code not in (429, 500, 502, 503, 504):
                break
            why = f"HTTP {r.status_code}"
        except requests.exceptions.Timeout:
            r, why = None, "timed out"
        wait = 2 ** attempt
        print(f"(LLM {why}. Retrying in {wait}s... attempt {attempt + 1}/4)")
        time.sleep(wait)
    if r is None:
        sys.exit("LLM never answered (timeouts). Try a different LLM_MODEL or try again later.")
    check(r, "LLM")
    return r.json()["choices"][0]["message"]["content"].strip()


HAS_MALAYALAM = re.compile(r"[\u0D00-\u0D7F]")


def think(user_text: str) -> str:
    """LLM step. The TTS reads Malayalam SCRIPT well but English-letter Malayalam badly, so if the model
    answers in English letters we ask it once to rewrite in Malayalam script (Manglish)."""
    history.append({"role": "user", "content": user_text})
    try:
        reply = _llm(history)
        if not HAS_MALAYALAM.search(reply):
            fix = history + [{"role": "assistant", "content": reply},
                             {"role": "user", "content": "Rewrite that exact reply as Manglish: Malayalam words in "
                              "Malayalam script, English words in English letters. Same meaning, under 25 words. "
                              "Output only the rewritten reply."}]
            reply = _llm(fix)
    except BaseException:
        history.pop()  # don't keep the unanswered user line in the conversation
        raise
    history.append({"role": "assistant", "content": reply})
    return reply


def tts(text: str, voice: str) -> bytes:
    r = requests.post(f"{API}/tts",
                      headers={**HEADERS, "Content-Type": "application/json", "Accept": "audio/wav"},
                      json={"text": text, "voice_id": voice, "model": "lightning_v3.1_pro",
                            "language": "ml", "sample_rate": 24000, "output_format": "wav"},
                      timeout=60)
    check(r, "TTS")
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
    print(f"buddy : {reply}")
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
    print("Kozhikode Buddy is live. സ്വാഗതം! (Ctrl+C or q to quit)")
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