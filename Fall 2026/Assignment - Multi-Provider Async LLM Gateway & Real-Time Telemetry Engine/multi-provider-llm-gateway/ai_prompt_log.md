# AI Prompt and Code Audit Log

## Step 2: Initial AI Code Generation

AI Assistant Used: ChatGPT  
Date: October 9, 2026  

### Initial Prompt

You are an expert Python AI Infrastructure Engineer. I need an asynchronous, streaming multi-provider SDK wrapper supporting both OpenAI (e.g., gpt-4o-mini, gpt-4o) and Anthropic (e.g., claude-3-5-sonnet, claude-3-5-haiku).

Requirements:

1. Environment: Python 3.11+, typed with Pydantic v2.
2. Architecture:
   - A unified class `UnifiedLLMGateway` with an async generator method:
     `async def stream(self, prompt: str, model: str, temperature: float = 0.7) -> AsyncGenerator[StreamChunk, None]:`
   - Use official async clients (`AsyncOpenAI` and `AsyncAnthropic`).

3. Normalization:
   - Define a Pydantic schema `StreamChunk` containing:
     - `delta_text: str`
     - `provider: str`
     - `model: str`
     - `is_final: bool`
     - `telemetry: Optional[ChunkTelemetry]`
   - Normalize streaming events so that differences in chunk structure between OpenAI and Anthropic are completely hidden from the consumer.

4. Token & Cost Telemetry:
   - Include a static pricing dictionary with USD rates per 1,000,000 input and output tokens for supported models.
   - For OpenAI: enable stream usage tracking (`stream_options={"include_usage": True}`) and use tiktoken for prompt token verification.
   - For Anthropic: capture `message_start` for input tokens and accumulate output tokens from stream events.
   - On the final chunk (`is_final=True`), provide exact input tokens, output tokens, total latency seconds, Time-to-First-Token, tokens per second, and calculated total request cost.

5. Error Handling:
   - Handle rate limits, invalid API keys, and connection errors by raising typed, custom domain exceptions.
   - Do not leak raw API keys or unhandled stack traces in logs or outputs.

Provide clean, production-ready code split into `schemas.py`, `pricing.py`, and `gateway.py`.

### Generated Files

- `src/schemas.py`
- `src/pricing.py`
- `src/gateway.py`

### Notes

This is the initial AI-generated draft. It will be manually audited in Step 3 before being treated as final implementation.


## Step 3: Manual Code Audit

### Audit Item 1: Async Event Loop Blocking

The initial AI draft correctly used `AsyncOpenAI` and `AsyncAnthropic` instead of synchronous clients such as `openai.OpenAI()`. The streaming methods are implemented as async generators and use `async for` to consume provider streams.

I did not find blocking `time.sleep()` calls or synchronous provider SDK calls inside the async streaming methods.

Result: Passed. No remediation required for this item.

### Audit Item 2A: OpenAI Streaming Delta Parsing

The assignment warns that OpenAI may send a final usage chunk with an empty `choices` array or with `choice.delta.content` equal to `None`.

The initial AI draft already checks for empty choices before accessing `event.choices[0]`:

```python
if not event.choices:
    continue
```
### Audit Item 2B: Anthropic Streaming Event Types

The initial AI draft handled `message_start`, `content_block_delta`, and `message_delta`, but it did not explicitly handle `message_stop`.

Although the code may not crash without this branch, the assignment specifically asks us to inspect Anthropic event stream types, including `message_stop`.

Before:

```python
elif event.type == "message_delta":
    output_tokens = event.usage.output_tokens
```

After:

```python
elif event.type == "message_delta":
    output_tokens = event.usage.output_tokens

elif event.type == "message_stop":
    pass
```

### Audit Item 3A: Time-to-First-Token Calculation

The assignment asks whether TTFT is computed only when the first non-empty text delta arrives.

The initial AI draft records `first_token_time` only after confirming that the provider returned a non-empty text delta.

For OpenAI and Anthropic, the draft checks:

```python
if not delta:
    continue
```
### Audit Item 3B: Cost Calculation and Fractional Cents

The initial AI draft used `Decimal` for token pricing calculations, which avoids common floating-point rounding issues.

Before:

```python
return float(rounded_cost)
```

After:

```python
return round(float(rounded_cost), 6)
```
### Audit Item 4: Client Instantiation Anti-Pattern

The assignment warns against creating provider clients inside every function call.

The initial AI draft avoids this anti-pattern by storing clients on the `UnifiedLLMGateway` instance:

```python
self.openai_client = None
self.anthropic_client = None
```