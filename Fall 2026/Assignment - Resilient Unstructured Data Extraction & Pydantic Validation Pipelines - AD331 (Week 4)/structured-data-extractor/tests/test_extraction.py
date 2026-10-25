from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError
from pypdf import PdfReader

from src import extractor
from src.schemas import InvoiceExtraction, LineItem


def valid_invoice() -> InvoiceExtraction:
    """Return a known-good invoice used by the unit tests."""
    return InvoiceExtraction(
        invoice_number="INV-2024-10-17-A",
        vendor_name="Northstar Office Supply Co.",
        invoice_date=date(2024, 10, 12),
        line_items=[
            LineItem(
                description="Desk chair",
                quantity=2,
                unit_price=399.00,
                line_total=798.00,
            ),
            LineItem(
                description="Docking station",
                quantity=3,
                unit_price=89.50,
                line_total=241.65,
            ),
            LineItem(
                description="Installation",
                quantity=1,
                unit_price=95.00,
                line_total=95.00,
            ),
        ],
        subtotal=1134.65,
        tax_amount=114.85,
        total_amount=1249.50,
        currency="USD",
    )


@pytest.mark.asyncio
async def test_golden_pdf_extracts_on_first_attempt(monkeypatch):
    """A readable sample PDF should produce a successful first attempt."""
    sample_path = Path("samples/invoice_messy.pdf")
    raw_text = PdfReader(sample_path).pages[0].extract_text()

    async def fake_extract(raw_text: str) -> InvoiceExtraction:
        assert "INV-2024-10-17-A" in raw_text
        return valid_invoice()

    monkeypatch.setattr(extractor, "extract_invoice", fake_extract)

    result = await extractor.extract_with_retry(raw_text)

    assert result.execution_status == "SUCCESS"
    assert result.attempts_used == 1
    assert result.error_log == []
    assert result.validated_data == valid_invoice()


def test_schema_rejects_invalid_quantity_and_negative_total():
    """Field constraints prevent invalid quantities and monetary totals."""
    with pytest.raises(ValidationError):
        LineItem(
            description="Invalid item",
            quantity=0,
            unit_price=10.00,
            line_total=0.00,
        )

    invoice_data = valid_invoice().model_dump()
    invoice_data["total_amount"] = -1.00

    with pytest.raises(ValidationError):
        InvoiceExtraction.model_validate(invoice_data)


def test_schema_rejects_unreconciled_totals():
    """The cross-field validator rejects totals that do not add up."""
    invoice_data = valid_invoice().model_dump()
    invoice_data["total_amount"] = 1200.00

    with pytest.raises(ValidationError, match="Subtotal plus tax"):
        InvoiceExtraction.model_validate(invoice_data)
