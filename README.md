# Kozhikode Buddy

A funny **Manglish** (Malayalam + English) voice agent that helps you plan an evening in Kozhikode (Calicut). Ask it where to find good biriyani, which beach to catch the sunset at, or what to do on a rainy day, and it answers out loud in short, casual Manglish.

Built from the **BUILD Day Cochin** voice-agent workshop by Abhishek Mishra ([@stalwartcoder](https://github.com/abhishekmishragithub)), adapted for Kozhikode with a new persona, a Gemini-powered brain, and a Manglish-script fix for better-sounding Malayalam speech.

> **Demo:** _add your video or post link here_

## How it works

Every voice agent is three pieces in a row:

| Piece | Job | Service |
|---|---|---|
| Ears | Speech to text | Smallest **Pulse** (`language=ml`) |
| Brain | Decides what to say | Any OpenAI-compatible LLM (Gemini by default here, OpenAI works too) |
| Mouth | Text to speech | Smallest **Lightning v3.1 Pro** with a Malayalam voice |

There are two versions of the same agent:

| File | What it is | Use it for |
|---|---|---|
| `three_api_calls.py` | The three calls one after another, one turn at a time, with a latency line per step | Learning how the pieces fit |
| `chechi_pipecat.py` | The proper version with [Pipecat](https://github.com/pipecat-ai/pipecat): streaming, Silero VAD, barge-in | The real agent in your browser |

The Pipecat version streams everything. Speech starts before the full reply exists, and you can talk over the agent and it stops mid-sentence.

## What I changed from the workshop

- **Persona:** Chechi became **Kozhikode Buddy**, with knowledge of Malabar biriyani, halwa on S.M. Street, Kozhikode and Kappad beaches, Mishkal Mosque, Mananchira Square and more.
- **Humour with limits:** jokes about food, humidity and traffic, never about religion, communities or politics.
- **Better Malayalam speech:** the voice model reads Malayalam script well but mangles Malayalam typed in English letters. The prompt now forces Malayalam words into script and English words into English letters. `three_api_calls.py` also checks each reply and asks the model to rewrite it once if it comes back without Malayalam script.
- **Any LLM:** the brain is configured with environment variables, so you can switch between Gemini, OpenAI or another OpenAI-compatible API without editing code.
- **Retries and clear errors:** busy servers (429/5xx) and timeouts are retried, and failures print the server's real message.

## Setup

You need Python 3.11 or newer, a mic and earphones (without earphones the agent hears itself and interrupts its own sentences).

```bash
git clone https://github.com/AYSHALINA-vk/Kozhikode-buddy.git
cd Kozhikode-buddy/kochi-build-day-2026
python -m venv .venv
```

Activate the virtual environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```
```bash
# macOS / Linux
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## API keys

| Variable | Needed for | Where to get it |
|---|---|---|
| `SMALLEST_API_KEY` | Speech to text and text to speech | Smallest AI dashboard, API Keys |
| `LLM_KEY` | The brain (a Gemini key by default) | Google AI Studio |
| `LLM_MODEL` | Which model to use, e.g. a Gemini Flash-Lite model | Google AI Studio model list |
| `LLM_BASE_URL` | Optional. Defaults to Gemini when `LLM_KEY` is set | Leave empty for OpenAI |
| `OPENAI_API_KEY` | Alternative brain if you use OpenAI instead | OpenAI dashboard (needs credit) |
| `CHECHI_VOICE` | Optional voice: `parvathy` (default), `lakshmi`, `vishnu`, `sreenath`, `unni`, `aravindan` | |
| `LLM_REASONING` | Optional, only for slow "thinking" models, e.g. `low` | |

Set them in your terminal (PowerShell shown, one line at a time):

```powershell
$env:SMALLEST_API_KEY="your-smallest-key"
$env:LLM_KEY="your-gemini-key"
$env:LLM_MODEL="your-model-name"
```

**Never commit your keys.** Use a `.env` file or your terminal, and make sure both are in `.gitignore`.

## Run it

**The streaming agent (recommended):**

```bash
python chechi_pipecat.py
```

Open http://localhost:7860, click **Connect**, allow the mic and say hi. The agent greets you first. Try asking in Malayalam, English or a mix, then interrupt it mid-sentence to see barge-in.

**The bare three-call version:**

```bash
python three_api_calls.py --type        # type your line, no mic needed
python three_api_calls.py               # push-to-talk with your mic
python three_api_calls.py --voice vishnu
```

Each turn prints a latency line like `STT 0.00s | LLM 4.95s | TTS 2.76s`, and every reply is saved as `reply_N.wav`.

## Tests

```bash
pytest -v test_chechi_call.py
```

These feed recorded Malayalam audio through the pipeline and check that speech recognition works (even at phone quality), the reply stays short and free of markdown, and the voice returns real audio. The live phone-call test is skipped unless you set up a SIP number.

## Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| Malayalam voice sounds robotic or wrong | The reply is in English letters. Keep the Manglish rule in the persona and use a Malayalam-script reply |
| `403 ... not available for your plan` | The free Smallest plan can't call its own LLM through the API. Use Gemini or OpenAI as the brain |
| `401` from OpenAI with a Gemini key | The request is going to OpenAI. Set `LLM_KEY` (it now defaults to Gemini) and check the startup line `LLM -> model=... endpoint=...` |
| `429 no credits remaining` (OpenAI) | The account has no balance. Add credit or use Gemini |
| `503` or timeouts from Gemini | The model is busy. Retry, or pick a Flash-Lite model, which is faster |
| `400 INVALID_ARGUMENT` | Clear `LLM_REASONING`, since some models reject it |
| `ModuleNotFoundError` | The virtual environment isn't active. Activate it first |
| The agent interrupts itself | Use earphones |

## Limitations

- Malayalam speech on the Smallest side is still in beta, so a few words may sound slightly off.
- The agent knows only what is written in its prompt. It is told never to invent prices, opening hours or entry fees, so check those locally.
- Replies from `three_api_calls.py` take several seconds because nothing streams there. Use the Pipecat version for a natural feel.

## Ideas to try next

- Switch to Tamil, Kannada, Telugu or Hindi by changing the language and the voice.
- Give it a tool, such as a weather lookup, so it can say whether tonight suits the beach.
- Put it on a real phone number with the phone-agent code from the workshop author's blog repo.

## Credits

- Workshop code and the original Chechi agent: Abhishek Mishra, BUILD Day Cochin, Kerala Piravi 2026. Check the [original repository](https://github.com/abhishekmishragithub/workshops) for its license before reusing the code.
- Speech and voice: [Smallest AI](https://smallest.ai).
- Orchestration: [Pipecat](https://github.com/pipecat-ai/pipecat) with Silero VAD.
- Kozhikode food and place details drawn from Tripadvisor's Kozhikode attractions page and local food guides.

Built by [@AYSHALINA-vk](https://github.com/AYSHALINA-vk) #BUILDDayCochin
