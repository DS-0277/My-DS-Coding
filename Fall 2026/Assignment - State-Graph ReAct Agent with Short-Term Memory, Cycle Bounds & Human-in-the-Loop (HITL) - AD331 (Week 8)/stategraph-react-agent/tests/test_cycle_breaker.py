"""Tests for the hard cycle bound and normalized payload fingerprints."""

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from src.circuit_breaker import MAX_ITERATIONS, is_consecutive_repeat, tool_call_fingerprint
from src.graph import build_graph
from tests.conftest import ScriptedModel, tool_call_message


def test_maximum_iteration_hard_bound() -> None:
    """A new tool request at cycle six routes to the graph's error node."""
    responses = [
        tool_call_message(
            "query_service_metrics",
            {"service_name": f"service-{index}"},
            f"cycle-{index}",
        )
        for index in range(1, MAX_ITERATIONS + 1)
    ]
    graph = build_graph(model=ScriptedModel(responses), checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "cycle-bound"}}

    result = graph.invoke({"messages": [HumanMessage(content="Keep checking services.")]}, config)

    assert result["iteration_count"] == MAX_ITERATIONS
    assert "Maximum iteration limit" in result["error"]
    assert result["execution_log"][-1] == "error_node"


def test_sha256_payload_hash_tripping() -> None:
    """Equivalent argument dictionaries create one repeat-detection fingerprint."""
    first = tool_call_fingerprint(
        "scale_kubernetes_cluster",
        {"service_name": "auth-service", "replica_count": 10},
    )
    second = tool_call_fingerprint(
        "scale_kubernetes_cluster",
        {"replica_count": 10, "service_name": "auth-service"},
    )

    assert first == second
    assert is_consecutive_repeat([first], second)


def test_identical_tool_call_routes_to_error_before_cycle_limit() -> None:
    """The graph blocks an immediate duplicate tool request after two cycles."""
    repeated_call = {"service_name": "auth-service"}
    graph = build_graph(
        model=ScriptedModel(
            [
                tool_call_message("query_service_metrics", repeated_call, "first-call"),
                tool_call_message("query_service_metrics", repeated_call, "second-call"),
            ]
        ),
        checkpointer=MemorySaver(),
    )

    result = graph.invoke(
        {"messages": [HumanMessage(content="Check auth-service twice.")]},
        {"configurable": {"thread_id": "duplicate-call"}},
    )

    assert result["iteration_count"] == 2
    assert result["iteration_count"] < MAX_ITERATIONS
    assert result["error"] == "Repeated tool call detected; execution stopped safely."
    assert "circuit_breaker:repeat" in result["execution_log"]
    assert result["execution_log"][-1] == "error_node"
