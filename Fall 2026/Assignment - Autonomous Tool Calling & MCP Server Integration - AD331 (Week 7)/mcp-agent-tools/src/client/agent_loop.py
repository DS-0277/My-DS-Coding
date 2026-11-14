"""Initial LLM function-calling loop draft."""

import json
from typing import Any

from openai import AsyncOpenAI
from dotenv import load_dotenv

from client.mcp_client import MCPClient


load_dotenv()


def mcp_tools_to_openai_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert MCP tool metadata into OpenAI function definitions."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "parameters": tool.get("inputSchema", {}),
            },
        }
        for tool in tools
    ]


async def run_agent(
    prompt: str,
    mcp_client: MCPClient,
    model: str = "gpt-4o-mini",
    max_turns: int = 5,
) -> str:
    """Run an initial multi-turn OpenAI tool-calling loop."""
    if not 1 <= max_turns <= 10:
        raise ValueError("max_turns must be between 1 and 10")
    client = AsyncOpenAI()
    try:
        discovered_tools = await mcp_client.connect("src/server/mcp_server.py")
        tools = mcp_tools_to_openai_tools(discovered_tools)
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "Use the database schema carefully: products contains sku and product_id; "
                    "inventory contains product_id, city, quantity, and reorder_level. "
                    "When a request names an SKU and asks for inventory, join inventory to "
                    "products using product_id."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        for _ in range(max_turns):
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )
            message = response.choices[0].message
            if not message.tool_calls:
                return message.content or "No response returned."

            messages.append(message.model_dump(exclude_none=True))
            for tool_call in message.tool_calls:
                try:
                    arguments = json.loads(tool_call.function.arguments)
                    result = await mcp_client.call_tool(tool_call.function.name, arguments)
                    content = str(result)
                except (json.JSONDecodeError, ValueError, TypeError, RuntimeError) as exc:
                    content = json.dumps({"error": f"Tool call failed: {exc}"})
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": content,
                    }
                )
    finally:
        await mcp_client.close()

    return "The tool-calling loop reached its maximum number of turns."
