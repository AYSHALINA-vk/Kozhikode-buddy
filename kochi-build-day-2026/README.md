# Build your first voice agent · BUILD Day Cochin · Kerala Piravi 2026
Workshop by Abhishek Mishra ([@stalwartcoder](https://x.com/stalwartcoder)) at BUILD Day Cochin, Jain University Kochi, 1 Nov 2026.
കേരളപ്പിറവി ആശംസകൾ! 🌴

Two ways to build a voice agent:
1. **No code, 15 min:** build one on a voice AI platform and talk to it in the browser.
2. **Code, 10 min:** run the pipeline yourself (speech to text → LLM → text to speech) and see where the time goes. Includes **Chechi**, a voice agent that speaks Manglish (Malayalam + English).

## What you need
- A laptop with Chrome and a mic (earphones help)
- An email to sign up with. New accounts get free credits, no card needed.
- For the code part: Python 3.10+

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

### Chechi, the Manglish agent 🥥
```bash
python manglish_agent.py                                      # press Enter, talk for 5 s
python manglish_agent.py --type                               # no mic: type your line
python manglish_agent.py --file samples/user_question_ml.wav  # no mic: feed it a wav
python manglish_agent.py --voice vishnu                       # male voice
```
Talk to her the way you talk to friends: *"Chechi, ഇന്ന് Kerala Piravi ആണല്ലോ, ഒരു fun fact പറയാമോ?"*
How she works:
- **Ears:** Smallest Pulse speech to text with `language=ml`
- **Brain:** an LLM with a prompt that says "reply in Malayalam with English mixed in, 1 or 2 sentences"
- **Mouth:** Lightning v3.1 Pro text to speech with a Malayalam voice (`parvathy`, `lakshmi`, `vishnu`, `sreenath`, `unni`, `aravindan`)

Every turn prints a latency line like `⏱ STT 1.76s | LLM 1.44s | TTS 3.77s`. This demo waits for each step to finish. Real agents stream every step, which is the main thing the talk is about. Making Chechi stream is a great next project.

### voice_loop.py, the English version
```bash
python voice_loop.py
```
Same loop, English, about 60 lines.

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
Feeds the recorded voices in `samples/` through Chechi and checks she understands Malayalam (even at phone quality), replies in Manglish without markdown, and returns real audio.
To test a real phone call, use [sipling](https://github.com/abhishekmishragithub/sipling), an open source pytest tool that places SIP calls. Setup notes are at the top of the test file.

---

## Build it yourself with open source
The talk part of the session: how a platform like this works underneath.
- **Orchestrators:** [Pipecat](https://docs.pipecat.ai) · [LiveKit Agents](https://docs.livekit.io/agents)
- **VAD:** Silero VAD · **Turn detection:** Pipecat Smart Turn, LiveKit turn detector
- **Speech to text:** Whisper (batch), or any streaming STT API
- **Text to speech:** Piper, Kokoro, AI4Bharat IndicF5 for Indian languages
- **The best free guide:** *Voice AI & Voice Agents: An Illustrated Primer*, voiceaiandvoiceagents.com
- **Slides and the full Pipecat demo** from the talk: https://github.com/abhishekmishragithub/voice-ai-talk/tree/main/2026-09-26-cloudways-voice-agents-demo-to-prod

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
- Port Chechi to Pipecat so every step streams, and watch the latency line drop.

Built something? Post it and tag **@stalwartcoder** with **#BUILDDayCochin**.
**Never commit your API key.** Use `.env` (already in `.gitignore`) or export it in your terminal.
