import os

from dotenv import load_dotenv
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.base_transport import BaseTransport, TransportParams

from tools import get_tools_functions, get_tools_schema


load_dotenv(override=True)


async def agent(transport: BaseTransport, runner_args: RunnerArguments):
    stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))

    tts = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY"),
        voice_id="f9836c6e-a0bd-460e-9d3c-f7299fa60f94",
        model="sonic-2",
        params=CartesiaTTSService.InputParams(
            speed="fast"
        )
    )

    llm = OpenAILLMService(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4.1",
    )

    tools_schema = get_tools_schema()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly voice assistant that helps users complete tasks in web browsers."
                "Keep responses short and conversational."
                "When the user asks you to do something in the browser, call start_browser_task with a clear, detailed task description."
                "If details are missing (e.g. restaurant name, address), ask a brief clarifying question first."
            ),
        },
    ]

    context = LLMContext(messages, tools=tools_schema)
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(vad_analyzer=SileroVADAnalyzer()),
    )

    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            user_aggregator,
            llm,
            tts,
            transport.output(),
            assistant_aggregator,
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(),
    )

    for tool in get_tools_functions():
        llm.register_direct_function(tool)

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        messages.append(
            {
                "role": "system",
                "content": "Say hello and briefly explain you can help the user do things in the browser, like ordering food.",
            }
        )
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        await task.cancel()

    runner = PipelineRunner(handle_sigint=runner_args.handle_sigint)

    await runner.run(task)


async def bot(runner_args: RunnerArguments):
    transport_params = {
        "webrtc": lambda: TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
        ),
    }

    transport = await create_transport(runner_args, transport_params)

    await agent(transport, runner_args)


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()
