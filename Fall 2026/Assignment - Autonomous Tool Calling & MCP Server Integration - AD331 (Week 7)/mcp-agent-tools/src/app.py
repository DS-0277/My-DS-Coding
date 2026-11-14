"""Streamlit operator console for the MCP agent."""

import asyncio
import json
import time
from pathlib import Path

import streamlit as st

from client.agent_loop import run_agent
from client.mcp_client import MCPClient
from server.tools.math_tool import calculate_expression
from server.tools.sql_tool import query_database


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SERVER_SCRIPT = "src/server/mcp_server.py"


def discover_tools() -> list[dict]:
    """Discover tools from the MCP server for the inspector panel."""
    async def _discover() -> list[dict]:
        client = MCPClient()
        try:
            return await client.connect(SERVER_SCRIPT)
        finally:
            await client.close()

    return asyncio.run(_discover())


def ask_agent(prompt: str) -> str:
    """Run the agent loop from Streamlit's synchronous callback model."""
    async def _ask() -> str:
        return await run_agent(prompt, MCPClient())

    return asyncio.run(_ask())


st.set_page_config(page_title="MCP Agent Tools", page_icon="🛠️", layout="wide")
st.title("MCP Agent Tools")
st.caption("Enterprise operations assistant with local, external, and deterministic tools")

with st.sidebar:
    st.header("MCP Tool Inspector")
    if st.button("Discover tools", use_container_width=True):
        try:
            st.session_state["tools"] = discover_tools()
            st.success("Tools discovered")
        except Exception as exc:
            st.error(f"Discovery failed: {exc}")

    tools = st.session_state.get("tools", [])
    if tools:
        for tool in tools:
            with st.expander(tool["name"]):
                st.write(tool.get("description") or "No description provided.")
                st.json(tool.get("inputSchema", {}))
    else:
        st.info("Click ‘Discover tools’ to inspect the MCP server.")

st.header("Operator Console")
prompt = st.text_area(
    "Enter an operations request",
    placeholder="Check Seattle inventory, get the current weather, and calculate 3.5% of order value 842.35.",
    height=120,
)
if st.button("Run assistant", type="primary"):
    if not prompt.strip():
        st.warning("Enter a request first.")
    else:
        with st.spinner("Running MCP agent..."):
            started = time.perf_counter()
            try:
                answer = ask_agent(prompt)
                elapsed = time.perf_counter() - started
                st.session_state["last_run"] = {"prompt": prompt, "answer": answer, "elapsed": elapsed}
            except Exception as exc:
                st.error(f"Agent run failed: {exc}")

last_run = st.session_state.get("last_run")
if last_run:
    st.subheader("Assistant response")
    st.write(last_run["answer"])
    st.caption(f"Completed in {last_run['elapsed']:.2f} seconds")

st.header("Security Test Workbench")
st.caption("These probes demonstrate that unsafe requests are rejected by the tools.")
col1, col2 = st.columns(2)
with col1:
    st.subheader("SQL injection probe")
    sql_probe = "SELECT * FROM orders; DROP TABLE inventory;--"
    st.code(sql_probe, language="sql")
    if st.button("Run SQL probe"):
        st.json(json.loads(query_database(sql_probe)))

with col2:
    st.subheader("Math sandbox probe")
    math_probe = '__import__("os").listdir(".")'
    st.code(math_probe, language="python")
    if st.button("Run math probe"):
        st.json(json.loads(calculate_expression(math_probe)))
