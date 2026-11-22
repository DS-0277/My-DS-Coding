"""Simulated operations tools used by the agent.

These functions do not contact real services or move real money.  They make the
workflow safe to demonstrate while keeping the same kinds of inputs a real
operations agent would require.
"""

from __future__ import annotations

from langchain_core.tools import BaseTool, tool


@tool
def query_service_metrics(service_name: str) -> str:
    """Return read-only health metrics for a named service."""
    metrics = {
        "auth-service": "error_rate=7.2%, latency_ms=240, status=degraded",
        "payments-service": "error_rate=0.4%, latency_ms=110, status=healthy",
    }
    return metrics.get(
        service_name,
        f"error_rate=1.0%, latency_ms=150, status=healthy for {service_name}",
    )


@tool
def check_billing_balance(account_id: str) -> str:
    """Return a read-only simulated billing balance for an account."""
    return f"account={account_id}, available_balance_usd=12000.00"


@tool
def scale_kubernetes_cluster(service_name: str, replica_count: int) -> str:
    """Simulate changing the replica count for a Kubernetes service."""
    if replica_count < 1:
        raise ValueError("replica_count must be at least 1")
    return f"SIMULATED: scaled {service_name} to {replica_count} replicas"


@tool
def execute_wire_transfer(recipient_id: str, amount_usd: float) -> str:
    """Simulate a financial wire transfer after human approval."""
    if amount_usd <= 0:
        raise ValueError("amount_usd must be greater than zero")
    return (
        "SIMULATED: wire transfer completed "
        f"recipient={recipient_id}, amount_usd={amount_usd:.2f}"
    )


SAFE_TOOL_NAMES = {"query_service_metrics", "check_billing_balance"}
SENSITIVE_TOOL_NAMES = {"scale_kubernetes_cluster", "execute_wire_transfer"}
TOOLS: list[BaseTool] = [
    query_service_metrics,
    check_billing_balance,
    scale_kubernetes_cluster,
    execute_wire_transfer,
]
TOOL_BY_NAME = {tool.name: tool for tool in TOOLS}


def is_sensitive(tool_name: str) -> bool:
    """Return whether a tool needs operator approval before it can run."""
    return tool_name in SENSITIVE_TOOL_NAMES
