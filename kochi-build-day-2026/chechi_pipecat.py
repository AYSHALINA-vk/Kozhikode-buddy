"""
chechi_pipecat.py: Chechi, the Manglish voice agent, built properly with Pipecat.

Same persona as three_api_calls.py, but this is how you'd actually build it:
  - everything streams: Pulse STT (Malayalam) and Lightning v3.1 Pro TTS over WebSockets
  - Silero VAD decides when you're talking
  - barge-in: start talking and Chechi stops mid-sentence
  - the LLM is an OpenAI model (gpt-4.1-mini by default, set OPENAI_MODEL to change it)

Run it:
  pip install -r requirements.txt
  export SMALLEST_API_KEY="your-smallest-key"   # STT + TTS (or put both in .env)
  export OPENAI_API_KEY="your-openai-key"       # the LLM
  python chechi_pipecat.py
  then open http://localhost:7860, click Connect, allow the mic, and wear headphones
  (on speakers she can hear herself and interrupt her own sentence).
"""

import os

from dotenv import load_dotenv
from loguru import logger
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import Frame, LLMRunFrame, MetricsFrame
from pipecat.metrics.metrics import TTFBMetricsData
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.task import PipelineParams
from pipecat.pipeline.worker import PipelineWorker
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.services.smallest.stt import SmallestSTTService
from pipecat.services.smallest.tts import SmallestTTSService
from pipecat.transcriptions.language import Language
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.workers.runner import WorkerRunner

load_dotenv(override=True)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")  # cheap and fast; any OpenAI chat model works
VOICE = os.getenv("CHECHI_VOICE", "parvathy")  # other Malayalam voices: lakshmi, vishnu, sreenath, unni, aravindan

# Same persona as three_api_calls.py
PERSONA = (
    "You are Chechi, a warm, funny voice assistant from Kochi, talking to students at BUILD Day Cochin "
    "on Kerala Piravi (1 November 2026, the 70th anniversary of Kerala state being formed on 1 November 1956). "
    "Never make up facts or numbers. "
    "Talk the way young people in Kerala actually talk: Malayalam written in Malayalam script, "
    "with English words mixed in naturally (code-switching), like 'ഇന്ന് നമ്മൾ ഒരു voice agent build ചെയ്യാം'. "
    "Reply in 1 or 2 short spoken sentences. No markdown, no emojis, no lists."
)


class LatencyMeter(FrameProcessor):
    """Prints time-to-first-byte for every service, every turn."""

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        if isinstance(frame, MetricsFrame):
            for d in frame.data:
                if isinstance(d, TTFBMetricsData) and d.value > 0:
                    name = d.processor.split("#")[0].replace("Service", "")
                    logger.info(f"⏱  {name:<20} time-to-first-byte {d.value * 1000:6.0f} ms")
        await self.push_frame(frame, direction)


def make_services():
    """The three models: Smallest for the ears and the mouth, OpenAI for the brain. All streaming."""
    smallest_key = os.getenv("SMALLEST_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    if not smallest_key or not openai_key:
        raise SystemExit("Set SMALLEST_API_KEY and OPENAI_API_KEY first (see .env.example).")
    stt = SmallestSTTService(
        api_key=smallest_key,
        settings=SmallestSTTService.Settings(language=Language.ML),  # Pulse, Malayalam
    )
    llm = OpenAILLMService(
        api_key=openai_key,
        settings=OpenAILLMService.Settings(model=OPENAI_MODEL, system_instruction=PERSONA),
    )
    tts = SmallestTTSService(
        api_key=smallest_key,
        settings=SmallestTTSService.Settings(
            model="lightning_v3.1_pro", voice=VOICE, language=Language.ML
        ),
    )
    return stt, llm, tts


async def run_bot(transport: BaseTransport, runner_args: RunnerArguments):
    stt, llm, tts = make_services()

    context = LLMContext(
        [
            {"role": "user", "content": "Greet the students in one short Manglish sentence and wish them a happy Kerala Piravi."},
        ]
    )
    ctx = LLMContextAggregatorPair(context)

    pipeline = Pipeline(
        [
            transport.input(),   # mic audio in, Silero VAD runs here
            stt,                 # audio to Malayalam text, streaming
            ctx.user(),          # add what you said to the history
            llm,                 # history to streaming tokens
            tts,                 # tokens to streaming audio
            LatencyMeter(),      # print the latency budget
            transport.output(),  # audio out to the browser
            ctx.assistant(),     # record only what was actually spoken (barge-in safe)
        ]
    )

    # Interruptions are on by default in Pipecat: when VAD hears you, Chechi stops talking.
    worker = PipelineWorker(pipeline, params=PipelineParams(enable_metrics=True))

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        await worker.queue_frames([LLMRunFrame()])  # Chechi speaks first

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        await worker.cancel()

    runner = WorkerRunner(handle_sigint=runner_args.handle_sigint)
    await runner.add_workers(worker)
    await runner.run()


async def bot(runner_args: RunnerArguments):
    transport = await create_transport(
        runner_args,
        {
            "webrtc": lambda: TransportParams(
                audio_in_enabled=True,
                audio_out_enabled=True,
                vad_analyzer=SileroVADAnalyzer(),
            ),
        },
    )
    await run_bot(transport, runner_args)


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()
