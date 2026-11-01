"""
test_chechi_call.py: show the room how you TEST a voice agent.

Two kinds of tests in one file:

1. OFFLINE tests (run by default, need only SMALLEST_API_KEY + internet).
   They feed the recorded wavs in samples/ through Chechi's ears, brain and mouth
   (the same functions three_api_calls.py uses) and assert on what comes back.
       pytest -v test_chechi_call.py

2. LIVE phone test (opt-in). sipling places a REAL SIP call to the agent's number
   and asserts it answered and spoke within a few seconds.
   Setup (macOS/Linux, not Windows):
       brew install pjproject            # or: sudo apt-get install pjsip-tools  (gives you `pjsua`)
       pip install "git+https://github.com/abhishekmishragithub/sipling"
       export CHECHI_SIP_URI='sip:+91XXXXXXXXXX@5rdbhjuwtlk.sip.livekit.cloud;transport=tcp'
       pytest -v --live -k live test_chechi_call.py
   sipling's probe checks "answered + heard audio", not the words. It is not a transcript.
   Only dial a number you own.
"""
import os
import re
import time

import pytest

if not os.environ.get("SMALLEST_API_KEY"):
    pytest.skip("set SMALLEST_API_KEY to run these tests", allow_module_level=True)

import three_api_calls as chechi  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MALAYALAM = re.compile(r"[\u0D00-\u0D7F]")  # Malayalam Unicode block


def wav(name):
    with open(os.path.join(HERE, "samples", name), "rb") as f:
        return f.read()


# ---------- OFFLINE: ears ----------
def test_ears_understand_the_kerala_piravi_greeting():
    heard = chechi.speech_to_text(wav("greeting_ml_parvathy.wav"))
    assert "കേരളപ്പിറവി" in heard, heard


def test_ears_still_work_on_phone_quality_audio():
    # same question, squashed to 8 kHz mu-law like a real phone line
    heard = chechi.speech_to_text(wav("phone8k_question_ml.wav"))
    assert "കേരള" in heard, heard


def test_ears_are_fast_enough():
    t0 = time.time()
    chechi.speech_to_text(wav("user_question_ml.wav"))
    assert time.time() - t0 < 5, "STT took too long for a conversation"


# ---------- OFFLINE: brain ----------
def test_brain_replies_in_manglish_and_keeps_it_short():
    reply = chechi.think("ചേച്ചി, ഇന്ന് Kerala Piravi ആണല്ലോ. ഒരു hi പറയാമോ?")
    assert MALAYALAM.search(reply), f"no Malayalam in: {reply}"
    assert len(reply) < 400, f"too long for a voice reply: {reply}"
    assert not re.search(r"[*#`]|^\s*-", reply, re.M), f"markdown sneaked in: {reply}"


# ---------- OFFLINE: mouth ----------
def test_mouth_returns_real_audio():
    audio = chechi.tts("കേരളപ്പിറവി ആശംസകൾ!", "parvathy")
    assert audio[:4] == b"RIFF" and len(audio) > 10_000


# ---------- LIVE: a real phone call with sipling ----------
@pytest.mark.live
def test_live_chechi_answers_the_phone():
    uri = os.environ.get("CHECHI_SIP_URI")
    if not uri:
        pytest.skip("set CHECHI_SIP_URI to the agent's number as a SIP URI")
    sipling = pytest.importorskip("sipling")
    result = sipling.probe(uri, transport="tcp", timeout=15)
    try:
        assert result.answered, result.ladder
        assert result.ring_time is not None and result.ring_time < 5
        assert result.answer_time is not None and result.answer_time < 10
        assert result.heard_audio(within=8), "answered, but the agent never spoke (no greeting?)"
    finally:
        result.hangup()
        result.save_ladder("ladder.json")
    assert result.clean_bye, result.ladder
