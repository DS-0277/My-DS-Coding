import os
import time
from typing import AsyncGenerator

import anthropic
import openai
import tiktoken
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from openai import AsyncOpenAI

from pricing import calculate_cost_usd, get_provider_for_model
from schemas import ChunkTelemetry, StreamChunk


load_dotenv()


class GatewayError(Exception):
    """Base exception for gateway errors."""


class GatewayAuthenticationError(GatewayError):
    """Raised when API authentication fails."""


class GatewayRateLimitError(GatewayError):
    """Raised when a provider rate limit is reached."""


class GatewayProviderError(GatewayError):
    """Raised when a provider request fails."""


class UnifiedLLMGateway:
    def __init__(self) -> None:
        self.openai_client: AsyncOpenAI | None = None
        self.anthropic_client: AsyncAnthropic | None = None

    def get_openai_client(self) -> AsyncOpenAI:
        if self.openai_client is None:
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise GatewayAuthenticationError(
                    "Missing OpenAI API key."
                )

            self.openai_client = AsyncOpenAI(api_key=api_key)

        return self.openai_client

    def get_anthropic_client(self) -> AsyncAnthropic:
        if self.anthropic_client is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")

            if not api_key:
                raise GatewayAuthenticationError(
                    "Missing Anthropic API key."
                )

            self.anthropic_client = AsyncAnthropic(api_key=api_key)

        return self.anthropic_client

    async def stream(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
    ) -> AsyncGenerator[StreamChunk, None]:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        if not 0 <= temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1.")

        provider = get_provider_for_model(model)

        if provider == "openai":
            async for chunk in self._stream_openai(
                prompt=prompt,
                model=model,
                temperature=temperature,
            ):
                yield chunk

        elif provider == "anthropic":
            async for chunk in self._stream_anthropic(
                prompt=prompt,
                model=model,
                temperature=temperature,
            ):
                yield chunk

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    async def _stream_openai(
        self,
        prompt: str,
        model: str,
        temperature: float,
    ) -> AsyncGenerator[StreamChunk, None]:
        client = self.get_openai_client()

        start_time = time.perf_counter()
        first_token_time: float | None = None

        input_tokens = self._count_openai_prompt_tokens(
            model=model,
            prompt=prompt,
        )
        output_tokens = 0

        try:
            stream = await client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=temperature,
                stream=True,
                stream_options={
                    "include_usage": True,
                },
            )

            async for event in stream:
                if event.usage is not None:
                    input_tokens = event.usage.prompt_tokens
                    output_tokens = event.usage.completion_tokens

                if not event.choices:
                    continue

                delta = event.choices[0].delta.content

                if not delta:
                    continue

                if first_token_time is None:
                    first_token_time = time.perf_counter()

                yield StreamChunk(
                    delta_text=delta,
                    provider="openai",
                    model=model,
                    is_final=False,
                )

        except openai.AuthenticationError:
            raise GatewayAuthenticationError(
                "Authentication failed for OpenAI."
            ) from None

        except openai.RateLimitError:
            raise GatewayRateLimitError(
                "Rate limit exceeded for OpenAI."
            ) from None

        except openai.APIConnectionError:
            raise GatewayProviderError(
                "Connection error while contacting OpenAI."
            ) from None

        except openai.APIError:
            raise GatewayProviderError(
                "OpenAI request failed."
            ) from None

        yield self._build_final_chunk(
            provider="openai",
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            start_time=start_time,
            first_token_time=first_token_time,
        )

    async def _stream_anthropic(
        self,
        prompt: str,
        model: str,
        temperature: float,
    ) -> AsyncGenerator[StreamChunk, None]:
        client = self.get_anthropic_client()

        start_time = time.perf_counter()
        first_token_time: float | None = None

        input_tokens = 0
        output_tokens = 0

        try:
            stream = await client.messages.create(
                model=model,
                max_tokens=1024,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                stream=True,
            )

            async for event in stream:
                if event.type == "message_start":
                    input_tokens = event.message.usage.input_tokens

                elif event.type == "content_block_delta":
                    if event.delta.type != "text_delta":
                        continue

                    delta = event.delta.text

                    if not delta:
                        continue

                    if first_token_time is None:
                        first_token_time = time.perf_counter()

                    yield StreamChunk(
                        delta_text=delta,
                        provider="anthropic",
                        model=model,
                        is_final=False,
                    )

                elif event.type == "message_delta":
                    output_tokens = event.usage.output_tokens

                elif event.type == "message_stop":
                    pass

        except anthropic.AuthenticationError:
            raise GatewayAuthenticationError(
                "Authentication failed for Anthropic."
            ) from None

        except anthropic.RateLimitError:
            raise GatewayRateLimitError(
                "Rate limit exceeded for Anthropic."
            ) from None

        except anthropic.APIConnectionError:
            raise GatewayProviderError(
                "Connection error while contacting Anthropic."
            ) from None

        except anthropic.APIError:
            raise GatewayProviderError(
                "Anthropic request failed."
            ) from None

        yield self._build_final_chunk(
            provider="anthropic",
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            start_time=start_time,
            first_token_time=first_token_time,
        )

    def _build_final_chunk(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        start_time: float,
        first_token_time: float | None,
    ) -> StreamChunk:
        end_time = time.perf_counter()
        total_latency_seconds = end_time - start_time

        if first_token_time is None:
            ttft_ms = 0.0
            generation_seconds = 0.0
        else:
            ttft_ms = (first_token_time - start_time) * 1000
            generation_seconds = end_time - first_token_time

        if generation_seconds > 0:
            tokens_per_second = output_tokens / generation_seconds
        else:
            tokens_per_second = 0.0

        total_cost_usd = calculate_cost_usd(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

        telemetry = ChunkTelemetry(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            total_latency_seconds=total_latency_seconds,
            ttft_ms=ttft_ms,
            tokens_per_second=tokens_per_second,
            total_cost_usd=total_cost_usd,
        )

        return StreamChunk(
            delta_text="",
            provider=provider,
            model=model,
            is_final=True,
            telemetry=telemetry,
        )

    def _count_openai_prompt_tokens(
        self,
        model: str,
        prompt: str,
    ) -> int:
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("o200k_base")

        return len(encoding.encode(prompt))