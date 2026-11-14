"""Tests for MCP discovery and the multi-step agent loop."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from client.agent_loop import run_agent
from client.mcp_client import MCPClient


@pytest.mark.asyncio
async def test_dynamic_tool_discovery() -> None:
    client = MCPClient()
    tools = await client.connect("src/server/mcp_server.py")
    try:
        names = {tool["name"] for tool in tools}
        assert names == {
            "query_database_tool",
            "get_current_weather_tool",
            "calculate_expression_tool",
        }
        assert all(tool.get("inputSchema") for tool in tools)
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_multi_step_chained_loop_terminates_with_assistant() -> None:
    fake_mcp = MagicMock()
    fake_mcp.connect = AsyncMock(
        return_value=[
            {"name": "calculate_expression_tool", "description": "Calculate", "inputSchema": {"type": "object"}}
        ]
    )
    fake_mcp.call_tool = AsyncMock(return_value='{"result": 29}')
    fake_mcp.close = AsyncMock()

    first_message = MagicMock()
    first_message.tool_calls = [
        MagicMock(
            id="call_1",
            function=MagicMock(
                name="calculate_expression_tool",
                arguments='{"expression":"2 + 3 * (4 - 1) ** 2"}',
            ),
        )
    ]
    first_message.model_dump.return_value = {"role": "assistant", "tool_calls": []}
    final_message = MagicMock(tool_calls=None, content="The answer is 29.")
    fake_openai = MagicMock()
    fake_openai.chat.completions.create = AsyncMock(
        side_effect=[MagicMock(choices=[MagicMock(message=first_message)]), MagicMock(choices=[MagicMock(message=final_message)])]
    )

    with patch("client.agent_loop.AsyncOpenAI", return_value=fake_openai):
        result = await run_agent("Calculate the expression.", fake_mcp, max_turns=3)

    assert result == "The answer is 29."
    assert fake_mcp.call_tool.await_count == 1
    fake_mcp.close.assert_awaited_once()
