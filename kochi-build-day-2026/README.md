# Build your first voice agent · BUILD Day Cochin · Kerala Piravi 2026
Workshop by Abhishek Mishra ([@stalwartcoder](https://x.com/stalwartcoder)) at BUILD Day Cochin, Jain University Kochi, 1 Nov 2026.
കേരളപ്പിറവി ആശംസകൾ! 🌴

Two ways to build a voice agent:
1. **No code, 15 min:** build one on a voice AI platform and talk to it in the browser.
2. **Code:** first see the three pieces bare (speech to text → LLM → text to speech), then run **Chechi**, a Manglish (Malayalam + English) agent, built properly with Pipecat.

## What you need
- A laptop with Chrome and a mic (earphones help)
- An email to sign up with. New accounts get free credits, no card needed.
- For the code part: Python 3.11+

---

## Part 1 · No-code agent (Smallest Atoms dashboard)
1. **Sign up:** https://app.smallest.ai/?utm_source=buildday_cochin&utm_medium=workshop&utm_campaign=nov26
2. **Create Agent** (green, top right) → **Start from Scratch** → **Single Prompt**. Name it `kochi-buddy`. Call Direction: **Inbound**. Pick a voice and preview it. Leave the model on the default.
3. **Paste this prompt** into the prompt editor:
   ```text
   # Role & Objective
   You are Kochi Buddy, a friendly, slightly cheeky local guide for students in Kochi.
   Your goal: help the caller plan a fun evening in Kochi in under 2 minutes.

   # Conversational Flow
   1. Greet the caller and ask their name.
   2. Ask what they're in the mood for: food, beach, history, or shopping.
   3. Suggest ONE specific idea (e.g. sunset at Fort Kochi beach, Chinese fishing nets, a Kerala meal), with one reason why.
   4. Ask if they want another idea or are happy.

   # Dos, Don'ts & Fallbacks
   - Speak in short sentences, max 2 at a time. This is a voice call, not an essay.
   - No lists, no markdown, no emojis.
   - If you don't know something specific (prices, opening hours), say so honestly.
   - If asked about anything unrelated to Kochi, joke about it briefly, then steer back.

   # End Conditions
   End the call politely when the caller says they're happy or says bye.
   ```
   **First message:** `Hey! I'm Kochi Buddy. Tell me your name and I'll plan your evening in Kochi.`
4. **Test Agent → Web Call**, allow the mic, and talk. Try a normal question, a weird one, and interrupt it mid-sentence.
   No mic? Use **Chat** mode.

Docs: https://docs.smallest.ai/voice-agents/quickstart

---

## Part 2 · Code: the pipeline yourself
Get an API key: dashboard → **API Keys** → **Create API Key**.
```bash
git clone https://github.com/abhishekmishragithub/workshops && cd workshops/kochi-build-day-2026
pip install -r requirements.txt
export SMALLEST_API_KEY="your-key"          # Windows PowerShell: $env:SMALLEST_API_KEY="your-key"
```

### Start here · `three_api_calls.py`, see the pieces
Chechi with everything stripped away: three Smallest API calls in a row, one turn at a time.
```bash
python three_api_calls.py                                      # press Enter, talk for 5 s
python three_api_calls.py --type                               # no mic: type your line
python three_api_calls.py --file samples/user_question_ml.wav  # no mic: feed it a wav
python three_api_calls.py --voice vishnu                       # male voice
```
Ctrl+C or `q` quits. Talk to her the way you talk to friends: *"Chechi, ഇന്ന് Kerala Piravi ആണല്ലോ, ഒരു fun fact പറയാമോ?"*
- **Ears:** Smallest Pulse speech to text with `language=ml`
- **Brain:** Electron, Smallest's LLM, with a prompt that says "reply in Malayalam with English mixed in, 1 or 2 sentences"
- **Mouth:** Lightning v3.1 Pro text to speech with a Malayalam voice (`parvathy`, `lakshmi`, `vishnu`, `sreenath`, `unni`, `aravindan`)

Every turn prints a latency line like `⏱ STT 1.76s | LLM 1.44s | TTS 3.77s`. Each step waits for the one before it. No streaming, no voice activity detection, no barge-in. That's on purpose, so you can see the pieces. It's for learning, not how you ship an agent.

`voice_loop.py` is the same idea in English, about 60 lines: `python voice_loop.py`.

### Build it properly · `chechi_pipecat.py`, streaming, VAD, barge-in
The same Chechi, built the way real voice agents are built, with [Pipecat](https://docs.pipecat.ai):
- **Streaming everything:** Pulse STT and Lightning TTS over WebSockets, an OpenAI model streaming tokens in between
- **Silero VAD** decides when you're talking
- **Barge-in:** talk over her and she stops mid-sentence, and her memory keeps only what she actually said
- A latency line per service, every turn

It needs two keys: Smallest for the ears and the voice, OpenAI for the brain. (`three_api_calls.py` only needs the Smallest key.)
```bash
export SMALLEST_API_KEY="your-smallest-key"
export OPENAI_API_KEY="your-openai-key"     # or copy .env.example to .env and fill both in
python chechi_pipecat.py
```
Open http://localhost:7860, click **Connect**, allow the mic and say hi. Wear earphones, or she hears herself and interrupts her own sentence. The LLM defaults to `gpt-4.1-mini`; set `OPENAI_MODEL` to try another. Set `CHECHI_VOICE=vishnu` for a male voice.

### Taking it to a phone and production
Same pipeline, different wire. My public [blog-code](https://github.com/abhishekmishragithub/blog-code) repo has the [voice-agent](https://github.com/abhishekmishragithub/blog-code/tree/main/voice-agent) this is based on and a [phone-agent](https://github.com/abhishekmishragithub/blog-code/tree/main/phone-agent) that puts it on a real phone number through Plivo or Twilio.

### Sample audio (`samples/`)
| File | What |
|---|---|
| `greeting_ml_parvathy.wav`, `greeting_ml_vishnu.wav` | "എല്ലാവർക്കും കേരളപ്പിറവി ആശംസകൾ! Welcome to BUILD Day Cochin..." |
| `user_question_ml.wav` | A Manglish question for Chechi |
| `chechi_reply_ml.wav` | Chechi's answer |
| `user_question_en.wav` | An English test line for voice_loop.py |
| `phone8k_greeting_ml.wav`, `phone8k_question_ml.wav` | The same audio squashed to 8 kHz mu-law, i.e. what a phone line sounds like |

### Test your agent
```bash
pytest -v test_chechi_call.py
```
Feeds the recorded voices in `samples/` through the functions in `three_api_calls.py` and checks she understands Malayalam (even at phone quality), replies in Manglish without markdown, and returns real audio.
To test a real phone call, use [sipling](https://github.com/abhishekmishragithub/sipling), an open source pytest tool that places SIP calls. Setup notes are at the top of the test file.

---

## Build it yourself with open source
The talk part of the session: how a platform like this works underneath.
- **Orchestrators:** [Pipecat](https://docs.pipecat.ai) · [LiveKit Agents](https://docs.livekit.io/agents)
- **VAD:** Silero VAD · **Turn detection:** Pipecat Smart Turn, LiveKit turn detector
- **Speech to text:** Whisper (batch), or any streaming STT API
- **Text to speech:** Piper, Kokoro, AI4Bharat IndicF5 for Indian languages
- **The best free guide:** *Voice AI & Voice Agents: An Illustrated Primer*, voiceaiandvoiceagents.com
- **Slides** from today are in [`deck/`](deck/), and the Pipecat code is `chechi_pipecat.py` above

## The slides (`deck/`)
The deck from the session is a [Slidev](https://sli.dev) project, with speaker notes on every slide. A PDF copy is at `deck/kochi-deck.pdf`.

```bash
cd deck
npm install
npx slidev slides.md          # opens the deck at http://localhost:3030 (press P for presenter mode with notes)
npx slidev build slides.md    # static site in deck/dist
npx slidev export slides.md --output kochi-deck.pdf   # needs playwright-chromium, installed by npm install
```

## Ideas to try next
- Make Chechi speak Tamil, Kannada, Telugu or Hindi (change `language` and the voice).
- Give your dashboard agent a tool (e.g. a weather API) so it can look things up.
- Put `chechi_pipecat.py` on a phone number with the phone-agent code linked above.

Built something? Post it and tag **@stalwartcoder** with **#BUILDDayCochin**.
**Never commit your API key.** Use `.env` (already in `.gitignore`) or export it in your terminal.
