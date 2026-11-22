"""Streamlit control room for the State-Graph ReAct agent."""

from __future__ import annotations

import uuid
import sys
from pathlib import Path
from typing import Any

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.types import Command

# Streamlit executes this file as a script, so make the project root available
# before importing the ``src`` package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.circuit_breaker import is_consecutive_repeat, tool_call_fingerprint
from src.graph import get_graph


graph = get_graph()


st.set_page_config(page_title="StateGraph ReAct Agent", page_icon="🧭", layout="wide")


def graph_config(thread_id: str) -> dict[str, dict[str, str]]:
    """Build the per-session configuration required by MemorySaver."""
    return {"configurable": {"thread_id": thread_id}}


def snapshot_values(thread_id: str) -> tuple[dict[str, Any], Any]:
    """Return the persisted state snapshot for this UI session."""
    snapshot = graph.get_state(graph_config(thread_id))
    return dict(snapshot.values), snapshot


def active_node(snapshot: Any) -> str:
    """Format the graph node(s) awaiting execution or input."""
    waiting = list(getattr(snapshot, "next", ()) or ())
    if not waiting:
        return "DONE / READY"
    return " → ".join(node.upper() for node in waiting)


def pending_approval(values: dict[str, Any], snapshot: Any) -> dict[str, Any] | None:
    """Read an approval ticket from state or the dynamic interrupt payload."""
    if values.get("pending_approval"):
        return values["pending_approval"]

    for task in getattr(snapshot, "tasks", ()) or ():
        for pending_interrupt in getattr(task, "interrupts", ()) or ():
            value = getattr(pending_interrupt, "value", None)
            if isinstance(value, dict) and "tool_name" in value:
                return value
    return None


def display_messages(values: dict[str, Any]) -> None:
    """Render user and assistant conversation messages, excluding tool internals."""
    for message in values.get("messages", []):
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage) and message.content:
            with st.chat_message("assistant"):
                st.write(message.content)
        elif isinstance(message, ToolMessage):
            with st.expander("Tool result", expanded=False):
                st.code(str(message.content))


def run_prompt(thread_id: str, prompt: str) -> None:
    """Start or continue the graph with one new human message."""
    graph.invoke({"messages": [HumanMessage(content=prompt)]}, graph_config(thread_id))


def resume_approval(thread_id: str, approved: bool) -> None:
    """Resume the paused graph from its persisted approval checkpoint."""
    graph.invoke(Command(resume={"approved": approved}), graph_config(thread_id))


if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"session-{uuid.uuid4().hex[:8]}"

st.title("🧭 State-Graph ReAct Agent")
st.caption("A controlled operations assistant with short-term memory and human approval gates.")

with st.sidebar:
    st.header("Session console")
    thread_id = st.text_input("Session thread ID", key="thread_id")
    st.caption("Use a different ID for a separate conversation and checkpoint history.")

    if st.button("Start a new session", use_container_width=True):
        st.session_state.thread_id = f"session-{uuid.uuid4().hex[:8]}"
        st.rerun()

    st.divider()
    st.header("Circuit-breaker demo")
    repeat_demo = st.toggle("Show duplicate-call detection", value=False)
    if repeat_demo:
        args = {"service_name": "auth-service"}
        fingerprint = tool_call_fingerprint("query_service_metrics", args)
        tripped = is_consecutive_repeat([fingerprint], fingerprint)
        st.warning(
            "Repeated identical tool call detected. In the graph, this condition routes to "
            "the error node instead of repeating the action."
            if tripped
            else "Repeat detector did not trip."
        )

values, snapshot = snapshot_values(thread_id)
approval_ticket = pending_approval(values, snapshot)

status_column, iteration_column, memory_column = st.columns(3)
status_column.metric("Active graph node", active_node(snapshot))
iteration_column.metric("Reasoning cycles", values.get("iteration_count", 0))
memory_column.metric("Messages in memory", len(values.get("messages", [])))

left_column, right_column = st.columns((3, 2), gap="large")

with left_column:
    st.subheader("Conversation")
    display_messages(values)

    if approval_ticket:
        st.warning("Execution is paused for human approval.")
        st.subheader("Approval required")
        st.write(f"**Requested action:** `{approval_ticket['tool_name']}`")
        st.json(approval_ticket.get("arguments", {}))
        st.write(f"**Risk classification:** {approval_ticket.get('risk', 'HIGH')}")

        approve_column, reject_column = st.columns(2)
        if approve_column.button("Approve action", type="primary", use_container_width=True):
            resume_approval(thread_id, approved=True)
            st.rerun()
        if reject_column.button("Reject action", use_container_width=True):
            resume_approval(thread_id, approved=False)
            st.rerun()
    else:
        prompt = st.chat_input("Ask about a service, billing account, scaling action, or transfer")
        if prompt:
            try:
                run_prompt(thread_id, prompt)
                st.rerun()
            except Exception as exc:
                st.error(f"The agent could not complete this request: {exc}")

with right_column:
    st.subheader("Checkpoint state")
    state_for_display = {
        "iteration_count": values.get("iteration_count", 0),
        "pending_approval": approval_ticket,
        "approval_status": values.get("approval_status"),
        "executed_tool_hashes": values.get("executed_tool_hashes", []),
        "execution_log": values.get("execution_log", []),
        "error": values.get("error"),
    }
    st.json(state_for_display)

    st.subheader("Node history")
    history = values.get("execution_log", [])
    if history:
        st.code(" → ".join(history))
    else:
        st.caption("Send a request to begin the graph.")
