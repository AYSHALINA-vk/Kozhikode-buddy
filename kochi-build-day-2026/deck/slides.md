---
theme: default
title: AI From Hype to BLDing your first Voice Agents
info: BUILD Day Cochin · Kerala Piravi 2026 · Abhishek Mishra · DevRel & DevEx, Smallest AI
colorSchema: light
highlighter: shiki
transition: fade
mdc: true
routerMode: hash
fonts:
  sans: Inter
  serif: Space Grotesk
  mono: JetBrains Mono
---

<div class="h-full flex flex-col justify-center text-center">

<div class="wave">▁▂▃▅▂▇▂▅▃▂▁▃▅▇▅▃▁▂▅▃▂▁▂▃▅▂▇▂▅▃▂▁</div>

<div class="mt-6" style="font-size:4rem; font-weight:700; color:var(--green700); line-height:1.3">കേരളപ്പിറവി ആശംസകൾ</div>

<div class="mt-4 text-2xl">Kerala Piravi ashamsakal</div>

<div class="mt-6 font-mono text-xl subtle">1 Nov 1956 → 1 Nov 2026 · Kerala turns 70</div>

<div class="mt-10 font-mono text-sm meta">Abhishek Mishra · @stalwartcoder</div>

</div>

<!--
Kerala Piravi ashamsakal, everyone!

Today is Kerala's birthday. Seventy years ago today, on 1 November 1956, the state was formed. So happy 70th, Kerala.

I'm not going to try too much Malayalam myself. In a minute you will meet someone who speaks it way better than me. She's a voice agent, and she talks in Manglish, the way you actually talk.

And then you are going to build your own.
-->

---
layout: center
title: AI From Hype to BLDing your first Voice Agents
---

<div class="wave">▁▂▃▅▂▇▂▅▃▂▁▃▅▇▅▃▁▂▅▃▂▁▂▃▅▂▇▂▅▃▂▁</div>

# AI · From Hype to BLDing
## <span class="subtle" style="font-weight: 400">your first voice agents</span>

<div class="mt-8 font-mono subtle">
Abhishek Mishra · @stalwartcoder
</div>
<div class="mt-1 font-mono text-sm meta">
DevRel &amp; DevEx · Smallest AI · BUILD Day Cochin
</div>

<!--
Quick intro. I'm Abhishek, I lead DevRel and DevEx at Smallest AI. We build voice AI, speech to text, text to speech, and voice agents.

There's a lot of hype around AI right now. Today is not about the hype. Today you build one, and then I show you what's inside it.
-->

---
layout: center
class: text-center
title: Meet Chechi
---

<div class="eyebrow mb-4">Meet Chechi</div>

<div class="font-mono" style="font-size:4.6rem; font-weight:700; letter-spacing:0.04em; white-space:nowrap; color:var(--green700); line-height:1.2">+91 22 6809 3636</div>

<div class="mt-8 text-2xl">Before we build anything, let's call her.</div>

<!--
60 seconds, no more.

"Before I explain anything, let me call someone." Call from your own phone, held to the mic, not on speaker.

Let her greet. She opens with the Kerala Piravi wish.

Ask one Malayalam question in one breath, no pause after "Chechi". Like "Chechi, Kochiyil evening enthu cheyyam?"

Then one in pure English, like "What should I eat in Fort Kochi?" She still answers in Manglish.

Hang up and say "That's a voice agent. In the next 10 minutes you'll build your own."

If the call fails, don't debug. Say "she's busy, we'll call her back later" and move on.
-->

---
title: Today
---

<div class="eyebrow">Today</div>

# Five things, in this order

<div class="mt-8 font-mono text-xl leading-loose">

1. **Meet Chechi** · a quick call <span class="meta">· ~1 min</span> <span style="color:var(--green)">→ phone</span>
2. **Build** your first voice agent <span class="meta">· ~12 min</span> <span style="color:var(--green)">→ laptops out</span>
3. **Look underneath**, with open source <span class="meta">· ~12 min</span>
4. **Demo and test** · Chechi again, then pytest <span class="meta">· ~7 min</span>
5. **Your turn** · take the repo home

</div>

<!--
Here's the plan. You just met Chechi. Now you build your own. No code, on a real platform, about twelve minutes.

Then I open the hood and show you how that thing works, all with open source.

Then we call Chechi again, properly this time, and I show you how to test an agent so it still works tomorrow.

And then you take everything home in a repo.
-->

---
layout: center
class: text-center
title: Sign up
---

<div class="eyebrow mb-4">Step 0 · get in</div>

# Scan, sign up, you're in

<div class="mt-6 flex items-center justify-center gap-12">
  <img src="/images/qr-signup.png" class="w-64 rounded-lg" style="border:1px solid var(--g200)" />
  <div class="text-left text-xl leading-loose">
    <div class="font-mono" style="color:var(--green700)">app.smallest.ai</div>
    <div>Any email works</div>
    <div>Free to start, no card</div>
    <div class="subtle">Slow wifi? One phone hotspot for three of you</div>
  </div>
</div>

<!--
Scan this and sign up with any email. It's free to start, you get free credits, no card needed.

If the wifi is slow, use a phone hotspot. One hotspot is enough for three people.

No laptop? Sit with a neighbour. Your job is to try and break their agent.

Wait about 90 seconds here. Walk to the side so everyone can see the QR.
-->

---
title: Build Kochi Buddy
---

<div class="eyebrow">Build along · follow my screen</div>

# Build Kochi Buddy

<div class="mt-6 text-lg leading-loose">

**1 ·** Create Agent (green, top right) → Start from Scratch → Single Prompt

**2 ·** Name it `kochi-buddy` · Call Direction Inbound

**3 ·** Pick a voice, hit preview · Malayalam (Beta) is in Languages, try it

**4 ·** Paste the prompt from the repo · add a first message · Save

**5 ·** Test Agent → Web Call → allow the mic → talk

</div>

<div class="callout mt-6 text-lg">
Try three things. A normal question. A weird one ("book me a flight to Mars"). Then interrupt it mid sentence.
</div>

<!--
Switch to the dashboard now and go slow, same pace as the room.

Green button, top right, Create Agent. Start from scratch, single prompt. Give it a name, I'm calling mine Kochi Buddy.

Now pick a voice. Click preview on a few. Nobody hears the name, everyone hears the voice, so take your time here. In Languages you'll see Malayalam, it's in beta, go for it.

The prompt box is the brain. It's plain English instructions. Role, how the conversation goes, what not to do, when to stop. The exact text is in the repo, copy it. Look at the line that says speak in short sentences. That's the most important line for voice. Nobody wants to listen to an essay.

The first message is what it says the second the call connects. Without it the agent just sits there waiting for you. Awkward.

Live tweak: add "You love puttu and kadala curry and bring it up once."

Then Test Agent, Web Call, allow the mic, and talk to it. Let the room get loud. Walk the rows. If mics fail, use Chat mode.

At the end ask "hands up if your agent talked back to you."
-->

---
layout: center
title: You just used a platform
---

<div class="eyebrow mb-4 text-center">The bridge</div>

# You just used a platform. <span style="color:var(--green)">Here's what's underneath.</span>

<img src="/images/pipeline-trim.svg" class="w-220 mx-auto mt-10" />

<!--
OK. In about ten minutes you built something that listens, thinks and talks back.

That was a platform doing a lot of work you didn't see. Now I want to open the hood. Everything I show you next is open source or a plain API, so you could build a platform like that yourself. That's the fun part.
-->

---
layout: center
title: The mental model everyone starts with
---

<div class="eyebrow mb-8">The mental model everyone starts with</div>

<img src="/images/text-agent.svg" class="w-180 mx-auto" />

<!--
This is a text agent. One model. One box. You send tokens, you get tokens.

Everything you know about building LLM apps lives inside this box. ChatGPT is this. Most of you have built something like this already.

And most people think a voice agent is the same thing with a mic stuck on the front. It's not.
-->

---
layout: center
title: The mental model you actually need
---

<div class="eyebrow mb-6">The mental model you actually need</div>

<v-click>

<img src="/images/pipeline.svg" class="w-230 mx-auto" />

</v-click>

<v-click>

<div class="text-center mt-10 text-xl">
<b style="color:var(--green)">Everything hard about voice AI lives in the arrows, not the boxes.</b>
</div>

</v-click>

<!--
[click] This is a voice agent. Same LLM, sitting in the middle, doing maybe 30% of the work. Around it, four more components. Something to detect speech, something to know when you stopped talking, speech to text, text to speech. Plus a real-time transport layer, and a clock that will not wait for you.

So it's not one model in one box. It's a system.

[click] This is the line the whole talk hangs on. Everything hard about voice AI lives in the arrows, not the boxes. In a minute we walk this diagram left to right, box by box.
-->

---
layout: center
title: The clock
---

<div class="grid grid-cols-3 gap-12 text-center">
<div>
  <div class="big-num">~200<span style="font-size:1.6rem">ms</span></div>
  <div class="num-label">average gap between human turns, 10 languages<br><span class="text-xs">Stivers et al., PNAS 2009</span></div>
</div>
<div>
  <div class="big-num" style="color:var(--g500)">1,500<span style="font-size:1.6rem">ms</span></div>
  <div class="num-label">"an important target to aim for", voice to voice<br><span class="text-xs">Voice AI &amp; Voice Agents primer</span></div>
</div>
<div>
  <div class="big-num" style="color:var(--amber)">?<span style="font-size:1.6rem">ms</span></div>
  <div class="num-label">what your agent actually does<br><span class="text-xs">you'll feel it on the phone demo</span></div>
</div>
</div>

<!--
When two people talk, the gap between one stopping and the other starting is about 200 milliseconds. That held across ten very different languages in one big study.

The voice AI primer says aim for about one and a half seconds, voice to voice.

If your agent takes three seconds, it feels broken. You probably felt that when you tested Kochi Buddy. That gap is the whole game.

Cut this slide if the build-along ran long.
-->

---
layout: center
title: Everything must stream
---

# Everything must stream

<div class="mt-8 text-xl font-mono">

<div style="color:var(--red)">✗ &nbsp;record → transcribe → think → synthesize → play</div>

<div class="mt-4" style="color:var(--green)">✓ &nbsp;stream → stream → stream → stream → stream</div>

</div>

<div class="mt-10 subtle">Every component emits partial results. Nothing waits for "done".</div>

<!--
If every step waits for the step before it, you add up all the waiting.

So everything streams. Words come out of speech to text while you're still talking. The brain starts answering before it's done thinking. The voice starts playing from the first chunk.
-->

---
title: Stop 1 transport
---

<img src="/images/strip-transport.svg" class="strip w-140" />

<div class="eyebrow">Stop 1 · transport</div>

# How your voice reaches the code

| | Use for | Why |
|---|---|---|
| **WebRTC** | Browser, mobile | Opus codec, jitter buffer, packet-loss concealment, echo cancellation |
| **WebSocket** | Server to server, telephony bridges | Simple, no media features built in |
| **SIP / PSTN** | Phone calls | How the phone network works. Narrowband audio (8 kHz). |

<div class="warnbox mt-6">
Do not build WebRTC yourself. NAT traversal, STUN/TURN, ICE, codec negotiation.
</div>

<!--
First, how does your voice even reach the code?

In the browser it's WebRTC. That's what your Web Call just used.

On the phone it's the phone network, bridged to your code over a WebSocket. That's what you'll hear in the Chechi demo.

Don't build WebRTC yourself. Seriously. Use what exists.
-->

---
title: Stop 2 VAD and STT
---

<img src="/images/strip-stt.svg" class="strip w-140" />

<div class="eyebrow">Stop 2 · VAD, then speech to text</div>

# Your sentence becomes words, while you speak

<div class="text-lg mt-4 leading-relaxed">

**VAD** decides "is someone speaking right now?" It gates everything downstream.

**Streaming STT** emits partial transcripts as audio arrives. Not after you stop.

</div>

<div class="callout mt-6 text-lg">
Batch-first models (Whisper-style) want the whole utterance. A live conversation can't give them that.
</div>

<div class="mt-4 text-sm subtle font-mono">Open source · Silero VAD · Whisper · AI4Bharat IndicConformer</div>

<!--
VAD is a tiny model with one job. Is someone talking right now, yes or no. Silero VAD is open source and it's what most people use.

Then speech to text turns your voice into words. Open source option, Whisper. But Whisper wants the whole sentence first, and a live conversation can't give it that. So for real time you want a streaming model.

For Indian languages, look at AI4Bharat. They do great open work for Malayalam and friends.
-->

---
title: Stop 3 the LLM, prompted for the ear
---

<img src="/images/strip-llm.svg" class="strip w-140" />

<div class="eyebrow">Stop 3 · the LLM, prompted for the ear</div>

# The reply must be speakable

| Text agent | Voice agent |
|---|---|
| Bullet points, markdown, emoji | Never |
| "₹1,234.50" | "twelve hundred thirty-four rupees and fifty paise" |
| Long, thorough answers | 1 or 2 sentences, then stop |
| "Let me know if you need anything else!" | Once. Not every turn. |

<!--
Remember the line in your prompt, short sentences? Here's why.

A text bot can send bullet points and emojis. A voice bot has to say everything out loud. Twelve hundred rupees has to become words.

One or two sentences, then stop.
-->

---
title: Stop 4 TTS and playback
---

<img src="/images/strip-tts.svg" class="strip w-140" />

<div class="eyebrow">Stop 4 · text to speech, then playback</div>

# The reply becomes a voice

<div class="text-lg mt-2 leading-relaxed">

TTS starts on the **first chunk** of LLM output, not the full reply.

Audio streams back over the same transport and plays while the rest is still being generated.

</div>

<div class="callout mt-6 text-lg">
The metric that matters is <b>TTFB</b>, time to first byte. Not total synthesis time.
</div>

<div class="mt-4 text-sm subtle font-mono">Open source · Piper · Kokoro · IndicF5</div>

<!--
Then text to speech. The number that matters is time to first byte, how fast the first bit of sound comes out. Not how long the whole sentence takes.

Open source here, Piper and Kokoro. And for Indian languages, AI4Bharat's IndicF5.
-->

---
title: One pipeline, interchangeable models
---

<img src="/images/strip-orch.svg" class="strip w-140" />

<div class="eyebrow">The whole agent as code · Pipecat</div>

# One pipeline, interchangeable models

```python {all|1-3|5-7|9-10|all}
stt = SmallestSTTService(api_key=SMALLEST_KEY)                     # Pulse
llm = AnthropicLLMService(settings=AnthropicLLMService.Settings(model="claude-haiku-4-5-20251001"))
tts = SmallestTTSService(api_key=SMALLEST_KEY, settings=SmallestTTSSettings(voice="meher"))

# the swap: one line, pipeline untouched
# tts = SmallestTTSService(api_key=SMALLEST_KEY, settings=SmallestTTSSettings(voice="nolan"))
# llm = OpenAILLMService(...)   tts = CartesiaTTSService(...)   stt = DeepgramSTTService(...)

pipeline = Pipeline([transport.input(), stt, ctx.user(), llm, tts,
                     transport.output(), ctx.assistant()])
```

<div class="mt-4 text-base subtle">
The orchestrator owns transport, turn-taking, interruption and context. <b>Pipecat</b> here. <b>LiveKit Agents</b> is the other big one. Both are open source.
</div>

<!--
This is the whole agent as code. This is Pipecat, an open source framework. LiveKit Agents is the other big one.

Look at it. It's a list. Input, speech to text, the brain, text to speech, output.

[click through the highlights]

Each line is a model, and you can swap any of them in one line. Open source STT, any LLM, any TTS.

The framework handles the hard part. The timing, the interruptions, the memory of what was said. This is roughly what the platform you used is doing for you.

The key comes from an environment variable. Never paste a key into code you push.
-->

---
layout: center
title: Hard part 1 endpointing
---

<div class="eyebrow mb-6">Hard part 1 · knowing when the human stopped talking</div>

<div class="text-3xl font-mono leading-relaxed">

"I'd like a large pizza…"

<div class="my-4 subtle" style="font-size:1.2rem">…done? Or</div>

"I'd like a large pizza… <span style="color:var(--green)">and garlic bread."</span>

</div>

<div class="mt-8 text-base subtle">
Silence timer → semantic endpointing → semantic + acoustic. <span class="font-mono text-sm">Pipecat Smart Turn · LiveKit turn detector</span>
</div>

<!--
Read this one slowly.

"I'd like a large pizza." Done? Or... "and garlic bread."

How does the agent know you finished? A silence timer is the simple answer and it's wrong half the time. The better answer looks at the words and the tone.

Pipecat's Smart Turn model is open source and does exactly this. Honest note, most of these models are best in English today. Malayalam turn-taking is still hard, which is a great problem for someone in this room to work on.
-->

---
title: Hard part 2 barge-in
---

<div class="eyebrow">Hard part 2 · barge-in, and the context bug</div>

# What did the agent actually say?

<div class="grid grid-cols-2 gap-8 mt-2 items-start">

<div class="text-base leading-relaxed">

Agent: <i>"Sure, I can book that for you on Tuesday at 3pm, and I'll send a confirm..."</i>

User cuts in at <b>"Tuesday."</b>

<div class="mt-4"><b>What does the conversation history say the agent said?</b></div>

<div class="mt-3">
<span style="color:var(--red)">✗ The full sentence.</span> The agent now believes 3pm is agreed. It is not.<br><br>
<span style="color:var(--green)">✓ Truncate to what was <b>actually played out loud</b>.</span>
</div>

</div>

<img src="/images/meme-they-dont-know.png" class="max-h-70 rounded-lg" />

</div>

<!--
Remember when you interrupted your agent? Here's the bug most people ship.

The agent was saying Tuesday at 3 pm, and you cut in at Tuesday. If the agent's memory says it said the whole sentence, it now thinks 3 pm is agreed. Nobody agreed.

Fix. Only remember what was actually played out loud.
-->

---
title: Ten building blocks
---

<div class="eyebrow">The shopping list</div>

# Ten building blocks

<div class="blocks mt-5">
<div class="block"><span class="t">1 · Transport</span><span class="d">WebRTC / WS / SIP. How audio moves.</span></div>
<div class="block"><span class="t">2 · VAD + turn detection</span><span class="d">When to listen, when to speak.</span></div>
<div class="block"><span class="t">3 · STT</span><span class="d">The ears. Streaming, always.</span></div>
<div class="block"><span class="t">4 · LLM + voice prompt</span><span class="d">The brain, prompted for the ear.</span></div>
<div class="block"><span class="t">5 · TTS</span><span class="d">The voice. TTFB is the metric.</span></div>
<div class="block hot"><span class="t">6 · Orchestrator</span><span class="d">The conductor. Pipecat or LiveKit Agents.</span></div>
<div class="block"><span class="t">7 · Tools / APIs</span><span class="d">The hands. Async, masked.</span></div>
<div class="block"><span class="t">8 · Knowledge / RAG</span><span class="d">The memory. Keep retrieval tight.</span></div>
<div class="block"><span class="t">9 · Telephony</span><span class="d">Optional. A number and a carrier.</span></div>
<div class="block"><span class="t">10 · Evals + observability</span><span class="d">Latency percentiles. Listen to calls.</span></div>
</div>

<div class="mt-5 text-base subtle">
The framework hands you 1, 2 and 6. You choose 3, 4, 5. You build 7 and 8. You rent 9. You never stop doing 10.
</div>

<!--
If you want to build a platform like the one you just used, this is your shopping list.

The framework gives you transport, turn detection and the orchestrator. You choose the ears, the brain and the voice. You build the tools and the knowledge. You rent a phone number. And you never stop testing.

That's the homework. Cut this slide if you're running late.
-->

---
layout: center
class: text-center
title: Call Chechi
---

<div class="eyebrow mb-4">Live · Chechi speaks Manglish</div>

<div class="font-mono" style="font-size:4.6rem; font-weight:700; letter-spacing:0.04em; white-space:nowrap; color:var(--green700); line-height:1.2">+91 22 6809 3636</div>

<div class="mt-8 text-2xl">I call, you shout the questions. English, Hindi or Malayalam.</div>

<div class="mt-6 text-sm subtle font-mono">It's an AI. Normal call charges. Try it yourself after the session, one call at a time.</div>

<!--
Now that you know how it works, let's call Chechi again. Same number as the start. This time listen for the pieces. Speech to text catching the Malayalam, the brain mixing in English, the voice coming back fast, and what happens when I cut her off.

Call from your own phone, hold it to the mic, NOT on speaker, so she doesn't hear herself and cut in. You're the only caller. In testing, parallel calls dropped, so don't ask the room to dial in.

1. Let her greet.
2. Ask a new Malayalam question (not the one from the cold open) in one breath, no pause after "Chechi". Like "Chechi, Kochiyil evening enthu cheyyam?"
3. Ask the next one in pure English. Point out she still answers in Manglish. That's the moment.
4. Talk over her once, firmly, for a couple of seconds, to show interruption. Tie it back to the barge-in slide.
5. Take 2 or 3 questions shouted from the room and ask her yourself.

If the call fails, don't debug. Say "live demos!", open Chechi v1 in the dashboard and use Test. If that fails too, run python three_api_calls.py --type in the terminal.
-->

---
title: How do you know it still works tomorrow
---

<div class="eyebrow">Test it</div>

# How do you know it still works tomorrow?

```python
def test_brain_replies_in_manglish_and_keeps_it_short():
    reply = chechi.think("ചേച്ചി, ഇന്ന് Kerala Piravi ആണല്ലോ. ഒരു hi പറയാമോ?")
    assert MALAYALAM.search(reply)          # Malayalam in the reply
    assert len(reply) < 400                 # short enough to say out loud

@pytest.mark.live
def test_live_chechi_answers_the_phone():
    result = sipling.probe(uri, transport="tcp", timeout=15)   # a real SIP call
```

<div class="mt-4 font-mono text-base leading-loose">
<span class="subtle">offline:</span> &nbsp;pytest -v test_chechi_call.py<br>
<span class="subtle">phone:</span> &nbsp;&nbsp;&nbsp;pytest -v --live -k live test_chechi_call.py
</div>

<div class="mt-2 text-sm subtle">sipling · open source · github.com/abhishekmishragithub/sipling</div>

<!--
Switch to the terminal, big font, in the repo folder, and run pytest -v test_chechi_call.py. Five should go green in a few seconds.

How do you know your agent still works tomorrow? You don't call it by hand every time. You write tests.

These feed recorded voices into the agent and check what comes back. One takes the same question squashed down to phone quality, 8 kilohertz, and checks it still understands Malayalam. This one checks the brain replies in Manglish and keeps it short, with no markdown.

And the live one uses a tool I wrote called sipling. It's open source. It makes a real phone call to the agent from a test and checks it picked up and actually spoke. So your CI can phone your agent every night.

If it fails, laugh. "And that's why we test." Move on.
-->

---
title: Resources
---

<div class="eyebrow">Where to actually learn this</div>

# Resources

<div class="grid grid-cols-2 gap-8 mt-2 items-start">

<div class="text-sm leading-relaxed">

**The textbook:** <i>Voice AI & Voice Agents: An Illustrated Primer</i> · `voiceaiandvoiceagents.com`

**Pipecat:** `docs.pipecat.ai` · `pip install "pipecat-ai[smallest]"`

**LiveKit Agents:** `docs.livekit.io/agents` · `pip install livekit-plugins-smallestai`

**Smallest Waves docs:** `docs.smallest.ai`

</div>

<div class="grid grid-cols-2 gap-3 text-center text-xs font-mono subtle">
  <div><img src="/images/qr-primer.png" class="w-26 rounded" style="border:1px solid var(--g200)" /><div class="mt-1">the primer</div></div>
  <div><img src="/images/qr-pipecat-trim.png" class="w-26 rounded" style="border:1px solid var(--g200)" /><div class="mt-1">pipecat</div></div>
  <div><img src="/images/qr-livekit.png" class="w-26 rounded" style="border:1px solid var(--g200)" /><div class="mt-1">livekit agents</div></div>
  <div><img src="/images/qr-smallest.png" class="w-26 rounded" style="border:1px solid var(--g200)" /><div class="mt-1">smallest docs</div></div>
</div>

</div>

<!--
If you want to go deeper after today, start here.

The primer is the best free textbook on voice AI right now. Read it end to end, it's worth it.

Pipecat and LiveKit Agents are the two open source frameworks I talked about. Both have a Smallest plugin, one pip install and you're running.

And our docs, if you want to go further with the platform you used today.

Pause here for 10 seconds so people can scan.
-->

---
layout: center
class: text-center
title: Take it home
---

<div class="eyebrow mb-4">Take it home</div>

# Everything from today is in here

<div class="mt-6 flex items-center justify-center gap-12">
  <img src="/images/qr-repo.png" class="w-60 rounded-lg" style="border:1px solid var(--g200)" />
  <div class="text-left text-xl leading-loose">
    <div><b>1 ·</b> Finish your agent at home</div>
    <div><b>2 ·</b> Run Chechi from the repo</div>
    <div><b>3 ·</b> Post it, tag <span class="font-mono">@stalwartcoder</span> <span class="font-mono">#BUILDDayCochin</span></div>
  </div>
</div>

<div class="mt-8 font-mono text-sm subtle">github.com/abhishekmishragithub/workshops · kochi-build-day-2026</div>

<!--
Everything I showed is in this repo. Your agent's prompt, Chechi's code, the audio samples, the tests and these slides.

Build your own version in your language. Tamil, Kannada, Hindi, mixed, whatever you speak at home. Post it and tag me, I'll share the best ones.

And keep your API key out of GitHub, please.
-->

---
layout: center
class: text-center
title: Questions
---

<div class="wave mb-8">▁▂▃▅▂▇▂▅▃▂▁▃▅▇▅▃▁▂▅▃▂▁▂▃▅▂▇▂▅▃▂▁</div>

# Questions

<div class="mt-8 flex items-center justify-center gap-8">
  <img src="/images/qr-linkedin.png" class="w-32 rounded" style="border:1px solid var(--g200)" />
  <div class="text-left font-mono">
    <div class="text-lg">Abhishek Mishra</div>
    <div class="subtle">linkedin.com/in/stalwartcoder</div>
    <div class="subtle">@stalwartcoder</div>
    <div class="text-sm meta mt-1">DevRel &amp; DevEx · Smallest AI</div>
  </div>
</div>

<div class="mt-8 text-sm subtle font-mono">Nanni, Kochi! Kerala Piravi ashamsakal</div>

<!--
Take 2 to 4 questions. Group selfie with the screen behind you at the end.

Hand over. "Next up is AI that runs on your device. I showed you AI you can talk to. Put the two together and that's a fun weekend project. Thank you Kochi, nanni!"
-->
