import json

import pytest

from src import extractor
from src import fallback
from src.schemas import InvoiceExtraction
from tests.test_extraction import valid_invoice


@pytest.mark.asyncio
async def test_reflection_loop_succeeds_on_second_attempt(monkeypatch):
    """A failed first response should be repaired by a second attempt."""
    calls = {"extract": 0, "repair": 0}

    async def fake_extract(raw_text: str) -> InvoiceExtraction:
        calls["extract"] += 1
        raise ValueError("currency: Field required")

    async def fake_repair(
        raw_text: str,
        previous_payload: str,
        validation_error: str,
    ) -> InvoiceExtraction:
        calls["repair"] += 1
        assert "currency" in validation_error
        return valid_invoice()

    monkeypatch.setattr(extractor, "extract_invoice", fake_extract)
    monkeypatch.setattr(extractor, "repair_invoice", fake_repair)

    result = await extractor.extract_with_retry("invoice text", max_retries=3)

    assert calls == {"extract": 1, "repair": 1}
    assert result.execution_status == "REPAIRED_VIA_REFLECTION"
    assert result.attempts_used == 2
    assert result.validated_data == valid_invoice()
    assert len(result.corrective_prompts) == 1


@pytest.mark.asyncio
async def test_irrecoverable_input_routes_to_dlq(monkeypatch, tmp_path):
    """An unrecoverable input must finish safely in the DLQ after retries."""
    async def always_fail_extract(raw_text: str) -> InvoiceExtraction:
        raise ValueError("No invoice fields found")

    async def always_fail_repair(
        raw_text: str,
        previous_payload: str,
        validation_error: str,
    ) -> InvoiceExtraction:
        raise ValueError("Still not a valid invoice")

    def fake_repair_json(payload: str):
        return None

    monkeypatch.setattr(extractor, "extract_invoice", always_fail_extract)
    monkeypatch.setattr(extractor, "repair_invoice", always_fail_repair)
    monkeypatch.setattr(extractor, "try_repair_and_validate", fake_repair_json)
    monkeypatch.setattr(fallback, "DLQ_DIR", tmp_path / "dlq")

    result = await extractor.extract_with_retry("total nonsense text", max_retries=3)

    assert result.execution_status == "DLQ_FAILED"
    assert result.attempts_used == 3
    assert result.validated_data is None
    assert len(result.error_log) == 3

    dlq_log = fallback.DLQ_DIR / "failed_extractions.jsonl"
    assert dlq_log.exists()
    saved_record = json.loads(dlq_log.read_text().strip())
    assert saved_record["raw_text"] == "total nonsense text"
