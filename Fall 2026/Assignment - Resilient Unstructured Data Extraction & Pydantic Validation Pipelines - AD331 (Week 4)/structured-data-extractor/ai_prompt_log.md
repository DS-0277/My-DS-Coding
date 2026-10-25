# AI Prompt Log

## Initial Prompt

You are a Staff AI Systems Engineer specializing in reliable programmatic LLM integration.

I need an automated, fault-tolerant unstructured data extractor in Python 3.11+ that parses raw PDF text or HTML documents into strictly validated Pydantic v2 models.

### Core Requirements

#### Data Model
Use the existing Pydantic v2 models from `src/schemas.py`:
- `LineItem`
- `InvoiceExtraction`

#### Extraction Engine (`src/extractor.py`)
- Accept raw document text.
- Use the OpenAI async client with structured output.
- Convert the LLM response into `InvoiceExtraction`.
- Implement:

`extract_with_retry(raw_text: str, max_retries: int = 3)`

The extraction process should:

1. Attempt normal structured extraction.
2. Catch Pydantic validation errors.
3. Send validation errors back to the LLM for correction.
4. Retry up to the maximum retry count.
5. If all attempts fail, use a fallback/DLQ mechanism.

#### Fallback (`src/fallback.py`)
- Store validation errors.
- Attempt JSON repair when appropriate.
- Save irrecoverable failed payloads into a Dead-Letter Queue (DLQ).

#### Result Metadata
Return an ExtractionResult containing:
- validated_data
- attempts_used
- error_log
- execution_status

Valid execution statuses:
- SUCCESS
- REPAIRED_VIA_REFLECTION
- DLQ_FAILED

Use Python 3.11+, Pydantic v2, async OpenAI calls, and clear beginner-friendly code.




# Audit & Verify the AI Output

## Audit 1: Pydantic v1 vs. v2 Syntax Collisions - in schema.py, we use v2 because '@field_validator'
## Audit 2: Context Stuffing / Token Bloat - The reflection retry prompt included the entire `raw_text` document on every retry. As for the risk, large PDFs would repeatedly consume unnecessary tokens, increase latency and increase API cost. As for the fix, we limit the retry context to a relevant snippet instead of resending the entire document.
## Audit 3: Loss of deterministic schema enforcement - The generated code does not reliably preserve the malformed LLM payload when validation fails. The `previous_payload` value is only updated after a successful validated extraction, so on a failed first attempt it can be empty. As a result, the reflection prompt and `json_repair` fallback may not receive the original malformed JSON. The required fix is to capture the raw model response separately before validation, then pass that raw payload to the reflection prompt and `json_repair`. After repairing JSON syntax, validate the repaired payload again with `InvoiceExtraction`. If validation still fails, route the record to the DLQ.
## Audit 4: Date and type coercion fragility - The initial schema relied only on Pydantic's default `date` parsing. As for the risk, non-standard dates such as `12th of Oct, 2024` may fail validation. As for the fix, we add a `mode="before"` field validator that normalizes or parses common date formats before Pydantic performs final type validation.
