import json
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import ValidationError

try:
    from .fallback import save_to_dlq, try_repair_and_validate
    from .schemas import ExtractionResult, InvoiceExtraction
except ImportError:
    from fallback import save_to_dlq, try_repair_and_validate
    from schemas import ExtractionResult, InvoiceExtraction


load_dotenv()


def get_client() -> AsyncOpenAI:
    """Create an API client only when an extraction request is made."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "Missing OPENAI_API_KEY. Add it to your .env file."
        )

    return AsyncOpenAI(api_key=api_key)


async def extract_invoice(
    raw_text: str,
) -> InvoiceExtraction:
    """
    Perform the first structured invoice extraction.
    """
    client = get_client()

    response = await client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Extract invoice information "
                    "from the provided document. "
                    "Return only information that "
                    "is supported by the document."
                ),
            },
            {
                "role": "user",
                "content": raw_text,
            },
        ],
        text_format=InvoiceExtraction,
    )

    if response.output_parsed is None:
        raise ValueError(
            "The model did not return "
            "a parsed invoice."
        )

    return response.output_parsed


async def repair_invoice(
    raw_text: str,
    previous_payload: str,
    validation_error: str,
) -> InvoiceExtraction:
    """
    Ask the LLM to repair an extraction that
    previously failed validation.
    """
    client = get_client()

    # Avoid sending a huge document again on
    # every reflection attempt.
    context_snippet = raw_text[:6000]

    repair_prompt = build_repair_prompt(
        raw_text=raw_text,
        previous_payload=previous_payload,
        validation_error=validation_error,
    )

    response = await client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You repair invalid structured "
                    "invoice extractions."
                ),
            },
            {
                "role": "user",
                "content": repair_prompt,
            },
        ],
        text_format=InvoiceExtraction,
    )

    if response.output_parsed is None:
        raise ValueError(
            "The model did not return "
            "a repaired invoice."
        )

    return response.output_parsed


def build_repair_prompt(
    raw_text: str,
    previous_payload: str,
    validation_error: str,
) -> str:
    """Build the bounded corrective prompt shown in the UI audit log."""
    context_snippet = raw_text[:6000]

    return f"""
The previous invoice extraction failed validation.

Relevant document context:
{context_snippet}

Previous output:
{previous_payload}

Validation error:
{validation_error}

Correct the invalid invoice fields.

Do not invent information that is not supported
by the original document.
"""


async def extract_with_retry(
    raw_text: str,
    max_retries: int = 3,
    simulate_failure: bool = False,
) -> ExtractionResult:
    """
    Run extraction with validation,
    reflection retries, fallback repair,
    and DLQ routing.
    """

    errors: list[str] = []
    corrective_prompts: list[str] = []

    previous_payload = ""

    for attempt in range(
        1,
        max_retries + 1,
    ):

        try:
            if simulate_failure:
                raise ValueError(
                    "Simulated edge-case failure: "
                    "no invoice data is available."
                )

            # First attempt = normal extraction
            if attempt == 1:
                invoice = await extract_invoice(
                    raw_text
                )

            # Later attempts = reflection repair
            else:
                corrective_prompts.append(
                    build_repair_prompt(
                        raw_text=raw_text,
                        previous_payload=previous_payload,
                        validation_error=errors[-1],
                    )
                )
                invoice = await repair_invoice(
                    raw_text=raw_text,
                    previous_payload=previous_payload,
                    validation_error=errors[-1],
                )

            # Store the successfully parsed invoice
            # as JSON so it is available for logging.
            previous_payload = json.dumps(
                invoice.model_dump(
                    mode="json"
                )
            )

            if attempt == 1:
                status = "SUCCESS"
            else:
                status = (
                    "REPAIRED_VIA_REFLECTION"
                )

            return ExtractionResult(
                validated_data=invoice,
                attempts_used=attempt,
                error_log=errors,
                corrective_prompts=corrective_prompts,
                execution_status=status,
            )

        except (
            ValidationError,
            ValueError,
        ) as error:

            error_message = str(error)

            errors.append(
                error_message
            )

    # Stage 3:
    # Try heuristic JSON repair after
    # reflection attempts have failed.
    repaired_invoice = (
        try_repair_and_validate(
            previous_payload
        )
    )

    if repaired_invoice is not None:
        return ExtractionResult(
            validated_data=repaired_invoice,
            attempts_used=max_retries,
            error_log=errors,
            corrective_prompts=corrective_prompts,
            execution_status=(
                "REPAIRED_VIA_REFLECTION"
            ),
        )

    # Nothing worked -> DLQ
    save_to_dlq(
        raw_text=raw_text,
        failed_payload=previous_payload,
        errors=errors,
    )

    return ExtractionResult(
        validated_data=None,
        attempts_used=max_retries,
        error_log=errors,
        corrective_prompts=corrective_prompts,
        execution_status="DLQ_FAILED",
    )
