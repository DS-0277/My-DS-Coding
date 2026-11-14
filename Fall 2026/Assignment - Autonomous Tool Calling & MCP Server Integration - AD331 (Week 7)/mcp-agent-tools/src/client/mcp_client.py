"""Initial MCP client draft for stdio connections and tool discovery."""

from contextlib import AsyncExitStack
from pathlib import Path
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """Manage an MCP stdio connection and expose discovered tools."""

    def __init__(self) -> None:
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()

    async def connect(self, server_script: str) -> list[dict[str, Any]]:
        """Start the server script and return its MCP tool definitions."""
        project_root = Path(__file__).resolve().parents[2]
        server_path = Path(server_script)
        module_parts = server_path.with_suffix("").parts
        if module_parts and module_parts[0] == "src":
            module_parts = module_parts[1:]
        module_name = ".".join(module_parts)
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", module_name],
            cwd=str(project_root),
            env={"PYTHONPATH": str(project_root / "src")},
        )
        read_stream, write_stream = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self.session.initialize()
        tools = await self.session.list_tools()
        return [tool.model_dump() for tool in tools.tools]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Call a discovered MCP tool."""
        if self.session is None:
            raise RuntimeError("MCP client is not connected")
        return await self.session.call_tool(name, arguments)

    async def close(self) -> None:
        """Close the MCP process and streams."""
        await self.exit_stack.aclose()
