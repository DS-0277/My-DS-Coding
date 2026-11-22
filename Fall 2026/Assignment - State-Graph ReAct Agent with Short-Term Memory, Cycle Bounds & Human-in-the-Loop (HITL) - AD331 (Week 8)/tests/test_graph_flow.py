"""Tests for ordinary safe-tool flow and checkpointed memory."""

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from src.graph import build_graph
from tests.conftest import ScriptedModel, tool_call_message


def test_safe_tool_autonomous_traversal() -> None:
    """A safe metrics lookup runs without pausing for human approval."""
    model = ScriptedModel(
        [
            tool_call_message(
                "query_service_metrics",
                {"service_name": "auth-service"},
                "safe-call-1",
            ),
            AIMessage(content="The auth-service error rate is 7.2%."),
        ]
    )
    graph = build_graph(model=model, checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "safe-flow"}}

    result = graph.invoke({"messages": [HumanMessage(content="Check auth-service metrics.")]}, config)

    assert result["execution_log"] == [
        "agent_node",
        "circuit_breaker:passed",
        "tool_executor:query_service_metrics",
        "agent_node",
    ]
    assert "error_rate=7.2%" in result["messages"][-2].content
    assert result["messages"][-1].content == "The auth-service error rate is 7.2%."
    assert graph.get_state(config).next == ()


def test_multi_turn_memory_checkpointing() -> None:
    """A second request on one thread receives the earlier conversation."""
    model = ScriptedModel(
        [
            AIMessage(content="I will remember that your name is Alice."),
            AIMessage(content="Your name is Alice."),
        ]
    )
    graph = build_graph(model=model, checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "memory-flow"}}

    graph.invoke({"messages": [HumanMessage(content="My name is Alice.")]}, config)
    result = graph.invoke({"messages": [HumanMessage(content="What is my name?")]}, config)

    second_model_input = model.invocations[1]
    assert any(getattr(message, "content", "") == "My name is Alice." for message in second_model_input)
    assert result["messages"][-1].content == "Your name is Alice."
