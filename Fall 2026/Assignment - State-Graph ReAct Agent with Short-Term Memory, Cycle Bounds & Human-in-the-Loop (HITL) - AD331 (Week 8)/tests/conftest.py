"""Shared deterministic model doubles for graph tests."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage


class ScriptedModel:
    """A minimal model double that returns predefined AI messages in order."""

    def __init__(self, responses: list[AIMessage]) -> None:
        self.responses = responses.copy()
        self.invocations: list[list[Any]] = []

    def bind_tools(self, _tools: list[Any]) -> "ScriptedModel":
        return self

    def invoke(self, messages: list[Any]) -> AIMessage:
        self.invocations.append(messages)
        if not self.responses:
            raise AssertionError("The graph requested more model responses than expected.")
        return self.responses.pop(0)


def tool_call_message(name: str, args: dict[str, Any], call_id: str) -> AIMessage:
    """Create one structured model tool-call response."""
    return AIMessage(
        content="",
        tool_calls=[{"name": name, "args": args, "id": call_id, "type": "tool_call"}],
    )
