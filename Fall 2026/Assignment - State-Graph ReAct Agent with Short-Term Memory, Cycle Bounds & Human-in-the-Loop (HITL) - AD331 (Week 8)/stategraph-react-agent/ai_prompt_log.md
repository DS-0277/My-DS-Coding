# AI Prompt Log

## Initial Prompt Used for Step 2

> You are a Principal AI Agent Architect specializing in deterministic state machines and LangGraph.
>
> Build a production-grade, state-graph-governed ReAct agent in Python 3.11+ featuring memory persistence, cycle breaking, and human-in-the-loop (HITL) approval gates.
>
> ### Core Architecture Requirements:
>
> **Agent State (`src/state.py`):**
>
> - Define an `AgentState(TypedDict)` containing:
>   - `messages: Annotated[list[AnyMessage], add_messages]` (conversational context)
>   - `iteration_count: int` (tracks reasoning cycles)
>   - `executed_tool_hashes: list[str]` (SHA-256 hashes of recent tool invocations)
>   - `pending_approval: Optional[dict]` (holds details of interrupted sensitive tool call)
>   - `approval_status: Optional[Literal["APPROVED", "REJECTED"]]`
>
> **Tools (`src/tools.py`):**
>
> - Safe tools: `query_service_metrics(service_name: str)`, `check_billing_balance(account_id: str)`.
> - Sensitive tools: `scale_kubernetes_cluster(service_name: str, replica_count: int)`, `execute_wire_transfer(recipient_id: str, amount_usd: float)`. Tag these with a custom metadata flag `is_sensitive=True`.
>
> **Graph Architecture (`src/graph.py`):**
>
> - Nodes:
>   - `agent_node`: Calls LLM with tool bindings; increments `iteration_count`.
>   - `circuit_breaker_node`: Checks `iteration_count <= 6` and asserts that SHA-256 hash of `(tool_name, args)` has not appeared consecutively. If tripped, routes to `error_node`.
>   - `human_approval_gate`: Uses LangGraph's dynamic `interrupt()` mechanism when a sensitive tool is called. Persists graph state to a `MemorySaver` checkpointer and halts.
>   - `tool_executor_node`: Invokes approved tools and appends ToolMessages.
>   - `error_node`: Emits graceful termination messages when loops or unauthorized actions occur.
>
> - Conditional Edges:
>   - From `agent_node`: If tool_calls exist, route to `circuit_breaker_node`. Else, route to END.
>   - From `circuit_breaker_node`: If tool is sensitive, route to `human_approval_gate`. Else, route to `tool_executor_node`.
>   - From `human_approval_gate`: If `APPROVED`, route to `tool_executor_node`. If `REJECTED`, route to `agent_node` with a rejection notification ToolMessage.
>   - From `tool_executor_node`: Route back to `agent_node`.
>
> **Checkpointing & Compilation:**
>
> - Compile the graph with a `MemorySaver()` checkpointer and configure `interrupt_before=["human_approval_gate"]` or use inline dynamic `interrupt()`. Support `thread_id` configurations for session continuity.
>
> Provide clean, modular, and strongly typed code across the designated files.

## Step 3 Audit Results

1. **State mutation vs. pure returns** — **Status: Good — no change.** Nodes return state updates instead of mutating the incoming state in place.

2. **Human-rejection loop** — **Status: Defect found but fixed.** Added `rejected_tool_hashes`; a rejected sensitive action is now remembered and blocked if requested again.

   - **Before:** the model received only a written reminder: “The human rejected this action. Do not ask again.” A model could ignore that reminder and request the same action later.
   - **After:** the application saves a fingerprint for the rejected tool call. If the model requests the same tool with the same arguments again, the circuit breaker blocks it before the tool can run.

3. **Payload-hash normalization** — **Status: Good — no change.** Tool arguments are normalized with sorted JSON keys before SHA-256 hashing.

4. **Thread ID and session isolation** — **Status: Good — no change.** The graph has no hardcoded thread ID and uses `MemorySaver`; Step 4 will supply a unique thread ID per UI session.

## Step 4: Interactive Web Interface

From the project folder, launch the Streamlit interface with:

```bash
uv run streamlit run src/app.py
```

## Step 5: Automated QA

Run the seven automated graph, memory, circuit-breaker, approval, and rejection checks with:

```bash
uv run pytest -v
```
