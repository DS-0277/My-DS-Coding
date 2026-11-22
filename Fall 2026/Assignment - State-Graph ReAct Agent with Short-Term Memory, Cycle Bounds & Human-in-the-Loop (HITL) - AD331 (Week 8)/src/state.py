"""The shared, checkpointed data used by every LangGraph node."""

from __future__ import annotations

from typing import Any, Literal, NotRequired, Optional
from typing_extensions import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """A single conversation's short-term memory and execution status."""

    messages: Annotated[list[AnyMessage], add_messages]
    iteration_count: int
    executed_tool_hashes: list[str]
    rejected_tool_hashes: NotRequired[list[str]]
    pending_tool_call: NotRequired[Optional[dict[str, Any]]]
    pending_approval: NotRequired[Optional[dict[str, Any]]]
    approval_status: NotRequired[Optional[Literal["APPROVED", "REJECTED"]]]
    execution_log: NotRequired[list[str]]
    error: NotRequired[Optional[str]]
