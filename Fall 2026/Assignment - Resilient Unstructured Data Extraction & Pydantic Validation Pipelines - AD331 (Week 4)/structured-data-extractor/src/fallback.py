import json
from datetime import datetime
from pathlib import Path

from json_repair import repair_json
from pydantic import ValidationError

try:
    from .schemas import InvoiceExtraction
except ImportError:
    from schemas import InvoiceExtraction


DLQ_DIR = Path("dlq")


def try_repair_and_validate(
    payload: str,
) -> InvoiceExtraction | None:
    """
    Try to repair malformed JSON and then validate
    the repaired data using Pydantic.
    """

    if not payload:
        return None

    try:
        # Step 1: Repair JSON syntax
        repaired_json = repair_json(payload)

        # Step 2: Convert JSON string into Python data
        repaired_data = json.loads(repaired_json)

        # Step 3: Validate using our Pydantic schema
        return InvoiceExtraction.model_validate(
            repaired_data
        )

    except (
        json.JSONDecodeError,
        ValidationError,
        TypeError,
        ValueError,
    ):
        return None


def save_to_dlq(
    raw_text: str,
    failed_payload: str,
    errors: list[str],
) -> None:
    """
    Save an extraction that could not be repaired
    into the Dead-Letter Queue.
    """

    DLQ_DIR.mkdir(exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "raw_text": raw_text,
        "failed_payload": failed_payload,
        "errors": errors,
    }

    file_path = (
        DLQ_DIR
        / "failed_extractions.jsonl"
    )

    with file_path.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            json.dumps(record)
            + "\n"
        )
