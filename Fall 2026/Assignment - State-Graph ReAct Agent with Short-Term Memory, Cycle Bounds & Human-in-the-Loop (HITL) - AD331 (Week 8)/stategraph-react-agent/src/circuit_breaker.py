"""Loop containment helpers for tool-calling agents."""

from __future__ import annotations

import hashlib
import json
from typing import Any


MAX_ITERATIONS = 6


def tool_call_fingerprint(tool_name: str, arguments: dict[str, Any]) -> str:
    """Create a stable SHA-256 fingerprint for a tool name and its arguments.

    Sorting JSON keys prevents equivalent dictionaries with different key order
    from producing different fingerprints.
    """
    normalized_payload = json.dumps(
        {"tool_name": tool_name, "arguments": arguments},
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(normalized_payload.encode("utf-8")).hexdigest()


def is_consecutive_repeat(history: list[str], candidate: str) -> bool:
    """Return True only when the immediate prior tool call is identical."""
    return bool(history) and history[-1] == candidate
