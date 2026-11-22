"""The explicit LangGraph workflow for the operations ReAct agent."""

from __future__ import annotations

import os
from typing import Any, Literal, Optional

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from .circuit_breaker import MAX_ITERATIONS, is_consecutive_repeat, tool_call_fingerprint
from .state import AgentState
from .tools import TOOL_BY_NAME, TOOLS, is_sensitive


SYSTEM_PROMPT = """You are an internal cloud and financial operations assistant.
Use tools when they are useful. Treat tool output as the source of truth. If a
tool action was rejected by a human operator, clearly explain that it was
cancelled and do not request the same action again."""


def create_model() -> BaseChatModel:
    """Create the OpenAI chat model used by the agent node."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            import streamlit as st

            api_key = st.secrets.get("OPENAI_API_KEY")
        except Exception:
            # Tests and local non-Streamlit imports do not need credentials.
            api_key = None
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        temperature=0,
        api_key=api_key,
    )


def _latest_tool_call(state: AgentState) -> dict[str, Any] | None:
    """Get the first tool call requested by the most recent model response."""
    if not state["messages"]:
        return None
    latest_message = state["messages"][-1]
    calls = getattr(latest_message, "tool_calls", [])
    return calls[0] if calls else None


def build_graph(
    *,
    model: Optional[BaseChatModel] = None,
    checkpointer: Optional[MemorySaver] = None,
):
    """Build a checkpointed graph; tests may provide a deterministic model."""
    bound_model = (model or create_model()).bind_tools(TOOLS)

    def agent_node(state: AgentState) -> dict[str, Any]:
        """Ask the model for the next answer or structured tool request."""
        response = bound_model.invoke([SystemMessage(content=SYSTEM_PROMPT), *state["messages"]])
        return {
            "messages": [response],
            "iteration_count": state.get("iteration_count", 0) + 1,
            "execution_log": [*state.get("execution_log", []), "agent_node"],
        }

    def circuit_breaker_node(state: AgentState) -> dict[str, Any]:
        """Reject unknown, repeated, or over-budget tool requests."""
        call = _latest_tool_call(state)
        if call is None:
            return {"error": "No tool call was available for safety checking."}

        tool_name = call["name"]
        arguments = call.get("args", {})
        fingerprint = tool_call_fingerprint(tool_name, arguments)
        history = state.get("executed_tool_hashes", [])
        rejected_history = state.get("rejected_tool_hashes", [])

        if state.get("iteration_count", 0) >= MAX_ITERATIONS:
            return {
                "error": f"Maximum iteration limit ({MAX_ITERATIONS}) reached.",
                "execution_log": [*state.get("execution_log", []), "circuit_breaker:max_iterations"],
            }
        if tool_name not in TOOL_BY_NAME:
            return {
                "error": f"Unknown tool requested: {tool_name}",
                "execution_log": [*state.get("execution_log", []), "circuit_breaker:unknown_tool"],
            }
        if is_consecutive_repeat(history, fingerprint):
            return {
                "error": "Repeated tool call detected; execution stopped safely.",
                "execution_log": [*state.get("execution_log", []), "circuit_breaker:repeat"],
            }
        if fingerprint in rejected_history:
            return {
                "error": "This sensitive action was already rejected by the human operator.",
                "execution_log": [*state.get("execution_log", []), "circuit_breaker:rejected_action"],
            }

        return {
            "pending_tool_call": call,
            "executed_tool_hashes": [*history, fingerprint],
            "execution_log": [*state.get("execution_log", []), "circuit_breaker:passed"],
            "error": None,
        }

    def human_approval_gate(state: AgentState) -> dict[str, Any]:
        """Persist and pause until an operator approves or rejects the action."""
        call = state["pending_tool_call"]
        approval_ticket = {
            "tool_name": call["name"],
            "arguments": call.get("args", {}),
            "risk": "HIGH",
        }
        decision = interrupt(approval_ticket)
        approved = isinstance(decision, dict) and decision.get("approved") is True
        return {
            "pending_approval": approval_ticket,
            "approval_status": "APPROVED" if approved else "REJECTED",
            "execution_log": [*state.get("execution_log", []), "human_approval_gate:resumed"],
        }

    def tool_executor_node(state: AgentState) -> dict[str, Any]:
        """Run a previously approved/local-safe tool and preserve its result."""
        call = state["pending_tool_call"]
        tool = TOOL_BY_NAME[call["name"]]
        try:
            result = tool.invoke(call.get("args", {}))
            content = str(result)
        except Exception as exc:  # Tool failures become context for the model.
            content = f"Tool execution error: {exc}"
        return {
            "messages": [
                ToolMessage(
                    content=content,
                    tool_call_id=call["id"],
                    name=call["name"],
                )
            ],
            "pending_tool_call": None,
            "pending_approval": None,
            "execution_log": [*state.get("execution_log", []), f"tool_executor:{call['name']}"],
        }

    def rejection_recovery_node(state: AgentState) -> dict[str, Any]:
        """Tell the model that the requested sensitive action was denied."""
        call = state["pending_tool_call"]
        rejected_fingerprint = tool_call_fingerprint(call["name"], call.get("args", {}))
        return {
            "messages": [
                ToolMessage(
                    content=(
                        "The human operator rejected this action. Do not request the "
                        "same action again; explain the cancellation or offer a safe alternative."
                    ),
                    tool_call_id=call["id"],
                    name=call["name"],
                )
            ],
            "pending_tool_call": None,
            "pending_approval": None,
            "rejected_tool_hashes": [
                *state.get("rejected_tool_hashes", []),
                rejected_fingerprint,
            ],
            "execution_log": [*state.get("execution_log", []), "rejection_recovery"],
        }

    def error_node(state: AgentState) -> dict[str, Any]:
        """End gracefully after a safety circuit breaker trip."""
        return {
            "messages": [AIMessage(content=f"Execution stopped safely: {state.get('error', 'unknown error')}")],
            "execution_log": [*state.get("execution_log", []), "error_node"],
        }

    def after_agent(state: AgentState) -> Literal["circuit_breaker", "end"]:
        return "circuit_breaker" if _latest_tool_call(state) else "end"

    def after_circuit_breaker(state: AgentState) -> Literal["tool_executor", "human_approval", "error"]:
        if state.get("error"):
            return "error"
        call = state["pending_tool_call"]
        return "human_approval" if is_sensitive(call["name"]) else "tool_executor"

    def after_approval(state: AgentState) -> Literal["tool_executor", "rejection_recovery"]:
        return "tool_executor" if state.get("approval_status") == "APPROVED" else "rejection_recovery"

    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("circuit_breaker", circuit_breaker_node)
    builder.add_node("human_approval", human_approval_gate)
    builder.add_node("tool_executor", tool_executor_node)
    builder.add_node("rejection_recovery", rejection_recovery_node)
    builder.add_node("error", error_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", after_agent, {"circuit_breaker": "circuit_breaker", "end": END})
    builder.add_conditional_edges(
        "circuit_breaker",
        after_circuit_breaker,
        {"tool_executor": "tool_executor", "human_approval": "human_approval", "error": "error"},
    )
    builder.add_conditional_edges(
        "human_approval",
        after_approval,
        {"tool_executor": "tool_executor", "rejection_recovery": "rejection_recovery"},
    )
    builder.add_edge("tool_executor", "agent")
    builder.add_edge("rejection_recovery", "agent")
    builder.add_edge("error", END)

    return builder.compile(checkpointer=checkpointer or MemorySaver())


_default_graph = None


def get_graph():
    """Create the default API-backed graph only when the app needs it.

    Keeping this lazy lets the deterministic test suite import ``build_graph``
    without requiring a real OpenAI API key.
    """
    global _default_graph
    if _default_graph is None:
        _default_graph = build_graph()
    return _default_graph
