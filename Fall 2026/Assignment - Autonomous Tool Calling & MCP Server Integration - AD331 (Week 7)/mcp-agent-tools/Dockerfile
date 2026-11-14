FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY data ./data

RUN uv sync --frozen --no-dev

EXPOSE 8503

CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=8503"]
