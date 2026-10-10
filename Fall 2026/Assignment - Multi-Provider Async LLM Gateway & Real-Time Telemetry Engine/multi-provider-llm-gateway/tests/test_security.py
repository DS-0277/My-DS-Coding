import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gateway import (
    GatewayAuthenticationError,
    GatewayProviderError,
    UnifiedLLMGateway,
)


# Test 4A: Missing OpenAI Key Handling - This test checks that a missing OPENAI_API_KEY raises a descriptive GatewayAuthenticationError instead of crashing.
def test_missing_openai_key_handling(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    gateway = UnifiedLLMGateway()

    with pytest.raises(GatewayAuthenticationError) as error:
        gateway.get_openai_client()

    assert "Missing OpenAI API key" in str(error.value)


# Test 4B: Missing Anthropic Key Handling - This test checks that a missing ANTHROPIC_API_KEY raises a descriptive GatewayAuthenticationError instead of crashing.
def test_missing_anthropic_key_handling(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    gateway = UnifiedLLMGateway()

    with pytest.raises(GatewayAuthenticationError) as error:
        gateway.get_anthropic_client()

    assert "Missing Anthropic API key" in str(error.value)


# Test 5: Secret Redaction - This test checks that gateway error messages do not expose raw API key substrings.
def test_secret_redaction():
    fake_api_key = "sk-test-secret-key-123456"

    error = GatewayProviderError(
        "OpenAI request failed."
    )

    error_message = str(error)

    assert fake_api_key not in error_message
    assert "sk-test" not in error_message
    assert "secret-key" not in error_message