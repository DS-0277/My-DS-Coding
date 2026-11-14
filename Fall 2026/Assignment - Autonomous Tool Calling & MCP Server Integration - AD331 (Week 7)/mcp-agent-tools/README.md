# MCP Agent Tools

Secure tool-calling assistant built around the Model Context Protocol.

## Run the operator console

```bash
uv run streamlit run src/app.py
```

The console can discover the three MCP tools, submit an operator request to the agent loop, and run the SQL and math security probes.

## Run with Docker

The Docker version uses port `8503`, separate from the local Streamlit port `8502`.

```bash
docker compose build
docker compose up
```

Open [http://localhost:8503](http://localhost:8503). The API key is loaded from the local `.env` file and is not copied into the image.

Stop the container with:

```bash
docker compose down
```
