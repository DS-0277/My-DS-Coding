import sys
import time
from pathlib import Path
from typing import AsyncGenerator

import pytest
import tiktoken

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gateway import UnifiedLLMGateway
from schemas import StreamChunk


async def fake_openai_stream(
    prompt: str,
    model: str,
    temperature: float,
) -> AsyncGenerator[StreamChunk, None]:
    yield StreamChunk(
        delta_text="Hello",
        provider="openai",
        model=model,
        is_final=False,
    )

    yield StreamChunk(
        delta_text=" world",
        provider="openai",
        model=model,
        is_final=False,
    )

    gateway = UnifiedLLMGateway()

    yield gateway._build_final_chunk(
        provider="openai",
        model=model,
        input_tokens=10,
        output_tokens=20,
        start_time=time.perf_counter() - 2,
        first_token_time=time.perf_counter() - 1,
    )


async def fake_anthropic_stream(
    prompt: str,
    model: str,
    temperature: float,
) -> AsyncGenerator[StreamChunk, None]:
    yield StreamChunk(
        delta_text="Hello",
        provider="anthropic",
        model=model,
        is_final=False,
    )

    yield StreamChunk(
        delta_text=" world",
        provider="anthropic",
        model=model,
        is_final=False,
    )

    gateway = UnifiedLLMGateway()

    yield gateway._build_final_chunk(
        provider="anthropic",
        model=model,
        input_tokens=10,
        output_tokens=20,
        start_time=time.perf_counter() - 2,
        first_token_time=time.perf_counter() - 1,
    )


# Test 1A: Unified Stream Protocol for OpenAI - This test checks that OpenAI streaming returns valid StreamChunk objects and concatenates text chunks into the expected response.
@pytest.mark.asyncio
async def test_unified_stream_protocol_openai(monkeypatch):
    gateway = UnifiedLLMGateway()

    monkeypatch.setattr(
        gateway,
        "_stream_openai",
        fake_openai_stream,
    )

    chunks = []

    async for chunk in gateway.stream(
        prompt="Say hello.",
        model="gpt-4o-mini",
        temperature=0.7,
    ):
        chunks.append(chunk)

    response_text = "".join(
        chunk.delta_text for chunk in chunks if not chunk.is_final
    )

    final_chunk = chunks[-1]

    assert all(isinstance(chunk, StreamChunk) for chunk in chunks)
    assert response_text == "Hello world"
    assert final_chunk.is_final is True
    assert final_chunk.telemetry is not None


# Test 1B: Unified Stream Protocol for Anthropic - This test checks that Anthropic streaming also returns valid StreamChunk objects and uses the same normalized output format as OpenAI.
@pytest.mark.asyncio
async def test_unified_stream_protocol_anthropic(monkeypatch):
    gateway = UnifiedLLMGateway()

    monkeypatch.setattr(
        gateway,
        "_stream_anthropic",
        fake_anthropic_stream,
    )

    chunks = []

    async for chunk in gateway.stream(
        prompt="Say hello.",
        model="claude-3-5-haiku",
        temperature=0.7,
    ):
        chunks.append(chunk)

    response_text = "".join(
        chunk.delta_text for chunk in chunks if not chunk.is_final
    )

    final_chunk = chunks[-1]

    assert all(isinstance(chunk, StreamChunk) for chunk in chunks)
    assert response_text == "Hello world"
    assert final_chunk.is_final is True
    assert final_chunk.telemetry is not None


# Test 2: Token Count Validation - This test checks that a deterministic 50-word prompt token count matches a direct tiktoken calculation within plus/minus 10%.
def test_token_count_validation_within_ten_percent():
    gateway = UnifiedLLMGateway()

    prompt_words = [
        "alpha", "bravo", "charlie", "delta", "echo",
        "foxtrot", "golf", "hotel", "india", "juliet",
        "kilo", "lima", "mike", "november", "oscar",
        "papa", "quebec", "romeo", "sierra", "tango",
        "uniform", "victor", "whiskey", "xray", "yankee",
        "zulu", "apple", "banana", "camera", "dragon",
        "engine", "forest", "garden", "harbor", "island",
        "jungle", "kitten", "lemon", "mountain", "number",
        "orange", "planet", "quiet", "river", "silver",
        "turtle", "umbrella", "valley", "window", "yellow",
    ]

    prompt = " ".join(prompt_words)

    recorded_prompt_tokens = gateway._count_openai_prompt_tokens(
        model="gpt-4o-mini",
        prompt=prompt,
    )

    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    expected_prompt_tokens = len(encoding.encode(prompt))

    difference = abs(recorded_prompt_tokens - expected_prompt_tokens)
    tolerance = expected_prompt_tokens * 0.10

    assert difference <= tolerance


# Test 3: Telemetry Sanity - This test checks that the final chunk contains telemetry where total_cost_usd, tokens_per_second, and ttft_ms are all greater than 0.
def test_telemetry_sanity_when_final_chunk_is_true():
    gateway = UnifiedLLMGateway()

    final_chunk = gateway._build_final_chunk(
        provider="openai",
        model="gpt-4o-mini",
        input_tokens=100,
        output_tokens=50,
        start_time=time.perf_counter() - 2,
        first_token_time=time.perf_counter() - 1,
    )

    telemetry = final_chunk.telemetry

    assert final_chunk.is_final is True
    assert telemetry is not None
    assert telemetry.total_cost_usd > 0
    assert telemetry.tokens_per_second > 0
    assert telemetry.ttft_ms > 0