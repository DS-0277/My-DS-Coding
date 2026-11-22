"""Tests for interruption, approval resumption, and rejection recovery."""

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from src.graph import build_graph
from tests.conftest import ScriptedModel, tool_call_message


def sensitive_scale_call() -> AIMessage:
    return tool_call_message(
        "scale_kubernetes_cluster",
        {"service_name": "auth-service", "replica_count": 10},
        "sensitive-call-1",
    )


def test_sensitive_action_interruption() -> None:
    """A sensitive tool pauses execution at the human-approval gate."""
    graph = build_graph(model=ScriptedModel([sensitive_scale_call()]), checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "approval-pause"}}

    graph.invoke({"messages": [HumanMessage(content="Scale auth-service to 10.")]}, config)
    snapshot = graph.get_state(config)

    assert snapshot.next == ("human_approval",)
    assert snapshot.tasks[0].interrupts[0].value["tool_name"] == "scale_kubernetes_cluster"


def test_approval_resumption_executes_sensitive_tool() -> None:
    """Approval resumes the checkpoint and runs the previously paused tool."""
    model = ScriptedModel([sensitive_scale_call(), AIMessage(content="Scaling completed.")])
    graph = build_graph(model=model, checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "approval-resume"}}

    graph.invoke({"messages": [HumanMessage(content="Scale auth-service to 10.")]}, config)
    result = graph.invoke(Command(resume={"approved": True}), config)

    assert result["approval_status"] == "APPROVED"
    assert any("SIMULATED: scaled auth-service to 10 replicas" in str(message.content) for message in result["messages"])
    assert result["messages"][-1].content == "Scaling completed."
    assert graph.get_state(config).next == ()


def test_rejection_recovery_bypasses_sensitive_tool() -> None:
    """Rejection adds a cancellation context and does not execute scaling."""
    model = ScriptedModel([sensitive_scale_call(), AIMessage(content="The scaling action was cancelled.")])
    graph = build_graph(model=model, checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "approval-reject"}}

    graph.invoke({"messages": [HumanMessage(content="Scale auth-service to 10.")]}, config)
    result = graph.invoke(Command(resume={"approved": False}), config)

    assert result["approval_status"] == "REJECTED"
    assert result["rejected_tool_hashes"]
    assert not any("SIMULATED: scaled" in str(message.content) for message in result["messages"])
    assert result["messages"][-1].content == "The scaling action was cancelled."
