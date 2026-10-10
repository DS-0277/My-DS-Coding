from decimal import Decimal, ROUND_HALF_UP


PRICING_PER_MILLION_TOKENS = {
    "gpt-4o-mini": {
        "provider": "openai",
        "input": Decimal("0.15"),
        "output": Decimal("0.60"),
    },
    "gpt-4o": {
        "provider": "openai",
        "input": Decimal("2.50"),
        "output": Decimal("10.00"),
    },
    "claude-3-5-haiku": {
        "provider": "anthropic",
        "input": Decimal("0.80"),
        "output": Decimal("4.00"),
    },
    "claude-3-5-sonnet": {
        "provider": "anthropic",
        "input": Decimal("3.00"),
        "output": Decimal("15.00"),
    },
}


def get_provider_for_model(model: str) -> str:
    if model not in PRICING_PER_MILLION_TOKENS:
        raise ValueError(f"Unsupported model: {model}")

    return PRICING_PER_MILLION_TOKENS[model]["provider"]


def calculate_cost_usd(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> float:
    if model not in PRICING_PER_MILLION_TOKENS:
        raise ValueError(f"Unsupported model: {model}")

    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("Token counts cannot be negative.")

    pricing = PRICING_PER_MILLION_TOKENS[model]

    input_cost = (
        Decimal(input_tokens) * pricing["input"]
    ) / Decimal("1000000")

    output_cost = (
        Decimal(output_tokens) * pricing["output"]
    ) / Decimal("1000000")

    total_cost = input_cost + output_cost

    rounded_cost = total_cost.quantize(
        Decimal("0.000001"),
        rounding=ROUND_HALF_UP,
    )

    return round(float(rounded_cost), 6)