import re
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class LineItem(BaseModel):
    description: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    line_total: float = Field(ge=0)


class InvoiceExtraction(BaseModel):
    invoice_number: str
    vendor_name: str
    invoice_date: date
    line_items: list[LineItem]

    subtotal: float = Field(ge=0)
    tax_amount: float = Field(ge=0)
    total_amount: float = Field(ge=0)

    currency: Literal["USD", "EUR", "GBP"]

    # Clean and validate invoice number and vendor name
    @field_validator("invoice_number", "vendor_name")
    @classmethod
    def must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field cannot be empty")

        return value.strip()

    # Convert common human-readable dates before Pydantic validates them
    @field_validator("invoice_date", mode="before")
    @classmethod
    def parse_invoice_date(cls, value):
        if not isinstance(value, str):
            return value

        # Example:
        # "12th of Oct, 2024" -> "12 of Oct, 2024"
        cleaned = re.sub(
            r"(\d+)(st|nd|rd|th)",
            r"\1",
            value.strip(),
        )

        formats = [
            "%Y-%m-%d",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
            "%d of %B, %Y",
            "%d of %b, %Y",
        ]

        for date_format in formats:
            try:
                return datetime.strptime(
                    cleaned,
                    date_format,
                ).date()

            except ValueError:
                continue

        # Let Pydantic perform its normal validation if
        # none of our custom formats worked.
        return value

    # Check relationships between invoice fields
    @model_validator(mode="after")
    def validate_totals(self):
        calculated_subtotal = sum(
            item.line_total
            for item in self.line_items
        )

        # Check line items against subtotal
        if abs(calculated_subtotal - self.subtotal) > 0.02:
            raise ValueError(
                "Line item totals must match subtotal "
                "within a 0.02 tolerance"
            )

        calculated_total = (
            calculated_subtotal
            + self.tax_amount
        )

        # Check subtotal + tax against final total
        if abs(calculated_total - self.total_amount) > 0.02:
            raise ValueError(
                "Subtotal plus tax must match total_amount "
                "within a 0.02 tolerance"
            )

        return self


class ExtractionResult(BaseModel):
    validated_data: Optional[InvoiceExtraction] = None
    attempts_used: int
    error_log: list[str]
    corrective_prompts: list[str] = Field(default_factory=list)

    execution_status: Literal[
        "SUCCESS",
        "REPAIRED_VIA_REFLECTION",
        "DLQ_FAILED",
    ]
