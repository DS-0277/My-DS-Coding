# AI Prompt and Audit Log

## Step 2: Initial Draft Prompt

The following prompt was copied from the assignment and used to create the initial draft:

> You are a Principal AI Agent Architect specializing in tool integration and the Model Context Protocol (MCP).
>
> Build an end-to-end Python 3.11+ system featuring an MCP server with three distinct tools and a client application executing an autonomous function-calling loop.
>
> **Architecture Requirements:**
>
> MCP Server (`src/server/mcp_server.py`) using the official MCP Python SDK (`FastMCP`):
> - Tool 1: `query_database(sql_query: str) -> str`
>   - Connects to SQLite (`data/enterprise_ops.db`).
>   - Enforces STRICT READ-ONLY safety: Parse the SQL using regular expressions or an AST validator to block any DDL/DML statements (DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, ATTACH). Open SQLite with `file:...uri=true?mode=ro`.
> - Tool 2: `get_current_weather(city: str) -> str`
>   - Calls a real REST API (e.g., Open-Meteo geocoding + forecast API) asynchronously via `httpx.AsyncClient`.
>   - Returns structured temperature, weather conditions, precipitation, and wind speed.
> - Tool 3: `calculate_expression(expression: str) -> str`
>   - Evaluates algebraic and arithmetic expressions deterministically.
>   - MUST NOT use Python's built-in `eval()` or `exec()`. Parse using `ast.parse` with a visitor pattern allowing only safe operators (+, -, *, /, **, %, parentheses, math functions).
>
> MCP Client & Agent Loop (`src/client/agent_loop.py`):
> - Connects to the MCP server via `stdio` transport using `mcp.ClientSession`.
> - Dynamically calls `session.list_tools()` to discover available tools and convert MCP tool schemas into standard OpenAI tool definitions.
> - Implements a robust multi-turn function-calling loop:
>   - Send user prompt and tool definitions to the LLM (e.g., gpt-4o-mini).
>   - If model returns `tool_calls`, invoke the matching MCP tool via `session.call_tool()`.
>   - Append the tool result message (`role="tool"`, matching `tool_call_id`) and repeat the loop until the model emits a final natural language answer (or reaches `max_turns=5`).
>
> **Error Handling & Typing:**
> - Provide type hints, docstrings, and informative tool descriptions so the LLM knows when to invoke each tool.
> - Tool failures must return formatted error messages to the model instead of crashing the server process.
>
> Provide clean, modular code split into the specified directory files.

This is intentionally recorded as the baseline draft. Step 3 documents the security audit, findings, and defensive refactorings.

## Step 3: Audit Findings and Refactorings

The four required audit areas are documented below in numbered blocks.

### 1. SQL Injection and Read-Only Access

**Initial status:** Not good enough.

**Reason:** The initial draft sent the SQL directly to the database. That meant a harmful request could potentially change or damage the data.

**Fix applied:** The tool now accepts only one `SELECT` statement. It rejects commands such as `DROP`, `DELETE`, `UPDATE`, and `INSERT`, rejects multiple statements, and opens SQLite with `mode=ro` so the database is read-only.

### 2. Arbitrary Code Execution in the Math Tool

**Initial status:** Partially good.

**Reason:** The draft did not use `eval()` or `exec()`, which was good. However, it still needed clear limits and safer handling for invalid or extremely large expressions.

**Fix applied:** The tool now uses `ast.parse()` to inspect the expression before calculating it. It allows only approved arithmetic AST nodes, rejects names and function calls, limits the expression and result sizes, and returns a clear error instead of crashing.

### 3. MCP Tool Schema Translation

**Initial status:** Good.

**Reason:** The draft correctly changed each discovered MCP tool into the format expected by the LLM.

**Fix applied:** We verified that every tool includes `type: function`, its name, its description, and its `inputSchema` as the function parameters. No major fix was needed.

### 4. Infinite Tool Loops and State Growth

**Initial status:** Partially good.

**Reason:** The draft had a maximum number of turns, which was good. However, invalid tool arguments or a failed tool could still stop the entire workflow unexpectedly.

**Fix applied:** The loop now checks the turn limit, catches invalid JSON and tool errors, sends a readable error message back to the LLM, and closes the MCP connection properly.

### Additional reliability audit

The weather tool was also improved. The initial draft called the external API correctly, but it needed stronger input and failure handling. It now validates the city name, uses a timeout, catches HTTP and response errors, and returns limited JSON fields instead of exposing an uncontrolled response.

## Step 4: Operator Console Demo

Launch the Streamlit interface with:

```bash
uv run streamlit run src/app.py
```

Use this operator-console request to demonstrate coordinated tool use:

> "Check if our inventory in Seattle has enough stock of SKU-90210 to fulfill order #4492, verify if rainfall there will delay ground dispatch today, and calculate the total shipping insurance cost at 3.5% of the order value."

## Step 5: Automated QA Test Suite

Run the complete test suite with:

```bash
uv run pytest -v
```

The assignment defines seven required test categories. Parameterized tests cover multiple SQL and math attack examples, so Pytest reports 12 individual checks:

```text
12 passed in 0.80s
```

The additional checks are intentional: four SQL attack cases and three math sandbox attack cases are tested independently so a failure identifies the exact unsafe input.

## Step 6: Docker Packaging

The Docker deployment uses port `8503` so it does not conflict with the local Streamlit instance on port `8502`.

Build the image:

```bash
docker compose build
```

Start the application:

```bash
docker compose up
```

Open the Docker dashboard at:

```text
http://localhost:8503
```

Stop the application:

```bash
docker compose down
```

The API key is supplied through the local `.env` file by `docker-compose.yml`. It is excluded from the Docker build context by `.dockerignore` and is not copied into the image.

### Verification performed

- Valid SQL returned the expected Seattle inventory quantity.
- A stacked SQL attack was rejected.
- The dangerous expression `__import__("os").listdir(".")` was rejected.
- The arithmetic expression `2 + 3 * (4 - 1) ** 2` returned `29`.
- The MCP client discovered all three registered tools.
